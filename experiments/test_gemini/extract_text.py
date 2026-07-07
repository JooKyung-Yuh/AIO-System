"""Transcribe a paper PDF with Gemini, producing the coverage denominators.

extract_aio.py measures coverage on three denominators (text / figures / tables). Scanned or
image-heavy PDFs have no usable local text layer (pypdf is empty and slow), and — more
importantly for a figure-driven paper — a plain text dump throws away the information that
lives in the figures. So we ask Gemini to do two things per page-chunk:

  1. enumerate EVERY figure and table and DESCRIBE its actual visual/tabular content densely
     (not just the caption) -> cached as <pdf>.assets.json  (figure/table denominators + a
     record of what each visual carries),
  2. transcribe the prose verbatim                          -> cached as <pdf>.txt (text
     denominator).

Run this ONCE per paper; extract_aio.py reads both caches on every (re)run for free, so
iterating the extraction prompt never re-pays the transcription cost.
"""
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import sys
import time
import datetime
from pathlib import Path
import hashlib
import json
import traceback

from aio_common import page_chunks, pdf_page_slice, usage_of, add_usage, token_line

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

paper_id = "PXX"
pdf_path = Path("./docs/VARC.pdf")
pages_per_chunk = 4
out_text_path = pdf_path.with_suffix(".txt")            # extract_aio SOURCE_TEXT_PATH
out_assets_path = pdf_path.with_suffix(".assets.json")  # extract_aio SOURCE_ASSETS_PATH

pdf_bytes = pdf_path.read_bytes()
pdf_sha256 = hashlib.sha256(pdf_bytes).hexdigest()

TRANSCRIBE_PROMPT = (
    "You are transcribing one page range of a scientific paper.\n\n"
    "STEP 1 — Figures & tables. Output a SINGLE fenced ```json block of this exact shape, "
    "enumerating every FIGURE and TABLE that appears on these pages. Describe each one's actual "
    "content densely — for a figure, what it visually shows (the examples, grids, curves, the "
    "trend or qualitative behaviour), NOT merely its caption; for a table, the comparison it "
    "reports and which way the numbers move:\n"
    "```json\n"
    "{\"figures\": [{\"id\": \"Figure 1\", \"description\": \"...\"}], "
    "\"tables\": [{\"id\": \"Table 1\", \"description\": \"...\"}]}\n"
    "```\n"
    "Use the figure/table's printed id verbatim. If there are none on these pages, use empty "
    "arrays.\n\n"
    "STEP 2 — Prose. After the closing fence, transcribe ALL running text of these pages "
    "verbatim in reading order (title, abstract, body, captions, footnotes, appendix). Do not "
    "summarize, translate, or add commentary. Do not wrap the prose in code fences."
)


def split_assets_and_prose(text):
    """Split a chunk response into (figures, tables, prose). Robust to a missing json block."""
    t = (text or "").strip()
    figures, tables = [], []
    if "```json" in t:
        _, rest = t.split("```json", 1)
        block, after = (rest.split("```", 1) if "```" in rest else (rest, ""))
        try:
            data = json.loads(block.strip())
            figures = data.get("figures") or []
            tables = data.get("tables") or []
        except json.JSONDecodeError:
            pass
        prose = after.strip()
    else:
        prose = t  # model skipped the json block; treat the whole thing as prose
    return figures, tables, prose


MAX_EMPTY_RETRIES = 3
EMPTY_RETRY_BACKOFF_SECONDS = 5  # base delay; doubles each retry (transient API flake, not content-driven)
MAX_SPLIT_DEPTH = 3  # 4 pages -> 2 pages -> 1 page floor


def _transcribe_bytes_once(pdf_slice_bytes):
    """Transcribe one page-range sub-PDF. Returns (figures, tables, prose, usage, finish)."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Part.from_bytes(data=pdf_slice_bytes, mime_type="application/pdf"),
            TRANSCRIBE_PROMPT,
        ],
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=65536),
    )
    text = response.text or ""
    finish_reason = response.candidates[0].finish_reason if response.candidates else None
    figures, tables, prose = split_assets_and_prose(text)
    return figures, tables, prose, usage_of(response), str(finish_reason)


def _attempt_range(pdf_slice_bytes, label):
    """Retry-with-backoff loop for one page-range slice. Returns (figures, tables, prose,
    usage, finish_reason, attempts, is_empty)."""
    total_usage = None
    figures, tables, prose, finish_reason = [], [], "", None
    for attempt in range(1, MAX_EMPTY_RETRIES + 2):
        figures, tables, prose, usage, finish_reason = _transcribe_bytes_once(pdf_slice_bytes)
        total_usage = add_usage(total_usage, usage)
        is_empty = not prose.strip() and not figures and not tables
        if not is_empty:
            return figures, tables, prose, total_usage, finish_reason, attempt, False
        print(
            f"  [WARN] {label} returned EMPTY (prose/figures/tables all blank, "
            f"finish_reason={finish_reason}) on attempt {attempt}/{MAX_EMPTY_RETRIES + 1}",
            file=sys.stderr,
        )
        if attempt <= MAX_EMPTY_RETRIES:
            delay = EMPTY_RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
            print(f"  retrying {label} in {delay}s ...", file=sys.stderr)
            time.sleep(delay)
    return figures, tables, prose, total_usage, finish_reason, attempt, True


def transcribe_range(pdf_bytes, page_start, page_end, depth=0):
    """Transcribe a page range. If it keeps coming back empty after retries and still spans
    more than one page (and we haven't hit MAX_SPLIT_DEPTH), split it in half and transcribe
    each half independently, merging results. This targets image-dense page ranges that seem
    to trigger occasional empty completions, without paying per-page overhead everywhere else.
    Returns a dict: figures, tables, prose, usage, finish_reason, attempts, empty, page_ranges,
    split (bool, whether this range required splitting)."""
    label = f"pages {page_start}-{page_end}"
    sub_bytes = pdf_page_slice(pdf_bytes, page_start, page_end)
    figures, tables, prose, usage, finish_reason, attempts, is_empty = _attempt_range(sub_bytes, label)

    if not is_empty or page_start == page_end or depth >= MAX_SPLIT_DEPTH:
        if is_empty:
            print(
                f"  [ERROR] {label} is STILL EMPTY after {attempts} attempt(s) and cannot be "
                f"split further -- this page is missing from the caches.",
                file=sys.stderr,
            )
        return {
            "figures": figures, "tables": tables, "prose": prose, "usage": usage,
            "finish_reason": finish_reason, "attempts": attempts, "empty": is_empty,
            "page_ranges": [label], "split": False,
        }

    mid = (page_start + page_end) // 2
    print(
        f"  [SPLIT] {label} still empty after {attempts} attempt(s) -- splitting into "
        f"{page_start}-{mid} and {mid + 1}-{page_end}",
        file=sys.stderr,
    )
    left = transcribe_range(pdf_bytes, page_start, mid, depth + 1)
    right = transcribe_range(pdf_bytes, mid + 1, page_end, depth + 1)

    merged_figures = list(left["figures"])
    _merge_assets(merged_figures, right["figures"])
    merged_tables = list(left["tables"])
    _merge_assets(merged_tables, right["tables"])
    return {
        "figures": merged_figures,
        "tables": merged_tables,
        "prose": (left["prose"] + "\n\n" + right["prose"]).strip(),
        "usage": add_usage(left["usage"], right["usage"]),
        "finish_reason": right["finish_reason"],
        "attempts": left["attempts"] + right["attempts"],
        "empty": left["empty"] and right["empty"],
        "page_ranges": left["page_ranges"] + right["page_ranges"],
        "split": True,
    }


def _merge_assets(existing, new_items):
    """Append new figure/table entries, de-duplicating by (case-insensitive) id, keep first."""
    seen = {(a.get("id") or "").strip().lower() for a in existing if isinstance(a, dict)}
    for item in new_items:
        key = (item.get("id") or "").strip().lower() if isinstance(item, dict) else str(item).lower()
        if key and key not in seen:
            seen.add(key)
            existing.append(item)


chunks = page_chunks(pdf_bytes, pages_per_chunk)

now = datetime.datetime.now().astimezone()
run_id = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{paper_id}_transcribe_{MODEL_NAME.replace('.', '-')}"
run_dir = Path("./runs") / run_id
run_dir.mkdir(parents=True, exist_ok=False)

metadata = {
    "run_id": run_id,
    "task": "transcribe",
    "timestamp": now.isoformat(),
    "paper_id": paper_id,
    "pdf_path": str(pdf_path),
    "pdf_sha256": pdf_sha256,
    "pdf_size_bytes": len(pdf_bytes),
    "model": MODEL_NAME,
    "temperature": 0.0,
    "pages_per_chunk": pages_per_chunk,
    "n_chunks": len(chunks),
    "out_text_path": str(out_text_path),
    "out_assets_path": str(out_assets_path),
}

try:
    prose_parts = []
    all_figures = []
    all_tables = []
    per_chunk_meta = []
    total_usage = None
    any_truncated = False
    empty_chunks = []

    for c in chunks:
        idx = c["chunk_index"]
        print(f"[chunk {idx}/{len(chunks)}] pages {c['page_range']} ...", file=sys.stderr)
        result = transcribe_range(pdf_bytes, c["page_start"], c["page_end"])
        figures, tables, prose = result["figures"], result["tables"], result["prose"]
        finish_reason, attempts, is_empty = result["finish_reason"], result["attempts"], result["empty"]
        total_usage = add_usage(total_usage, result["usage"])

        if finish_reason != "FinishReason.STOP":
            any_truncated = True
            print(f"  [WARN] chunk {idx} finish_reason={finish_reason} (may be truncated)", file=sys.stderr)

        if is_empty:
            empty_chunks.append({"chunk_index": idx, "page_range": c["page_range"]})
            print(
                f"  [ERROR] chunk {idx} (pages {c['page_range']}) is STILL EMPTY after "
                f"{attempts} attempt(s) across {result['page_ranges']} -- this page range is "
                f"missing from {out_text_path} and {out_assets_path}.",
                file=sys.stderr,
            )
        elif result["split"]:
            print(f"  [OK] chunk {idx} recovered via split: {result['page_ranges']}", file=sys.stderr)

        _merge_assets(all_figures, figures)
        _merge_assets(all_tables, tables)
        prose_parts.append(f"\n\n===== pages {c['page_range']} =====\n\n{prose}")
        per_chunk_meta.append({
            "chunk_index": idx,
            "page_range": c["page_range"],
            "prose_chars": len(prose),
            "n_figures": len(figures),
            "n_tables": len(tables),
            "finish_reason": finish_reason,
            "attempts": attempts,
            "empty": is_empty,
            "split": result["split"],
            "sub_ranges": result["page_ranges"],
            "usage": result["usage"],
        })

    full_text = "".join(prose_parts).strip() + "\n"
    assets = {"figures": all_figures, "tables": all_tables}

    out_text_path.write_text(full_text, encoding="utf-8")
    out_assets_path.write_text(json.dumps(assets, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / "transcript.txt").write_text(full_text, encoding="utf-8")
    (run_dir / "assets.json").write_text(json.dumps(assets, indent=2, ensure_ascii=False), encoding="utf-8")

    metadata["status"] = "success"
    metadata["char_count"] = len(full_text)
    metadata["n_figures"] = len(all_figures)
    metadata["n_tables"] = len(all_tables)
    metadata["any_truncated"] = any_truncated
    metadata["any_empty_chunks"] = bool(empty_chunks)
    metadata["empty_chunks"] = empty_chunks
    metadata["chunks"] = per_chunk_meta
    metadata["usage"] = total_usage

    tl = token_line(total_usage)
    (run_dir / "usage.txt").write_text(
        f"run_id: {run_id}\ntask: transcribe\ntimestamp: {now.isoformat()}\n"
        f"model: {MODEL_NAME}\nn_chunks: {len(chunks)}\nchar_count: {len(full_text)}\n"
        f"figures: {len(all_figures)}\ntables: {len(all_tables)}\n"
        f"tokens (summed over chunks): {tl}\n",
        encoding="utf-8",
    )
    with (Path("./runs") / "token_usage.log").open("a", encoding="utf-8") as f:
        f.write(f"{now.isoformat()}\textract_text\ttranscribe\t{run_id}\t{tl}\tchunks={len(chunks)}\n")

    print(f"\nSaved transcript ({len(full_text)} chars) to: {out_text_path}", file=sys.stderr)
    print(f"Saved {len(all_figures)} figures + {len(all_tables)} tables to: {out_assets_path}", file=sys.stderr)
    print(f"Tokens (summed over {len(chunks)} chunks): {tl}", file=sys.stderr)
    if empty_chunks:
        ranges = ", ".join(f"pages {ec['page_range']}" for ec in empty_chunks)
        print(
            f"\n[ERROR] {len(empty_chunks)}/{len(chunks)} chunk(s) came back empty after "
            f"retries and are MISSING from the caches: {ranges}. Coverage numbers computed "
            f"against these caches will overstate figure/table/text coverage.",
            file=sys.stderr,
        )

except Exception as e:
    metadata["status"] = "error"
    metadata["error_type"] = type(e).__name__
    metadata["error_message"] = str(e)
    (run_dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
    print(traceback.format_exc(), file=sys.stderr)
    raise

finally:
    (run_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
