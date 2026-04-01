import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import os

os.makedirs("figures", exist_ok=True)

# Read data
pm_summary = pd.read_csv("results/pm_summary.csv")
px_summary = pd.read_csv("results/px_summary.csv")
pop_summary = pd.read_csv("results/population_summary.csv")
tour_summary = pd.read_csv("results/tournament_summary.csv")

print("Creating radar chart for parameter importance...")

# Calculate range (max - min) for each parameter to see sensitivity
pm_range = pm_summary["max"].max() - pm_summary["min"].min()
px_range = px_summary["max"].max() - px_summary["min"].min()
pop_range = pop_summary["max"].max() - pop_summary["min"].min()
tour_range = tour_summary["max"].max() - tour_summary["min"].min()

# Print actual ranges for reference
print(f"\nParameter Ranges (Impact on Makespan):")
print(f"  Mutation Probability:     {pm_range:.1f}")
print(f"  Crossover Probability:    {px_range:.1f}")
print(f"  Population Size:          {pop_range:.1f}")
print(f"  Tournament Size:          {tour_range:.1f}")

# Normalize to 0-1 scale (higher = more impact)
max_range = max(pm_range, px_range, pop_range, tour_range)
sensitivities = {
    "Mutation\nProbability": pm_range / max_range,
    "Crossover\nProbability": px_range / max_range,
    "Population\nSize": pop_range / max_range,
    "Tournament\nSize": tour_range / max_range,
}

# Radar chart
categories = list(sensitivities.keys())
values = list(sensitivities.values())
N = len(categories)

# Compute angles for each category
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]  # Close the loop
values += values[:1]  # Close the loop

# Create the radar chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection="polar"))

# Plot the data
ax.plot(angles, values, "o-", linewidth=2, color="#2E86AB", markersize=8)
ax.fill(angles, values, alpha=0.25, color="#A3C4E8")

# Set category labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight="bold")

# Set y-axis limits and labels
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(["Low", "", "Medium", "", "High"], fontsize=9)

# Add grid
ax.grid(True, alpha=0.3)

# Add title
ax.set_title(
    "Parameter Sensitivity Analysis\n(Impact on Makespan)",
    fontsize=14,
    fontweight="bold",
    pad=20,
)

# Add a note about what the values mean
ax.text(
    0.5,
    -0.1,
    "Higher values indicate greater parameter influence on makespan",
    transform=ax.transAxes,
    fontsize=10,
    ha="center",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
)

plt.tight_layout()
plt.savefig("figures/radar_sensitivity.png", dpi=150, bbox_inches="tight")
plt.show()

# Print interpretation
print("\n" + "=" * 60)
print("INTERPRETATION:")
print("=" * 60)
print("The radar chart shows which parameters have the biggest impact on makespan.")
print("Higher values (closer to the outer edge) = More sensitive parameter.")
print("\nParameter Sensitivity Ranking (Highest to Lowest):")

# Sort parameters by sensitivity
sorted_params = sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)
for param, value in sorted_params:
    bar = "█" * int(value * 20)
    print(f"  {param.replace(chr(10), ' '):20} {bar:20} {value:.2%}")

print(f"\nMost sensitive parameter: {sorted_params[0][0].replace(chr(10), ' ')}")
print(f"Least sensitive parameter: {sorted_params[-1][0].replace(chr(10), ' ')}")
print("\n" + "=" * 60)
print("Radar chart saved to figures/radar_sensitivity.png")
print("=" * 60)
