import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sns.set(style="whitegrid")

rose_white_cmap = LinearSegmentedColormap.from_list(
    "rose_white",
    [
        "#a50f15",  # Dark rose-red (low values)
        "#f7685c",  # Medium rose-red
        "#fff5f0",
    ],  # Very light cream/white (high values)
)

rose_cream_cmap = LinearSegmentedColormap.from_list(
    "rose_cream",
    [
        "#d7301f",  # Deep rose-red
        "#fcbba1",  # Soft peach
        "#fffaf0",
    ],  # Floral white/cream
)

default_cmap = rose_white_cmap

df = pd.read_csv("ga_param_study.csv")


def filter_data(df, fixed_params):
    filtered = df.copy()
    for key, value in fixed_params.items():
        filtered = filtered[filtered[key] == value]
    return filtered


def plot_single_param(df, param, fixed_params={}):
    data = filter_data(df, fixed_params)

    stats = data.groupby(param)["Makespan"].agg(["mean", "std"]).reset_index()

    plt.figure()
    sns.lineplot(data=stats, x=param, y="mean", marker="o", color="#d7301f")

    plt.fill_between(
        stats[param],
        stats["mean"] - stats["std"],
        stats["mean"] + stats["std"],
        alpha=0.2,
        color="#fcbba1",
    )

    title_fixed = ", ".join([f"{k}={v}" for k, v in fixed_params.items()])
    plt.title(f"{param} influence\n({title_fixed})")

    plt.ylabel("Average Makespan")
    plt.xlabel(param)

    plt.tight_layout()
    plt.show()


def plot_heatmap(df, param1, param2, fixed_params={}, cmap=None, center=None):
    data = filter_data(df, fixed_params)

    if cmap is None:
        cmap = default_cmap

    pivot = data.pivot_table(
        values="Makespan", index=param1, columns=param2, aggfunc="mean"
    )

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        cmap=cmap,
        cbar_kws={"label": "Makespan", "shrink": 0.8},
        center=center,
    )

    title_fixed = ", ".join([f"{k}={v}" for k, v in fixed_params.items()])
    plt.title(f"{param1} vs {param2}\n({title_fixed})", fontsize=12, pad=20)

    plt.tight_layout()
    plt.show()


plot_single_param(
    df,
    param="Population",
    fixed_params={"Generations": 100, "Tournament": 5, "Mutation": 0.1},
)

plot_single_param(
    df,
    param="Mutation",
    fixed_params={"Population": 180, "Generations": 100, "Tournament": 5},
)

plot_heatmap(
    df,
    param1="Tournament",
    param2="Mutation",
    fixed_params={"Population": 180, "Generations": 100},
)

plot_heatmap(
    df,
    param1="Population",
    param2="Mutation",
    fixed_params={"Generations": 100, "Tournament": 5},
    cmap=rose_cream_cmap,
)

