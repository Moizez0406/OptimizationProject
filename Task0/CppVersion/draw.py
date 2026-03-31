import matplotlib.pyplot as plt
import csv
from collections import defaultdict

data = defaultdict(list)
with open("results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[row["Algorithm"]].append(int(row["Makespan"]))

fig, ax = plt.subplots(figsize=(10, 6))

colors = {"RS": "blue", "SA": "orange", "GA": "green", "GR": "red"}
labels = {
    "RS": "Random Search",
    "SA": "Simulated Annealing",
    "GA": "Genetic Algorithm",
    "GR": "Greedy",
}

for algo, makespans in data.items():
    runs = list(range(1, len(makespans) + 1))
    avg = sum(makespans) / len(makespans)

    # plot run values
    ax.plot(runs, makespans,
            label=f"{labels[algo]} (avg={avg:.0f})",
            color=colors[algo],
            marker="o",
            markersize=4)

    # plot average as dashed line
    ax.axhline(y=avg,
               color=colors[algo],
               linestyle="--",
               alpha=0.5)

# UB and LB reference lines
ax.axhline(y=2297, color="black", linestyle=":", linewidth=1.5, label="UB=2297")
ax.axhline(y=1911, color="gray",  linestyle=":", linewidth=1.5, label="LB=1911")

ax.set_xlabel("Run")
ax.set_ylabel("Makespan")
ax.set_title("Algorithm Performance Across 20 Runs (tai200_20_0)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("performance_comparison.png")
plt.show()
