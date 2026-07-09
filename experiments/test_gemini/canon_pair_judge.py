"""canon_pair_judge.py — fill merge_decisions.json for the intervention pairs canonicalize_v0
could not resolve by rule (merge_queue.json).

The LLM decides SAME/DIFFERENT (judgment ONLY). All union / representative / id generation stays
in canonicalize_v0 (deterministic union-find). Every decision is cached, so a pair already in
merge_decisions.json is NEVER re-asked -> reruns are identical. Scope = the intervention/reference
pairs canonicalize_v0 queued (overlap >= CAND_OVERLAP, non-exact); context/eval/am are untouched.

Flow (wired by run_cohort.py): canonicalize (pass 1, emits merge_queue) -> THIS -> canonicalize
(pass 2, consumes cache). Standalone:
    python canon_pair_judge.py --canonical-dir <cohort>/canonical
"""
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
import json
import os
import sys
from pathlib import Path

from aio_common import load_prompt

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"
JUDGE_PROMPT = Path("./prompts/canon_pair_judge_v1.md")


def judge_pair(a_text, b_text):
    """Return 'yes' (same intervention) or 'no' (different). temp=0, tiny output. Conservative:
    anything not clearly starting 'y' -> 'no' (never over-merge; raw nodes are always kept)."""
    prompt = load_prompt(JUDGE_PROMPT, a=a_text or "", b=b_text or "")
    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=8),
    )
    return "yes" if (resp.text or "").strip().lower().startswith("y") else "no"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical-dir", required=True,
                    help="<cohort>/canonical holding merge_queue.json + merge_decisions.json")
    args = ap.parse_args()
    d = Path(args.canonical_dir)
    queue = json.loads((d / "merge_queue.json").read_text(encoding="utf-8"))
    cache_path = d / "merge_decisions.json"
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}

    new = 0
    for item in queue:
        key = "|".join(sorted(item["pair"]))
        if key in cache:                      # already judged -> never re-ask (determinism)
            continue
        cache[key] = judge_pair(item.get("a", ""), item.get("b", ""))
        new += 1
        print(f"  {key}: {cache[key]}", file=sys.stderr)

    cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")
    yes = sum(1 for v in cache.values() if v == "yes")
    print(f"judged {new} new pair(s); cache now {len(cache)} ({yes} merge / {len(cache) - yes} keep)")


if __name__ == "__main__":
    main()
