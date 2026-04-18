import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

try:
    plt.style.use("seaborn-v0_8-darkgrid")
except:
    try:
        plt.style.use("seaborn-darkgrid")
    except:
        plt.style.use("default")

pm_summary   = pd.read_csv("../results/pm_summary_tai500_20_0.csv")
px_summary   = pd.read_csv("../results/px_summary_tai500_20_0.csv")
pop_summary  = pd.read_csv("../results/population_summary_tai500_20_0.csv")
tour_summary = pd.read_csv("../results/tournament_summary_tai500_20_0.csv")

FIXED_LABELS = {
    "pm":         "pop=360, gens=50, ts=5, px=0.85",
    "px":         "pop=360, gens=50, ts=5, pm=0.10",
    "population": "budget=18 000, ts=5, pm=0.10, px=0.85",
    "tournament": "pop=360, gens=50, pm=0.10, px=0.85",
}

COLORS = {
    "pm":         "#2E86AB",
    "px":         "#A23B72",
    "population": "#F18F01",
    "tournament": "#73AB84",
}

print("Plot 1: Combined sensitivity overview...")

all_means = pd.concat([
    pm_summary["mean"],
    px_summary["mean"],
    pop_summary["mean"],
    tour_summary["mean"],
])
global_mean = all_means.mean()

def normalise(series):
    return (series - global_mean) / global_mean * 100

datasets = [
    ("Mutation prob. (pm)",   pm_summary,   "pm",            "pm"),
    ("Crossover prob. (px)",  px_summary,   "px",            "px"),
    ("Population size",       pop_summary,  "population_size","population"),
    ("Tournament size",       tour_summary, "tournament_size","tournament"),
]

fig, axes = plt.subplots(1, 4, figsize=(18, 5), sharey=True)
fig.suptitle(
    "GA Parameter Sensitivity — Normalised Makespan\n"
    "(% deviation from grand mean; lower = better)",
    fontsize=14, fontweight="bold", y=1.02,
)

for ax, (label, df, xcol, key) in zip(axes, datasets):
    x      = df[xcol].values
    y_norm = normalise(df["mean"]).values
    ci_lo  = normalise(df["ci_lower"]).values
    ci_hi  = normalise(df["ci_upper"]).values
    sd     = (df["std_dev"] / global_mean * 100).values

    color = COLORS[key]

    ax.fill_between(range(len(x)), y_norm - sd, y_norm + sd,
                    alpha=0.15, color=color)
    ax.fill_between(range(len(x)), ci_lo, ci_hi,
                    alpha=0.30, color=color, label="95 % CI")
    ax.plot(range(len(x)), y_norm, "o-", color=color,
            linewidth=2, markersize=7, label="Mean")

    best_i = np.argmin(df["mean"].values)
    ax.scatter(best_i, y_norm[best_i], s=180, c="gold",
               edgecolors="black", zorder=5, marker="*")

    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")

    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(
        [f"{v:.2f}" if isinstance(v, float) else str(int(v)) for v in x],
        rotation=40, ha="right", fontsize=8,
    )
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_xlabel(xcol, fontsize=9)

    ax.text(0.02, 0.98, FIXED_LABELS[key],
            transform=ax.transAxes, fontsize=7,
            va="top", ha="left", color="dimgray",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.6))

axes[0].set_ylabel("Normalised makespan (% from grand mean)", fontsize=10)

handles = [
    plt.Line2D([0], [0], color="gray", linewidth=2, marker="o", label="Mean"),
    plt.fill([0], [0], alpha=0.30, color="gray", label="95 % CI")[0],
    plt.fill([0], [0], alpha=0.15, color="gray", label="±1 SD")[0],
    plt.scatter([0], [0], s=120, c="gold", edgecolors="black",
                marker="*", label="Best config"),
]
fig.legend(handles=handles, loc="lower center", ncol=4,
           bbox_to_anchor=(0.5, -0.06), fontsize=9)

plt.tight_layout()
plt.savefig("../figures/sensitivity_overview.png", dpi=150, bbox_inches="tight")
plt.show()
print("  Saved: sensitivity_overview.png")


# ════════════════════════════════════════════════════════════════════════════
# PLOT 2 — Mean vs Std-dev scatter (performance vs stability)
# ════════════════════════════════════════════════════════════════════════════
print("Plot 2: Performance vs stability scatter...")

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_title(
    "Performance vs Stability Across All Parameter Configurations\n"
    "(bottom-left = low makespan AND low variance → ideal)",
    fontsize=13, fontweight="bold",
)

for label, df, xcol, key in datasets:
    x_vals = df[xcol].values
    means  = df["mean"].values
    stds   = df["std_dev"].values
    color  = COLORS[key]

    sc = ax.scatter(means, stds, s=90, color=color,
                    edgecolors="white", linewidths=0.8,
                    label=label, zorder=3)

    for mean_v, std_v, xv in zip(means, stds, x_vals):
        txt = f"{xv:.2f}" if isinstance(xv, float) else str(int(xv))
        ax.annotate(txt, (mean_v, std_v),
                    textcoords="offset points", xytext=(5, 4),
                    fontsize=7, color=color)

    best_i = np.argmin(means)
    ax.scatter(means[best_i], stds[best_i], s=250, color=color,
               edgecolors="black", linewidths=1.5,
               marker="*", zorder=5)

ax.annotate("", xy=(ax.get_xlim()[0] if ax.get_xlim()[0] else 0,
                    ax.get_ylim()[0] if ax.get_ylim()[0] else 0),
            xytext=(0.18, 0.18), textcoords="axes fraction",
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
ax.text(0.20, 0.13, "Ideal direction", transform=ax.transAxes,
        fontsize=9, color="black", style="italic")

ax.set_xlabel("Mean Makespan", fontsize=12, fontweight="bold")
ax.set_ylabel("Std Dev of Makespan", fontsize=12, fontweight="bold")
ax.legend(title="Parameter", fontsize=9, title_fontsize=9,
          loc="upper right")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../figures/performance_vs_stability.png", dpi=150, bbox_inches="tight")
plt.show()
print("  Saved: performance_vs_stability.png")


# ════════════════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("OPTIMAL PARAMETERS SUMMARY")
print("=" * 60)

for label, df, xcol, key in datasets:
    row = df.loc[df["mean"].idxmin()]
    val = f"{row[xcol]:.3f}" if isinstance(row[xcol], float) else str(int(row[xcol]))
    extra = ""
    if key == "population":
        extra = f"  (gens={int(row['generations'])})"
    print(f"\n{label}:")
    print(f"   Optimal value : {val}{extra}")
    print(f"   Mean makespan : {row['mean']:.1f} ± {row['std_dev']:.1f}")
    print(f"   Best single   : {row['min']:.0f}")
    print(f"   95 % CI       : [{row['ci_lower']:.1f}, {row['ci_upper']:.1f}]")

print("\n" + "=" * 60)
print("Figures saved to ../figures/")
print("=" * 60)
