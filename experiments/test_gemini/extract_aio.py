"""AIO Layer-1 extraction (synchronous, page-chunked).

Splits the PDF into page-range chunks and extracts atomic AIO spans from each chunk in a
simple loop, then merges them into one spans.json. Chunking keeps each call's output well
under the token cap, so a long paper no longer truncates. For large-scale runs use the
cheaper async extract_aio_batch.py; use this for the fast iterate-and-rerun loop.
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

from aio_common import (
    load_prompt,
    page_chunks,
    parse_json_array,
    usage_of,
    add_usage,
    token_line,
    merge_spans,
    quote_char_coverage,
    load_asset_ids,
    coverage_report,
    coverage_line,
)

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

paper_id = "PXX"
paper_title_hint = "unknown"
pdf_path = Path("./docs/VARC.pdf")
pages_per_chunk = 4

pdf_bytes = pdf_path.read_bytes()
pdf_sha256 = hashlib.sha256(pdf_bytes).hexdigest()

PROMPT_VERSION = "aiocm_debug_v7"
PROMPT_PATH = Path("./prompts") / f"{PROMPT_VERSION}.md"

# Coverage denominators, both produced once per paper by extract_text.py:
#   <pdf>.txt          — prose transcription (text-coverage denominator)
#   <pdf>.assets.json  — enumerated figures/tables (figure- and table-coverage denominators)
# Absent -> that coverage dimension is null; extraction still runs.
SOURCE_TEXT_PATH = pdf_path.with_suffix(".txt")
SOURCE_ASSETS_PATH = pdf_path.with_suffix(".assets.json")


def extract_chunk(chunk):
    """Call the model on one page-chunk sub-PDF. Returns (spans, raw_text, usage, finish_reason)."""
    prompt = load_prompt(
        PROMPT_PATH,
        paper_id=paper_id,
        paper_title_hint=paper_title_hint,
        page_range=chunk["page_range"],
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Part.from_bytes(data=chunk["bytes"], mime_type="application/pdf"),
            prompt,
        ],
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=65536),
    )
    text = response.text or ""
    finish_reason = response.candidates[0].finish_reason if response.candidates else None
    usage = usage_of(response)

    spans = []
    salvaged = False
    parse_error = None
    try:
        spans, salvaged = parse_json_array(text)
    except json.JSONDecodeError as e:
        parse_error = str(e)
    return spans, text, usage, str(finish_reason), salvaged, parse_error


chunks = page_chunks(pdf_bytes, pages_per_chunk)

now = datetime.datetime.now().astimezone()
run_id = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{paper_id}_{MODEL_NAME.replace('.', '-')}"
run_dir = Path("./runs") / run_id
run_dir.mkdir(parents=True, exist_ok=False)
chunks_dir = run_dir / "chunks"
chunks_dir.mkdir()

metadata = {
    "run_id": run_id,
    "mode": "sync",
    "timestamp": now.isoformat(),
    "paper_id": paper_id,
    "paper_title_hint": paper_title_hint,
    "pdf_path": str(pdf_path),
    "pdf_sha256": pdf_sha256,
    "pdf_size_bytes": len(pdf_bytes),
    "model": MODEL_NAME,
    "temperature": 0.0,
    "prompt_version": PROMPT_VERSION,
    "prompt_path": str(PROMPT_PATH),
    "pages_per_chunk": pages_per_chunk,
    "n_chunks": len(chunks),
}

try:
    chunk_results = []
    per_chunk_meta = []
    total_usage = None
    any_salvaged = False

    for c in chunks:
        idx = c["chunk_index"]
        print(f"[chunk {idx}/{len(chunks)}] pages {c['page_range']} ...", file=sys.stderr)
        spans, raw_text, usage, finish_reason, salvaged, parse_error = extract_chunk(c)

        (chunks_dir / f"chunk_{idx:02d}_p{c['page_range']}.md").write_text(raw_text, encoding="utf-8")
        total_usage = add_usage(total_usage, usage)
        any_salvaged = any_salvaged or salvaged

        if finish_reason != "FinishReason.STOP":
            print(f"  [WARN] chunk {idx} finish_reason={finish_reason} (may be truncated)", file=sys.stderr)
        if salvaged:
            print(f"  [WARN] chunk {idx} salvaged from truncation ({len(spans)} spans)", file=sys.stderr)
        if parse_error:
            print(f"  [WARN] chunk {idx} JSON parse failed: {parse_error}", file=sys.stderr)

        chunk_results.append({"chunk_index": idx, "page_range": c["page_range"], "spans": spans})
        per_chunk_meta.append({
            "chunk_index": idx,
            "page_range": c["page_range"],
            "span_count": len(spans),
            "finish_reason": finish_reason,
            "salvaged": salvaged,
            "parse_error": parse_error,
            "usage": usage,
        })

    merged = merge_spans(chunk_results)
    n_pages = chunks[-1]["page_end"] if chunks else 0

    # Coverage denominators come from extract_text.py's cached artifacts (no local PDF parsing):
    #   text  -> <pdf>.txt (prose)      figures/tables -> <pdf>.assets.json (enumerated ids)
    source_text = SOURCE_TEXT_PATH.read_text(encoding="utf-8") if SOURCE_TEXT_PATH.exists() else ""
    cov_covered, cov_total = quote_char_coverage(source_text, merged)
    figure_ids, table_ids = load_asset_ids(SOURCE_ASSETS_PATH)
    coverage = coverage_report(merged, n_pages, cov_covered, cov_total, figure_ids, table_ids)
    (run_dir / "spans.json").write_text(
        json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    # notes.md (PART 2 reflection) is a separate later pass; placeholder keeps build_factors happy
    (run_dir / "notes.md").write_text(
        "(sync chunked mode: classification-notes reflection pass not run)\n", encoding="utf-8"
    )

    metadata["status"] = "success"
    metadata["span_count"] = len(merged)
    metadata["any_salvaged"] = any_salvaged
    metadata["chunks"] = per_chunk_meta
    metadata["usage"] = total_usage
    metadata["coverage"] = coverage

    cl = coverage_line(coverage)
    (run_dir / "coverage.json").write_text(
        json.dumps(coverage, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with (Path("./runs") / "coverage.log").open("a", encoding="utf-8") as f:
        f.write(f"{now.isoformat()}\textract_aio\t{PROMPT_VERSION}\t{run_id}\t{cl}\n")

    tl = token_line(total_usage)
    (run_dir / "usage.txt").write_text(
        f"run_id: {run_id}\nmode: sync\ntimestamp: {now.isoformat()}\n"
        f"model: {MODEL_NAME}\nprompt_version: {PROMPT_VERSION}\n"
        f"n_chunks: {len(chunks)}\nspan_count: {len(merged)}\n"
        f"tokens (summed over chunks): {tl}\n",
        encoding="utf-8",
    )
    with (Path("./runs") / "token_usage.log").open("a", encoding="utf-8") as f:
        f.write(f"{now.isoformat()}\textract_aio\t{PROMPT_VERSION}\t{run_id}\t{tl}\tchunks={len(chunks)}\n")

    print(f"\nSaved {len(merged)} spans to: {run_dir / 'spans.json'}", file=sys.stderr)
    print(f"Coverage: {cl}", file=sys.stderr)
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
