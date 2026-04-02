import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create figures directory
os.makedirs("figures", exist_ok=True)

# Try to set a nice style
try:
    plt.style.use("seaborn-v0-8-darkgrid")
except:
    try:
        plt.style.use("seaborn-darkgrid")
    except:
        plt.style.use("default")
        print("Note: Using default matplotlib style")

# Read the data
df = pd.read_csv("results/tai20_5_0_comparison.csv")

# Define algorithms and their colors
algorithms = ["random_search", "greedy", "simulated_annealing", "genetic_algorithm"]
algorithm_names = [
    "Random Search",
    "Greedy",
    "Simulated Annealing",
    "Genetic Algorithm",
]
colors = ["#96CEB4", "#9E4ECD", "#45B7D1", "#FF6B6B"]

# Calculate mean values for each algorithm
means = {algo: df[algo].mean() for algo in algorithms}

# Define bounds
UB = 1278
LB = 1232

# Create the line plot
fig, ax = plt.subplots(figsize=(14, 8))

# Plot each algorithm's run-by-run performance
for i, algo in enumerate(algorithms):
    ax.plot(
        df.index,
        df[algo],
        "o-",
        label=f"{algorithm_names[i]} (Mean: {means[algo]:.0f})",
        color=colors[i],
        linewidth=2,
        markersize=6,
        alpha=0.8,
        markerfacecolor="white",
        markeredgewidth=1.5,
    )

# Add horizontal lines for the mean of each algorithm
for i, algo in enumerate(algorithms):
    mean_value = means[algo]
    ax.axhline(y=mean_value, color=colors[i], linestyle="--", linewidth=1.5, alpha=0.5)

# Add Upper Bound and Lower Bound lines
ax.axhline(
    y=UB,
    color="green",
    linestyle=":",
    linewidth=2,
    label=f"Upper Bound (UB): {UB}",
    alpha=0.8,
)
ax.axhline(
    y=LB,
    color="green",
    linestyle=":",
    linewidth=2,
    label=f"Lower Bound (LB): {LB}",
    alpha=0.8,
)

ax.set_xlabel("Run Number", fontsize=12, fontweight="bold")
ax.set_ylabel("Makespan", fontsize=12, fontweight="bold")
ax.set_title(
    "Algorithm Performance Comparison Across 20 Runs", fontsize=14, fontweight="bold"
)
ax.legend(
    loc="upper right",
    fontsize=10,
    framealpha=0.95,
    fancybox=True,
    shadow=True,
    borderpad=1,
)
ax.grid(True, alpha=0.3)
ax.set_xticks(range(0, len(df), 2))  # Show every 2nd run
ax.set_xticklabels(range(0, len(df), 2))

# Add a light background for better readability
ax.set_facecolor("#fafafa")

plt.tight_layout()
plt.show()
