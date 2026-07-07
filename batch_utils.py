"""
PDF 페이지 청킹 + JSON 파싱(트렁케이션 복구) + 파이프라인 병합 유틸리티.

JooKyung/AIO-System/Layer 1/test_gemini/aio_common.py의 아이디어(페이지 단위 청킹,
잘린 JSON 응답 salvage, 청크별 usage 합산)를 참고하되, 이 프로젝트의 스키마에 맞게
일반화했다.

파이프라인은 두 단계로 나뉜다 (extract_aio.py = Stage 1, assemble_global.py = Stage 2):

- page_chunks: PDF를 페이지 구간별 sub-PDF로 분할한다 (Gemini의 output token 한계를
  넘지 않도록, 한 번의 호출이 처리하는 페이지 수를 제한하기 위함). Stage 1(논문 1편)에서만
  쓰인다.
- parse_json_response: 코드펜스를 벗기고, 정상 파싱이 실패하면(=max_output_tokens에
  걸려 응답이 중간에 잘린 경우) 괄호/문자열 상태를 추적해 "안전하게 잘라낼 수 있는
  지점"들을 찾고, 그 지점에서 남은 컨테이너를 닫아 재파싱을 시도한다(salvage). Stage
  1/2 공통으로 쓰인다.
- merge_node_chunks (Stage 1 청크 병합): 각 청크는 assigned_label이 달린 flat span
  배열을 출력한다(청크마다 source_span이 S1부터 다시 시작). 이를 카테고리별로 나누면서
  node_id(A1/M1/...)를 전역 시퀀스로 재번호하고, source_span/parent도 청크 내에서
  전역 S-번호로 재매핑해 같은 문장에서 나온 노드들의 연결(parent)이 카테고리 파일이
  나뉜 뒤에도 유지되게 한다. 논문(paper_id) 안에서만 전역이며, 여러 논문을 가로지르는
  전역성은 Stage 2에서 비로소 생긴다.
- chunk_list / sort_for_batching / merge_registry_batches / merge_factor_batches_global
  (Stage 2 배치 분할 및 병합): Stage 2는 "여러 논문에서 모인 노드 전체 풀"을 대상으로
  한 번에 canonicalize/factor-조립하는 것이 원칙이라 기본값은 배치를 나누지 않는다
  (chunk_list(nodes, None) -> 통째로 1개 배치). 출력 토큰 한계 때문에 --max-nodes-per-batch로
  명시적으로 나눌 수도 있는데, 이때도 sort_for_batching으로 같은 카테고리 노드끼리
  묶어 cross-paper 중복 탐지 기회를 최대한 살린다. canonical_node_id/node_id는 Stage
  1에서 이미 전역이라 배치를 나눠도 재매핑이 필요 없고, factor_id만 배치마다 F1부터
  다시 시작하므로 전역 재번호가 필요하다.
"""
import json
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter

# "observable"은 실제 카테고리가 아니라 eval_metric(측정 지표/프로토콜 정의)과
# pattern(측정값이 조건에 따라 보인 추세/양상)이라는 두 개의 실제 카테고리를 묶어
# 부르는 이름이다. node_id 넘버링은 항상 eval_metric(E)/pattern(P)로만 매겨지고,
# observable.json / observable_canonicalized.json 저장 시에만 둘을 한 파일로 묶는다.
FLAT_CATEGORIES = ["assumption", "mechanism", "context", "intervention"]
OBSERVABLE_SUBCATEGORIES = ["eval_metric", "pattern"]
CATEGORIES = FLAT_CATEGORIES + OBSERVABLE_SUBCATEGORIES
# "unresolved"는 실제 카테고리가 아니라 Pass 1이 확신(confidence)이 낮을 때 붙이는
# 라벨이다. 별도 파일로만 남기고 Pass 2 factor 조립에는 넣지 않는다.
CATEGORY_PREFIX = {
    "assumption": "A",
    "mechanism": "M",
    "context": "C",
    "intervention": "I",
    "eval_metric": "E",
    "pattern": "P",
    "unresolved": "U",
}


def load_prompt(prompt_path, **subs):
    """프롬프트 템플릿을 읽고 {key} 자리를 값으로 치환한다."""
    text = Path(prompt_path).read_text(encoding="utf-8")
    for key, value in subs.items():
        text = text.replace("{" + key + "}", value)
    return text


def page_chunks(pdf_bytes, pages_per_chunk):
    """PDF를 페이지 구간별 sub-PDF로 분할한다.

    반환: chunk_index(1-base), page_start/page_end(1-base), page_range(문자열),
    bytes(해당 구간만 담은 새 PDF)를 담은 dict의 리스트, reading order.
    """
    if pages_per_chunk <= 0:
        raise ValueError("pages_per_chunk must be a positive integer")

    reader = PdfReader(BytesIO(pdf_bytes))
    n = len(reader.pages)
    chunks = []
    for start in range(0, n, pages_per_chunk):
        end = min(start + pages_per_chunk, n)
        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        buf = BytesIO()
        writer.write(buf)
        chunks.append({
            "chunk_index": len(chunks) + 1,
            "page_start": start + 1,
            "page_end": end,
            "page_range": f"{start + 1}-{end}",
            "pdf_bytes": buf.getvalue(),
            "text": None,
        })
    return chunks


def _strip_code_fence(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        t = t.rsplit("```", 1)[0]
    return t.strip()


def _repair_truncated_json(t):
    """잘린 JSON 텍스트에서 안전하게 자를 수 있는 지점들을 찾아, 가장 뒤에서부터
    시도하며 남은 괄호를 닫아 재파싱한다. 최상위가 배열/객체 어느 쪽이든 동작하고,
    중첩 구조 안에서도 완전한 값 단위로만 잘라내므로 깨진 값이 섞여 들어가지 않는다.
    """
    stack = []  # 현재까지 열려 있는 '{'/'[' 스택
    in_string = False
    escape = False
    candidates = []  # (cut_index, 그 시점의 stack 스냅샷)

    for i, ch in enumerate(t):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch in "{[":
            stack.append(ch)
        elif ch in "}]":
            if stack:
                stack.pop()
            if stack:
                # 값 하나가 방금 닫혔고, 아직 바깥 컨테이너가 남아있다 -> 여기서 잘라도 안전
                candidates.append((i + 1, list(stack)))
        elif ch == "," and stack:
            # 콤마 직전까지는 완전한 값이다 -> 콤마를 버리고 여기서 잘라도 안전
            candidates.append((i, list(stack)))

    for cut, snapshot in reversed(candidates):
        closing = "".join("}" if c == "{" else "]" for c in reversed(snapshot))
        try:
            return json.loads(t[:cut] + closing)
        except json.JSONDecodeError:
            continue

    raise json.JSONDecodeError("could not repair truncated JSON", t, 0)


def parse_json_response(text):
    """모델 응답(코드펜스 포함 가능, 잘렸을 수 있음)에서 JSON을 파싱한다.
    반환: (parsed_obj, salvaged_bool). 살릴 수 없으면 json.JSONDecodeError를 낸다.
    """
    t = _strip_code_fence(text)
    try:
        return json.loads(t), False
    except json.JSONDecodeError:
        return _repair_truncated_json(t), True


def usage_of(response):
    """GenerateContentResponse에서 토큰 usage를 뽑아낸다 (없으면 None)."""
    u = getattr(response, "usage_metadata", None)
    if not u:
        return None
    return {
        "prompt_token_count": getattr(u, "prompt_token_count", None),
        "thoughts_token_count": getattr(u, "thoughts_token_count", None),
        "candidates_token_count": getattr(u, "candidates_token_count", None),
        "total_token_count": getattr(u, "total_token_count", None),
    }


def add_usage(acc, new):
    """usage dict 두 개를 필드별로 합산한다 (None은 0으로 취급)."""
    if new is None:
        return acc
    if acc is None:
        acc = {k: 0 for k in new}
    return {k: (acc.get(k) or 0) + (new.get(k) or 0) for k in new}


def token_line(usage):
    """usage 요약 한 줄."""
    if not usage:
        return "no usage reported"
    return (
        f"prompt={usage.get('prompt_token_count')} "
        f"thoughts={usage.get('thoughts_token_count')} "
        f"output={usage.get('candidates_token_count')} "
        f"total={usage.get('total_token_count')}"
    )


# ---------------------------------------------------------------------------
# Pass 1 (per-chunk extraction) merge
# ---------------------------------------------------------------------------

def merge_node_chunks(chunk_results):
    """Pass 1의 청크별 flat span 배열을 카테고리별 전역 리스트로 나누며 합친다.

    chunk_results: chunk_index, page_range, spans(list of {node_id, source_span,
    parent, text, location, experiment_ref(intervention/pattern만), classification_reasoning,
    alternative_labels_considered, ambiguity_reason, assigned_label, confidence})를 담은
    dict의 리스트, 처리 순서(=문서 reading order)대로.

    각 청크는 독립적으로 카테고리별 node_id(A1/M1/...)와 source_span(S1...)을 1부터
    다시 매기므로, 그대로 합치면 서로 다른 청크의 A1/S1이 충돌한다. 이를 막기 위해:
    - node_id: 카테고리별로 전역 시퀀스(A1..AN, M1..MN, ...)로 재번호. confidence가
      낮아 assigned_label이 "unresolved"인 span은 별도의 U1..UN 시퀀스로 분리한다
      (실제 카테고리가 아니므로 CATEGORIES에는 포함되지 않고, unresolved.json으로만
      저장되어 Pass 2 factor 조립 대상에서는 제외된다).
    - source_span/parent: 청크 내에서 등장한 순서대로 전역 S-번호로 재매핑해, 같은
      원문 문장에서 갈라져 나온 노드들의 연결 관계(parent)가 카테고리별로 파일이
      나뉜 뒤에도 유지되게 한다.

    반환: {category: [{"node_id", "source_span", "parent", "text", "location",
    "experiment_ref", "confidence", "ambiguity_reason", "source_chunk", "page_range"}, ...]} -
    카테고리별(+ "unresolved") 전역 리스트. "experiment_ref"는 Stage 1에서는 아직 raw
    문자열(또는 None)이고, Stage 2A(canonicalize)가 리스트로 바꾼다.
    """
    buckets = list(CATEGORY_PREFIX.keys())  # CATEGORIES + "unresolved"
    merged = {cat: [] for cat in buckets}
    counters = {cat: 0 for cat in buckets}
    global_ss = 0

    for cr in chunk_results:
        spans = cr.get("spans") or []

        # 1) 이 청크에서 등장하는 모든 source_span을 등장 순서대로 수집해 전역 S-번호를 배정.
        ss_map = {}
        for s in spans:
            old = s.get("source_span")
            if old is not None and old not in ss_map:
                global_ss += 1
                ss_map[old] = f"S{global_ss}"

        # 2) 카테고리별 node_id 재번호 + source_span/parent 재매핑 + provenance 태깅.
        for s in spans:
            label = s.get("assigned_label") or "unresolved"
            bucket = label if label in merged else "unresolved"
            counters[bucket] += 1

            new_node = {
                "node_id": f"{CATEGORY_PREFIX[bucket]}{counters[bucket]}",
                "source_span": ss_map.get(s.get("source_span"), s.get("source_span")),
                "parent": ss_map.get(s.get("parent"), s.get("parent")) if s.get("parent") is not None else None,
                "text": s.get("text"),
                "location": s.get("location"),
                "experiment_ref": s.get("experiment_ref"),  # intervention/pattern에만 있음 (R1c); 그 외 카테고리는 None
                "confidence": s.get("confidence"),
                "ambiguity_reason": s.get("ambiguity_reason"),
                "source_chunk": cr["chunk_index"],
                "page_range": cr["page_range"],
            }
            merged[bucket].append(new_node)

    return merged


# ---------------------------------------------------------------------------
# Stage 2 (global cross-paper canonicalization + global ID-only factor assembly)
# ---------------------------------------------------------------------------

def chunk_list(items, chunk_size):
    """items를 chunk_size개씩 나눈다. chunk_size가 None/0이면 통째로 하나의 배치로 묶는다
    (기본값 - Stage 2 프롬프트는 "전체 풀을 한 번에 본다"는 전제로 쓰여 있으므로, 노드 수가
    출력 토큰 한계를 넘길 걸로 예상될 때만 --max-nodes-per-batch로 명시적으로 쪼갠다).
    """
    if not items:
        return []
    if not chunk_size:
        return [items]
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def sort_for_batching(nodes):
    """카테고리("label")별로 묶어 정렬한다. 배치를 나눠야 할 때 같은 카테고리의 노드끼리
    (여러 논문에서 온 노드라도) 같은 배치에 들어가야 cross-paper 중복 탐지 기회가 생긴다."""
    cat_rank = {c: i for i, c in enumerate(CATEGORIES)}
    return sorted(nodes, key=lambda n: cat_rank.get(n.get("label"), len(CATEGORIES)))


def merge_registry_batches(batch_registries):
    """Stage 2A(canonicalization) 배치별 node_registry 리스트를 이어붙인다. canonical_node_id는
    Stage 1에서 이미 전역으로 번호가 매겨져 있으므로(파일 저장 시 paper별로 유니크했던 것을
    Stage 2 로딩 시 "{paper_id}:{node_id}" 형태로 다시 유니크화하므로) 재매핑이 필요 없다.

    batch_registries: 배치 순서대로, 각 배치의 node_registry(list)를 담은 리스트.
    """
    merged = []
    for batch_index, registry in enumerate(batch_registries, start=1):
        for reg in registry or []:
            new_reg = dict(reg)
            new_reg["source_batch"] = batch_index
            merged.append(new_reg)
    return merged


def merge_factor_batches_global(batch_factor_lists):
    """Stage 2B(factor 조립) 배치별 factors 리스트를 하나로 합친다. factor_id만 배치마다
    F1부터 다시 시작하므로 전역 순서로 재번호한다 (node_id는 이미 전역이라 재매핑 불필요).

    batch_factor_lists: 배치 순서대로, 각 배치의 factors(list)를 담은 리스트.
    """
    merged = []
    global_n = 0
    for batch_index, factors in enumerate(batch_factor_lists, start=1):
        for f in factors or []:
            new_f = dict(f)
            global_n += 1
            new_f["factor_id"] = f"F{global_n}"
            new_f["source_batch"] = batch_index
            merged.append(new_f)
    return merged


def apply_canonicalization(node_lists, node_registry):
    """Stage 2A의 node_registry(중복 클러스터 + 텍스트 일반화)를 카테고리별 노드 리스트에
    적용해, canonicalization "이후" 버전을 만든다. 클러스터에서 canonical이 아닌(=병합되어
    사라진) node_id는 제거하고, 살아남은 canonical 노드에는 어떤 id들이 그리로 합쳐졌는지
    "merged_from"으로 남긴다. node_registry 항목에 "canonical_text"가 있으면(다른 논문에서도
    재사용 가능하도록 불필요한 세부사항을 뺀 일반화된 문장) 해당 canonical 노드의 "text"를
    그 값으로 교체하고, 원문은 "original_text"로 보존한다.

    node_lists: 여러 논문의 merge_node_chunks() 결과를 합쳐 만든 전역 pool (category ->
    node list; "unresolved" 포함해도 무방하지만 canonicalization은 CATEGORIES에 대해서만
    계산한다). node_id는 assemble_global.py가 이미 "{paper_id}::{원래 node_id}" 형태로
    전역 유니크화해둔 값이어야 한다.
    node_registry: merge_registry_batches()가 만든 최종 node_registry 리스트. intervention/
    pattern 노드는 "experiment_ref"가 리스트(병합됐으면 원본들의 합집합)로 들어있을 수
    있고, 있으면 canonical 노드의 experiment_ref를 그 리스트로 덮어써 cross-ref 병합 결과가
    <category>_canonicalized.json에도 반영되게 한다.

    반환: {category: [node, ...]} - CATEGORIES 각각에 대한 canonicalization 이후 리스트.
    """
    absorbed = set()  # 병합되어 사라지는(=canonical이 아닌) node_id
    merged_from = {}  # canonical_node_id -> [흡수된 node_id, ...]
    canonical_text = {}  # canonical_node_id -> 일반화된 대체 text (있는 경우만)
    canonical_experiment_ref = {}  # canonical_node_id -> experiment_ref 리스트 (있는 경우만)

    for reg in node_registry or []:
        canonical = reg.get("canonical_node_id")
        members = reg.get("merged_node_ids") or []
        for m in members:
            if m != canonical:
                absorbed.add(m)
        if canonical:
            merged_from.setdefault(canonical, [])
            merged_from[canonical].extend(m for m in members if m != canonical)
            text = reg.get("canonical_text")
            if text:
                canonical_text[canonical] = text
            ref = reg.get("experiment_ref")
            if ref is not None:
                canonical_experiment_ref[canonical] = ref

    canonicalized = {}
    for cat in CATEGORIES:
        kept = []
        for n in node_lists.get(cat) or []:
            if n["node_id"] in absorbed:
                continue
            new_n = dict(n)
            if n["node_id"] in merged_from:
                new_n["merged_from"] = merged_from[n["node_id"]]
            if n["node_id"] in canonical_text:
                new_n["original_text"] = new_n["text"]
                new_n["text"] = canonical_text[n["node_id"]]
            if n["node_id"] in canonical_experiment_ref:
                new_n["experiment_ref"] = canonical_experiment_ref[n["node_id"]]
            kept.append(new_n)
        canonicalized[cat] = kept
    return canonicalized


def find_incomplete_factors(factors, experiment_ref_by_id=None):
    """p2b_assemble.md의 HARD GATE를 위반하는 factor를 찾는다:
    (1) intervention이 정확히 하나 있어야 한다 (없으면 위반).
    (2) observable pair 중 "pattern"이 채워진 쌍이 최소 하나 있어야 한다 (eval_metric만
        있고 pattern이 없는 건 관측이 아니므로 인정하지 않는다).
    (3) ANCHOR INTEGRITY (pattern만 검사): factor에 쓰인 모든 pattern의 experiment_ref
        리스트가 intervention의 experiment_ref 리스트와 최소 하나는 겹쳐야 한다(set overlap,
        완전 일치가 아님 - canonicalization에서 서로 다른 experiment_ref를 가진 노드끼리도
        내용이 같으면 병합했을 수 있어 리스트가 여러 개일 수 있다). eval_metric은 이 검사에서
        완전히 면제된다 (experiment_ref 자체가 없음). experiment_ref_by_id(node_id ->
        experiment_ref 리스트 dict)가 주어지면 코드로 직접 검증하고, 생략하면 건너뛴다.

    LLM 출력을 신뢰하되(자동으로 factor를 지우거나 고치지 않음) 위반 사례만 모아
    metadata에 기록해 후속 확인이 가능하게 한다.

    반환: [{"factor_id", "missing": [위반한 규칙, ...]}, ...] - 하나라도 위반한 factor만.
    """
    incomplete = []
    for f in factors or []:
        violations = []

        intervention_id = f.get("intervention")
        if not intervention_id:
            violations.append("missing_intervention")

        observable_pairs = f.get("observable") or []
        pattern_ids = [(pair or {}).get("pattern") for pair in observable_pairs if (pair or {}).get("pattern")]
        if not pattern_ids:
            violations.append("missing_pattern")

        if intervention_id and pattern_ids and experiment_ref_by_id is not None:
            intervention_refs = set(experiment_ref_by_id.get(intervention_id) or [])
            no_overlap = [pid for pid in pattern_ids if not (set(experiment_ref_by_id.get(pid) or []) & intervention_refs)]
            if no_overlap:
                violations.append(f"experiment_ref_no_overlap:{no_overlap}")

        if violations:
            incomplete.append({"factor_id": f.get("factor_id"), "missing": violations})
    return incomplete


def build_id_only_descriptors(all_nodes, node_registry):
    """Stage 2A(canonicalize)의 node_registry를 이용해 Stage 2B(ID-only 조립)에 넘길
    경량 서술자 {"node_id", "label", "experiment_ref"(intervention/pattern만), "text"}
    목록을 만든다. "text"는 canonicalization이 다시 쓴 문장("canonical_text")이 있으면
    그것을, 없으면 원본 pool의 text를 그대로 쓴다. "experiment_ref"는 intervention/pattern
    노드에만 리스트로 붙고(등록 항목의 값을 우선, 없으면 원본의 단일 문자열을 리스트로
    감싼다), assumption/mechanism/context/eval_metric 노드에는 키 자체를 넣지 않는다.

    all_nodes: Stage 2A에 실제로 넘긴 전역 노드 pool (flat list; 각 노드는 이미 전역 유일
    "node_id"와 "label"/"text"를 갖고 있어야 하고, intervention/pattern은 "experiment_ref"
    (원본 단일 문자열 또는 None)도 갖고 있어야 한다).
    node_registry: Stage 2A가 만든 canonicalization 결과. 병합되었거나 문장/experiment_ref가
    바뀐 노드만 항목이 있을 수 있고(단순 통과 노드는 항목이 없어도 됨), 그런 노드는 원본
    pool의 값으로 보완한다.

    반환: (descriptors, unregistered_node_ids) - unregistered_node_ids는 흡수되지 않고
    살아남았지만 node_registry에 항목이 없어서 원본 pool 값만으로 서술자를 만든 노드 id
    목록 (참고용; text 자체는 원본 그대로라 품질 손실은 없다).
    """
    by_id = {n["node_id"]: n for n in all_nodes}

    absorbed = set()
    entry_by_canonical = {}
    for reg in node_registry or []:
        canonical = reg.get("canonical_node_id")
        if not canonical:
            continue
        entry_by_canonical[canonical] = reg
        for m in reg.get("merged_node_ids") or []:
            if m != canonical:
                absorbed.add(m)

    descriptors = []
    unregistered = []
    for node_id, n in by_id.items():
        if node_id in absorbed:
            continue
        entry = entry_by_canonical.get(node_id)
        label = (entry.get("label") if entry else None) or n.get("label")
        text = (entry.get("canonical_text") if entry else None) or n.get("text")

        descriptor = {"node_id": node_id, "label": label}
        if label in ("intervention", "pattern"):
            ref = entry.get("experiment_ref") if entry else None
            if ref is None:
                raw_ref = n.get("experiment_ref")
                ref = [raw_ref] if raw_ref else []
            descriptor["experiment_ref"] = ref
        descriptor["text"] = text
        descriptors.append(descriptor)

        if not entry:
            unregistered.append(node_id)
    return descriptors, unregistered
