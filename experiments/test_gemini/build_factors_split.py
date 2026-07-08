"""Layer-2 factor assembly, split into three focused Gemini calls.

Instead of one call that turns all spans into flat factors at once (build_factors.py), this
assembles two small card types first and links them:

  Call 1  extract_cio    evidence_units.json  ->  cio_cards.json   (context + intervention + reference
                                                                    arm + eval_metric + pattern; NO M/A)
  Call 2  extract_am     mechanism/assumption ->  am_cards.json    (genuine belief targets, deduped)
                         spans
  Call 3  link_factors   cio_cards + am_cards  ->  links.json      (belief_update edges: which
                                                                    observation strengthens/weakens
                                                                    which mechanism/assumption)

The paper itself (prose transcription + figure/table descriptions) is fed to ALL THREE calls so
context is never lost after Layer 1. A deterministic join then writes factors.json (each CIO card
plus its belief edges) for human reading.

Run group_evidence_units.py first to produce evidence_units.json.
"""
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
import collections
import datetime
import json
import sys
import traceback
from pathlib import Path

from aio_common import load_prompt, parse_json_array, usage_of, add_usage, token_line

load_dotenv()
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"
PROMPTS = Path("./prompts")
# Per-call prompt versions. Bump one and re-run to create a new, separately tagged cohort
# (build_dir carries BUILD_TAG) so runs on different prompts never mix in one ensemble vote.
CIO_PROMPT = "extract_cio_v2_1"
AM_PROMPT = "extract_am_v3_1"
LINK_PROMPT = "link_factors_v1"


def _ver(prompt_name):
    """'extract_am_v3_1' -> 'am_v3_1'. Strips only the 'extract_'/'link_' verb prefix so
    multi-part versions (v3_1) stay intact — a bare rsplit('_') would keep only '1'."""
    for prefix in ("extract_", "link_"):
        if prompt_name.startswith(prefix):
            return prompt_name[len(prefix):]
    return prompt_name


BUILD_TAG = f"factor_split_{_ver(CIO_PROMPT)}_{_ver(AM_PROMPT)}_{_ver(LINK_PROMPT)}"
AM_LABELS = ("assumption", "mechanism")
PREFIX_CAT = {"A": "assumption", "M": "mechanism", "C": "context",
              "I": "intervention", "E": "eval_metric", "P": "pattern"}


def call(prompt_path: Path, subs: dict, out_dir: Path, tag: str):
    """Run one Gemini call, save raw + parsed, return (parsed_list, usage)."""
    prompt = load_prompt(prompt_path, **subs)
    (out_dir / f"prompt_{tag}.md").write_text(prompt, encoding="utf-8")
    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=65536),
    )
    raw = resp.text or ""
    (out_dir / f"raw_{tag}.md").write_text(raw, encoding="utf-8")
    finish = resp.candidates[0].finish_reason if resp.candidates else None
    if str(finish) != "FinishReason.STOP":
        print(f"  [WARN] {tag}: finish_reason={finish} (maybe truncated)", file=sys.stderr)
    parsed, salvaged = parse_json_array(raw)
    if salvaged:
        print(f"  [WARN] {tag}: salvaged a truncated JSON array", file=sys.stderr)
    (out_dir / f"{tag}.json").write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
    usage = usage_of(resp)
    print(f"  {tag}: {len(parsed)} items | {token_line(usage)}", file=sys.stderr)
    return parsed, usage


def join_factors(cio_cards, am_cards, links):
    """Deterministic join: each CIO card plus its outgoing belief edges (resolved to AM nodes)."""
    am_by_id = {a["am_id"]: a for a in am_cards if isinstance(a, dict) and a.get("am_id")}
    links_by_cio = collections.defaultdict(list)
    for e in links:
        if isinstance(e, dict):
            links_by_cio[e.get("source_cio")].append(e)
    factors = []
    for i, c in enumerate(cio_cards, 1):
        if not isinstance(c, dict):
            continue
        beliefs = []
        for e in links_by_cio.get(c.get("cio_id"), []):
            am = am_by_id.get(e.get("target_am"), {})
            beliefs.append({
                "target_am": e.get("target_am"),
                "kind": am.get("kind"),
                "node": am.get("node"),
                "gloss": am.get("gloss"),
                "direction": e.get("direction"),
                "evidence": e.get("evidence"),
            })
        factors.append({"factor_id": f"F{i:03d}", "cio": c, "beliefs": beliefs})
    return factors


def split_coverage(spans, cio_cards, am_cards, links):
    totals = collections.Counter(s["assigned_label"] for s in spans)
    used = collections.defaultdict(set)

    def mark(nid):
        if isinstance(nid, str) and nid[:1] in PREFIX_CAT:
            used[PREFIX_CAT[nid[0]]].add(nid)

    for c in cio_cards:
        if not isinstance(c, dict):
            continue
        for nid in c.get("context") or []:
            mark(nid)
        for k in ("intervention", "reference", "eval_metric", "pattern"):
            mark(c.get(k))
    for a in am_cards:
        if not isinstance(a, dict):
            continue
        mark(a.get("node"))
        for nid in a.get("aliases") or []:
            mark(nid)

    node_cov = {}
    tot_cov = tot_all = 0
    for cat, tot in totals.items():
        cov = len(used.get(cat, set()))
        node_cov[cat] = {"covered": cov, "total": tot,
                         "coverage_pct": round(100 * cov / tot, 1) if tot else None}
        tot_cov += cov
        tot_all += tot

    cio_ids = {c.get("cio_id") for c in cio_cards if isinstance(c, dict)}
    am_ids = {a.get("am_id") for a in am_cards if isinstance(a, dict)}
    linked_cio = {e.get("source_cio") for e in links if isinstance(e, dict)}
    linked_am = {e.get("target_am") for e in links if isinstance(e, dict)}
    with_ref = sum(1 for c in cio_cards if isinstance(c, dict) and c.get("reference"))
    pat_cls = collections.Counter(c.get("pattern_class") for c in cio_cards if isinstance(c, dict))
    directions = collections.Counter(e.get("direction") for e in links if isinstance(e, dict))

    return {
        "cio_count": len(cio_cards),
        "am_count": len(am_cards),
        "link_count": len(links),
        "cio_with_reference": with_ref,
        "pattern_class": dict(pat_cls),
        "link_direction": dict(directions),
        "orphan_cio": len(cio_ids - linked_cio),   # observation with no interpretation (OK)
        "orphan_am": len(am_ids - linked_am),       # belief target no observation votes on
        "node_coverage": node_cov,
        "node_coverage_total": {
            "covered": tot_cov, "total": tot_all,
            "coverage_pct": round(100 * tot_cov / tot_all, 1) if tot_all else None,
        },
    }


def parse_args():
    p = argparse.ArgumentParser(description="Assemble AIO factors via 3 focused Gemini calls (CIO / AM / link).")
    p.add_argument("--run-dir", required=True, help="runs/<run_id> with spans.json + evidence_units.json")
    p.add_argument("--paper-id", default="PXX")
    p.add_argument("--paper-title-hint", default="unknown")
    p.add_argument("--paper-text", default="./docs/VARC.txt", help="prose transcription fed to every call")
    p.add_argument("--assets", default="./docs/VARC.assets.json", help="figure/table descriptions fed to every call")
    p.add_argument("--build-index", default=None,
                   help="unique suffix for build_id; required when builds are launched in parallel "
                        "(the second-granularity timestamp alone collides). Default: none (sequential).")
    p.add_argument("--builds-dir", default=None,
                   help="where to write this build's folder (default: <run-dir>/factors). "
                        "run_cohort.py points this at <cohort>/builds so an ensemble stays self-contained.")
    return p.parse_args()


def main():
    args = parse_args()
    run_dir = Path(args.run_dir)
    spans = json.loads((run_dir / "spans.json").read_text(encoding="utf-8"))
    evidence_units = (run_dir / "evidence_units.json").read_text(encoding="utf-8")
    paper_text = Path(args.paper_text).read_text(encoding="utf-8")
    assets = Path(args.assets).read_text(encoding="utf-8")
    am_spans = json.dumps(
        [{k: s.get(k) for k in ("node_id", "assigned_label", "text", "note", "location", "parent", "source_span")}
         for s in spans if s["assigned_label"] in AM_LABELS],
        ensure_ascii=False, indent=2,
    )

    now = datetime.datetime.now().astimezone()
    idx = f"{args.build_index}_" if args.build_index else ""   # avoid same-second build_id collision in parallel
    build_id = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{idx}{BUILD_TAG}"
    builds_root = Path(args.builds_dir) if args.builds_dir else run_dir / "factors"
    build_dir = builds_root / build_id
    build_dir.mkdir(parents=True, exist_ok=False)

    base = {"paper_id": args.paper_id, "paper_title_hint": args.paper_title_hint,
            "paper_text": paper_text, "assets": assets}
    metadata = {"build_id": build_id, "source_run_dir": str(run_dir), "timestamp": now.isoformat(),
                "model": MODEL_NAME, "build_tag": BUILD_TAG,
                "prompts": {"cio": CIO_PROMPT, "am": AM_PROMPT, "link": LINK_PROMPT},
                "paper_text_path": args.paper_text, "assets_path": args.assets}
    total_usage = None

    try:
        cio_cards, u1 = call(PROMPTS / f"{CIO_PROMPT}.md",
                             {**base, "evidence_units": evidence_units}, build_dir, "cio_cards")
        am_cards, u2 = call(PROMPTS / f"{AM_PROMPT}.md",
                            {**base, "am_spans": am_spans}, build_dir, "am_cards")
        links, u3 = call(PROMPTS / f"{LINK_PROMPT}.md",
                         {**base,
                          "cio_cards": json.dumps(cio_cards, ensure_ascii=False, indent=2),
                          "am_cards": json.dumps(am_cards, ensure_ascii=False, indent=2)},
                         build_dir, "links")
        for u in (u1, u2, u3):
            total_usage = add_usage(total_usage, u)

        factors = join_factors(cio_cards, am_cards, links)
        (build_dir / "factors.json").write_text(
            json.dumps(factors, indent=2, ensure_ascii=False), encoding="utf-8")

        coverage = split_coverage(spans, cio_cards, am_cards, links)
        (build_dir / "coverage.json").write_text(
            json.dumps(coverage, indent=2, ensure_ascii=False), encoding="utf-8")

        metadata.update({"status": "success", "cio_count": len(cio_cards),
                         "am_count": len(am_cards), "link_count": len(links),
                         "factor_count": len(factors), "usage_total": total_usage,
                         "coverage": coverage})
        print(f"\nCIO={len(cio_cards)}  AM={len(am_cards)}  links={len(links)}  factors={len(factors)}",
              file=sys.stderr)
        print(f"node coverage: {coverage['node_coverage_total']['coverage_pct']}%  "
              f"(v4 was 29.4%) | CIO with reference arm: "
              f"{coverage['cio_with_reference']}/{coverage['cio_count']}", file=sys.stderr)
        print(f"Saved to: {build_dir}", file=sys.stderr)

    except Exception as e:
        metadata["status"] = "error"
        metadata["error_type"] = type(e).__name__
        metadata["error_message"] = str(e)
        (build_dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        print(traceback.format_exc(), file=sys.stderr)
        raise
    finally:
        (build_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
