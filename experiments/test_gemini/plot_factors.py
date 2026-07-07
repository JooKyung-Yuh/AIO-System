"""Render the two-layer AIO factor graph from a split build as SEPARATE figures.

build_factors_split.py emits cio_cards.json + am_cards.json + links.json. This draws four
standalone PNGs, each doing one job (no crowding a single canvas):

  belief_tally.png     diverging bars: which mechanisms/assumptions the paper's own results
                       strengthen (blue) vs weaken (red)
  cio_completeness.png heatmap: which slots each observation card fills; a comparison card
                       missing its reference arm is flagged red
  node_coverage.png    bars: share of Layer-1 nodes (per category) that reached a card
  factor_graph.png     provenance -> observation -> belief, curved edges colored by vote

Colors follow a CVD-validated palette (blue<->red diverging for votes; aqua/orange categorical
for pattern_class). Pass an old flat-format build and it will error clearly.
"""
import argparse
import collections
import glob
import json
import sys
from pathlib import Path

# CVD-validated palette (light surface)
SURFACE, INK, SECOND, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"
STRENGTHEN, WEAKEN = "#2a78d6", "#e34948"        # diverging pair (votes)
PRIMARY_CLS, COMPARISON_CLS = "#1baf7a", "#eb6834"  # categorical (pattern_class)
FILLED, EMPTY = "#5b5f66", "#eeede9"             # presence
SLOTS = ["context", "intervention", "reference", "eval_metric", "pattern"]


def rc():
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": BASELINE, "axes.labelcolor": SECOND, "text.color": INK,
        "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
        "axes.spines.right": False, "font.size": 11,
        "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"],
    })


def parse_args():
    p = argparse.ArgumentParser(description="Render split-build factor graphs as separate PNGs.")
    p.add_argument("--run-dir", required=True)
    p.add_argument("--build-dir", default=None, help="factors/<build> (default: newest split build)")
    p.add_argument("--no-show", action="store_true")
    return p.parse_args()


def locate_build(run_dir: Path, override):
    if override:
        return Path(override)
    hits = sorted(glob.glob(str(run_dir / "factors" / "*" / "cio_cards.json")))
    if not hits:
        sys.exit(f"no split build (cio_cards.json) under {run_dir/'factors'}; run build_factors_split.py")
    return Path(hits[-1]).parent


def filled(card, slot):
    v = card.get(slot)
    return bool(v) if slot != "context" else bool(v)


# ---------------------------------------------------------------- belief tally
def plot_belief_tally(am, tally, out):
    import matplotlib.pyplot as plt
    ranked = [a for a in am if tally[a["am_id"]]["strengthen"] + tally[a["am_id"]]["weaken"] > 0]
    ranked.sort(key=lambda a: -(tally[a["am_id"]]["strengthen"] + tally[a["am_id"]]["weaken"]))
    n = len(ranked)
    fig, ax = plt.subplots(figsize=(11, 0.46 * n + 1.8))
    ys = range(n)
    for i, a in enumerate(ranked):
        t = tally[a["am_id"]]
        ax.barh(i, t["strengthen"], color=STRENGTHEN, height=0.66, zorder=3)
        ax.barh(i, -t["weaken"], color=WEAKEN, height=0.66, zorder=3)
        if t["strengthen"]:
            ax.text(t["strengthen"] + 0.15, i, str(t["strengthen"]), va="center", ha="left",
                    fontsize=8, color=SECOND)
        if t["weaken"]:
            ax.text(-t["weaken"] - 0.15, i, str(t["weaken"]), va="center", ha="right",
                    fontsize=8, color=SECOND)
    ax.axvline(0, color=BASELINE, lw=1.0, zorder=4)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([f"{a['node']}  {a.get('gloss','')[:44]}" for a in ranked], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("weaken  ←   votes cast by observations   →  strengthen", fontsize=9)
    ax.tick_params(length=0)
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title("Belief tally — which claims the paper's own results support vs contest",
                 fontsize=13, color=INK, loc="left", pad=12)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------- CIO completeness heat
def plot_completeness(cio, out):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    cards = sorted(cio, key=lambda c: ((c.get("provenance") or {}).get("location", "~"), c["cio_id"]))
    n = len(cards)
    fig, ax = plt.subplots(figsize=(8.5, 0.17 * n + 2.2))
    gap = 0.12
    for i, c in enumerate(cards):
        is_cmp = c.get("pattern_class") == "comparison"
        # pattern_class strip
        ax.add_patch(Rectangle((-1 + gap, i + gap), 1 - 2 * gap, 1 - 2 * gap,
                     facecolor=COMPARISON_CLS if is_cmp else PRIMARY_CLS, edgecolor="none"))
        for j, slot in enumerate(SLOTS):
            if filled(c, slot):
                fc = FILLED
            elif slot == "reference" and is_cmp:
                fc = WEAKEN                       # comparison missing its reference arm
            else:
                fc = EMPTY
            ax.add_patch(Rectangle((j + gap, i + gap), 1 - 2 * gap, 1 - 2 * gap,
                         facecolor=fc, edgecolor="none"))
    # provenance group labels
    prev = None
    for i, c in enumerate(cards):
        loc = (c.get("provenance") or {}).get("location", "?")
        if loc != prev:
            ax.text(-1.25, i + 0.5, loc[:20], va="center", ha="right", fontsize=6.5, color=MUTED)
            if i:
                ax.axhline(i, color=GRID, lw=0.5)
            prev = loc
    ax.set_xlim(-1.3, len(SLOTS))
    ax.set_ylim(n, 0)
    ax.set_xticks([-0.5] + [j + 0.5 for j in range(len(SLOTS))])
    ax.set_xticklabels(["class"] + [s.replace("_", "\n") for s in SLOTS], fontsize=8)
    ax.xaxis.set_ticks_position("top")
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Observation completeness — filled slots per card\n"
                 "(red = comparison missing its reference arm)",
                 fontsize=12, color=INK, loc="left", pad=10)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------- node coverage
def plot_coverage(cov, out):
    import matplotlib.pyplot as plt
    nc = cov["node_coverage"]
    cats = ["context", "intervention", "mechanism", "eval_metric", "pattern", "assumption"]
    cats = [c for c in cats if c in nc]
    pcts = [nc[c]["coverage_pct"] or 0 for c in cats]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(range(len(cats)), pcts, color=STRENGTHEN, width=0.66, zorder=3)
    for b, c in zip(bars, cats):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5,
                f"{nc[c]['covered']}/{nc[c]['total']}", ha="center", va="bottom",
                fontsize=8, color=SECOND)
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels([c.replace("_", "\n") for c in cats], fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of Layer-1 nodes referenced by ≥1 card", fontsize=9)
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    tot = cov["node_coverage_total"]
    ax.set_title(f"Node coverage by category — total {tot['covered']}/{tot['total']} "
                 f"= {tot['coverage_pct']}%", fontsize=12, color=INK, loc="left", pad=10)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------- graph
def plot_graph(cio, am, links, tally, out):
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, Patch

    cio_sorted = sorted(cio, key=lambda c: ((c.get("provenance") or {}).get("location", "~"), c["cio_id"]))
    am_sorted = sorted(am, key=lambda a: -(tally[a["am_id"]]["strengthen"] + tally[a["am_id"]]["weaken"]))
    locs = []
    for c in cio_sorted:
        loc = (c.get("provenance") or {}).get("location", "?")
        if loc not in locs:
            locs.append(loc)

    def spaced(k):
        return [1 - (i + 0.5) / k for i in range(k)]  # top->bottom in [0,1]

    y_loc = {l: y for l, y in zip(locs, spaced(len(locs)))}
    y_cio = {c["cio_id"]: y for c, y in zip(cio_sorted, spaced(len(cio_sorted)))}
    y_am = {a["am_id"]: y for a, y in zip(am_sorted, spaced(len(am_sorted)))}
    X_LOC, X_CIO, X_AM = 0.0, 1.0, 2.0

    fig, ax = plt.subplots(figsize=(15, 13))

    # edges: provenance->cio faint grey; cio->am blue/red by vote
    for c in cio_sorted:
        loc = (c.get("provenance") or {}).get("location", "?")
        ax.add_patch(FancyArrowPatch((X_LOC, y_loc[loc]), (X_CIO, y_cio[c["cio_id"]]),
                     connectionstyle="arc3,rad=0.12", arrowstyle="-", lw=0.4,
                     color=MUTED, alpha=0.18, zorder=1))
    for e in links:
        cid, aid = e.get("source_cio"), e.get("target_am")
        if cid in y_cio and aid in y_am:
            col = STRENGTHEN if e.get("direction") == "strengthen" else WEAKEN
            ax.add_patch(FancyArrowPatch((X_CIO, y_cio[cid]), (X_AM, y_am[aid]),
                         connectionstyle="arc3,rad=0.12", arrowstyle="-", lw=0.7,
                         color=col, alpha=0.45, zorder=2))

    # nodes
    for l, y in y_loc.items():
        ax.scatter(X_LOC, y, s=60, marker="s", color=BASELINE, edgecolors=MUTED, linewidths=0.5, zorder=3)
        ax.text(X_LOC - 0.03, y, l[:20], va="center", ha="right", fontsize=6.5, color=MUTED)
    for c in cio_sorted:
        cls = c.get("pattern_class")
        ax.scatter(X_CIO, y_cio[c["cio_id"]], s=42,
                   color=COMPARISON_CLS if cls == "comparison" else PRIMARY_CLS,
                   edgecolors=WEAKEN if (cls == "comparison" and not c.get("reference")) else "white",
                   linewidths=1.0 if (cls == "comparison" and not c.get("reference")) else 0.4, zorder=3)
    for a in am_sorted:
        t = tally[a["am_id"]]
        v = t["strengthen"] + t["weaken"]
        ax.scatter(X_AM, y_am[a["am_id"]], s=90 + 130 * (v ** 0.5),  # sqrt: keep big beliefs bounded
                   color="#e9e8e3" if v == 0 else INK, edgecolors=MUTED, linewidths=0.6, zorder=3)
        ax.text(X_AM + 0.08, y_am[a["am_id"]], f"{a['node']} {a.get('gloss','')[:28]}",
                va="center", ha="left", fontsize=6.5, color=INK if v else MUTED)

    for x, lab in ((X_LOC, "paper location"), (X_CIO, "observation (CIO)"), (X_AM, "belief (M/A)")):
        ax.text(x, 1.03, lab, ha="center", va="bottom", fontsize=10, color=SECOND, weight="bold")
    legend = [
        Patch(facecolor=PRIMARY_CLS, edgecolor="none", label="primary_result"),
        Patch(facecolor=COMPARISON_CLS, edgecolor="none", label="comparison"),
        Patch(facecolor="white", edgecolor=WEAKEN, label="comparison missing reference"),
        Patch(facecolor=STRENGTHEN, edgecolor="none", label="strengthen vote"),
        Patch(facecolor=WEAKEN, edgecolor="none", label="weaken vote"),
    ]
    ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.06),
              ncol=5, fontsize=8, frameon=False)
    ax.set_xlim(-0.55, 2.95)
    ax.set_ylim(-0.05, 1.1)
    ax.axis("off")
    ax.set_title("AIO factor graph — paper location → observation → belief",
                 fontsize=13, color=INK, pad=6)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    args = parse_args()
    run_dir = Path(args.run_dir)
    build = locate_build(run_dir, args.build_dir)
    cio = json.loads((build / "cio_cards.json").read_text(encoding="utf-8"))
    am = json.loads((build / "am_cards.json").read_text(encoding="utf-8"))
    links = json.loads((build / "links.json").read_text(encoding="utf-8"))
    cov = json.loads((build / "coverage.json").read_text(encoding="utf-8"))

    tally = collections.defaultdict(lambda: {"strengthen": 0, "weaken": 0})
    for e in links:
        if e.get("direction") in ("strengthen", "weaken"):
            tally[e["target_am"]][e["direction"]] += 1

    try:
        import matplotlib
        if args.no_show:
            matplotlib.use("Agg")
        rc()
    except ImportError:
        sys.exit("matplotlib is not installed. Run: pip install matplotlib")

    outputs = {
        "belief_tally.png": lambda p: plot_belief_tally(am, tally, p),
        "cio_completeness.png": lambda p: plot_completeness(cio, p),
        "node_coverage.png": lambda p: plot_coverage(cov, p),
        "factor_graph.png": lambda p: plot_graph(cio, am, links, tally, p),
    }
    for name, fn in outputs.items():
        fn(build / name)
        print(f"saved: {build / name}")


if __name__ == "__main__":
    main()
