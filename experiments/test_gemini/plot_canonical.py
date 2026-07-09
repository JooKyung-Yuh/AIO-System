"""Render the CANONICAL cohort graph (canonicalize_v0 output), not a single raw build.

plot_factors.py draws one build's raw cards; this draws the canonicalized cohort — the layer
that carries note-aware context splits, representative/referenced_by, and confidence bands. Three
standalone PNGs (no hairball):

  canonical_hubs.png   the backbone: canonical nodes sized/ranked by ref_count (how many
                       observations lean on them). Surfaces the paper's core mechanisms/metrics.
  canonical_graph.png  paper location -> canonical observation (pattern) -> canonical belief
                       (M/A cluster). Comparison card missing its reference arm is outlined red;
                       belief edge opacity = vote confidence.
  belief_tally.png     diverging bars: which canonical beliefs the paper's own results
                       strengthen (blue) vs weaken (red).

Reads a cohort dir (ensemble.json + canonical/) plus the run-dir (evidence_units.json for
document order, spans.json only if needed). Deterministic; no LLM.
"""
import argparse
import collections
import json
import sys
from pathlib import Path

# CVD-validated palette (light surface), shared with plot_factors.py
SURFACE, INK, SECOND, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"
STRENGTHEN, WEAKEN = "#2a78d6", "#e34948"
PRIMARY_CLS, COMPARISON_CLS = "#1baf7a", "#eb6834"
# categorical by canonical type (hub view)
TYPE_COLOR = {"mechanism": "#2a78d6", "assumption": "#7c4dff", "intervention": "#eb6834",
              "eval_metric": "#1baf7a", "context": "#898781"}
BAND_ALPHA = {"observed": 0.9, "supported": 0.55, "uncertain": 0.28}


def rc():
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": BASELINE, "axes.labelcolor": SECOND, "text.color": INK,
        "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
        "axes.spines.right": False, "font.size": 11,
        "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"],
    })


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def location_order(run_dir):
    path = Path(run_dir) / "evidence_units.json"
    if not path.exists():
        return {}
    return {u["location"]: i for i, u in enumerate(load(path))}


def belief_edges(ens, r2c):
    """(pattern, canonical_am, direction) -> max vote confidence, mapping each link's raw am
    atom through raw2canon so the belief graph is drawn on canonical clusters."""
    edges = {}
    for v in ens["nodes"]["links"].values():
        cam = r2c.get(v["am_node"])
        if not cam:
            continue
        key = (v["cio_pattern"], cam, v["direction"])
        edges[key] = max(edges.get(key, 0.0), v.get("confidence", 0.0))
    return edges


# ------------------------------------------------------------- hub backbone
def plot_hubs(registry, out, top=30):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    rows = []
    for kind in ("context", "intervention", "eval_metric", "am"):
        for cid, rec in registry[kind].items():
            t = rec.get("type", kind)                      # am carries mechanism/assumption
            rows.append((rec.get("ref_count", 0), t, rec.get("gloss") or cid))
    rows = [r for r in rows if r[0] > 0]
    rows.sort(key=lambda r: (-r[0]))
    rows = rows[:top]
    n = len(rows)
    fig, ax = plt.subplots(figsize=(11, 0.42 * n + 1.6))
    for i, (rc_, t, gloss) in enumerate(rows):
        ax.barh(i, rc_, color=TYPE_COLOR.get(t, MUTED), height=0.66, zorder=3)
        ax.text(rc_ + 0.2, i, str(rc_), va="center", ha="left", fontsize=8, color=SECOND)
        ax.text(-0.3, i, gloss[:60], va="center", ha="right", fontsize=8, color=INK)
    ax.set_yticks([])
    ax.set_xlabel("ref_count — observations (CIO patterns) that reference this canonical node", fontsize=9)
    ax.invert_yaxis()
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    ax.set_xlim(0, max(r[0] for r in rows) * 1.08)
    seen = [t for _, t, _ in rows]
    legend = [Patch(facecolor=TYPE_COLOR[t], edgecolor="none", label=t)
              for t in ("mechanism", "assumption", "intervention", "eval_metric", "context") if t in seen]
    ax.legend(handles=legend, loc="lower right", fontsize=8, frameon=False)
    ax.set_title(f"Canonical backbone — top {n} nodes by how many observations lean on them",
                 fontsize=13, color=INK, loc="left", pad=12)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------- location -> obs -> belief
def plot_canonical_graph(cons, registry, edges, loc_order, out):
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, Patch

    def loc_rank(c):
        return loc_order.get((c.get("provenance") or {}).get("location", "?"), 10**9)

    pats = sorted(cons.values(), key=lambda c: (loc_rank(c), c["pattern"]))
    locs = []
    for c in pats:
        loc = (c.get("provenance") or {}).get("location", "?")
        if loc not in locs:
            locs.append(loc)

    am_reg = registry["am"]
    out_votes = collections.Counter()
    for (pat, cam, d) in edges:
        out_votes[cam] += 1
    ams = sorted(am_reg.keys(), key=lambda a: (-out_votes[a], a))

    def spaced(k):
        return [1 - (i + 0.5) / k for i in range(k)] if k else []

    y_loc = dict(zip(locs, spaced(len(locs))))
    y_pat = {c["pattern"]: y for c, y in zip(pats, spaced(len(pats)))}
    y_am = dict(zip(ams, spaced(len(ams))))
    X_LOC, X_PAT, X_AM = 0.0, 1.0, 2.0

    fig, ax = plt.subplots(figsize=(15, max(9, 0.26 * len(pats))))

    for c in pats:
        loc = (c.get("provenance") or {}).get("location", "?")
        ax.add_patch(FancyArrowPatch((X_LOC, y_loc[loc]), (X_PAT, y_pat[c["pattern"]]),
                     connectionstyle="arc3,rad=0.12", arrowstyle="-", lw=0.4,
                     color=MUTED, alpha=0.16, zorder=1))
    for (pat, cam, d), conf in edges.items():
        if pat in y_pat and cam in y_am:
            col = STRENGTHEN if d == "strengthen" else WEAKEN if d == "weaken" else MUTED
            ax.add_patch(FancyArrowPatch((X_PAT, y_pat[pat]), (X_AM, y_am[cam]),
                         connectionstyle="arc3,rad=0.1", arrowstyle="-", lw=0.6,
                         color=col, alpha=0.12 + 0.5 * conf, zorder=2))

    for l, y in y_loc.items():
        ax.scatter(X_LOC, y, s=52, marker="s", color=BASELINE, edgecolors=MUTED, linewidths=0.5, zorder=3)
        ax.text(X_LOC - 0.03, y, l[:22], va="center", ha="right", fontsize=6.5, color=MUTED)
    for c in pats:
        cls = c.get("pattern_class")
        miss_ref = cls == "comparison" and not (c.get("canonical") or {}).get("reference")
        ax.scatter(X_PAT, y_pat[c["pattern"]], s=40,
                   color=COMPARISON_CLS if cls == "comparison" else PRIMARY_CLS,
                   edgecolors=WEAKEN if miss_ref else "white",
                   linewidths=1.1 if miss_ref else 0.4, zorder=3)
    for a in ams:
        rec = am_reg[a]
        v = out_votes[a]
        ax.scatter(X_AM, y_am[a], s=70 + 120 * (rec.get("ref_count", 0) ** 0.5),
                   color=TYPE_COLOR.get(rec.get("type"), INK),
                   alpha=BAND_ALPHA.get(rec.get("band"), 0.9),
                   edgecolors=MUTED, linewidths=0.6, zorder=3)
        ax.text(X_AM + 0.06, y_am[a], (rec.get("gloss") or a)[:34], va="center", ha="left",
                fontsize=6.5, color=INK if v else MUTED)

    for x, lab in ((X_LOC, "paper location"), (X_PAT, "observation (canonical CIO)"),
                   (X_AM, "belief (canonical M/A)")):
        ax.text(x, 1.03, lab, ha="center", va="bottom", fontsize=10, color=SECOND, weight="bold")
    legend = [
        Patch(facecolor=PRIMARY_CLS, edgecolor="none", label="primary_result"),
        Patch(facecolor=COMPARISON_CLS, edgecolor="none", label="comparison"),
        Patch(facecolor="white", edgecolor=WEAKEN, label="comparison missing reference"),
        Patch(facecolor=STRENGTHEN, edgecolor="none", label="strengthen"),
        Patch(facecolor=WEAKEN, edgecolor="none", label="weaken"),
    ]
    ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.04),
              ncol=5, fontsize=8, frameon=False)
    ax.set_xlim(-0.6, 2.75)
    ax.set_ylim(-0.05, 1.1)
    ax.axis("off")
    ax.set_title("AIO canonical factor graph — location → observation → belief",
                 fontsize=13, color=INK, pad=6)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------- belief tally
def plot_belief_tally(registry, edges, out):
    import matplotlib.pyplot as plt
    tally = collections.defaultdict(lambda: {"strengthen": set(), "weaken": set()})
    for (pat, cam, d) in edges:
        if d in ("strengthen", "weaken"):
            tally[cam][d].add(pat)
    am_reg = registry["am"]
    ranked = [a for a in am_reg if tally[a]["strengthen"] or tally[a]["weaken"]]
    ranked.sort(key=lambda a: -(len(tally[a]["strengthen"]) + len(tally[a]["weaken"])))
    n = len(ranked)
    fig, ax = plt.subplots(figsize=(11, 0.46 * n + 1.8))
    for i, a in enumerate(ranked):
        s, w = len(tally[a]["strengthen"]), len(tally[a]["weaken"])
        ax.barh(i, s, color=STRENGTHEN, height=0.66, zorder=3)
        ax.barh(i, -w, color=WEAKEN, height=0.66, zorder=3)
        if s:
            ax.text(s + 0.15, i, str(s), va="center", ha="left", fontsize=8, color=SECOND)
        if w:
            ax.text(-w - 0.15, i, str(w), va="center", ha="right", fontsize=8, color=SECOND)
    ax.axvline(0, color=BASELINE, lw=1.0, zorder=4)
    ax.set_yticks(range(n))
    ax.set_yticklabels([(am_reg[a].get("gloss") or a)[:46] for a in ranked], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("weaken  ←   distinct observations   →  strengthen", fontsize=9)
    ax.tick_params(length=0)
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title("Belief tally — canonical claims the paper's own results support vs contest",
                 fontsize=13, color=INK, loc="left", pad=12)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description="Render the canonical cohort graph as separate PNGs.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--cohort", required=True, help="cohort dir (ensemble.json + canonical/)")
    ap.add_argument("--out-dir", default=None, help="where to write PNGs (default: <cohort>/plots)")
    ap.add_argument("--no-show", action="store_true")
    args = ap.parse_args()

    cohort = Path(args.cohort)
    cons = load(cohort / "canonical" / "cio_consensus.json")
    registry = load(cohort / "canonical" / "registry.json")
    ens = load(cohort / "ensemble.json")
    edges = belief_edges(ens, registry["raw2canon"])
    loc_order = location_order(args.run_dir)

    try:
        import matplotlib
        if args.no_show:
            matplotlib.use("Agg")
        rc()
    except ImportError:
        sys.exit("matplotlib is not installed in this venv.")

    out_dir = Path(args.out_dir) if args.out_dir else cohort / "plots"
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_hubs(registry, out_dir / "canonical_hubs.png")
    plot_canonical_graph(cons, registry, edges, loc_order, out_dir / "canonical_graph.png")
    plot_belief_tally(registry, edges, out_dir / "belief_tally.png")
    for name in ("canonical_hubs.png", "canonical_graph.png", "belief_tally.png"):
        print(f"saved: {out_dir / name}")


if __name__ == "__main__":
    main()
