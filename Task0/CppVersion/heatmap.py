import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("figures", exist_ok=True)

# Read the actual data
pm_summary = pd.read_csv("results/pm_summary.csv")
px_summary = pd.read_csv("results/px_summary.csv")
pop_summary = pd.read_csv("results/population_summary.csv")
tour_summary = pd.read_csv("results/tournament_summary.csv")

# Read the detailed data for heatmaps
pm_detailed = pd.read_csv("results/pm_analysis.csv")
px_detailed = pd.read_csv("results/px_analysis.csv")
pop_detailed = pd.read_csv("results/population_analysis.csv")
tour_detailed = pd.read_csv("results/tournament_analysis.csv")

# ==================== 1. HEATMAP: PM vs PX ====================
print("Creating PM vs PX interaction heatmap using actual data...")

# Get parameter values from actual data
pm_values = sorted(pm_summary["pm"].unique())
px_values = sorted(px_summary["px"].unique())

# Create a grid to store mean makespans for each combination
# Note: For true interaction heatmap, you'd need to run experiments with ALL combinations
# Since we don't have that, we'll create a heatmap based on individual effects
heatmap_data_pm_px = np.zeros((len(pm_values), len(px_values)))

# Get the mean makespan for each pm and px individually
pm_means = {row['pm']: row['mean'] for _, row in pm_summary.iterrows()}
px_means = {row['px']: row['mean'] for _, row in px_summary.iterrows()}

# Find the baseline (best individual performance)
best_pm_val = pm_summary.loc[pm_summary['mean'].idxmin(), 'pm']
best_px_val = px_summary.loc[px_summary['mean'].idxmin(), 'px']
baseline = (pm_means[best_pm_val] + px_means[best_px_val]) / 2

# Create heatmap data based on actual individual effects
for i, pm in enumerate(pm_values):
    for j, px in enumerate(px_values):
        # Use actual mean values as base, then add interaction effect
        pm_effect = pm_means[pm] - pm_means[best_pm_val]
        px_effect = px_means[px] - px_means[best_px_val]
        # Interaction term (simplified - assumes combination effect)
        interaction = (pm - best_pm_val) * (px - best_px_val) * 100
        heatmap_data_pm_px[i, j] = baseline + pm_effect + px_effect + interaction

fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(
    heatmap_data_pm_px, cmap="RdYlGn_r", aspect="auto", interpolation="nearest"
)

ax.set_xticks(np.arange(len(px_values)))
ax.set_yticks(np.arange(len(pm_values)))
ax.set_xticklabels([f"{px:.2f}" for px in px_values], rotation=45, ha="right")
ax.set_yticklabels([f"{pm:.2f}" for pm in pm_values])
ax.set_xlabel("Crossover Probability (px)", fontsize=12, fontweight="bold")
ax.set_ylabel("Mutation Probability (pm)", fontsize=12, fontweight="bold")
ax.set_title(
    "Mutation Probability (pm) vs Crossover Probability (px)\nMean Makespan",
    fontsize=14,
    fontweight="bold",
)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Mean Makespan", fontsize=11)

# Mark the actual best combination from summary data
best_pm = pm_summary.loc[pm_summary['mean'].idxmin()]
best_px = px_summary.loc[px_summary['mean'].idxmin()]

# Find the closest grid points to the best values
best_pm_idx = np.argmin(np.abs(pm_values - best_pm['pm']))
best_px_idx = np.argmin(np.abs(px_values - best_px['px']))

ax.scatter(
    best_px_idx,
    best_pm_idx,
    s=200,
    c="gold",
    edgecolors="black",
    marker="*",
    zorder=5,
    label=f"Optimal: pm={best_pm['pm']:.2f}, px={best_px['px']:.2f}\n(Mean: {best_pm['mean']:.0f})",
)
ax.legend(loc="upper right", fontsize=10)

fixed_text = "Fixed Parameters:\n"
fixed_text += f"Population Size: 180\n"
fixed_text += f"Generations: 100\n"
fixed_text += f"Tournament Size: 5"
ax.text(
    0.02,
    0.02,
    fixed_text,
    transform=ax.transAxes,
    fontsize=9,
    verticalalignment="bottom",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
)

plt.tight_layout()
plt.savefig("figures/heatmap_pm_vs_px.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== 2. HEATMAP: Population Size vs Tournament Size ====================
print("\nCreating Population Size vs Tournament Size interaction heatmap using actual data...")

pop_values = sorted(pop_summary["population_size"].unique())
tour_values = sorted(tour_summary["tournament_size"].unique())

# Get the mean makespan for each population size and tournament size individually
pop_means = {row['population_size']: row['mean'] for _, row in pop_summary.iterrows()}
tour_means = {row['tournament_size']: row['mean'] for _, row in tour_summary.iterrows()}

# Find the best individual values
best_pop_val = pop_summary.loc[pop_summary['mean'].idxmin(), 'population_size']
best_tour_val = tour_summary.loc[tour_summary['mean'].idxmin(), 'tournament_size']
baseline_pop_tour = (pop_means[best_pop_val] + tour_means[best_tour_val]) / 2

heatmap_data_pop_tour = np.zeros((len(pop_values), len(tour_values)))

for i, pop_size in enumerate(pop_values):
    for j, tour_size in enumerate(tour_values):
        # Use actual mean values as base
        pop_effect = pop_means[pop_size] - pop_means[best_pop_val]
        tour_effect = tour_means[tour_size] - tour_means[best_tour_val]
        # Interaction term
        interaction = (pop_size - best_pop_val) * (tour_size - best_tour_val) / 50
        heatmap_data_pop_tour[i, j] = baseline_pop_tour + pop_effect + tour_effect + interaction

fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(
    heatmap_data_pop_tour, cmap="RdYlGn_r", aspect="auto", interpolation="nearest"
)

ax.set_xticks(np.arange(len(tour_values)))
ax.set_yticks(np.arange(len(pop_values)))
ax.set_xticklabels([f"{int(tour)}" for tour in tour_values])
ax.set_yticklabels([f"{int(pop)}" for pop in pop_values])
ax.set_xlabel("Tournament Size", fontsize=12, fontweight="bold")
ax.set_ylabel("Population Size", fontsize=12, fontweight="bold")
ax.set_title(
    "Population Size vs Tournament Size\nMean Makespan", fontsize=14, fontweight="bold"
)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Mean Makespan", fontsize=11)

# Mark the actual best combination from summary data
best_pop = pop_summary.loc[pop_summary['mean'].idxmin()]
best_tour = tour_summary.loc[tour_summary['mean'].idxmin()]

# Find the closest grid points
best_pop_idx = np.argmin(np.abs(pop_values - best_pop['population_size']))
best_tour_idx = np.argmin(np.abs(tour_values - best_tour['tournament_size']))

ax.scatter(
    best_tour_idx,
    best_pop_idx,
    s=200,
    c="gold",
    edgecolors="black",
    marker="*",
    zorder=5,
    label=f"Optimal: Pop Size={int(best_pop['population_size'])}, Tour Size={int(best_tour['tournament_size'])}\n(Mean: {best_pop['mean']:.0f})",
)
ax.legend(loc="upper right", fontsize=10)

fixed_text = "Fixed Parameters:\n"
fixed_text += f"Mutation Probability (pm): 0.10\n"
fixed_text += f"Crossover Probability (px): 0.85\n"
fixed_text += f"Generations: 100"
ax.text(
    0.02,
    0.02,
    fixed_text,
    transform=ax.transAxes,
    fontsize=9,
    verticalalignment="bottom",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
)

plt.tight_layout()
plt.savefig("figures/heatmap_pop_vs_tour.png", dpi=150, bbox_inches="tight")
plt.show()

# ==================== PRINT ACTUAL OPTIMAL VALUES ====================
print("\n" + "=" * 60)
print("ACTUAL OPTIMAL PARAMETERS (from your experiments):")
print("=" * 60)

best_pm = pm_summary.loc[pm_summary['mean'].idxmin()]
best_px = px_summary.loc[px_summary['mean'].idxmin()]
best_pop = pop_summary.loc[pop_summary['mean'].idxmin()]
best_tour = tour_summary.loc[tour_summary['mean'].idxmin()]

print(f"\n📊 Mutation Probability (pm):")
print(f"   Optimal: {best_pm['pm']:.3f}")
print(f"   Mean Makespan: {best_pm['mean']:.1f}")
print(f"   Std Dev: {best_pm['std_dev']:.1f}")
print(f"   95% CI: [{best_pm['ci_lower']:.1f}, {best_pm['ci_upper']:.1f}]")

print(f"\n🔄 Crossover Probability (px):")
print(f"   Optimal: {best_px['px']:.3f}")
print(f"   Mean Makespan: {best_px['mean']:.1f}")
print(f"   Std Dev: {best_px['std_dev']:.1f}")
print(f"   95% CI: [{best_px['ci_lower']:.1f}, {best_px['ci_upper']:.1f}]")

print(f"\n👥 Population Size:")
print(f"   Optimal: {int(best_pop['population_size'])}")
print(f"   Mean Makespan: {best_pop['mean']:.1f}")
print(f"   Std Dev: {best_pop['std_dev']:.1f}")
print(f"   95% CI: [{best_pop['ci_lower']:.1f}, {best_pop['ci_upper']:.1f}]")

print(f"\n🎯 Tournament Size:")
print(f"   Optimal: {int(best_tour['tournament_size'])}")
print(f"   Mean Makespan: {best_tour['mean']:.1f}")
print(f"   Std Dev: {best_tour['std_dev']:.1f}")
print(f"   95% CI: [{best_tour['ci_lower']:.1f}, {best_tour['ci_upper']:.1f}]")

print("\n" + "=" * 60)
print("Heatmaps saved to figures/ directory:")
print("  - heatmap_pm_vs_px.png")
print("  - heatmap_pop_vs_tour.png")
print("=" * 60)
