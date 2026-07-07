"""
LLM 호출 없이, result.json의 factor(node_id 참조로만 되어 있는 assumption/mechanism/
context/intervention/observable)를 <category>_canonicalized.json + observable_canonicalized.json
에서 실제 node(text/location/paper_id 등)를 찾아 채워, 사람이 바로 읽을 수 있는 형태로
바꾸는 순수 로컬 후처리 스크립트.

result.json 자체에는 factor마다 node_id만 있고, 그 node_id가 가리키는 실제 문장은
canonicalization이 적용된 <category>_canonicalized.json(assumption/mechanism/context/
intervention)과 observable_canonicalized.json(eval_metric/pattern)에 흩어져 있다. 이
스크립트는 그 두 종류의 파일을 한 run_dir에서 같이 읽어 node_id -> node 매핑을 만들고,
factor의 각 필드를 그 매핑으로 치환한다.

두 세대의 factor 스키마를 모두 지원한다:
  - 이전(단일 논문 배치) 스키마: assumption/context/intervention이 단일 node_id 문자열
    또는 null, observable이 {"eval_metric","pattern"} 단일 dict.
  - 현재(assemble_global.py) 스키마: assumption/context가 node_id 리스트, observable이
    {"eval_metric","pattern"} pair의 리스트.
값이 리스트인지 아닌지로 자동 판별하므로 별도 옵션 없이 둘 다 그대로 넣으면 된다.

사용 예:
    python resolve_factors.py --run-dir outputs/global_20260101_000000
    python resolve_factors.py --run-dir outputs/VARC_20260707_115413 --output readable.json
"""

import argparse
import json
import sys
from pathlib import Path

from batch_utils import FLAT_CATEGORIES, OBSERVABLE_SUBCATEGORIES

DEFAULT_FIELDS = ["text", "paper_id", "location"]


def load_node_lookup(run_dir):
    """run_dir의 <category>_canonicalized.json(+ observable_canonicalized.json)을 모두
    읽어 node_id -> node dict 매핑을 만든다. 파일이 없는 카테고리는 조용히 건너뛴다
    (예: intervention이 하나도 없었던 논문)."""
    run_dir = Path(run_dir)
    lookup = {}

    for cat in FLAT_CATEGORIES:
        path = run_dir / f"{cat}_canonicalized.json"
        if not path.exists():
            continue
        for n in json.loads(path.read_text(encoding="utf-8")):
            lookup[n["node_id"]] = n

    observable_path = run_dir / "observable_canonicalized.json"
    if observable_path.exists():
        bundle = json.loads(observable_path.read_text(encoding="utf-8"))
        for sub in OBSERVABLE_SUBCATEGORIES:
            for n in bundle.get(sub) or []:
                lookup[n["node_id"]] = n

    return lookup


def resolve_node(node_id, lookup, fields):
    """node_id 하나를 lookup에서 찾아 {"node_id", <fields>...}로 바꾼다. null이면 null을
    그대로 돌려주고, lookup에 없으면(canonicalization으로 흡수됐는데 factor가 옛 id를 여전히
    참조하는 경우 등) "_warning"을 달아 표시한다."""
    if node_id is None:
        return None
    node = lookup.get(node_id)
    if node is None:
        return {
            "node_id": node_id,
            "text": None,
            "_warning": "node_id not found in *_canonicalized.json (absorbed by canonicalization, or a data issue)",
        }
    resolved = {"node_id": node_id}
    for f in fields:
        if f in node:
            resolved[f] = node[f]
    return resolved


def resolve_id_or_list(value, lookup, fields):
    """assumption/context 필드: 이전 스키마는 단일 node_id 문자열, 현재 스키마는 리스트다.
    입력 형태를 그대로 유지해서(리스트면 리스트로, 단일이면 단일로) 돌려준다."""
    if value is None:
        return None
    if isinstance(value, list):
        return [resolve_node(v, lookup, fields) for v in value]
    return resolve_node(value, lookup, fields)


def resolve_observable(value, lookup, fields):
    """observable 필드: 이전 스키마는 {"eval_metric","pattern"} 단일 dict, 현재 스키마는
    그 dict들의 리스트다. 항상 리스트로 정규화해서 돌려준다(단일 입력도 원소 1개짜리
    리스트가 됨 - 두 스키마를 같은 모양으로 다루기 위함)."""
    if value is None:
        return None
    pairs = value if isinstance(value, list) else [value]
    return [
        {
            "eval_metric": resolve_node((pair or {}).get("eval_metric"), lookup, fields),
            "pattern": resolve_node((pair or {}).get("pattern"), lookup, fields),
        }
        for pair in pairs
    ]


def _collect_missing(resolved_value, missing_ids):
    """resolve_node가 만든 "_warning" 달린 항목들의 node_id를 모은다 (단일 dict/리스트 모두)."""
    items = resolved_value if isinstance(resolved_value, list) else [resolved_value]
    for item in items:
        if item and item.get("_warning"):
            missing_ids.add(item["node_id"])


def resolve_factors(factors, lookup, fields):
    resolved = []
    missing_ids = set()

    for f in factors:
        entry = {"factor_id": f.get("factor_id")}
        entry["assumption"] = resolve_id_or_list(f.get("assumption"), lookup, fields)
        entry["mechanism"] = resolve_node(f.get("mechanism"), lookup, fields)
        entry["context"] = resolve_id_or_list(f.get("context"), lookup, fields)
        entry["intervention"] = resolve_node(f.get("intervention"), lookup, fields)
        entry["observable"] = resolve_observable(f.get("observable"), lookup, fields)
        resolved.append(entry)

        _collect_missing(entry["assumption"], missing_ids)
        _collect_missing(entry["mechanism"], missing_ids)
        _collect_missing(entry["context"], missing_ids)
        _collect_missing(entry["intervention"], missing_ids)
        for pair in entry["observable"] or []:
            _collect_missing(pair.get("eval_metric"), missing_ids)
            _collect_missing(pair.get("pattern"), missing_ids)

    return resolved, missing_ids


def parse_args():
    parser = argparse.ArgumentParser(description="Resolve result.json's node_id-only factors into actual text, using *_canonicalized.json (no LLM call).")
    parser.add_argument("--run-dir", type=str, required=True, help="result.json + <category>_canonicalized.json + observable_canonicalized.json이 있는 디렉터리")
    parser.add_argument("--result-file", type=str, default=None, help="factor 목록이 있는 파일 경로 (생략 시 <run-dir>/result.json)")
    parser.add_argument("--output", type=str, default=None, help="결과를 저장할 파일 경로 (생략 시 <run-dir>/result_resolved.json)")
    parser.add_argument("--fields", type=str, nargs="+", default=DEFAULT_FIELDS, help=f"각 노드에서 가져올 필드 목록 (node_id는 항상 포함; 기본값: {DEFAULT_FIELDS})")
    return parser.parse_args()


def main():
    args = parse_args()
    run_dir = Path(args.run_dir)
    result_path = Path(args.result_file) if args.result_file else run_dir / "result.json"
    output_path = Path(args.output) if args.output else run_dir / "result_resolved.json"

    if not result_path.exists():
        print(f"[ERROR] {result_path} not found.", file=sys.stderr)
        sys.exit(1)

    factors = json.loads(result_path.read_text(encoding="utf-8")).get("factors") or []
    lookup = load_node_lookup(run_dir)
    print(f"[INFO] loaded {len(lookup)} canonicalized node(s) from {run_dir}", file=sys.stderr)

    resolved, missing_ids = resolve_factors(factors, lookup, args.fields)
    output_path.write_text(json.dumps({"factors": resolved}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[INFO] resolved {len(resolved)} factor(s) -> {output_path}", file=sys.stderr)

    if missing_ids:
        print(
            f"[WARN] {len(missing_ids)} node_id(s) referenced by factors were not found in "
            f"*_canonicalized.json (likely absorbed by canonicalization without the factor being "
            f"re-pointed to the canonical id, or a genuine data issue): {sorted(missing_ids)}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
