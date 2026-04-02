import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the convergence data
df = pd.read_csv("convergence_ga20.csv")

# Create the convergence plot
plt.figure(figsize=(12, 8))

# Plot the three lines
plt.plot(df["generation"], df["best_makespan"], 
         label="Best", linewidth=2, color='green')
plt.plot(df["generation"], df["avg_makespan"], 
         label="Average", linewidth=1.5, color='blue')
plt.plot(df["generation"], df["worst_makespan"], 
         label="Worst", linewidth=1, color='red', alpha=0.7)

# Add confidence interval (optional)
# This shows the spread between best and worst
plt.fill_between(df["generation"], 
                 df["best_makespan"], 
                 df["worst_makespan"], 
                 alpha=0.2, color='gray', label='Spread')

# Customize the plot
plt.xlabel("Generation", fontsize=12)
plt.ylabel("Makespan", fontsize=12)
plt.title("Genetic Algorithm Convergence", fontsize=14, fontweight='bold')
plt.legend(loc='upper right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Add a small table with final statistics
final_best = df["best_makespan"].iloc[-1]
final_avg = df["avg_makespan"].iloc[-1]
final_worst = df["worst_makespan"].iloc[-1]
initial_best = df["best_makespan"].iloc[0]
improvement = initial_best - final_best

stats_text = f"Final Best: {final_best}\nFinal Avg: {final_avg:.1f}\nImprovement: {improvement}"
plt.annotate(stats_text, xy=(0.02, 0.98), xycoords='axes fraction', 
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Save the figure
plt.savefig("convergence_ga.png", dpi=150, bbox_inches='tight')
plt.show()

# Print summary statistics
print("\n=== Convergence Analysis ===")
print(f"Initial Best: {initial_best}")
print(f"Final Best: {final_best}")
print(f"Improvement: {improvement} ({improvement/initial_best*100:.1f}%)")
print(f"\nBest Generation: {df['best_makespan'].idxmin()}")
print(f"Best Makespan: {df['best_makespan'].min()}")
print(f"\nFinal Average Makespan: {final_avg:.1f}")
print(f"Final Worst Makespan: {final_worst}")

# Optional: Create a second plot showing the improvement rate
plt.figure(figsize=(12, 5))
improvement_rate = df["best_makespan"].pct_change().abs() * 100
plt.plot(df["generation"][1:], improvement_rate[1:], 
         label="Improvement Rate (%)", color='orange')
plt.xlabel("Generation", fontsize=12)
plt.ylabel("Improvement Rate (%)", fontsize=12)
plt.title("GA Convergence Rate", fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("convergence_rate.png", dpi=150, bbox_inches='tight')
plt.show()
