"""run_cohort.py — run one self-contained N-build ensemble cohort end to end.

One invocation = one cohort folder that holds everything for that experiment, so re-running
never overwrites a previous vote and separate ensembles never cross-pool:

  runs/<run>/factors/<cohort_id>/
    builds/
      <build_1>/ ... <build_N>/     # the N split builds (build_factors_split.py, --builds-dir)
    ensemble.json                    # k-of-N vote over THIS cohort's builds (aggregate_ensemble.py)
    canonical/                       # canonicalization over THIS cohort (canonicalize_v0.py)
    cohort_meta.json                 # n, prompt set, timestamps

Each step shells out to the existing per-stage scripts with --builds-dir pointed at the cohort's
builds/, so the stages stay independently runnable and testable. --dry-run prints the plan
without spending tokens.
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def prompt_set():
    """Read the current prompt versions straight from build_factors_split so the cohort id
    reflects exactly what will run. Parse the constants textually — importing the module would
    trigger its API-key check at import time."""
    text = (HERE / "build_factors_split.py").read_text(encoding="utf-8")
    vals = {}
    for key in ("CIO_PROMPT", "AM_PROMPT", "LINK_PROMPT"):
        for line in text.splitlines():
            if line.startswith(key):
                vals[key] = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    return vals


def run(cmd, dry, fatal=True):
    print("  $ " + " ".join(str(c) for c in cmd), flush=True)
    if dry:
        return 0
    r = subprocess.run(cmd)
    if r.returncode != 0 and fatal:
        sys.exit(f"step failed ({r.returncode}): {' '.join(str(c) for c in cmd)}")
    return r.returncode


def parse_args():
    p = argparse.ArgumentParser(description="Run one N-build ensemble cohort end to end.")
    p.add_argument("--run-dir", required=True, help="runs/<run_id> with spans.json + evidence_units.json")
    p.add_argument("--n", type=int, default=5, help="number of builds in the cohort")
    p.add_argument("--no-canonical", action="store_true", help="stop after the vote, skip canonicalization")
    p.add_argument("--ctx-min", type=int, default=3, help="passed to canonicalize_v0")
    p.add_argument("--parallel", type=int, default=1,
                   help="max builds to run at once (builds are independent). Start at 3; raise to N "
                        "once the rate limit is comfortable. Default 1 = sequential.")
    p.add_argument("--dry-run", action="store_true", help="print the plan without running anything")
    return p.parse_args()


def main():
    args = parse_args()
    run_dir = Path(args.run_dir)
    now = datetime.datetime.now().astimezone()
    ps = prompt_set()
    am_tag = ps.get("AM_PROMPT", "am").replace("extract_", "")
    cohort_id = f"cohort_{now.strftime('%Y-%m-%d_%H-%M-%S')}_{am_tag}_N{args.n}"
    cohort = run_dir / "factors" / cohort_id
    builds_dir = cohort / "builds"
    print(f"cohort: {cohort}")
    print(f"prompts: {ps}")

    if not args.dry_run:
        builds_dir.mkdir(parents=True, exist_ok=False)

    py = sys.executable
    # --- Stage: N builds into the cohort's builds/ (bounded parallel; each build is independent) ---
    def one_build(i):
        print(f"[build {i}/{args.n}] start", flush=True)
        rc = run([py, str(HERE / "build_factors_split.py"),
                  "--run-dir", str(run_dir), "--builds-dir", str(builds_dir),
                  "--build-index", str(i)], args.dry_run, fatal=False)
        print(f"[build {i}/{args.n}] done rc={rc}", flush=True)
        return i, rc

    if args.parallel > 1 and not args.dry_run:
        import concurrent.futures as cf
        with cf.ThreadPoolExecutor(max_workers=args.parallel) as ex:
            results = list(ex.map(one_build, range(1, args.n + 1)))
    else:
        results = [one_build(i) for i in range(1, args.n + 1)]

    if not args.dry_run:
        ok = [i for i, rc in results if rc == 0]
        if len(ok) < 2:
            sys.exit(f"only {len(ok)}/{args.n} builds succeeded; need >=2 to vote (raise --parallel headroom or check rate limits)")
        if len(ok) < args.n:
            print(f"[WARN] {args.n - len(ok)} build(s) failed; voting over {len(ok)} (aggregate ignores incomplete builds)", flush=True)

    # --- Stage: vote over exactly this cohort's builds ---
    print("[vote]")
    ensemble_path = cohort / "ensemble.json"
    run([py, str(HERE / "aggregate_ensemble.py"),
         "--run-dir", str(run_dir), "--builds-dir", str(builds_dir),
         "--auto", "--out", str(ensemble_path)], args.dry_run)

    # --- Stage: canonicalization over this cohort (pass1 emits merge_queue -> LLM judge fills the
    # decision cache -> pass2 consumes it and merges). The judge only decides yes/no; every merge
    # is still applied by the deterministic union-find, and the cache freezes reruns. ---
    if not args.no_canonical:
        canon_dir = cohort / "canonical"
        canon_cmd = [py, str(HERE / "canonicalize_v0.py"),
                     "--run-dir", str(run_dir), "--builds-dir", str(builds_dir),
                     "--ensemble", str(ensemble_path), "--out-dir", str(canon_dir),
                     "--ctx-min", str(args.ctx_min)]
        print("[canonicalize pass 1 — emit merge_queue]")
        run(canon_cmd, args.dry_run)
        print("[judge pending intervention pairs — LLM yes/no, cached]")
        run([py, str(HERE / "canon_pair_judge.py"), "--canonical-dir", str(canon_dir)], args.dry_run)
        print("[canonicalize pass 2 — consume cache, merge]")
        run(canon_cmd, args.dry_run)

    meta = {"cohort_id": cohort_id, "n": args.n, "prompts": ps,
            "started": now.isoformat(), "run_dir": str(run_dir),
            "canonical": not args.no_canonical}
    if not args.dry_run:
        (cohort / "cohort_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False),
                                                 encoding="utf-8")
    print(f"\ncohort complete: {cohort}")


if __name__ == "__main__":
    main()
