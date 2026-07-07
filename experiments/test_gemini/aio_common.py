"""Shared helpers for the AIO Layer-1 extraction pipeline (sync + batch)."""
import json
import re
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def load_prompt(prompt_path, **subs):
    """Read a prompt template and replace {key} placeholders with the given values."""
    text = Path(prompt_path).read_text(encoding="utf-8")
    for key, value in subs.items():
        text = text.replace("{" + key + "}", value)
    return text


def pdf_page_slice(pdf_bytes, page_start, page_end):
    """Return a fresh sub-PDF's bytes covering 1-indexed pages [page_start, page_end]
    (inclusive) of pdf_bytes."""
    reader = PdfReader(BytesIO(pdf_bytes))
    writer = PdfWriter()
    for i in range(page_start - 1, page_end):
        writer.add_page(reader.pages[i])
    buf = BytesIO()
    writer.write(buf)
    return buf.getvalue()


def page_chunks(pdf_bytes, pages_per_chunk):
    """Split a PDF into page-range sub-PDFs. Returns a list of dicts with a fresh
    sub-PDF's bytes plus its 1-indexed page range, in reading order."""
    reader = PdfReader(BytesIO(pdf_bytes))
    n = len(reader.pages)
    chunks = []
    for start in range(0, n, pages_per_chunk):
        end = min(start + pages_per_chunk, n)
        chunks.append({
            "chunk_index": len(chunks) + 1,
            "page_start": start + 1,
            "page_end": end,
            "page_range": f"{start + 1}-{end}",
            "bytes": pdf_page_slice(pdf_bytes, start + 1, end),
        })
    return chunks


def parse_json_array(text):
    """Parse a (possibly fenced, possibly truncated) JSON array from model output.
    Returns (list, salvaged_bool). Raises json.JSONDecodeError if nothing usable."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        t = t.split("```", 1)[0]
    t = t.strip()
    try:
        return json.loads(t), False
    except json.JSONDecodeError:
        # Salvage a truncated array: trim to the last complete object, then close it.
        last = t.rfind("},")
        if last != -1:
            return json.loads(t[:last + 1] + "\n]"), True
        raise


def usage_of(response):
    """Extract token usage from a GenerateContentResponse (or None)."""
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
    """Sum two usage dicts field-wise (treating None as 0)."""
    if new is None:
        return acc
    if acc is None:
        acc = {k: 0 for k in new}
    return {k: (acc.get(k) or 0) + (new.get(k) or 0) for k in new}


def token_line(usage):
    """One-line human-readable token summary."""
    if not usage:
        return "no usage reported"
    return (
        f"prompt={usage.get('prompt_token_count')} "
        f"thoughts={usage.get('thoughts_token_count')} "
        f"output={usage.get('candidates_token_count')} "
        f"total={usage.get('total_token_count')}"
    )


CATEGORY_PREFIX = {
    "assumption": "A",
    "context": "C",
    "mechanism": "M",
    "intervention": "I",
    "eval_metric": "E",
    "pattern": "P",
    "unresolved": "U",
}


def merge_spans(chunk_results):
    """Merge per-chunk node lists into one, fixing the id collisions that arise because each
    chunk restarts its numbering independently. For the v5 schema this means:

    - source_span (S-numbers): renumbered to a single global reading-order sequence (S1..SN),
      with all nodes from the same source sentence keeping the same new number.
    - parent (references a source_span S-number): remapped through the same per-chunk map.
    - node_id (per-category A1/C1/M1/I1/E1/P1): renumbered globally per category, in order.
    - each node tagged with source_chunk and page_range for provenance.

    chunk_results: list of dicts with keys chunk_index, page_range, spans (list)."""
    merged = []
    cat_counters = {}
    global_ss = 0
    for cr in chunk_results:
        ss_map = {}  # this chunk's old source_span -> new global source_span
        for s in cr.get("spans") or []:
            old = s.get("source_span")
            if old is not None and old not in ss_map:
                global_ss += 1
                ss_map[old] = f"S{global_ss}"
        for s in cr.get("spans") or []:
            new = dict(s)
            new.pop("span_id", None)  # legacy field from the old schema, if present

            old_ss = s.get("source_span")
            if old_ss in ss_map:
                new["source_span"] = ss_map[old_ss]

            parent = s.get("parent")
            if parent is not None:
                new["parent"] = ss_map.get(parent, parent)

            label = s.get("assigned_label") or "unresolved"
            prefix = CATEGORY_PREFIX.get(label, "U")
            cat_counters[prefix] = cat_counters.get(prefix, 0) + 1
            new["node_id"] = f"{prefix}{cat_counters[prefix]}"

            new["source_chunk"] = cr["chunk_index"]
            new["page_range"] = cr["page_range"]
            merged.append(new)
    return merged


# --- Coverage: how much of the paper did the extracted spans actually capture? -------------
# Two complementary signals are recorded per run:
#   1. text_char_coverage_pct — fraction of the paper's characters that fall inside a verbatim
#      span quote. This is the closest thing to "% of the paper covered". The denominator is a
#      full-text transcription of the paper produced *by Gemini* (see extract_text.py) and
#      cached next to the PDF as <name>.txt — we do NOT parse the PDF text layer locally
#      (pypdf is slow and empty on scanned/image PDFs). It is null when no such .txt exists.
#   2. structural counts — total spans, per-category counts, distinct source sentences.
# Coverage is diagnostic only; a failure here must never abort an extraction run.

CATEGORY_LABELS = ("assumption", "context", "mechanism", "intervention",
                   "eval_metric", "pattern", "unresolved")


def _norm(s):
    """Collapse whitespace and lowercase, so quote-vs-source matching is robust to reflow."""
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def quote_char_coverage(source_text, spans):
    """(covered_chars, total_chars): how many normalized characters of the paper's full text
    are spanned by the extracted verbatim quotes. Paraphrased spans (marked '(paraphrase)')
    and very short quotes (< 8 chars) are ignored. Returns (0, 0) when source_text is empty."""
    norm_text = _norm(source_text)
    total = len(norm_text)
    if total == 0:
        return 0, 0
    covered = bytearray(total)
    for s in spans or []:
        txt = s.get("text") or ""
        if "(paraphrase)" in txt:
            continue
        q = _norm(txt)
        if len(q) < 8:
            continue
        start = norm_text.find(q)
        if start == -1:
            continue
        for i in range(start, start + len(q)):
            covered[i] = 1
    return sum(covered), total


def category_counts(spans):
    """Per-category span counts keyed by full label (assumption/context/.../unresolved)."""
    counts = {label: 0 for label in CATEGORY_LABELS}
    for s in spans or []:
        label = s.get("assigned_label") or "unresolved"
        counts[label] = counts.get(label, 0) + 1
    return counts


# --- Figure / Table references: coverage is measured on THREE denominators, not one ---------
# text coverage    = chars of the prose transcript spanned by verbatim quotes
# figure coverage  = distinct figures cited by >=1 span / total figures in the paper
# table coverage   = distinct tables cited by >=1 span / total tables in the paper
# The figure/table denominators come from <pdf>.assets.json (enumerated by extract_text.py).

_FIG_RE = re.compile(r"\bfig(?:ure)?\.?\s*([0-9]+[a-z]?)", re.I)
_TAB_RE = re.compile(r"\btab(?:le)?\.?\s*([0-9]+[a-z]?)", re.I)


def ref_ids(text):
    """(figure_ids, table_ids) mentioned in a string, normalized to 'figure N' / 'table N'."""
    figs = {f"figure {m.group(1).lower()}" for m in _FIG_RE.finditer(text or "")}
    tabs = {f"table {m.group(1).lower()}" for m in _TAB_RE.finditer(text or "")}
    return figs, tabs


def cited_figures_tables(spans):
    """Union of figure/table ids that the extracted spans are grounded in (location + text)."""
    figs, tabs = set(), set()
    for s in spans or []:
        f, t = ref_ids(f"{s.get('location', '')} {s.get('text', '')}")
        figs |= f
        tabs |= t
    return figs, tabs


def _asset_set(asset_list, kind):
    """Normalize an assets.json figures/tables list into a set of 'figure N' / 'table N' ids."""
    out = set()
    for a in asset_list or []:
        raw = a.get("id", "") if isinstance(a, dict) else str(a)
        figs, tabs = ref_ids(raw)
        out |= (figs if kind == "figure" else tabs)
    return out


def load_asset_ids(assets_path):
    """Read <pdf>.assets.json -> (figure_ids, table_ids). Missing/bad file -> (set(), set())."""
    try:
        data = json.loads(Path(assets_path).read_text(encoding="utf-8"))
    except Exception:
        return set(), set()
    return _asset_set(data.get("figures"), "figure"), _asset_set(data.get("tables"), "table")


def _pct(n, d):
    return round(100 * n / d, 1) if d else None


def coverage_report(merged_spans, n_pages, char_covered, char_total,
                    figure_ids=None, table_ids=None):
    """Assemble the per-run coverage dict with three separate denominators (text/figure/table)
    plus structural counts. figure_ids/table_ids are the paper's full sets (from assets.json);
    when empty, that dimension's coverage_pct is null."""
    figure_ids = set(figure_ids or ())
    table_ids = set(table_ids or ())
    cited_figs, cited_tabs = cited_figures_tables(merged_spans)
    fig_hit = cited_figs & figure_ids
    tab_hit = cited_tabs & table_ids
    distinct_sentences = len({s.get("source_span") for s in merged_spans
                              if s.get("source_span")})
    return {
        "text": {
            "coverage_pct": _pct(char_covered, char_total),
            "chars_covered": char_covered,
            "chars_total": char_total,
            "extractable": char_total > 0,
        },
        "figures": {
            "coverage_pct": _pct(len(fig_hit), len(figure_ids)),
            "covered": len(fig_hit),
            "total": len(figure_ids),
            "covered_ids": sorted(fig_hit),
            "missing_ids": sorted(figure_ids - cited_figs),
        },
        "tables": {
            "coverage_pct": _pct(len(tab_hit), len(table_ids)),
            "covered": len(tab_hit),
            "total": len(table_ids),
            "covered_ids": sorted(tab_hit),
            "missing_ids": sorted(table_ids - cited_tabs),
        },
        "structural": {
            "total_spans": len(merged_spans),
            "by_category": category_counts(merged_spans),
            "distinct_source_sentences": distinct_sentences,
            "n_pages": n_pages,
            "spans_per_page": round(len(merged_spans) / n_pages, 2) if n_pages else None,
        },
    }


def coverage_line(cov):
    """One-line human-readable summary of the three coverage dimensions."""
    t, f, tb, s = cov["text"], cov["figures"], cov["tables"], cov["structural"]

    def p(x):
        return f"{x}%" if x is not None else "n/a"

    return (
        f"text={p(t['coverage_pct'])} ({t['chars_covered']}/{t['chars_total']} chars)  "
        f"figures={p(f['coverage_pct'])} ({f['covered']}/{f['total']})  "
        f"tables={p(tb['coverage_pct'])} ({tb['covered']}/{tb['total']})  "
        f"spans={s['total_spans']} sentences={s['distinct_source_sentences']}"
    )


FACTOR_SLOTS = ["assumption", "mechanism", "context", "intervention", "eval_metric", "pattern"]


def factor_coverage_report(spans, factors):
    """Assemble a Layer-2 (factor merge) coverage dict: for each of the 6 slots, (1) what
    fraction of factors have that slot filled, and (2) what fraction of that category's
    Layer-1 nodes are referenced by at least one factor (the node-level "orphan rate"). Also
    flags any factor whose slot value points to a node of the wrong category (a merge bug,
    not a coverage gap)."""
    cat_total = category_counts(spans)
    referenced_by_slot = {slot: set() for slot in FACTOR_SLOTS}
    mismatches = []

    for i, f in enumerate(factors):
        for slot in FACTOR_SLOTS:
            v = f.get(slot)
            if not v:
                continue
            referenced_by_slot[slot].add(v)
            actual_prefix = "".join(ch for ch in v if ch.isalpha())[:1]
            expected_prefix = CATEGORY_PREFIX.get(slot)
            if actual_prefix != expected_prefix:
                mismatches.append({"factor_index": i, "slot": slot, "node_id": v})

    n_factors = len(factors)
    slot_fill = {
        slot: {"filled": sum(1 for f in factors if f.get(slot)), "total": n_factors}
        for slot in FACTOR_SLOTS
    }
    node_coverage = {
        slot: {
            "covered": len(referenced_by_slot[slot]),
            "total": cat_total.get(slot, 0),
            "coverage_pct": _pct(len(referenced_by_slot[slot]), cat_total.get(slot, 0)),
        }
        for slot in FACTOR_SLOTS
    }
    total_referenced = set().union(*referenced_by_slot.values()) if referenced_by_slot else set()
    total_nodes = sum(cat_total.get(slot, 0) for slot in FACTOR_SLOTS)

    return {
        "factor_count": n_factors,
        "slot_fill": slot_fill,
        "node_coverage": node_coverage,
        "node_coverage_total": {
            "covered": len(total_referenced),
            "total": total_nodes,
            "coverage_pct": _pct(len(total_referenced), total_nodes),
        },
        "category_mismatches": mismatches,
    }


def factor_coverage_line(cov):
    """One-line human-readable summary of factor slot-fill and node-coverage."""
    fill = ",".join(
        f"{slot}={cov['slot_fill'][slot]['filled']}/{cov['slot_fill'][slot]['total']}"
        for slot in FACTOR_SLOTS
    )
    nodecov = ",".join(
        f"{slot}={cov['node_coverage'][slot]['covered']}/{cov['node_coverage'][slot]['total']}"
        for slot in FACTOR_SLOTS
    )
    t = cov["node_coverage_total"]
    return (
        f"factors={cov['factor_count']}  slot_fill({fill})  "
        f"node_coverage({nodecov},total={t['covered']}/{t['total']})  "
        f"mismatches={len(cov['category_mismatches'])}"
    )
