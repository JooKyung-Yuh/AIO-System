from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
import datetime
import hashlib
import json
import os
import sys
import traceback
from pathlib import Path

from aio_common import factor_coverage_report, factor_coverage_line

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

PROMPT_VERSION = "factor_merge_v4"
PROMPT_PATH = Path("./prompts") / f"{PROMPT_VERSION}.md"


def load_prompt(prompt_path: Path, paper_id: str, paper_title_hint: str, layer1_extraction: str) -> str:
    template = prompt_path.read_text(encoding="utf-8")
    return (
        template
        .replace("{paper_id}", paper_id)
        .replace("{paper_title_hint}", paper_title_hint)
        .replace("{layer1_extraction}", layer1_extraction)
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Merge a Layer-1 AIO span extraction into flat factor-level JSON records.")
    parser.add_argument("--run-dir", type=str, required=True, help="runs/<run_id> directory that already contains spans.json + notes.md from extract_aio.py")
    parser.add_argument("--paper-id", type=str, default="PXX")
    parser.add_argument("--paper-title-hint", type=str, default="unknown")
    return parser.parse_args()


def main():
    args = parse_args()
    run_dir = Path(args.run_dir)
    spans_text = (run_dir / "spans.json").read_text(encoding="utf-8")
    notes_text = (run_dir / "notes.md").read_text(encoding="utf-8")
    layer1_extraction = f"### Spans (JSON)\n{spans_text}\n\n### Classification notes\n{notes_text}"

    # Append-only: each build gets its own subfolder tagged by time + prompt version,
    # so re-running never overwrites a previous factors.json.
    now = datetime.datetime.now().astimezone()
    build_id = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{PROMPT_VERSION}"
    build_dir = run_dir / "factors" / build_id
    build_dir.mkdir(parents=True, exist_ok=False)

    prompt = load_prompt(PROMPT_PATH, args.paper_id, args.paper_title_hint, layer1_extraction)
    (build_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    metadata = {
        "build_id": build_id,
        "source_run_dir": str(run_dir),
        "timestamp": now.isoformat(),
        "paper_id": args.paper_id,
        "paper_title_hint": args.paper_title_hint,
        "model": MODEL_NAME,
        "temperature": 0.0,
        "prompt_version": PROMPT_VERSION,
        "prompt_path": str(PROMPT_PATH),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "prompt_chars": len(prompt),
    }

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=65536,
            ),
        )
        output_text = response.text
        finish_reason = response.candidates[0].finish_reason if response.candidates else None
        if str(finish_reason) != "FinishReason.STOP":
            print(f"[WARN] response did not finish normally (finish_reason={finish_reason}) — output may be truncated", file=sys.stderr)

        (build_dir / "raw_response.md").write_text(output_text, encoding="utf-8")

        stripped = output_text.strip()
        if stripped.startswith("```"):
            stripped = stripped.split("\n", 1)[1] if "\n" in stripped else ""
            stripped = stripped.rsplit("```", 1)[0].strip()

        factors = json.loads(stripped)

        (build_dir / "factors.json").write_text(
            json.dumps(factors, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        spans = json.loads(spans_text)
        coverage = factor_coverage_report(spans, factors)
        (build_dir / "coverage.json").write_text(
            json.dumps(coverage, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        cov_line = factor_coverage_line(coverage)
        with (Path("./runs") / "coverage.log").open("a", encoding="utf-8") as f:
            f.write(f"{now.isoformat()}\tbuild_factors\t{PROMPT_VERSION}\t{build_id}\t{cov_line}\n")
        if coverage["category_mismatches"]:
            print(f"  [WARN] {len(coverage['category_mismatches'])} category mismatch(es): "
                  f"{coverage['category_mismatches']}", file=sys.stderr)
        if coverage["factor_count"] == 0:
            print("  [ERROR] model returned 0 factors -- likely an empty/flaky response, not a "
                  "genuine empty paper. Consider re-running.", file=sys.stderr)

        usage = response.usage_metadata
        usage_dict = {
            "prompt_token_count": getattr(usage, "prompt_token_count", None),
            "thoughts_token_count": getattr(usage, "thoughts_token_count", None),
            "candidates_token_count": getattr(usage, "candidates_token_count", None),
            "total_token_count": getattr(usage, "total_token_count", None),
        } if usage else None

        metadata["status"] = "success"
        metadata["finish_reason"] = str(finish_reason)
        metadata["factor_count"] = len(factors)
        metadata["usage"] = usage_dict
        metadata["coverage"] = coverage

        if usage_dict:
            token_line = (
                f"prompt={usage_dict['prompt_token_count']} "
                f"thoughts={usage_dict['thoughts_token_count']} "
                f"output={usage_dict['candidates_token_count']} "
                f"total={usage_dict['total_token_count']}"
            )
            # per-build human-readable file
            (build_dir / "usage.txt").write_text(
                f"build_id: {build_id}\n"
                f"source_run_dir: {run_dir}\n"
                f"timestamp: {now.isoformat()}\n"
                f"model: {MODEL_NAME}\n"
                f"prompt_version: {PROMPT_VERSION}\n"
                f"finish_reason: {finish_reason}\n"
                f"tokens: {token_line}\n",
                encoding="utf-8",
            )
            # append-only cumulative log across all runs
            with (Path("./runs") / "token_usage.log").open("a", encoding="utf-8") as f:
                f.write(
                    f"{now.isoformat()}\tbuild_factors\t{PROMPT_VERSION}\t{build_id}\t"
                    f"{token_line}\tfinish={finish_reason}\n"
                )

        print(json.dumps(factors, indent=2, ensure_ascii=False))
        print(f"\nSaved factors to: {build_dir / 'factors.json'}", file=sys.stderr)
        print(f"Coverage: {cov_line}", file=sys.stderr)
        if usage_dict:
            print(f"Tokens: {token_line}", file=sys.stderr)

    except Exception as e:
        metadata["status"] = "error"
        metadata["error_type"] = type(e).__name__
        metadata["error_message"] = str(e)

        (build_dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        print(traceback.format_exc(), file=sys.stderr)
        raise

    finally:
        (build_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
