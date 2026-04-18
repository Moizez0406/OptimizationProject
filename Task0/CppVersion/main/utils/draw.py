import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


try:
    plt.style.use("seaborn-v0-8-darkgrid")
except:
    try:
        plt.style.use("seaborn-darkgrid")
    except:
        plt.style.use("default")
        print("Note: Using default matplotlib style")

df = pd.read_csv("../results/Comparison_tai500_20_0.csv")

algorithms = ["random_search", "greedy", "simulated_annealing", "genetic_algorithm"]
algorithm_names = [
    "Random Search",
    "Greedy",
    "Simulated Annealing",
    "Genetic Algorithm",
]
colors = ["#96CEB4", "#9E4ECD", "#45B7D1", "#FF6B6B"]

means = {algo: df[algo].mean() for algo in algorithms}

UB = 26189
LB = 26922
fig, ax = plt.subplots(figsize=(14, 8))

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

for i, algo in enumerate(algorithms):
    mean_value = means[algo]
    ax.axhline(y=mean_value, color=colors[i], linestyle="--", linewidth=1.5, alpha=0.5)

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
ax.set_xticks(range(0, len(df), 2))
ax.set_xticklabels(range(0, len(df), 2))

ax.set_facecolor("#fafafa")

plt.tight_layout()
plt.show()
