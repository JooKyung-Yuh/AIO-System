"""
Stage 2: 여러 논문(Stage 1 = extract_aio.py의 run_dir들)에서 모인 evidence node 전체
pool을 대상으로 (1) 전역 cross-paper canonicalization(prompts/p2a_canonicalize.md)과
(2) ID-only 전역 factor 조립(prompts/p2b_assemble.md)을 수행한다. LLM은 Gemini
(google-genai)를 사용한다.

기존에는 "논문 1편 안에서 page-chunk 배치별로 factor 조립 + canonicalization을 같은
프롬프트(p2.md)로 동시에 수행"했지만, 다음 이유로 전역/2단계로 분리했다:
  - canonicalization이 논문 하나 안에서만 이뤄지면 다른 논문에 있는 같은 개념의 노드와
    병합될 기회가 없다. 여러 논문을 하나의 pool로 모아야 cross-paper 중복 제거/일반화가
    가능하다.
  - factor 조립은 canonical 노드의 "{node_id, label, experiment_ref, text}" 경량
    서술자만 봐도 충분하다 - 여러 논문의 노드를 한 번에 보며 조립하려면 이 경량화(요약이
    아니라 experiment_ref+text로 판정)가 출력 token 예산을 지켜준다.

Stage 2A (prompts/p2a_canonicalize.md): 전체 pool(기본값) 또는 --max-nodes-per-batch로
    나눈 배치마다 1회 호출. 중복 노드를 하나의 canonical node_id로 합치되, intervention/
    pattern은 experiment_ref가 달라도 내용(주어/비교대상/방향&크기)이 같으면 병합하고
    experiment_ref를 합집합 리스트로 보존한다(반대로 experiment_ref가 같아도 내용이
    다르면 병합하지 않음 - experiment_ref는 약한 보조 신호일 뿐, 게이트는 내용이다).
    eval_metric은 experiment_ref 자체가 없는 재사용 가능한 정의라 이 제약과 무관하게
    자유롭게 병합한다. 비교를 나타내는 pattern/intervention은 방향(어느 쪽이 이겼는지)을
    절대 지우지 않는다. 결과는 node_registry.json에 저장. canonicalization 적용 결과는
    <category>_canonicalized.json(+ observable은 observable_canonicalized.json에
    eval_metric/pattern로 나눠 저장)에 남긴다.

Stage 2B (prompts/p2b_assemble.md): node_registry에서 살아남은(흡수되지 않은) canonical
    노드마다 만든 경량 서술자 전체(기본값) 또는 배치마다 1회 호출. intervention과 그것이
    만든 pattern(experiment_ref 리스트가 하나라도 겹치는 것 - 완전 일치가 아니라 set
    overlap)을 anchor로 먼저 묶고(intervention이 없거나 겹치는 pattern이 없으면 factor가
    되지 않음; eval_metric은 이 겹침 검사에서 완전히 면제), 그 실험 단위에서 mechanism/
    assumption/context를 붙이는 순서로 factor를 조립한다. assumption/context/observable은
    리스트를 허용하고, mechanism은 단일 값 또는 null, intervention은 반드시 단일 값(null
    불가)이다. 결과는 result.json({"factors": [...]})에 저장.

node_id 전역화: Stage 1의 node_id(예: "A3")는 논문 안에서만 유일하므로, 이 스크립트가
논문마다 파일을 읽어들일 때 "{paper_id}::{원래 node_id}"(예: "2409.16118v3::A3")로 다시
써서 여러 논문을 가로질러도 유일하게 만든다. 이후 모든 산출물(node_registry, factors)은
이 전역 id만 사용한다.

사용 예:
    python extract_aio.py --pdf papers/a.pdf --paper-id a
    python extract_aio.py --pdf papers/b.pdf --paper-id b
    python assemble_global.py --run-dirs outputs/a_20260101_000000 outputs/b_20260101_000100
    python assemble_global.py --outputs-dir outputs   # 위 run_dir들을 자동으로 찾아서 사용
    python assemble_global.py --outputs-dir outputs --max-nodes-per-batch 150  # pool이 너무 커서 한 번에 안 될 때
"""

import argparse
import datetime
import json
import sys
import traceback
from pathlib import Path

from llm_client import generate_with_retry, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_OUTPUT_TOKENS
from batch_utils import (
    CATEGORIES,
    FLAT_CATEGORIES,
    OBSERVABLE_SUBCATEGORIES,
    load_prompt,
    parse_json_response,
    usage_of,
    add_usage,
    token_line,
    chunk_list,
    sort_for_batching,
    merge_registry_batches,
    merge_factor_batches_global,
    apply_canonicalization,
    find_incomplete_factors,
    build_id_only_descriptors,
)

SCRIPT_DIR = Path(__file__).resolve().parent
P2A_PROMPT_PATH = SCRIPT_DIR / "prompts" / "p2a_canonicalize.md"
P2B_PROMPT_PATH = SCRIPT_DIR / "prompts" / "p2b_assemble.md"
KST = datetime.timezone(datetime.timedelta(hours=9))

MAX_CALL_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 5


def parse_args():
    parser = argparse.ArgumentParser(description="Stage 2: GLOBAL cross-paper node canonicalization (p2a) + ID-only factor assembly (p2b), over the pooled Stage-1 output of one or more papers.")
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--run-dirs", type=str, nargs="+", help="Stage 1(extract_aio.py) run_dir 경로들 (논문마다 하나씩)")
    source_group.add_argument("--outputs-dir", type=str, help="이 디렉터리의 직계 하위 디렉터리 중 Stage 1 run_dir처럼 보이는 것들(metadata.json/assumption.json/observable.json을 모두 가진 디렉터리)을 자동으로 모아 사용")

    parser.add_argument("--p2a-prompt", type=str, default=str(P2A_PROMPT_PATH), help="Stage 2A(전역 canonicalization) 프롬프트 파일 경로")
    parser.add_argument("--p2b-prompt", type=str, default=str(P2B_PROMPT_PATH), help="Stage 2B(ID-only factor 조립) 프롬프트 파일 경로")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--max-output-tokens", type=int, default=DEFAULT_MAX_OUTPUT_TOKENS, help="호출당 최대 output token (기본: 모델 최대치인 65536)")
    parser.add_argument("--max-nodes-per-batch", type=int, default=None, help="지정하면 전역 pool을 이 크기로 나눠 여러 번 호출한다 (출력 token 한계 대비 fallback). 생략하면 pool 전체를 한 번에 처리한다 - p2a/p2b 프롬프트가 전제하는 기본 동작이며, cross-batch로 나뉜 중복은 못 잡을 수 있으니 pool이 큰데도 생략하면 살펴봐야 한다.")
    parser.add_argument("--run-dir", type=str, default=None, help="산출물(node_registry.json, <category>_canonicalized.json, result.json, 배치별 raw 응답, metadata)을 저장할 디렉터리 (생략 시 outputs/global_<timestamp>에 자동 생성)")
    parser.add_argument("--api-key", type=str, default=None, help="GEMINI_API_KEY를 인자로 직접 override (생략 시 .env/환경변수 사용)")
    return parser.parse_args()


def discover_run_dirs(outputs_dir):
    """outputs_dir의 직계 하위 디렉터리 중 Stage 1 run_dir처럼 보이는 것만 고른다
    (assemble_global.py 자신이 만든 outputs/global_* 디렉터리는 assumption.json이 이미
    canonicalize 전 raw 형태가 아니라서 자연히 제외된다 - 실제로는 assumption.json 자체를
    안 만들므로 이 체크만으로 걸러진다)."""
    found = []
    for child in sorted(Path(outputs_dir).iterdir()):
        if not child.is_dir():
            continue
        if (child / "metadata.json").exists() and (child / "assumption.json").exists() and (child / "observable.json").exists():
            found.append(child)
    return found


def _globalize_nodes(nodes, label, fallback_paper_id):
    """노드 각각에 label(카테고리)을 채우고, paper_id가 없으면 fallback_paper_id를 채운 뒤
    node_id를 "{paper_id}::{원래 node_id}"로 바꿔 전역 유일하게 만든다. 원래 id는
    "local_node_id"로 보존한다."""
    out = []
    for n in nodes:
        g = dict(n)
        paper_id = g.get("paper_id") or fallback_paper_id
        g["paper_id"] = paper_id
        g["label"] = label
        g["local_node_id"] = g["node_id"]
        g["node_id"] = f"{paper_id}::{g['node_id']}"
        out.append(g)
    return out


def load_run_dir(run_dir):
    """Stage 1 run_dir 하나에서 카테고리별 노드 파일을 읽어 전역화한다(unresolved.json은
    Stage 2 대상이 아니므로 읽지 않음). paper_id는 각 노드에 이미 태깅돼 있으면 그 값을,
    없으면(리팩터링 이전에 만든 run_dir 등) metadata.json의 paper_id를, 그마저 없으면
    run_dir 이름을 쓴다.

    반환: (node_lists, paper_id) - node_lists는 {category: [전역화된 node, ...]}
    (CATEGORIES 전체 키).
    """
    run_dir = Path(run_dir)
    metadata = {}
    metadata_path = run_dir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    fallback_paper_id = metadata.get("paper_id") or run_dir.name

    node_lists = {}
    for cat in FLAT_CATEGORIES:
        path = run_dir / f"{cat}.json"
        raw = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        node_lists[cat] = _globalize_nodes(raw, cat, fallback_paper_id)

    observable_path = run_dir / "observable.json"
    observable_raw = json.loads(observable_path.read_text(encoding="utf-8")) if observable_path.exists() else {}
    for sub in OBSERVABLE_SUBCATEGORIES:
        node_lists[sub] = _globalize_nodes(observable_raw.get(sub) or [], sub, fallback_paper_id)

    return node_lists, fallback_paper_id


def build_global_pool(run_dirs):
    """여러 run_dir의 전역화된 노드들을 하나의 pool로 모은다.

    반환: (pool, all_nodes, paper_id_by_run_dir) - pool은 {category: [node, ...]}
    (CATEGORIES 전체 키, 여러 논문 노드가 섞여 있음), all_nodes는 그 flat 버전.
    """
    pool = {cat: [] for cat in CATEGORIES}
    paper_id_by_run_dir = {}
    for run_dir in run_dirs:
        node_lists, paper_id = load_run_dir(run_dir)
        paper_id_by_run_dir[str(run_dir)] = paper_id
        for cat in CATEGORIES:
            pool[cat].extend(node_lists[cat])
    all_nodes = [n for cat in CATEGORIES for n in pool[cat]]
    return pool, all_nodes, paper_id_by_run_dir


# ---------------------------------------------------------------------------
# Stage 2A: global cross-paper canonicalization
# ---------------------------------------------------------------------------

def run_stage2a(args, all_nodes, run_dir):
    batches = chunk_list(sort_for_batching(all_nodes), args.max_nodes_per_batch)
    n_batches = len(batches)
    per_batch_meta = []
    batch_registries = []
    total_usage = None
    any_salvaged = False
    any_success = n_batches == 0

    for i, batch in enumerate(batches, start=1):
        print(f"[stage2a batch {i}/{n_batches}] {len(batch)} node(s) ...", file=sys.stderr)
        payload = [
            {
                "node_id": n["node_id"],
                "label": n["label"],
                "source_span": n.get("source_span"),
                "experiment_ref": n.get("experiment_ref"),  # intervention/pattern에만 존재; 그 외는 None
                "paper_id": n.get("paper_id"),
                "text": n.get("text"),
                "location": n.get("location"),
            }
            for n in batch
        ]
        system_prompt = load_prompt(args.p2a_prompt, nodes=json.dumps(payload, indent=2, ensure_ascii=False))

        finish_reason, usage, parse_error, salvaged = None, None, None, False
        node_registry = []
        raw_text = ""

        try:
            response = generate_with_retry(
                max_attempts=MAX_CALL_ATTEMPTS,
                retry_backoff_seconds=RETRY_BACKOFF_SECONDS,
                system_prompt=system_prompt,
                user_prompt="Proceed with the task described in the system prompt now.",
                pdf_bytes=None,
                model=args.model,
                temperature=args.temperature,
                max_output_tokens=args.max_output_tokens,
                api_key=args.api_key,
            )
            raw_text = response.text or ""
            finish_reason = str(response.candidates[0].finish_reason) if response.candidates else None
            usage = usage_of(response)
            total_usage = add_usage(total_usage, usage)

            try:
                parsed, salvaged = parse_json_response(raw_text)
                if isinstance(parsed, dict):
                    node_registry = parsed.get("node_registry") or []
                any_success = True
            except json.JSONDecodeError as e:
                parse_error = str(e)
        except Exception as e:
            parse_error = f"API call failed after {MAX_CALL_ATTEMPTS} attempts: {e}"
            print(f"  [ERROR] stage2a batch {i}: {parse_error}", file=sys.stderr)

        (run_dir / f"stage2a_batch_{i:02d}.md").write_text(raw_text, encoding="utf-8")
        any_salvaged = any_salvaged or salvaged

        if finish_reason and "STOP" not in finish_reason:
            print(f"  [WARN] stage2a batch {i} finish_reason={finish_reason} (may be truncated)", file=sys.stderr)
        if salvaged:
            print(f"  [WARN] stage2a batch {i} salvaged from truncation ({len(node_registry)} node_registry entries recovered)", file=sys.stderr)
        if parse_error:
            print(f"  [WARN] stage2a batch {i} JSON parse failed: {parse_error}", file=sys.stderr)

        batch_registries.append(node_registry)
        per_batch_meta.append({
            "batch_index": i,
            "node_count": len(batch),
            "registry_entry_count": len(node_registry),
            "finish_reason": finish_reason,
            "salvaged": salvaged,
            "parse_error": parse_error,
            "usage": usage,
        })

    if not any_success:
        raise RuntimeError(f"Stage 2A: all {n_batches} batch(es) failed to produce usable output; see {run_dir} for raw responses/errors.")

    node_registry = merge_registry_batches(batch_registries)
    return node_registry, per_batch_meta, total_usage, any_salvaged


# ---------------------------------------------------------------------------
# Stage 2B: global ID-only factor assembly
# ---------------------------------------------------------------------------

def run_stage2b(args, descriptors, run_dir):
    batches = chunk_list(sort_for_batching(descriptors), args.max_nodes_per_batch)
    n_batches = len(batches)
    per_batch_meta = []
    batch_factor_lists = []
    total_usage = None
    any_salvaged = False
    any_success = n_batches == 0

    for i, batch in enumerate(batches, start=1):
        print(f"[stage2b batch {i}/{n_batches}] {len(batch)} node(s) ...", file=sys.stderr)
        system_prompt = load_prompt(args.p2b_prompt, nodes_id_only=json.dumps(batch, indent=2, ensure_ascii=False))

        finish_reason, usage, parse_error, salvaged = None, None, None, False
        factors = []
        raw_text = ""

        try:
            response = generate_with_retry(
                max_attempts=MAX_CALL_ATTEMPTS,
                retry_backoff_seconds=RETRY_BACKOFF_SECONDS,
                system_prompt=system_prompt,
                user_prompt="Proceed with the task described in the system prompt now.",
                pdf_bytes=None,
                model=args.model,
                temperature=args.temperature,
                max_output_tokens=args.max_output_tokens,
                api_key=args.api_key,
            )
            raw_text = response.text or ""
            finish_reason = str(response.candidates[0].finish_reason) if response.candidates else None
            usage = usage_of(response)
            total_usage = add_usage(total_usage, usage)

            try:
                parsed, salvaged = parse_json_response(raw_text)
                if isinstance(parsed, dict):
                    factors = parsed.get("factors") or []
                any_success = True
            except json.JSONDecodeError as e:
                parse_error = str(e)
        except Exception as e:
            parse_error = f"API call failed after {MAX_CALL_ATTEMPTS} attempts: {e}"
            print(f"  [ERROR] stage2b batch {i}: {parse_error}", file=sys.stderr)

        (run_dir / f"stage2b_batch_{i:02d}.md").write_text(raw_text, encoding="utf-8")
        any_salvaged = any_salvaged or salvaged

        if finish_reason and "STOP" not in finish_reason:
            print(f"  [WARN] stage2b batch {i} finish_reason={finish_reason} (may be truncated)", file=sys.stderr)
        if salvaged:
            print(f"  [WARN] stage2b batch {i} salvaged from truncation ({len(factors)} factors recovered)", file=sys.stderr)
        if parse_error:
            print(f"  [WARN] stage2b batch {i} JSON parse failed: {parse_error}", file=sys.stderr)

        batch_factor_lists.append(factors)
        per_batch_meta.append({
            "batch_index": i,
            "node_count": len(batch),
            "factor_count": len(factors),
            "finish_reason": finish_reason,
            "salvaged": salvaged,
            "parse_error": parse_error,
            "usage": usage,
        })

    if not any_success:
        raise RuntimeError(f"Stage 2B: all {n_batches} batch(es) failed to produce usable output; see {run_dir} for raw responses/errors.")

    factors = merge_factor_batches_global(batch_factor_lists)
    return factors, per_batch_meta, total_usage, any_salvaged


def main():
    args = parse_args()

    if args.run_dirs:
        run_dirs = [Path(d) for d in args.run_dirs]
    else:
        run_dirs = discover_run_dirs(args.outputs_dir)
    if not run_dirs:
        print("[ERROR] no Stage 1 run_dir found (check --run-dirs / --outputs-dir).", file=sys.stderr)
        sys.exit(1)
    print(f"[INFO] pooling {len(run_dirs)} paper run_dir(s): {[str(d) for d in run_dirs]}", file=sys.stderr)

    pool, all_nodes, paper_id_by_run_dir = build_global_pool(run_dirs)
    if not all_nodes:
        print("[ERROR] the pooled node set is empty (no assumption/mechanism/context/intervention/eval_metric/pattern nodes found in the given run_dirs).", file=sys.stderr)
        sys.exit(1)

    now = datetime.datetime.now(KST)
    if args.run_dir:
        run_dir = Path(args.run_dir)
    else:
        run_dir = SCRIPT_DIR / "outputs" / f"global_{now.strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "timestamp": now.isoformat(),
        "run_dirs": [str(d) for d in run_dirs],
        "paper_id_by_run_dir": paper_id_by_run_dir,
        "model": args.model,
        "temperature": args.temperature,
        "max_output_tokens": args.max_output_tokens,
        "max_nodes_per_batch": args.max_nodes_per_batch,
        "pooled_node_count": len(all_nodes),
    }

    try:
        print(f"[INFO] stage 2a: canonicalizing {len(all_nodes)} node(s) globally across {len(run_dirs)} paper(s)...", file=sys.stderr)
        node_registry, stage2a_meta, stage2a_usage, stage2a_salvaged = run_stage2a(args, all_nodes, run_dir)
        print(f"[INFO] stage 2a done: {len(node_registry)} node_registry entry(ies).", file=sys.stderr)

        (run_dir / "node_registry.json").write_text(json.dumps({"node_registry": node_registry}, indent=2, ensure_ascii=False), encoding="utf-8")

        canonical_node_lists = apply_canonicalization(pool, node_registry)
        canonical_counts = {cat: len(canonical_node_lists[cat]) for cat in CATEGORIES}
        for cat in FLAT_CATEGORIES:
            (run_dir / f"{cat}_canonicalized.json").write_text(json.dumps(canonical_node_lists[cat], indent=2, ensure_ascii=False), encoding="utf-8")
        observable_canonicalized_bundle = {sub: canonical_node_lists[sub] for sub in OBSERVABLE_SUBCATEGORIES}
        (run_dir / "observable_canonicalized.json").write_text(json.dumps(observable_canonicalized_bundle, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[INFO] canonicalized node counts: {canonical_counts}. Saved to {run_dir}/<category>_canonicalized.json (eval_metric+pattern bundled into observable_canonicalized.json)", file=sys.stderr)

        descriptors, unregistered = build_id_only_descriptors(all_nodes, node_registry)
        if unregistered:
            print(f"[WARN] {len(unregistered)} surviving node(s) had no node_registry entry from stage 2a; used their original text/experiment_ref as-is: {unregistered}", file=sys.stderr)

        print(f"[INFO] stage 2b: assembling factors from {len(descriptors)} canonical node descriptor(s)...", file=sys.stderr)
        factors, stage2b_meta, stage2b_usage, stage2b_salvaged = run_stage2b(args, descriptors, run_dir)
        print(f"[INFO] stage 2b done: {len(factors)} factor(s).", file=sys.stderr)

        # descriptors는 이미 canonicalization이 반영된(병합 시 experiment_ref 합집합) 값이므로,
        # 여기서 그대로 재사용해야 factor 검증이 stage2b에 실제로 보여준 것과 일치한다.
        experiment_ref_by_id = {d["node_id"]: d.get("experiment_ref") or [] for d in descriptors}
        incomplete_factors = find_incomplete_factors(factors, experiment_ref_by_id)
        if incomplete_factors:
            print(f"[WARN] {len(incomplete_factors)}/{len(factors)} factor(s) fail the hard gate (missing intervention/pattern, or experiment_ref has no overlap): {incomplete_factors}", file=sys.stderr)

        (run_dir / "result.json").write_text(json.dumps({"factors": factors}, indent=2, ensure_ascii=False), encoding="utf-8")

        total_usage = add_usage(stage2a_usage, stage2b_usage)
        metadata["status"] = "success"
        metadata["stage2a"] = {
            "node_registry_count": len(node_registry),
            "unregistered_node_ids": unregistered,
            "any_salvaged": stage2a_salvaged,
            "batches": stage2a_meta,
            "usage": stage2a_usage,
        }
        metadata["stage2b"] = {
            "factor_count": len(factors),
            "incomplete_factors": incomplete_factors,
            "any_salvaged": stage2b_salvaged,
            "batches": stage2b_meta,
            "usage": stage2b_usage,
        }
        metadata["canonical_node_counts"] = canonical_counts
        metadata["usage_total"] = total_usage
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"[INFO] tokens (stage2a+stage2b): {token_line(total_usage)}", file=sys.stderr)
        print(f"[INFO] run artifacts saved under: {run_dir}", file=sys.stderr)
    except Exception:
        metadata["status"] = "error"
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        print(traceback.format_exc(), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
