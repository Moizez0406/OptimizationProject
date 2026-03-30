import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('convergence.csv')

# Create the plot
plt.figure(figsize=(10, 6))

plt.plot(df['Generation'], df['Best'], label='Best Fitness', color='green', linewidth=2)
plt.plot(df['Generation'], df['Avg'], label='Average Fitness', color='blue', linestyle='--')
plt.plot(df['Generation'], df['Worst'], label='Worst Fitness', color='red', alpha=0.5)

# Formatting
plt.title('Genetic Algorithm Convergence')
plt.xlabel('Generation')
plt.ylabel('Fitness Value')
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)

# Show plot
plt.tight_layout()
plt.show()
