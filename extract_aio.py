"""
HyperGraphRAG에서 hypergraph 구축/저장/검색 로직을 모두 제거하고, 논문 한 편에서
AIO(Assumption/Mechanism/Context/Intervention/Observable) evidence node를 추출하는
Stage 1 스크립트. LLM은 Gemini(google-genai)를 사용한다.

파이프라인은 이제 두 개의 독립된 스크립트로 나뉜다:
  Stage 1 (이 스크립트, 논문 1편 단위) -> Stage 2 (assemble_global.py, 여러 논문을
  가로지르는 전역 canonicalization + factor 조립).
Stage 2가 여러 논문의 node를 한 pool로 모아 처리하므로, 이 스크립트는 논문별로 여러 번
실행해 각각의 run_dir을 만들어두고, 그 run_dir들을 assemble_global.py에 넘기면 된다.

Gemini의 output token 한계(미지정 시 8192, 명시해도 모델별 상한 존재) 때문에 한 번의
호출로 논문 전체를 처리하면 응답이 중간에 잘려 JSON이 깨지는 문제가 있다. 이를
페이지 단위 청크 분할 + 잘린 JSON 복구(salvage) + 청크 결과 병합으로 해결한다
(JooKyung/AIO-System/Layer 1/test_gemini의 page-chunk 방식을 참고, batch_utils.py 참고).

Stage 1 (prompts/p1.md, 페이지 청크마다 1회 호출):
    PDF를 --pages-per-chunk 페이지씩 잘라 청크마다 독립적으로 호출한다. 각 호출은
    해당 페이지 구간에서 evidence span들을 추출해 assumption/mechanism/context/
    intervention/eval_metric/pattern(+ 확신도가 낮으면 unresolved) 중 하나로 분류한
    flat JSON 배열을 돌려준다. eval_metric(측정 지표/프로토콜 정의)과 pattern(측정값이
    조건에 따라 보인 추세)은 둘 다 "observable"에 속하는 실제 카테고리로, 각각 E/P로
    넘버링된다(observable 자체는 노드 라벨이 아니라 이 둘을 부르는 이름). node_id/
    source_span은 청크 내부에서 1부터 다시 매겨진다. 모든 청크가 끝나면 카테고리별로
    이 논문 안에서 전역 번호(A1..AN 등)를 다시 매기며 병합하고, 모든 노드에 이 논문의
    paper_id를 태깅해 assumption.json / mechanism.json / context.json /
    intervention.json / observable.json(eval_metric+pattern을 나눠 담음) /
    unresolved.json 6개 파일로 저장한다. node_id는 이 논문 안에서만 전역이며(예:
    "A3"), 여러 논문을 가로지르는 전역 유일성은 assemble_global.py가 "{paper_id}::A3"
    형태로 만들어준다.

사용 예:
    python extract_aio.py --pdf papers/2409.16118v3.pdf --paper-id 2409.16118v3
    python extract_aio.py --pdf papers/2409.16118v3.pdf --pages-per-chunk 6
    python extract_aio.py --input paper_chunk.txt --paper-id my_paper
    python extract_aio.py --text "some text" --model gemini-2.5-pro --temperature 0

여러 논문을 처리한 뒤에는:
    python assemble_global.py --outputs-dir outputs
"""

import argparse
import datetime
import json
import sys
import traceback
from pathlib import Path

from llm_client import generate_with_retry, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_OUTPUT_TOKENS
from batch_utils import (
    CATEGORY_PREFIX,
    FLAT_CATEGORIES,
    OBSERVABLE_SUBCATEGORIES,
    load_prompt,
    page_chunks,
    parse_json_response,
    usage_of,
    add_usage,
    token_line,
    merge_node_chunks,
)

SCRIPT_DIR = Path(__file__).resolve().parent
P1_SYSTEM_PROMPT_PATH = SCRIPT_DIR / "prompts" / "p1.md"
OUTPUT_BUCKETS = list(CATEGORY_PREFIX.keys())  # CATEGORIES + "unresolved"
KST = datetime.timezone(datetime.timedelta(hours=9))  # 실행 서버 시간대와 무관하게 산출물 이름은 한국 시간 기준

MAX_CALL_ATTEMPTS = 3  # API 호출 자체가 실패할 때(네트워크/일시적 오류)의 재시도 횟수
RETRY_BACKOFF_SECONDS = 5


def parse_args():
    parser = argparse.ArgumentParser(description="Stage 1: per-paper Gemini node extraction (chunked to stay under output-token limits). Run assemble_global.py afterward to canonicalize + assemble factors across papers.")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--pdf", type=str, help="입력 논문 PDF 파일 경로 (페이지 구간별로 청크 분할)")
    input_group.add_argument("--input", type=str, help="입력 텍스트 파일 경로 (청크 분할 없이 단일 입력으로 취급)")
    input_group.add_argument("--text", type=str, help="입력 텍스트를 직접 문자열로 전달 (청크 분할 없이 단일 입력으로 취급)")

    parser.add_argument("--p1-system-prompt", type=str, default=str(P1_SYSTEM_PROMPT_PATH), help="Stage 1(추출) SYSTEM 프롬프트 파일 경로")
    parser.add_argument("--paper-id", type=str, default="PXX", help="이 논문의 고유 id. 모든 추출 노드에 태깅되고, Stage 2에서 논문을 가로질러 node_id를 전역 유일하게 만드는 데 쓰이므로 여러 논문을 같이 처리할 계획이면 논문마다 달라야 한다.")
    parser.add_argument("--paper-title-hint", type=str, default="unknown", help="프롬프트에 채워넣을 paper_title_hint (참고/로깅용)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--max-output-tokens", type=int, default=DEFAULT_MAX_OUTPUT_TOKENS, help="호출당 최대 output token (기본: 모델 최대치인 65536)")
    parser.add_argument("--pages-per-chunk", type=int, default=6, help="--pdf 사용 시, 호출 1회당 처리할 페이지 수")
    parser.add_argument("--run-dir", type=str, default=None, help="산출물(카테고리별 노드 json, 청크별 raw 응답, metadata)을 저장할 디렉터리 (생략 시 outputs/ 아래에 자동 생성; 이 디렉터리를 assemble_global.py --run-dirs에 넘긴다)")
    parser.add_argument("--api-key", type=str, default=None, help="GEMINI_API_KEY를 인자로 직접 override (생략 시 .env/환경변수 사용)")
    return parser.parse_args()


def build_source_chunks(args):
    """--pdf는 페이지 구간별 sub-PDF 청크로, --text/--input은 청크 분할 없이 단일
    가상 청크로 변환해 이후 파이프라인이 동일한 코드 경로를 쓰게 한다."""
    if args.pdf:
        pdf_path = Path(args.pdf)
        chunks = page_chunks(pdf_path.read_bytes(), args.pages_per_chunk)
        total_pages = chunks[-1]["page_end"] if chunks else 0
        source_name = pdf_path.stem
        return chunks, total_pages, source_name

    input_text = args.text if args.text is not None else Path(args.input).read_text(encoding="utf-8")
    chunk = {
        "chunk_index": 1,
        "page_start": None,
        "page_end": None,
        "page_range": "n/a",
        "pdf_bytes": None,
        "text": input_text,
    }
    source_name = "text_input"
    return [chunk], None, source_name


def chunk_context_note(chunk, n_chunks, total_pages):
    """청크가 전체 문서의 일부 페이지만 담은 sub-PDF임을 알려주는 짧은 안내문. sub-PDF
    자체에 해당 페이지만 들어 있으므로 모델이 다른 페이지 내용을 지어낼 수는 없지만,
    "location"에 적을 실제 페이지 번호를 정확히 알려주기 위해 페이지 구간만 짧게 덧붙인다
    (JooKyung의 aiocm_debug_v5 원본은 이 안내문 없이 PDF 자체만으로 충분했으므로, 여기서도
    최소한만 남긴다)."""
    if total_pages is None:
        return "(The following is the full source text for this request.)"
    return f"(This excerpt covers PDF pages {chunk['page_range']} of {total_pages} total pages.)"


# ---------------------------------------------------------------------------
# Stage 1: per-chunk node extraction
# ---------------------------------------------------------------------------

def run_stage1(args, p1_system_prompt, chunks, total_pages, run_dir):
    n_chunks = len(chunks)
    chunk_results = []
    per_chunk_meta = []
    total_usage = None
    any_salvaged = False
    any_success = False

    for c in chunks:
        idx = c["chunk_index"]
        print(f"[stage1 chunk {idx}/{n_chunks}] pages {c['page_range']} ...", file=sys.stderr)

        note = chunk_context_note(c, n_chunks, total_pages)
        if c["pdf_bytes"] is not None:
            user_prompt, pdf_bytes = note, c["pdf_bytes"]
        else:
            user_prompt = f"{note}\n\n--- SOURCE TEXT START ---\n{c['text']}\n--- SOURCE TEXT END ---"
            pdf_bytes = None

        finish_reason, usage, parse_error, salvaged = None, None, None, False
        spans = []  # flat list: [{"node_id","source_span","parent","text","location",...,"assigned_label","confidence"}]
        raw_text = ""

        try:
            response = generate_with_retry(
                max_attempts=MAX_CALL_ATTEMPTS,
                retry_backoff_seconds=RETRY_BACKOFF_SECONDS,
                system_prompt=p1_system_prompt,
                user_prompt=user_prompt,
                pdf_bytes=pdf_bytes,
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
                if isinstance(parsed, list):
                    spans = parsed
                any_success = True
            except json.JSONDecodeError as e:
                parse_error = str(e)
        except Exception as e:
            parse_error = f"API call failed after {MAX_CALL_ATTEMPTS} attempts: {e}"
            print(f"  [ERROR] stage1 chunk {idx}: {parse_error}", file=sys.stderr)

        (run_dir / f"stage1_chunk_{idx:02d}_p{c['page_range']}.md").write_text(raw_text, encoding="utf-8")
        any_salvaged = any_salvaged or salvaged

        if finish_reason and "STOP" not in finish_reason:
            print(f"  [WARN] stage1 chunk {idx} finish_reason={finish_reason} (may be truncated)", file=sys.stderr)
        if salvaged:
            print(f"  [WARN] stage1 chunk {idx} salvaged from truncation ({len(spans)} spans recovered)", file=sys.stderr)
        if parse_error:
            print(f"  [WARN] stage1 chunk {idx} JSON parse failed: {parse_error}", file=sys.stderr)

        label_tally = {}
        for s in spans:
            label = (s.get("assigned_label") if isinstance(s, dict) else None) or "unresolved"
            label_tally[label] = label_tally.get(label, 0) + 1

        chunk_results.append({"chunk_index": idx, "page_range": c["page_range"], "spans": spans})
        per_chunk_meta.append({
            "chunk_index": idx,
            "page_range": c["page_range"],
            "span_count": len(spans),
            "label_tally": label_tally,
            "finish_reason": finish_reason,
            "salvaged": salvaged,
            "parse_error": parse_error,
            "usage": usage,
        })

    if not any_success:
        raise RuntimeError(f"Stage 1: all {n_chunks} chunk(s) failed to produce usable output; see {run_dir} for raw responses/errors.")

    node_lists = merge_node_chunks(chunk_results)
    return node_lists, per_chunk_meta, total_usage, any_salvaged


def tag_paper_id(node_lists, paper_id):
    """모든 카테고리(+ unresolved)의 모든 노드에 이 논문의 paper_id를 태깅한다.
    Stage 2(assemble_global.py)가 여러 논문의 노드를 하나의 pool로 모을 때 이 값으로
    node_id를 전역 유일하게 만들고("{paper_id}::{node_id}"), factor 조립 시 어떤 노드가
    같은 논문(=같은 실험 단위일 가능성)에서 왔는지 판단하는 데 쓴다."""
    for cat in OUTPUT_BUCKETS:
        for n in node_lists.get(cat) or []:
            n["paper_id"] = paper_id
    return node_lists


def main():
    args = parse_args()
    p1_system_prompt = load_prompt(args.p1_system_prompt, paper_id=args.paper_id, paper_title_hint=args.paper_title_hint)

    chunks, total_pages, source_name = build_source_chunks(args)

    now = datetime.datetime.now(KST)
    if args.run_dir:
        run_dir = Path(args.run_dir)
    else:
        run_dir = SCRIPT_DIR / "outputs" / f"{source_name}_{now.strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "timestamp": now.isoformat(),
        "source": args.pdf or (args.input or "(--text)"),
        "paper_id": args.paper_id,
        "paper_title_hint": args.paper_title_hint,
        "model": args.model,
        "temperature": args.temperature,
        "max_output_tokens": args.max_output_tokens,
        "pages_per_chunk": args.pages_per_chunk,
        "n_chunks": len(chunks),
        "total_pages": total_pages,
    }

    try:
        print(f"[INFO] stage 1: extracting nodes from {len(chunks)} chunk(s)...", file=sys.stderr)
        node_lists, stage1_meta, stage1_usage, stage1_salvaged = run_stage1(args, p1_system_prompt, chunks, total_pages, run_dir)
        node_lists = tag_paper_id(node_lists, args.paper_id)

        node_counts = {cat: len(node_lists[cat]) for cat in OUTPUT_BUCKETS}
        for cat in FLAT_CATEGORIES:
            (run_dir / f"{cat}.json").write_text(json.dumps(node_lists[cat], indent=2, ensure_ascii=False), encoding="utf-8")
        (run_dir / "unresolved.json").write_text(json.dumps(node_lists["unresolved"], indent=2, ensure_ascii=False), encoding="utf-8")
        observable_bundle = {sub: node_lists[sub] for sub in OBSERVABLE_SUBCATEGORIES}
        (run_dir / "observable.json").write_text(json.dumps(observable_bundle, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[INFO] stage 1 done: {node_counts} (total {sum(node_counts.values())} nodes, {node_counts['unresolved']} unresolved). Saved to {run_dir}/<category>.json (eval_metric+pattern bundled into observable.json)", file=sys.stderr)

        total_usage = stage1_usage
        metadata["status"] = "success"
        metadata["stage1"] = {"node_counts": node_counts, "any_salvaged": stage1_salvaged, "chunks": stage1_meta, "usage": stage1_usage}
        metadata["usage_total"] = total_usage
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"[INFO] tokens (stage1): {token_line(total_usage)}", file=sys.stderr)
        print(f"[INFO] run artifacts saved under: {run_dir}", file=sys.stderr)
        print(f"[INFO] once all papers are extracted, run: python assemble_global.py --run-dirs {run_dir} [more run_dirs...]", file=sys.stderr)
    except Exception:
        metadata["status"] = "error"
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        print(traceback.format_exc(), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
