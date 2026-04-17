import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    plt.style.use("seaborn-v0-8-darkgrid")
except:
    try:
        plt.style.use("seaborn-darkgrid")
    except:
        plt.style.use("default")
        print("Note: Using default matplotlib style")

COLOR_SCHEMES = {
    "pm":         {"main": "#2E86AB", "fill": "#A3C4E8"},
    "px":         {"main": "#A23B72", "fill": "#E4B8D4"},
    "population": {"main": "#F18F01", "fill": "#FFD9B5"},
    "tournament": {"main": "#73AB84", "fill": "#C8E6D9"},
}

# Fixed params taken directly from the 4 separate cpp files
FIXED_PARAMS = {
    "pm": {
        "Population Size": 360,
        "Generations": 50,
        "Tournament Size": 5,
        "Crossover Probability (px)": 0.85,
    },
    "px": {
        "Population Size": 360,
        "Generations": 50,
        "Tournament Size": 5,
        "Mutation Probability (pm)": 0.10,
    },
    "population": {
        "Eval Budget (Pop × Gens)": "18,000 (fixed)",
        "Tournament Size": 5,
        "Mutation Probability (pm)": 0.10,
        "Crossover Probability (px)": 0.85,
    },
    "tournament": {
        "Population Size": 360,
        "Generations": 50,
        "Mutation Probability (pm)": 0.10,
        "Crossover Probability (px)": 0.85,
    },
}

INSTANCE = "tai20_20_0"
RUNS = 20


def add_fixed_parameters_text(ax, param_type, x_pos=0.98, y_pos=0.02):
    fixed = FIXED_PARAMS[param_type]
    text = "Fixed Parameters:\n" + "\n".join([f"{k}: {v}" for k, v in fixed.items()])
    ax.text(
        x_pos, y_pos, text,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="bottom",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8, edgecolor="gray"),
    )


def plot_sensitivity(ax, x, summary, param_key, xlabel, color_key):
    """Generic sensitivity plot: error bars + std dev band."""
    ax.errorbar(
        x, summary["mean"],
        yerr=[summary["mean"] - summary["ci_lower"],
              summary["ci_upper"] - summary["mean"]],
        fmt="o-", capsize=5, capthick=2, elinewidth=2, markersize=8,
        color=COLOR_SCHEMES[color_key]["main"], ecolor="gray", label="Mean ± 95% CI",
    )
    ax.fill_between(
        x,
        summary["mean"] - summary["std_dev"],
        summary["mean"] + summary["std_dev"],
        alpha=0.2, color=COLOR_SCHEMES[color_key]["fill"], label="±1 Std Dev",
    )
    ax.set_xlabel(xlabel, fontsize=12, fontweight="bold")
    ax.set_ylabel("Makespan", fontsize=12, fontweight="bold")
    ax.grid(True, alpha=0.3)

    best_idx  = summary["mean"].idxmin()
    best_x    = summary.loc[best_idx, param_key]
    best_mean = summary.loc[best_idx, "mean"]
    return best_idx, best_x, best_mean


# ==================== 1. Mutation Probability (pm) ====================
print("Plotting Mutation Probability analysis...")

pm_summary = pd.read_csv(f"../results/pm_summary_{INSTANCE}.csv")

fig, ax = plt.subplots(figsize=(10, 6))
best_idx, best_pm, best_mean = plot_sensitivity(
    ax, pm_summary["pm"], pm_summary, "pm",
    "Mutation Probability (pm)", "pm"
)
ax.set_title("Mutation Probability (pm) Sensitivity Analysis", fontsize=14, fontweight="bold")
ax.legend(loc="upper left")

ax.scatter(best_pm, best_mean, s=200, c="gold", edgecolors="black", zorder=5, marker="*")
ax.annotate(
    f"Optimal: pm={best_pm:.3f}\nMean={best_mean:.1f}",
    xy=(best_pm, best_mean), xytext=(15, 15), textcoords="offset points",
    fontsize=10, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8, edgecolor="black"),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="black"),
)
add_fixed_parameters_text(ax, "pm")
plt.tight_layout()
plt.savefig("../figures/pm_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== 2. Crossover Probability (px) ====================
print("Plotting Crossover Probability analysis...")

px_summary = pd.read_csv(f"../results/px_summary_{INSTANCE}.csv")

fig, ax = plt.subplots(figsize=(10, 6))
best_idx, best_px, best_mean = plot_sensitivity(
    ax, px_summary["px"], px_summary, "px",
    "Crossover Probability (px)", "px"
)
ax.set_title("Crossover Probability (px) Sensitivity Analysis", fontsize=14, fontweight="bold")
ax.legend(loc="upper left")

ax.scatter(best_px, best_mean, s=200, c="gold", edgecolors="black", zorder=5, marker="*")
ax.annotate(
    f"Optimal: px={best_px:.3f}\nMean={best_mean:.1f}",
    xy=(best_px, best_mean), xytext=(15, 15), textcoords="offset points",
    fontsize=10, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8, edgecolor="black"),
    arrowprops=dict(arrowstyle="->", color="black"),
)
add_fixed_parameters_text(ax, "px")
plt.tight_layout()
plt.savefig("../figures/px_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== 3. Population Size ====================
print("Plotting Population Size analysis...")

pop_summary = pd.read_csv(f"../results/population_summary_{INSTANCE}.csv")

fig, ax = plt.subplots(figsize=(10, 6))
best_idx, best_pop, best_mean = plot_sensitivity(
    ax, pop_summary["population_size"], pop_summary, "population_size",
    "Population Size", "population"
)

# Label each point with its paired generation count
for _, row in pop_summary.iterrows():
    ax.annotate(
        f"gens={int(row['generations'])}",
        xy=(row["population_size"], row["mean"]),
        xytext=(0, 14), textcoords="offset points",
        fontsize=8, ha="center", color="dimgray",
    )

ax.set_title(
    "Population Size Sensitivity Analysis\n(Fixed Eval Budget = 18,000)",
    fontsize=14, fontweight="bold"
)
ax.legend(loc="upper left")

best_gens = pop_summary.loc[best_idx, "generations"]
ax.scatter(best_pop, best_mean, s=200, c="gold", edgecolors="black", zorder=5, marker="*")
ax.annotate(
    f"Optimal: Size={int(best_pop)}\nGens={int(best_gens)}\nMean={best_mean:.1f}",
    xy=(best_pop, best_mean), xytext=(15, -50), textcoords="offset points",
    fontsize=10, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8, edgecolor="black"),
    arrowprops=dict(arrowstyle="->", color="black"),
)
add_fixed_parameters_text(ax, "population")
plt.tight_layout()
plt.savefig("../figures/population_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== 4. Tournament Size ====================
print("Plotting Tournament Size analysis...")

tour_summary = pd.read_csv(f"../results/tournament_summary_{INSTANCE}.csv")

fig, ax = plt.subplots(figsize=(10, 6))
best_idx, best_tour, best_mean = plot_sensitivity(
    ax, tour_summary["tournament_size"], tour_summary, "tournament_size",
    "Tournament Size", "tournament"
)
ax.set_title("Tournament Size Sensitivity Analysis", fontsize=14, fontweight="bold")
ax.legend(loc="upper left")

ax.scatter(best_tour, best_mean, s=200, c="gold", edgecolors="black", zorder=5, marker="*")
ax.annotate(
    f"Optimal: Size={int(best_tour)}\nMean={best_mean:.1f}",
    xy=(best_tour, best_mean), xytext=(15, 15), textcoords="offset points",
    fontsize=10, fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8, edgecolor="black"),
    arrowprops=dict(arrowstyle="->", color="black"),
)
add_fixed_parameters_text(ax, "tournament")
plt.tight_layout()
plt.savefig("../figures/tournament_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== Summary ====================
print("\n" + "=" * 60)
print("OPTIMAL PARAMETERS SUMMARY")
print("=" * 60)

best_pm_row   = pm_summary.loc[pm_summary["mean"].idxmin()]
best_px_row   = px_summary.loc[px_summary["mean"].idxmin()]
best_pop_row  = pop_summary.loc[pop_summary["mean"].idxmin()]
best_tour_row = tour_summary.loc[tour_summary["mean"].idxmin()]

for label, row, key, fmt in [
    ("Mutation Probability (pm)",  best_pm_row,   "pm",              ".3f"),
    ("Crossover Probability (px)", best_px_row,   "px",              ".3f"),
    ("Tournament Size",            best_tour_row, "tournament_size", ".0f"),
]:
    print(f"\n{label}:")
    print(f"   Optimal: {row[key]:{fmt}}")
    print(f"   Mean Makespan: {row['mean']:.1f} ± {row['std_dev']:.1f}")
    print(f"   Best in {RUNS} runs: {row['min']:.0f}")
    print(f"   95% CI: [{row['ci_lower']:.1f}, {row['ci_upper']:.1f}]")

print(f"\nPopulation Size:")
print(f"   Optimal: {int(best_pop_row['population_size'])} (with {int(best_pop_row['generations'])} generations)")
print(f"   Mean Makespan: {best_pop_row['mean']:.1f} ± {best_pop_row['std_dev']:.1f}")
print(f"   Best in {RUNS} runs: {best_pop_row['min']:.0f}")
print(f"   95% CI: [{best_pop_row['ci_lower']:.1f}, {best_pop_row['ci_upper']:.1f}]")

print("\n" + "=" * 60)
print("Figures saved to ../figures/ directory")
print("=" * 60)
