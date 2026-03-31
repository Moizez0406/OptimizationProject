import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")


# =========================
# Load data
# =========================
df = pd.read_csv("ga_param_study.csv")


# =========================
# Filtering function
# =========================
def filter_data(df, fixed_params):
    filtered = df.copy()
    for key, value in fixed_params.items():
        filtered = filtered[filtered[key] == value]
    return filtered


# =========================
# 1️⃣ Single parameter plot
# =========================
def plot_single_param(df, param, fixed_params={}):
    data = filter_data(df, fixed_params)

    stats = data.groupby(param)["Makespan"].agg(["mean", "std"]).reset_index()

    plt.figure()
    sns.lineplot(data=stats, x=param, y="mean", marker="o")

    plt.fill_between(
        stats[param],
        stats["mean"] - stats["std"],
        stats["mean"] + stats["std"],
        alpha=0.2,
    )

    title_fixed = ", ".join([f"{k}={v}" for k, v in fixed_params.items()])
    plt.title(f"{param} influence\n({title_fixed})")

    plt.ylabel("Average Makespan")
    plt.xlabel(param)

    plt.tight_layout()
    plt.show()


# =========================
# 2️⃣ Heatmap (2 params)
# =========================
def plot_heatmap(df, param1, param2, fixed_params={}):
    data = filter_data(df, fixed_params)

    pivot = data.pivot_table(
        values="Makespan", index=param1, columns=param2, aggfunc="mean"
    )

    plt.figure()
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="viridis")

    title_fixed = ", ".join([f"{k}={v}" for k, v in fixed_params.items()])
    plt.title(f"{param1} vs {param2}\n({title_fixed})")

    plt.tight_layout()
    plt.show()


# =========================
# ✅ EXAMPLES
# =========================

# --- 1️⃣ Population influence (others fixed)
plot_single_param(
    df,
    param="Population",
    fixed_params={"Generations": 100, "Tournament": 5, "Mutation": 0.1},
)

# --- 2️⃣ Mutation influence
plot_single_param(
    df,
    param="Mutation",
    fixed_params={"Population": 180, "Generations": 100, "Tournament": 5},
)

# --- 3️⃣ Interaction: Population vs Mutation
plot_heatmap(
    df,
    param1="Population",
    param2="Mutation",
    fixed_params={"Generations": 100, "Tournament": 5},
)

# --- 4️⃣ Interaction: Tournament vs Mutation
plot_heatmap(
    df,
    param1="Tournament",
    param2="Mutation",
    fixed_params={"Population": 180, "Generations": 100},
)
