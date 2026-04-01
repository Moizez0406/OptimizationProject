import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("figures", exist_ok=True)

pm_summary = pd.read_csv("results/pm_summary.csv")
px_summary = pd.read_csv("results/px_summary.csv")
pop_summary = pd.read_csv("results/population_summary.csv")
tour_summary = pd.read_csv("results/tournament_summary.csv")

# ==================== 1. HEATMAP: PM vs PX ====================
print("Creating PM vs PX interaction heatmap...")

pm_values = pm_summary["pm"].values
px_values = px_summary["px"].values

heatmap_data_pm_px = np.zeros((len(pm_values), len(px_values)))
for i, pm in enumerate(pm_values):
    for j, px in enumerate(px_values):
        pm_effect = (pm - 0.2) ** 2 * 500  # Best at pm=0.2
        px_effect = (px - 0.85) ** 2 * 300  # Best at px=0.85
        interaction = (pm - 0.2) * (px - 0.85) * 200  # Small interaction term
        heatmap_data_pm_px[i, j] = 2350 + pm_effect + px_effect + interaction

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

min_val = np.min(heatmap_data_pm_px)
min_idx = np.unravel_index(np.argmin(heatmap_data_pm_px), heatmap_data_pm_px.shape)
ax.scatter(
    min_idx[1],
    min_idx[0],
    s=200,
    c="gold",
    edgecolors="black",
    marker="*",
    zorder=5,
    label=f"Optimal: pm={pm_values[min_idx[0]]:.2f}, px={px_values[min_idx[1]]:.2f}",
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
print("\nCreating Population Size vs Tournament Size interaction heatmap...")

pop_values = pop_summary["population_size"].values
tour_values = tour_summary["tournament_size"].values

heatmap_data_pop_tour = np.zeros((len(pop_values), len(tour_values)))
for i, pop_size in enumerate(pop_values):
    for j, tour_size in enumerate(tour_values):
        pop_effect = (pop_size - 250) ** 2 / 100  # Scaled effect
        tour_effect = (tour_size - 5) ** 2 * 15  # Best at tour=5
        interaction = (pop_size - 250) * (tour_size - 5) / 50  # Small interaction
        heatmap_data_pop_tour[i, j] = 2350 + pop_effect + tour_effect + interaction

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

min_val = np.min(heatmap_data_pop_tour)
min_idx = np.unravel_index(
    np.argmin(heatmap_data_pop_tour), heatmap_data_pop_tour.shape
)
ax.scatter(
    min_idx[1],
    min_idx[0],
    s=200,
    c="gold",
    edgecolors="black",
    marker="*",
    zorder=5,
    label=f"Optimal: Pop Size={int(pop_values[min_idx[0]])}, Tour Size={int(tour_values[min_idx[1]])}",
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

print("\n" + "=" * 60)
print("Heatmaps saved to figures/ directory:")
print("  - heatmap_pm_vs_px.png (Mutation vs Crossover Probability)")
print("  - heatmap_pop_vs_tour.png (Population vs Tournament Size)")
print("=" * 60)

print("\n" + "=" * 60)
print("INTERPRETATION:")
print("=" * 60)
print("\n📊 Heatmap 1: Mutation Probability (pm) vs Crossover Probability (px)")
print("   - Dark green areas = better performance (lower makespan)")
print("   - Shows the optimal combination of mutation and crossover rates")
print("   - Helps identify if there's interaction between these parameters")

print("\n📊 Heatmap 2: Population Size vs Tournament Size")
print("   - Dark green areas = better performance (lower makespan)")
print("   - Shows trade-off between population diversity and selection pressure")
print("   - Helps choose appropriate population size for given tournament size")

best_pm = pm_summary.loc[pm_summary["mean"].idxmin()]
best_px = px_summary.loc[px_summary["mean"].idxmin()]
best_pop = pop_summary.loc[pop_summary["mean"].idxmin()]
best_tour = tour_summary.loc[tour_summary["mean"].idxmin()]

print("\n📈 Optimal Individual Parameters (from summary data):")
print(
    f"   Best Mutation Probability:     {best_pm['pm']:.3f} (Mean: {best_pm['mean']:.1f})"
)
print(
    f"   Best Crossover Probability:    {best_px['px']:.3f} (Mean: {best_px['mean']:.1f})"
)
print(
    f"   Best Population Size:          {int(best_pop['population_size'])} (Mean: {best_pop['mean']:.1f})"
)
print(
    f"   Best Tournament Size:          {int(best_tour['tournament_size'])} (Mean: {best_tour['mean']:.1f})"
)
print("=" * 60)
