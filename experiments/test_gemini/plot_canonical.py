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
# belief node color by ontology_type, grouped by link_policy so the picture reads by policy:
# direct = blue/teal, paper_thesis = gold, qualifier family = purple/magenta, demoted = grey.
ONTOLOGY_COLOR = {"mechanism": "#2a78d6", "aggregate_claim": "#1f9e8f", "paper_thesis": "#d4a017",
                  "assumption": "#7c4dff", "scope_condition": "#9c6ade", "precondition": "#b39ddb",
                  "limitation": "#c2185b", "qualitative_observation": "#898781"}
ROLLUP = "#a8791f"                                        # claim -> thesis roll-up edge (thesis-gold family)
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


def load_belief_edges(cohort, n_builds_max=5):
    """Read canonical/belief_edges.json (link_policy-enforced) for the 4-column graph. Returns:
      direct     {(pat, claim, dir): conf}     pat -> mechanism|aggregate (belief_update)
      nd_claim   {(pat, claim, bucket): conf}   pat -> qualifier|demoted claim (NOT belief)
      obs_thesis {(pat, thesis, bucket): conf}  pat -> thesis (reported_as_main_result | unresolved)
      rollups    [(claim, thesis, n_supporting)] claim -> thesis (rolls_up, the 2-level edge)
    conf = n_builds / n_builds_max so edge opacity reflects reproducibility."""
    be = load(cohort / "canonical" / "belief_edges.json")
    direct, nd_claim, obs_thesis, rollups = {}, {}, {}, []
    for e in be.get("direct", []):
        direct[(e["observation"], e["target"], e["direction"])] = e["n_builds"] / n_builds_max
    for bucket in ("qualifier", "demoted"):
        for e in be.get(bucket, []):
            nd_claim[(e["observation"], e["target"], bucket)] = e["n_builds"] / n_builds_max
    for bucket in ("reported_as_main_result", "unresolved_thesis_link"):
        for e in be.get(bucket, []):
            obs_thesis[(e["observation"], e["target"], bucket)] = e["n_builds"] / n_builds_max
    for e in be.get("rolls_up", []):
        rollups.append((e["observation"], e["target"], e.get("n_supporting_observations", 0)))
    return direct, nd_claim, obs_thesis, rollups


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


# -------------------------------------- location -> observation -> claim -> thesis (4 columns)
def plot_canonical_graph(cons, registry, direct, nd_claim, obs_thesis, rollups, loc_order, out):
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, Patch
    from matplotlib.lines import Line2D

    def loc_rank(c):
        return loc_order.get((c.get("provenance") or {}).get("location", "?"), 10**9)

    pats = sorted(cons.values(), key=lambda c: (loc_rank(c), c["pattern"]))
    locs = []
    for c in pats:
        loc = (c.get("provenance") or {}).get("location", "?")
        if loc not in locs:
            locs.append(loc)

    am_reg = registry["am"]
    thesis_ids = sorted(a for a, r in am_reg.items() if r.get("ontology_type") == "paper_thesis")
    thesis_set = set(thesis_ids)
    out_votes = collections.Counter()
    for (pat, cam, d) in direct:
        out_votes[cam] += 1
    claims = sorted((a for a in am_reg if a not in thesis_set), key=lambda a: (-out_votes[a], a))

    def spaced(k):
        return [1 - (i + 0.5) / k for i in range(k)] if k else []

    y_loc = dict(zip(locs, spaced(len(locs))))
    y_pat = {c["pattern"]: y for c, y in zip(pats, spaced(len(pats)))}
    y_claim = dict(zip(claims, spaced(len(claims))))
    y_thesis = dict(zip(thesis_ids, [0.5] if len(thesis_ids) == 1 else spaced(len(thesis_ids))))
    X_LOC, X_PAT, X_CLAIM, X_THESIS = 0.0, 1.0, 2.0, 3.0

    fig, ax = plt.subplots(figsize=(17, max(9, 0.26 * len(pats))))

    for c in pats:                                           # location -> observation
        loc = (c.get("provenance") or {}).get("location", "?")
        ax.add_patch(FancyArrowPatch((X_LOC, y_loc[loc]), (X_PAT, y_pat[c["pattern"]]),
                     connectionstyle="arc3,rad=0.12", arrowstyle="-", lw=0.4, color=MUTED, alpha=0.16, zorder=1))
    for (pat, cam, bucket), conf in nd_claim.items():        # observation -> qualifier/demoted claim (not belief)
        if pat in y_pat and cam in y_claim:
            ax.add_patch(FancyArrowPatch((X_PAT, y_pat[pat]), (X_CLAIM, y_claim[cam]),
                         connectionstyle="arc3,rad=0.1", arrowstyle="-", lw=0.5, linestyle=(0, (2, 2)),
                         color=MUTED, alpha=0.10 + 0.28 * conf, zorder=2))
    for (pat, cam, d), conf in direct.items():               # observation -> mechanism/aggregate (belief_update)
        if pat in y_pat and cam in y_claim:
            col = STRENGTHEN if d == "strengthen" else WEAKEN if d == "weaken" else MUTED
            ax.add_patch(FancyArrowPatch((X_PAT, y_pat[pat]), (X_CLAIM, y_claim[cam]),
                         connectionstyle="arc3,rad=0.1", arrowstyle="-", lw=0.7, color=col, alpha=0.18 + 0.5 * conf, zorder=3))
    for (pat, tgt, bucket), conf in obs_thesis.items():      # observation -> thesis (headline/unresolved), skips claim col
        if pat in y_pat and tgt in y_thesis:
            ax.add_patch(FancyArrowPatch((X_PAT, y_pat[pat]), (X_THESIS, y_thesis[tgt]),
                         connectionstyle="arc3,rad=0.22", arrowstyle="-", lw=0.5, linestyle=(0, (1, 2)),
                         color=MUTED, alpha=0.12 + 0.3 * conf, zorder=2))
    for (src, tgt, nsupp) in rollups:                        # claim -> thesis (rolls_up), the 2-level edge
        if src in y_claim and tgt in y_thesis:
            ax.add_patch(FancyArrowPatch((X_CLAIM, y_claim[src]), (X_THESIS, y_thesis[tgt]),
                         connectionstyle="arc3,rad=0.15", arrowstyle="-|>", mutation_scale=8,
                         lw=0.9, color=ROLLUP, alpha=0.6, zorder=4))

    for l, y in y_loc.items():
        ax.scatter(X_LOC, y, s=52, marker="s", color=BASELINE, edgecolors=MUTED, linewidths=0.5, zorder=3)
        ax.text(X_LOC - 0.03, y, l[:22], va="center", ha="right", fontsize=6.5, color=MUTED)
    for c in pats:
        cls = c.get("pattern_class")
        miss_ref = cls == "comparison" and not (c.get("canonical") or {}).get("reference")
        ax.scatter(X_PAT, y_pat[c["pattern"]], s=40,
                   color=COMPARISON_CLS if cls == "comparison" else PRIMARY_CLS,
                   edgecolors=WEAKEN if miss_ref else "white", linewidths=1.1 if miss_ref else 0.4, zorder=3)
    for a in claims:
        rec = am_reg[a]
        ax.scatter(X_CLAIM, y_claim[a], s=70 + 120 * (rec.get("ref_count", 0) ** 0.5),
                   color=ONTOLOGY_COLOR.get(rec.get("ontology_type"), TYPE_COLOR.get(rec.get("type"), INK)),
                   alpha=BAND_ALPHA.get(rec.get("band"), 0.9), edgecolors=MUTED, linewidths=0.6, zorder=3)
        ax.text(X_CLAIM + 0.05, y_claim[a], (rec.get("gloss") or a)[:30], va="center", ha="left",
                fontsize=6.3, color=INK if out_votes[a] else MUTED)
    for a in thesis_ids:                                     # thesis column
        rec = am_reg[a]
        ax.scatter(X_THESIS, y_thesis[a], s=200, color=ONTOLOGY_COLOR["paper_thesis"],
                   alpha=0.92, edgecolors=MUTED, linewidths=0.8, zorder=3)
        ax.text(X_THESIS + 0.05, y_thesis[a], (rec.get("gloss") or a)[:34], va="center", ha="left",
                fontsize=7, color=INK, weight="bold")

    for x, lab in ((X_LOC, "paper location"), (X_PAT, "observation (canonical CIO)"),
                   (X_CLAIM, "claim (mechanism / aggregate / qualifier)"), (X_THESIS, "paper_thesis")):
        ax.text(x, 1.03, lab, ha="center", va="bottom", fontsize=9.5, color=SECOND, weight="bold")
    legend = [
        Patch(facecolor=PRIMARY_CLS, edgecolor="none", label="primary_result"),
        Patch(facecolor=COMPARISON_CLS, edgecolor="none", label="comparison"),
        Patch(facecolor=STRENGTHEN, edgecolor="none", label="strengthen"),
        Patch(facecolor=WEAKEN, edgecolor="none", label="weaken"),
        Line2D([0], [0], color=MUTED, lw=1.0, linestyle=(0, (2, 2)), label="re-routed (not belief)"),
        Line2D([0], [0], color=ROLLUP, lw=1.2, label="rolls_up → thesis"),
    ]
    leg1 = ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.04),
                     ncol=6, fontsize=8, frameon=False)
    ax.add_artist(leg1)
    onto_legend = [                                          # one swatch per ontology_type color (1:1)
        Line2D([0], [0], marker="o", linestyle="none", markersize=8, markeredgecolor="none",
               markerfacecolor=ONTOLOGY_COLOR["mechanism"], label="mechanism (direct)"),
        Line2D([0], [0], marker="o", linestyle="none", markersize=8, markeredgecolor="none",
               markerfacecolor=ONTOLOGY_COLOR["aggregate_claim"], label="aggregate_claim (direct)"),
        Line2D([0], [0], marker="o", linestyle="none", markersize=8, markeredgecolor="none",
               markerfacecolor=ONTOLOGY_COLOR["paper_thesis"], label="paper_thesis (rolls_up)"),
        Line2D([0], [0], marker="o", linestyle="none", markersize=8, markeredgecolor="none",
               markerfacecolor=ONTOLOGY_COLOR["assumption"], label="assumption"),
        Line2D([0], [0], marker="o", linestyle="none", markersize=8, markeredgecolor="none",
               markerfacecolor=ONTOLOGY_COLOR["scope_condition"], label="scope_condition"),
        Line2D([0], [0], marker="o", linestyle="none", markersize=8, markeredgecolor="none",
               markerfacecolor=ONTOLOGY_COLOR["limitation"], label="limitation"),
        Line2D([0], [0], marker="o", linestyle="none", markersize=8, markeredgecolor="none",
               markerfacecolor=ONTOLOGY_COLOR["qualitative_observation"], label="demoted observation"),
    ]
    ax.legend(handles=onto_legend, loc="upper right", bbox_to_anchor=(1.03, 1.0), fontsize=7.5,
              frameon=False, title="belief node type", title_fontsize=8)
    ax.set_xlim(-0.6, 3.9)
    ax.set_ylim(-0.05, 1.1)
    ax.axis("off")
    ax.set_title("AIO canonical factor graph — location → observation → claim → thesis",
                 fontsize=13, color=INK, pad=6)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------- belief tally
def plot_belief_tally(registry, direct, out):
    import matplotlib.pyplot as plt
    tally = collections.defaultdict(lambda: {"strengthen": set(), "weaken": set()})
    for (pat, cam, d) in direct:                              # direct belief_update only (policy-enforced)
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
    ax.set_title("Belief tally — direct belief_update: claims the paper's own results support vs contest",
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
    direct, nd_claim, obs_thesis, rollups = load_belief_edges(cohort)
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
    plot_canonical_graph(cons, registry, direct, nd_claim, obs_thesis, rollups, loc_order, out_dir / "canonical_graph.png")
    plot_belief_tally(registry, direct, out_dir / "belief_tally.png")
    for name in ("canonical_hubs.png", "canonical_graph.png", "belief_tally.png"):
        print(f"saved: {out_dir / name}")


if __name__ == "__main__":
    main()
