import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("ga_pm_results.csv")

# Optional: prettier labels (use ONE consistently)
df["pm_label"] = df["pm"].apply(lambda x: f"{x}")

plt.figure(figsize=(12, 6))

# Boxplot with colors
sns.boxplot(
    x="pm_label",
    y="Makespan",
    data=df,
    palette="Set2",  # 🎨 colors per box
    showmeans=True,
    meanprops={"marker": "^", "markerfacecolor": "black", "markeredgecolor": "black"},
)

# Overlay points (aligned now)
sns.stripplot(
    x="pm_label", y="Makespan", data=df, color="black", alpha=0.5, jitter=True
)

plt.title("Effect of Mutation Probability on Makespan")
plt.xlabel("Mutation Probability (pm)")
plt.ylabel("Makespan")

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
