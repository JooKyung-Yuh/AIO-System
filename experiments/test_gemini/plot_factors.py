"""Plot the factor graph from one run as a plain multipartite graph.

Joins factors.json (flat factor records) with spans.json (node id -> text) and draws a
bipartite factor graph: factor nodes on a center column, the A/M/C/I/E/P nodes they
reference in category columns on either side. Node labels are node ids only; the id -> text
mapping is printed to the console so long span quotes do not clutter the plot.

This is a structural view. The flat factor format carries no belief direction, so no
strengthen/weaken coloring is drawn here.
"""
import argparse
import glob
import json
import sys
from pathlib import Path

import networkx as nx

from aio_common import factor_coverage_report

SLOTS = ["assumption", "mechanism", "context", "intervention", "eval_metric", "pattern"]

PREFIX = {
    "A": "assumption",
    "M": "mechanism",
    "C": "context",
    "I": "intervention",
    "E": "eval_metric",
    "P": "pattern",
}

# left-to-right column order; factor sits in the middle
LAYER = {
    "assumption": 0,
    "mechanism": 1,
    "context": 2,
    "factor": 3,
    "intervention": 4,
    "eval_metric": 5,
    "pattern": 6,
}

COLORS = {
    "assumption": "#e41a1c",
    "mechanism": "#377eb8",
    "context": "#4daf4a",
    "intervention": "#ff7f00",
    "eval_metric": "#984ea3",
    "pattern": "#a65628",
    "factor": "#bbbbbb",
}


def parse_args():
    p = argparse.ArgumentParser(description="Plot the factor graph of one extraction run.")
    p.add_argument("--run-dir", required=True, help="runs/<run_id> directory that contains spans.json")
    p.add_argument("--factors-json", default=None, help="path to factors.json (default: newest under <run-dir>/factors/*/)")
    p.add_argument("--out", default=None, help="PNG path (default: factor_graph.png next to the factors.json used)")
    p.add_argument("--no-show", action="store_true", help="save only, do not open a window (headless)")
    p.add_argument("--limit", type=int, default=None, help="plot only the first N factors (readability)")
    return p.parse_args()


def locate_factors(run_dir: Path, override: str | None) -> Path:
    if override:
        return Path(override)
    candidates = sorted(glob.glob(str(run_dir / "factors" / "*" / "factors.json")))
    if not candidates:
        sys.exit(f"no factors.json found under {run_dir / 'factors'}; pass --factors-json")
    return Path(candidates[-1])


def is_empty(v) -> bool:
    return v in (None, "", "null")


def category_of(node_id: str) -> str:
    return PREFIX.get(node_id[:1], "context")


def num_of(node_id: str) -> int:
    digits = "".join(ch for ch in node_id[1:] if ch.isdigit())
    return int(digits) if digits else 0


def main():
    args = parse_args()
    run_dir = Path(args.run_dir)

    spans_path = run_dir / "spans.json"
    if not spans_path.exists():
        sys.exit(f"spans.json not found in {run_dir}")
    factors_path = locate_factors(run_dir, args.factors_json)

    spans = json.loads(spans_path.read_text(encoding="utf-8"))
    all_factors = json.loads(factors_path.read_text(encoding="utf-8"))
    text_of = {s["node_id"]: s.get("text", "") for s in spans}

    # node coverage is a property of the whole run, not of whatever --limit trims for display
    full_coverage = factor_coverage_report(spans, all_factors)

    factors = all_factors[: args.limit] if args.limit is not None else all_factors

    G = nx.Graph()
    for i, f in enumerate(factors):
        fid = f"F{i}"
        G.add_node(fid, kind="factor")
        for slot in SLOTS:
            v = f.get(slot)
            if is_empty(v):
                continue
            G.add_node(v, kind=category_of(v))
            G.add_edge(fid, v)

    for n, data in G.nodes(data=True):
        data["subset"] = LAYER[data["kind"]]

    # console legend: node id -> text, so the plot can stay label-light
    referenced = sorted(
        (n for n, d in G.nodes(data=True) if d["kind"] != "factor"),
        key=lambda n: (LAYER[category_of(n)], num_of(n)),
    )
    print(f"factors plotted: {sum(1 for _, d in G.nodes(data=True) if d['kind'] == 'factor')}")
    print(f"variable nodes:  {len(referenced)}")
    print("-" * 72)
    for n in referenced:
        t = text_of.get(n, "(not in spans.json)").replace("\n", " ")
        print(f"{n:5} [{G.nodes[n]['kind']:12}] {t[:80]}")

    if args.out:
        out_path = Path(args.out)
    else:
        default_name = f"factor_graph{('_limit%d' % args.limit) if args.limit else ''}.png"
        out_path = factors_path.parent / default_name

    try:
        import matplotlib
        if args.no_show:
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.colors
        from matplotlib.patches import Patch
        import numpy as np
    except ImportError:
        sys.exit("matplotlib is not installed. Run: pip install matplotlib")

    pos = nx.multipartite_layout(G, subset_key="subset")

    fig = plt.figure(figsize=(22, 11))
    gs = fig.add_gridspec(2, 2, width_ratios=[2.4, 1], height_ratios=[2, 1], wspace=0.25, hspace=0.35)
    ax = fig.add_subplot(gs[:, 0])
    ax_matrix = fig.add_subplot(gs[0, 1])
    ax_bar = fig.add_subplot(gs[1, 1])

    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.25, width=0.6)
    for kind in LAYER:
        nodes = [n for n, d in G.nodes(data=True) if d["kind"] == kind]
        if not nodes:
            continue
        nx.draw_networkx_nodes(
            G, pos, ax=ax, nodelist=nodes,
            node_color=COLORS[kind],
            node_shape="s" if kind == "factor" else "o",
            node_size=320 if kind == "factor" else 220,
            linewidths=0.5, edgecolors="#333333",
        )
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=6)

    legend = [Patch(facecolor=COLORS[k], edgecolor="#333333", label=k) for k in LAYER]
    ax.legend(handles=legend, loc="upper right", fontsize=8, framealpha=0.9)
    ax.set_title(f"factor graph: {run_dir.name}", fontsize=11)
    ax.axis("off")

    # --- completeness matrix: one row per factor, one column per slot, colored if filled ---
    n = len(factors)
    grid = np.ones((max(n, 1), len(SLOTS), 3))  # white = empty
    for i, f in enumerate(factors):
        for j, slot in enumerate(SLOTS):
            if not is_empty(f.get(slot)):
                grid[i, j] = matplotlib.colors.to_rgb(COLORS[slot])
    ax_matrix.imshow(grid, aspect="auto", interpolation="none")
    ax_matrix.set_xticks(range(len(SLOTS)))
    ax_matrix.set_xticklabels([s[:4] for s in SLOTS], fontsize=7, rotation=45, ha="right")
    step = max(1, n // 25)
    ax_matrix.set_yticks(range(0, n, step))
    ax_matrix.set_yticklabels([f"F{i}" for i in range(0, n, step)], fontsize=6)
    ax_matrix.set_title("factor completeness (row = factor, white = null)", fontsize=9)

    # --- per-category node coverage: what fraction of spans.json nodes each category
    #     actually ends up referenced by >=1 factor (the orphan-rate breakdown). Computed
    #     over ALL factors regardless of --limit, since coverage is a whole-run property.
    cov = full_coverage
    pcts = [cov["node_coverage"][slot]["coverage_pct"] or 0 for slot in SLOTS]
    labels = [
        f"{cov['node_coverage'][slot]['covered']}/{cov['node_coverage'][slot]['total']}"
        for slot in SLOTS
    ]
    bars = ax_bar.bar(range(len(SLOTS)), pcts, color=[COLORS[s] for s in SLOTS], edgecolor="#333333")
    ax_bar.set_xticks(range(len(SLOTS)))
    ax_bar.set_xticklabels([s[:4] for s in SLOTS], fontsize=7, rotation=45, ha="right")
    ax_bar.set_ylim(0, 100)
    ax_bar.set_ylabel("% of nodes covered", fontsize=8)
    total = cov["node_coverage_total"]
    ax_bar.set_title(
        f"node coverage by category (total {total['covered']}/{total['total']} = "
        f"{total['coverage_pct']}%)", fontsize=9,
    )
    for bar, label in zip(bars, labels):
        ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, label,
                    ha="center", va="bottom", fontsize=6)

    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"\nsaved: {out_path}")
    print(f"node coverage (whole run): {full_coverage['node_coverage_total']}")
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
