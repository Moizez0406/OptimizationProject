import matplotlib.pyplot as plt
import csv

generations, best, worst, avg = [], [], [], []
with open("convergence.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        generations.append(int(row["Generation"]))
        best.append(int(row["Best"]))
        worst.append(int(row["Worst"]))
        avg.append(float(row["Avg"]))


def rolling_avg(data, window=10):
    result = []
    for i in range(len(data)):
        start = max(0, i - window + 1)
        result.append(sum(data[start : i + 1]) / (i - start + 1))
    return result


# running best — never goes up
running_best = float("inf")
smooth_best = []
for b in best:
    running_best = min(running_best, b)
    smooth_best.append(running_best)

fig, ax = plt.subplots(figsize=(10, 6))

# plot only once each
ax.plot(generations, smooth_best, label="Best", color="blue")
ax.plot(generations, rolling_avg(avg, 10), label="Average", color="green")
ax.plot(generations, rolling_avg(worst, 10), label="Worst", color="orange")

ax.set_xlabel("Generation")
ax.set_ylabel("Makespan")
ax.set_title("GA Convergence (tai500_20_0)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("convergence.png")
plt.show()
