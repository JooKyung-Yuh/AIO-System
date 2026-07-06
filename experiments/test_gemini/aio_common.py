"""Shared helpers for the AIO Layer-1 extraction pipeline (sync + batch)."""
import json
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def load_prompt(prompt_path, **subs):
    """Read a prompt template and replace {key} placeholders with the given values."""
    text = Path(prompt_path).read_text(encoding="utf-8")
    for key, value in subs.items():
        text = text.replace("{" + key + "}", value)
    return text


def page_chunks(pdf_bytes, pages_per_chunk):
    """Split a PDF into page-range sub-PDFs. Returns a list of dicts with a fresh
    sub-PDF's bytes plus its 1-indexed page range, in reading order."""
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
            "bytes": buf.getvalue(),
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
