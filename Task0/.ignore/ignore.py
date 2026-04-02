import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create figures directory
os.makedirs("figures", exist_ok=True)

# Try to set a nice style
try:
    plt.style.use('seaborn-v0-8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('default')
        print("Note: Using default matplotlib style")

# Read the data
df = pd.read_csv("results/ignore.csv")
summary = pd.read_csv("results/ignore_summary.csv")

# Fixed configuration parameters (from your optimal settings)
FIXED_CONFIG = {
    'Population Size': 400,
    'Generations': 100,
    'Tournament Size': 2,
    'Crossover Probability (px)': 1.0
}

print("=" * 80)
print("MUTATION PROBABILITY TEST RESULTS")
print("=" * 80)
print("\nFixed Configuration:")
for param, value in FIXED_CONFIG.items():
    print(f"  {param}: {value}")
print(f"\nRuns per configuration: {len(df) / len(df['pm'].unique()):.0f}")
print("\n" + "-" * 80)

# Display summary table
print("\n{:^10} {:^12} {:^10} {:^10} {:^10} {:^12} {:^20}".format(
    "pm", "Mean", "Std Dev", "Min", "Max", "Median", "95% CI"
))
print("-" * 80)

for _, row in summary.iterrows():
    print("{:^10.3f} {:^12.1f} {:^10.1f} {:^10.0f} {:^10.0f} {:^12.1f} [{:^8.1f}, {:^8.1f}]".format(
        row['pm'], row['mean'], row['std_dev'], row['min'], 
        row['max'], row['median'], row['ci_lower'], row['ci_upper']
    ))

# Find best pm
best_idx = summary['mean'].idxmin()
best_pm = summary.loc[best_idx, 'pm']
best_mean = summary.loc[best_idx, 'mean']
best_min = summary.loc[best_idx, 'min']

print("\n" + "-" * 80)
print(f"\n🎯 BEST MUTATION PROBABILITY: {best_pm:.3f}")
print(f"   Mean Makespan: {best_mean:.1f}")
print(f"   Best in {len(df) / len(df['pm'].unique()):.0f} runs: {best_min:.0f}")
print("=" * 80)

# ==================== CREATE PLOTS ====================

# 1. Error Bar Plot (Mean with Confidence Intervals)
fig, ax = plt.subplots(figsize=(12, 7))

ax.errorbar(summary['pm'], summary['mean'], 
             yerr=[summary['mean'] - summary['ci_lower'], 
                   summary['ci_upper'] - summary['mean']],
             fmt='o-', capsize=5, capthick=2, elinewidth=2, 
             markersize=8, color='#2E86AB', ecolor='gray', 
             label='Mean ± 95% CI')

# Add standard deviation band
ax.fill_between(summary['pm'], 
                 summary['mean'] - summary['std_dev'],
                 summary['mean'] + summary['std_dev'],
                 alpha=0.2, color='#A3C4E8', 
                 label='±1 Std Dev')

ax.set_xlabel('Mutation Probability (pm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Makespan', fontsize=12, fontweight='bold')
ax.set_title('Mutation Probability Effect on GA Performance\n(Fixed: Pop=400, Gen=100, Tour=2, Px=1.0)', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right')

# Mark best point
ax.scatter(best_pm, best_mean, s=200, c='gold', edgecolors='black', 
           zorder=5, marker='*', label=f'Best: pm={best_pm:.3f}')
ax.annotate(f'Optimal: pm={best_pm:.3f}\nMean={best_mean:.1f}', 
             xy=(best_pm, best_mean), xytext=(10, 10),
             textcoords='offset points', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# Add fixed parameters text box
fixed_text = "Fixed Parameters:\n" + "\n".join([f"{k}: {v}" for k, v in FIXED_CONFIG.items()])
ax.text(0.02, 0.98, fixed_text, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('figures/pm_test_errorbar.png', dpi=150, bbox_inches='tight')
plt.show()

# 2. Box Plot (Distribution of results)
fig, ax = plt.subplots(figsize=(14, 7))

# Prepare data for box plot
pm_values = sorted(df['pm'].unique())
box_data = [df[df['pm'] == pm]['makespan'].values for pm in pm_values]
pm_labels = [f'{pm:.2f}' for pm in pm_values]

bp = ax.boxplot(box_data, labels=pm_labels, patch_artist=True,
                medianprops=dict(color='red', linewidth=2),
                whiskerprops=dict(color='gray'),
                capprops=dict(color='gray'))

# Color the boxes with gradient
for i, box in enumerate(bp['boxes']):
    box.set_facecolor(plt.cm.Blues(0.3 + i * 0.06))
    box.set_alpha(0.7)

ax.set_xlabel('Mutation Probability (pm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Makespan', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Results by Mutation Probability\n(Fixed: Pop=400, Gen=100, Tour=2, Px=1.0)', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha='right')

# Add fixed parameters text box
ax.text(0.02, 0.98, fixed_text, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('figures/pm_test_boxplot.png', dpi=150, bbox_inches='tight')
plt.show()

# 3. Line Plot (Run-by-run comparison)
fig, ax = plt.subplots(figsize=(14, 8))

# Plot each run as a line
for pm in pm_values:
    pm_data = df[df['pm'] == pm]
    ax.plot(pm_data['run'], pm_data['makespan'], 'o-', 
            label=f'pm={pm:.2f}', linewidth=1.5, markersize=4, alpha=0.7)

ax.set_xlabel('Run Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Makespan', fontsize=12, fontweight='bold')
ax.set_title('Run-by-Run Performance for Different Mutation Probabilities\n(Fixed: Pop=400, Gen=100, Tour=2, Px=1.0)', 
             fontsize=14, fontweight='bold')
ax.legend(loc='upper right', ncol=2, fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xticks(range(0, len(df) / len(pm_values), 2))

plt.tight_layout()
plt.savefig('figures/pm_test_runbyrun.png', dpi=150, bbox_inches='tight')
plt.show()

# 4. Summary Bar Chart
fig, ax = plt.subplots(figsize=(12, 7))

x_pos = np.arange(len(pm_values))
bars = ax.bar(x_pos, summary['mean'], yerr=summary['std_dev'], 
              capsize=5, color='#2E86AB', alpha=0.7, edgecolor='black',
              label='Mean ± Std Dev')

# Add value labels on top of bars
for i, (bar, row) in enumerate(zip(bars, summary.iterrows())):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + row[1]['std_dev'] + 5,
            f'{row[1]["mean"]:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels([f'{pm:.2f}' for pm in pm_values], rotation=45, ha='right')
ax.set_xlabel('Mutation Probability (pm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Makespan', fontsize=12, fontweight='bold')
ax.set_title('Mean Makespan by Mutation Probability\n(Fixed: Pop=400, Gen=100, Tour=2, Px=1.0)', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
ax.legend()

plt.tight_layout()
plt.savefig('figures/pm_test_barchart.png', dpi=150, bbox_inches='tight')
plt.show()

# Print summary of findings
print("\n" + "=" * 80)
print("ANALYSIS SUMMARY")
print("=" * 80)

print("\n📈 Performance Trend:")
if best_pm == summary['pm'].iloc[0]:
    print("   Best performance at lowest pm value (0.50)")
elif best_pm == summary['pm'].iloc[-1]:
    print("   Best performance at highest pm value (1.00)")
else:
    print(f"   Best performance at pm = {best_pm:.3f}")

print("\n📊 Stability Analysis:")
for _, row in summary.iterrows():
    if row['pm'] == best_pm:
        print(f"   At pm={row['pm']:.3f}:")
        print(f"     - Std Dev: {row['std_dev']:.1f} (Lower is more stable)")
        print(f"     - Range: [{row['min']:.0f}, {row['max']:.0f}]")

print("\n" + "=" * 80)
print("Figures saved to figures/ directory:")
print("  - pm_test_errorbar.png (Mean with confidence intervals)")
print("  - pm_test_boxplot.png (Distribution box plot)")
print("  - pm_test_runbyrun.png (Run-by-run comparison)")
print("  - pm_test_barchart.png (Bar chart with error bars)")
print("=" * 80)
