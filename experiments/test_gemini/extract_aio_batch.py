"""AIO Layer-1 extraction via the Gemini Batch API (page-chunked).

For LATER, large-scale use: submit one batch job containing one request per page-chunk,
poll until it finishes (async, ~50% cheaper), then merge the results into a single
spans.json — identical in shape to the synchronous extract_aio.py output.

Because page-chunking has no dependency chain (all chunks are known upfront from the page
count), the entire paper goes into ONE batch job. For the fast iterate-and-rerun loop, use
extract_aio.py instead; use this when processing many papers where latency does not matter.

Usage:
    python extract_aio_batch.py                     # uses the defaults below
    python extract_aio_batch.py --pdf docs/VARC.pdf --paper-id P_VARC --pages-per-chunk 4
    python extract_aio_batch.py --resume batches/<job_name>.txt   # reconnect to a running job
"""
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
import datetime
import hashlib
import json
import os
import sys
import time
from pathlib import Path

from aio_common import (
    load_prompt,
    page_chunks,
    parse_json_array,
    usage_of,
    add_usage,
    token_line,
    merge_spans,
)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# Chunk-scoped extraction prompt (page excerpt). Left as a constant so it stays in sync
# with extract_aio.py; the prompt file itself is managed separately.
PROMPT_VERSION = "aiocm_debug_v5"
PROMPT_PATH = Path("./prompts") / f"{PROMPT_VERSION}.md"

POLL_INTERVAL_SECONDS = 30
TERMINAL_STATES = {
    "JOB_STATE_SUCCEEDED",
    "JOB_STATE_FAILED",
    "JOB_STATE_CANCELLED",
    "JOB_STATE_EXPIRED",
    "JOB_STATE_PARTIALLY_SUCCEEDED",
}


def parse_args():
    p = argparse.ArgumentParser(description="AIO Layer-1 extraction via the Gemini Batch API (page-chunked).")
    p.add_argument("--pdf", type=str, default="./docs/VARC.pdf")
    p.add_argument("--paper-id", type=str, default="PXX")
    p.add_argument("--paper-title-hint", type=str, default="unknown")
    p.add_argument("--pages-per-chunk", type=int, default=4)
    p.add_argument("--poll-interval", type=int, default=POLL_INTERVAL_SECONDS)
    p.add_argument("--resume", type=str, default=None,
                   help="path to a saved batch-job pointer (batches/<job>.txt) to reconnect instead of submitting a new job")
    return p.parse_args()


def build_requests(chunks, paper_id, paper_title_hint):
    """One InlinedRequest per page-chunk: the chunk's sub-PDF + the extraction prompt."""
    requests = []
    for c in chunks:
        prompt = load_prompt(
            PROMPT_PATH,
            paper_id=paper_id,
            paper_title_hint=paper_title_hint,
            page_range=c["page_range"],
        )
        requests.append(types.InlinedRequest(
            model=MODEL_NAME,
            contents=[
                types.Part.from_bytes(data=c["bytes"], mime_type="application/pdf"),
                types.Part(text=prompt),
            ],
            config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=65536),
            metadata={"chunk_index": str(c["chunk_index"]), "page_range": c["page_range"]},
        ))
    return requests


def poll_until_done(job_name, poll_interval):
    job = client.batches.get(name=job_name)
    while str(job.state) not in TERMINAL_STATES:
        print(f"  batch state: {job.state} — waiting {poll_interval}s...", file=sys.stderr)
        time.sleep(poll_interval)
        job = client.batches.get(name=job_name)
    print(f"  batch state: {job.state} (terminal)", file=sys.stderr)
    return job


def main():
    args = parse_args()
    pdf_path = Path(args.pdf)
    pdf_bytes = pdf_path.read_bytes()
    pdf_sha256 = hashlib.sha256(pdf_bytes).hexdigest()

    chunks = page_chunks(pdf_bytes, args.pages_per_chunk)

    now = datetime.datetime.now().astimezone()
    run_id = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{args.paper_id}_{MODEL_NAME.replace('.', '-')}_batch"
    run_dir = Path("./runs") / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    chunks_dir = run_dir / "chunks"
    chunks_dir.mkdir()
    batches_dir = Path("./batches")
    batches_dir.mkdir(exist_ok=True)

    metadata = {
        "run_id": run_id,
        "mode": "batch",
        "timestamp": now.isoformat(),
        "paper_id": args.paper_id,
        "paper_title_hint": args.paper_title_hint,
        "pdf_path": str(pdf_path),
        "pdf_sha256": pdf_sha256,
        "pdf_size_bytes": len(pdf_bytes),
        "model": MODEL_NAME,
        "temperature": 0.0,
        "prompt_version": PROMPT_VERSION,
        "prompt_path": str(PROMPT_PATH),
        "pages_per_chunk": args.pages_per_chunk,
        "n_chunks": len(chunks),
    }

    # --- submit (or resume) the batch job ---
    if args.resume:
        job_name = Path(args.resume).read_text(encoding="utf-8").strip()
        print(f"Resuming batch job: {job_name}", file=sys.stderr)
    else:
        requests = build_requests(chunks, args.paper_id, args.paper_title_hint)
        job = client.batches.create(
            model=MODEL_NAME,
            src=requests,
            config=types.CreateBatchJobConfig(display_name=f"aio_{run_id}"),
        )
        job_name = job.name
        (batches_dir / f"{run_id}.txt").write_text(job_name, encoding="utf-8")
        print(f"Submitted batch job: {job_name} ({len(requests)} chunk requests)", file=sys.stderr)

    metadata["batch_job_name"] = job_name

    # --- poll to completion ---
    job = poll_until_done(job_name, args.poll_interval)
    metadata["batch_state"] = str(job.state)

    if str(job.state) not in ("JOB_STATE_SUCCEEDED", "JOB_STATE_PARTIALLY_SUCCEEDED"):
        metadata["status"] = "error"
        metadata["error_message"] = f"batch ended in state {job.state}: {getattr(job, 'error', None)}"
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        raise RuntimeError(metadata["error_message"])

    # --- collect results (order matches the submitted src order) ---
    responses = job.dest.inlined_responses or []
    chunk_results = []
    total_usage = None
    any_salvaged = False
    for c, r in zip(chunks, responses):
        idx = c["chunk_index"]
        if getattr(r, "error", None):
            print(f"[WARN] chunk {idx} (pages {c['page_range']}) errored: {r.error}", file=sys.stderr)
            chunk_results.append({"chunk_index": idx, "page_range": c["page_range"], "spans": []})
            continue
        resp = r.response
        text = resp.text or ""
        (chunks_dir / f"chunk_{idx:02d}_p{c['page_range']}.md").write_text(text, encoding="utf-8")
        total_usage = add_usage(total_usage, usage_of(resp))
        try:
            spans, salvaged = parse_json_array(text)
            any_salvaged = any_salvaged or salvaged
            if salvaged:
                print(f"[WARN] chunk {idx} salvaged from truncation ({len(spans)} spans)", file=sys.stderr)
        except json.JSONDecodeError as e:
            print(f"[WARN] chunk {idx} JSON parse failed: {e}", file=sys.stderr)
            spans = []
        chunk_results.append({"chunk_index": idx, "page_range": c["page_range"], "spans": spans})

    merged = merge_spans(chunk_results)
    (run_dir / "spans.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    # notes.md is produced in a later reflection pass; leave a placeholder so build_factors can read it
    (run_dir / "notes.md").write_text("(batch mode: classification-notes reflection pass not run)\n", encoding="utf-8")

    metadata["status"] = "success"
    metadata["span_count"] = len(merged)
    metadata["spans_per_chunk"] = [len(cr["spans"]) for cr in chunk_results]
    metadata["any_salvaged"] = any_salvaged
    metadata["usage"] = total_usage
    (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    tl = token_line(total_usage)
    (run_dir / "usage.txt").write_text(
        f"run_id: {run_id}\nmode: batch\nbatch_job_name: {job_name}\n"
        f"timestamp: {now.isoformat()}\nmodel: {MODEL_NAME}\n"
        f"prompt_version: {PROMPT_VERSION}\nn_chunks: {len(chunks)}\n"
        f"tokens (summed over chunks): {tl}\n",
        encoding="utf-8",
    )
    with (Path("./runs") / "token_usage.log").open("a", encoding="utf-8") as f:
        f.write(f"{now.isoformat()}\textract_aio_batch\t{PROMPT_VERSION}\t{run_id}\t{tl}\tstate={job.state}\n")

    print(f"\nSaved {len(merged)} spans to: {run_dir / 'spans.json'}", file=sys.stderr)
    print(f"Tokens (summed over {len(chunks)} chunks): {tl}", file=sys.stderr)


if __name__ == "__main__":
    main()
