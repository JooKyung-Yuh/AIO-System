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
import datetime
from pathlib import Path
import hashlib
import json
import traceback

from aio_common import page_chunks, usage_of, add_usage, token_line

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


def transcribe_chunk(chunk):
    """Transcribe one page-chunk sub-PDF. Returns (figures, tables, prose, usage, finish)."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Part.from_bytes(data=chunk["bytes"], mime_type="application/pdf"),
            TRANSCRIBE_PROMPT,
        ],
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=65536),
    )
    text = response.text or ""
    finish_reason = response.candidates[0].finish_reason if response.candidates else None
    figures, tables, prose = split_assets_and_prose(text)
    return figures, tables, prose, usage_of(response), str(finish_reason)


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

    for c in chunks:
        idx = c["chunk_index"]
        print(f"[chunk {idx}/{len(chunks)}] pages {c['page_range']} ...", file=sys.stderr)
        figures, tables, prose, usage, finish_reason = transcribe_chunk(c)
        total_usage = add_usage(total_usage, usage)

        if finish_reason != "FinishReason.STOP":
            any_truncated = True
            print(f"  [WARN] chunk {idx} finish_reason={finish_reason} (may be truncated)", file=sys.stderr)

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
            "usage": usage,
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
