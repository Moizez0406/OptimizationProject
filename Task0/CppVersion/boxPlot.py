import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Try to set a nice style, fall back if not available
try:
    plt.style.use("seaborn-v0-8-darkgrid")
except:
    try:
        plt.style.use("seaborn-darkgrid")
    except:
        plt.style.use("default")
        print("Note: Using default matplotlib style")

# Create figures directory if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Define color schemes for different parameter types
COLOR_SCHEMES = {
    "pm": {"main": "#2E86AB", "fill": "#A3C4E8"},
    "px": {"main": "#A23B72", "fill": "#E4B8D4"},
    "population": {"main": "#F18F01", "fill": "#FFD9B5"},
    "tournament": {"main": "#73AB84", "fill": "#C8E6D9"},
}

# Define fixed parameters for each experiment
FIXED_PARAMS = {
    "pm": {
        "Population Size": 180,
        "Generations": 100,
        "Tournament Size": 5,
        "Crossover Probability (px)": 0.85,
    },
    "px": {
        "Population Size": 180,
        "Generations": 100,
        "Tournament Size": 5,
        "Mutation Probability (pm)": 0.10,
    },
    "population": {
        "Generations": 100,
        "Tournament Size": 5,
        "Mutation Probability (pm)": 0.10,
        "Crossover Probability (px)": 0.85,
    },
    "tournament": {
        "Population Size": 180,
        "Generations": 100,
        "Mutation Probability (pm)": 0.10,
        "Crossover Probability (px)": 0.85,
    },
}


def add_fixed_parameters_text(ax, param_type, x_pos=0.98, y_pos=0.02):
    """Add fixed parameters text box to the plot"""
    fixed = FIXED_PARAMS[param_type]

    text = "Fixed Parameters:\n" + "\n".join([f"{k}: {v}" for k, v in fixed.items()])

    ax.text(
        x_pos,
        y_pos,
        text,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="bottom",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8, edgecolor="gray"),
    )


# ==================== 1. Plot Mutation Probability (pm) ====================
print("Plotting Mutation Probability analysis...")

pm_summary = pd.read_csv("results/pm_summary.csv")

fig, ax = plt.subplots(figsize=(10, 6))

# Plot mean with error bars (95% CI)
ax.errorbar(
    pm_summary["pm"],
    pm_summary["mean"],
    yerr=[
        pm_summary["mean"] - pm_summary["ci_lower"],
        pm_summary["ci_upper"] - pm_summary["mean"],
    ],
    fmt="o-",
    capsize=5,
    capthick=2,
    elinewidth=2,
    markersize=8,
    color=COLOR_SCHEMES["pm"]["main"],
    ecolor="gray",
    label="Mean ± 95% CI",
)

# Add standard deviation band
ax.fill_between(
    pm_summary["pm"],
    pm_summary["mean"] - pm_summary["std_dev"],
    pm_summary["mean"] + pm_summary["std_dev"],
    alpha=0.2,
    color=COLOR_SCHEMES["pm"]["fill"],
    label="±1 Std Dev",
)

ax.set_xlabel("Mutation Probability (pm)", fontsize=12, fontweight="bold")
ax.set_ylabel("Makespan", fontsize=12, fontweight="bold")
ax.set_title(
    "Mutation Probability (pm) Sensitivity Analysis", fontsize=14, fontweight="bold"
)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

# Find best pm
best_idx = pm_summary["mean"].idxmin()
best_pm = pm_summary.loc[best_idx, "pm"]
best_mean = pm_summary.loc[best_idx, "mean"]
ax.scatter(
    best_pm,
    best_mean,
    s=200,
    c="gold",
    edgecolors="black",
    zorder=5,
    marker="*",
    label=f"Best: pm={best_pm:.3f}",
)
ax.annotate(
    f"Optimal: pm={best_pm:.3f}\nMean={best_mean:.1f}",
    xy=(best_pm, best_mean),
    xytext=(15, 15),
    textcoords="offset points",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8, edgecolor="black"),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="black"),
)

# Add fixed parameters text
add_fixed_parameters_text(ax, "pm", x_pos=0.98, y_pos=0.02)

plt.tight_layout()
plt.savefig("figures/pm_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== 2. Plot Crossover Probability (px) ====================
print("Plotting Crossover Probability analysis...")

px_summary = pd.read_csv("results/px_summary.csv")

fig, ax = plt.subplots(figsize=(10, 6))

ax.errorbar(
    px_summary["px"],
    px_summary["mean"],
    yerr=[
        px_summary["mean"] - px_summary["ci_lower"],
        px_summary["ci_upper"] - px_summary["mean"],
    ],
    fmt="o-",
    capsize=5,
    capthick=2,
    elinewidth=2,
    markersize=8,
    color=COLOR_SCHEMES["px"]["main"],
    ecolor="gray",
    label="Mean ± 95% CI",
)

ax.fill_between(
    px_summary["px"],
    px_summary["mean"] - px_summary["std_dev"],
    px_summary["mean"] + px_summary["std_dev"],
    alpha=0.2,
    color=COLOR_SCHEMES["px"]["fill"],
    label="±1 Std Dev",
)

ax.set_xlabel("Crossover Probability (px)", fontsize=12, fontweight="bold")
ax.set_ylabel("Makespan", fontsize=12, fontweight="bold")
ax.set_title(
    "Crossover Probability (px) Sensitivity Analysis", fontsize=14, fontweight="bold"
)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

best_idx = px_summary["mean"].idxmin()
best_px = px_summary.loc[best_idx, "px"]
best_mean = px_summary.loc[best_idx, "mean"]
ax.scatter(
    best_px,
    best_mean,
    s=200,
    c="gold",
    edgecolors="black",
    zorder=5,
    marker="*",
    label=f"Best: px={best_px:.3f}",
)
ax.annotate(
    f"Optimal: px={best_px:.3f}\nMean={best_mean:.1f}",
    xy=(best_px, best_mean),
    xytext=(15, 15),
    textcoords="offset points",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8),
    arrowprops=dict(arrowstyle="->"),
)

add_fixed_parameters_text(ax, "px", x_pos=0.98, y_pos=0.02)

plt.tight_layout()
plt.savefig("figures/px_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== 3. Plot Population Size ====================
print("Plotting Population Size analysis...")

pop_summary = pd.read_csv("results/population_summary.csv")

fig, ax = plt.subplots(figsize=(10, 6))

ax.errorbar(
    pop_summary["population_size"],
    pop_summary["mean"],
    yerr=[
        pop_summary["mean"] - pop_summary["ci_lower"],
        pop_summary["ci_upper"] - pop_summary["mean"],
    ],
    fmt="o-",
    capsize=5,
    capthick=2,
    elinewidth=2,
    markersize=8,
    color=COLOR_SCHEMES["population"]["main"],
    ecolor="gray",
    label="Mean ± 95% CI",
)

ax.fill_between(
    pop_summary["population_size"],
    pop_summary["mean"] - pop_summary["std_dev"],
    pop_summary["mean"] + pop_summary["std_dev"],
    alpha=0.2,
    color=COLOR_SCHEMES["population"]["fill"],
    label="±1 Std Dev",
)

ax.set_xlabel("Population Size", fontsize=12, fontweight="bold")
ax.set_ylabel("Makespan", fontsize=12, fontweight="bold")
ax.set_title("Population Size Sensitivity Analysis", fontsize=14, fontweight="bold")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

best_idx = pop_summary["mean"].idxmin()
best_pop = pop_summary.loc[best_idx, "population_size"]
best_mean = pop_summary.loc[best_idx, "mean"]
ax.scatter(
    best_pop,
    best_mean,
    s=200,
    c="gold",
    edgecolors="black",
    zorder=5,
    marker="*",
    label=f"Best: Size={int(best_pop)}",
)
ax.annotate(
    f"Optimal: Size={int(best_pop)}\nMean={best_mean:.1f}",
    xy=(best_pop, best_mean),
    xytext=(15, 15),
    textcoords="offset points",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8),
    arrowprops=dict(arrowstyle="->"),
)

add_fixed_parameters_text(ax, "population", x_pos=0.98, y_pos=0.02)

plt.tight_layout()
plt.savefig("figures/population_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== 4. Plot Tournament Size ====================
print("Plotting Tournament Size analysis...")

tour_summary = pd.read_csv("results/tournament_summary.csv")

fig, ax = plt.subplots(figsize=(10, 6))

ax.errorbar(
    tour_summary["tournament_size"],
    tour_summary["mean"],
    yerr=[
        tour_summary["mean"] - tour_summary["ci_lower"],
        tour_summary["ci_upper"] - tour_summary["mean"],
    ],
    fmt="o-",
    capsize=5,
    capthick=2,
    elinewidth=2,
    markersize=8,
    color=COLOR_SCHEMES["tournament"]["main"],
    ecolor="gray",
    label="Mean ± 95% CI",
)

ax.fill_between(
    tour_summary["tournament_size"],
    tour_summary["mean"] - tour_summary["std_dev"],
    tour_summary["mean"] + tour_summary["std_dev"],
    alpha=0.2,
    color=COLOR_SCHEMES["tournament"]["fill"],
    label="±1 Std Dev",
)

ax.set_xlabel("Tournament Size", fontsize=12, fontweight="bold")
ax.set_ylabel("Makespan", fontsize=12, fontweight="bold")
ax.set_title("Tournament Size Sensitivity Analysis", fontsize=14, fontweight="bold")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

best_idx = tour_summary["mean"].idxmin()
best_tour = tour_summary.loc[best_idx, "tournament_size"]
best_mean = tour_summary.loc[best_idx, "mean"]
ax.scatter(
    best_tour,
    best_mean,
    s=200,
    c="gold",
    edgecolors="black",
    zorder=5,
    marker="*",
    label=f"Best: Size={int(best_tour)}",
)
ax.annotate(
    f"Optimal: Size={int(best_tour)}\nMean={best_mean:.1f}",
    xy=(best_tour, best_mean),
    xytext=(15, 15),
    textcoords="offset points",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8),
    arrowprops=dict(arrowstyle="->"),
)

add_fixed_parameters_text(ax, "tournament", x_pos=0.98, y_pos=0.02)

plt.tight_layout()
plt.savefig("figures/tournament_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== Summary with Optimal Parameters ====================
print("\n" + "=" * 60)
print("OPTIMAL PARAMETERS SUMMARY")
print("=" * 60)

best_pm_row = pm_summary.loc[pm_summary["mean"].idxmin()]
best_px_row = px_summary.loc[px_summary["mean"].idxmin()]
best_pop_row = pop_summary.loc[pop_summary["mean"].idxmin()]
best_tour_row = tour_summary.loc[tour_summary["mean"].idxmin()]

print(f"\nMutation Probability (pm):")
print(f"   Optimal: {best_pm_row['pm']:.3f}")
print(f"   Mean Makespan: {best_pm_row['mean']:.1f} ± {best_pm_row['std_dev']:.1f}")
print(f"   Best in 30 runs: {best_pm_row['min']:.0f}")
print(f"   95% CI: [{best_pm_row['ci_lower']:.1f}, {best_pm_row['ci_upper']:.1f}]")

print(f"\nCrossover Probability (px):")
print(f"   Optimal: {best_px_row['px']:.3f}")
print(f"   Mean Makespan: {best_px_row['mean']:.1f} ± {best_px_row['std_dev']:.1f}")
print(f"   Best in 30 runs: {best_px_row['min']:.0f}")
print(f"   95% CI: [{best_px_row['ci_lower']:.1f}, {best_px_row['ci_upper']:.1f}]")

print(f"\nPopulation Size:")
print(f"   Optimal: {int(best_pop_row['population_size'])}")
print(f"   Mean Makespan: {best_pop_row['mean']:.1f} ± {best_pop_row['std_dev']:.1f}")
print(f"   Best in 30 runs: {best_pop_row['min']:.0f}")
print(f"   95% CI: [{best_pop_row['ci_lower']:.1f}, {best_pop_row['ci_upper']:.1f}]")

print(f"\nTournament Size:")
print(f"   Optimal: {int(best_tour_row['tournament_size'])}")
print(f"   Mean Makespan: {best_tour_row['mean']:.1f} ± {best_tour_row['std_dev']:.1f}")
print(f"   Best in 30 runs: {best_tour_row['min']:.0f}")
print(f"   95% CI: [{best_tour_row['ci_lower']:.1f}, {best_tour_row['ci_upper']:.1f}]")

print("\n" + "=" * 60)
print("Figures saved to figures/ directory")
print("=" * 60)
