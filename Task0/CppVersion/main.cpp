#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

#include "Subject_solution.h"
#include "algo.h"
#include "load.h"

// Structure to store statistics for each algorithm
struct AlgorithmStats {
    std::string name;
    std::vector<int> makespans;
    double mean;
    double std_dev;
    double min;
    double max;
    double median;
    double ci_lower;
    double ci_upper;
};

// Function to compute statistics
AlgorithmStats compute_stats(const std::string& name,
                             const std::vector<int>& values) {
    AlgorithmStats stats;
    stats.name = name;
    stats.makespans = values;

    int n = values.size();

    // Basic statistics
    stats.min = *std::min_element(values.begin(), values.end());
    stats.max = *std::max_element(values.begin(), values.end());

    double sum = 0;
    for (int val : values) {
        sum += val;
    }
    stats.mean = sum / n;

    // Standard deviation
    double sq_sum = 0;
    for (int val : values) {
        sq_sum += (val - stats.mean) * (val - stats.mean);
    }
    stats.std_dev = std::sqrt(sq_sum / n);

    // Median
    std::vector<int> sorted = values;
    std::sort(sorted.begin(), sorted.end());
    if (n % 2 == 0) {
        stats.median = (sorted[n / 2 - 1] + sorted[n / 2]) / 2.0;
    } else {
        stats.median = sorted[n / 2];
    }

    // 95% confidence interval
    double standard_error = stats.std_dev / std::sqrt(n);
    stats.ci_lower = stats.mean - 1.96 * standard_error;
    stats.ci_upper = stats.mean + 1.96 * standard_error;

    return stats;
}

int main() {
    // Create results directory
    system("mkdir -p results");

    // Load the instance
    TaillardInstance inst = load_taillard("../tai500_20_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    // Experiment parameters
    const int RUNS = 20;
    unsigned int base_seed = 12345;

    // GA Parameters (optimized from sensitivity analysis)
    int population_size = 250;
    int generations = 100;
    int tournament_size = 5;
    double pm = 0.20;
    double px = 0.90;

    // SA Parameters
    double initial_temp = 100.0;
    double cooling_rate = 0.95;
    int sa_iterations = 10000;

    // RS Parameters
    int rs_iterations = 10000;

    // Vectors to store results for each algorithm
    std::vector<int> rs_results;
    std::vector<int> greedy_results;
    std::vector<int> sa_results;
    std::vector<int> ga_results;

    // Store best solutions
    Subject_solution best_rs = base_sol.copy();
    Subject_solution best_greedy = base_sol.copy();
    Subject_solution best_sa = base_sol.copy();
    Subject_solution best_ga = base_sol.copy();

    // Open CSV file for detailed results
    std::ofstream csvFile("results/algorithm_comparison.csv");
    csvFile
        << "run,random_search,greedy,simulated_annealing,genetic_algorithm\n";

    // Run experiments
    for (int run = 0; run < RUNS; run++) {
        // Create unique seeds for each algorithm in this run
        unsigned int seed_rs = base_seed + run * 100 + 1;
        unsigned int seed_greedy = base_seed + run * 100 + 2;
        unsigned int seed_sa = base_seed + run * 100 + 3;
        unsigned int seed_ga = base_seed + run * 100 + 4;

        // Run Random Search
        gen.seed(seed_rs);
        Subject_solution rs_sol = randomSearch(base_sol, rs_iterations);
        int rs_makespan = rs_sol.get_makespan();
        rs_results.push_back(rs_makespan);
        if (rs_makespan < best_rs.get_makespan()) {
            best_rs = rs_sol.copy();
        }

        // Run Greedy
        gen.seed(seed_greedy);
        Subject_solution greedy_sol = greedy(base_sol);
        int greedy_makespan = greedy_sol.get_makespan();
        greedy_results.push_back(greedy_makespan);
        if (greedy_makespan < best_greedy.get_makespan()) {
            best_greedy = greedy_sol.copy();
        }

        // Run Simulated Annealing
        gen.seed(seed_sa);
        Subject_solution sa_sol = simulatedAnnealing(
            base_sol, initial_temp, cooling_rate, sa_iterations);
        int sa_makespan = sa_sol.get_makespan();
        sa_results.push_back(sa_makespan);
        if (sa_makespan < best_sa.get_makespan()) {
            best_sa = sa_sol.copy();
        }

        // Run Genetic Algorithm
        gen.seed(seed_ga);
        Subject_solution ga_sol = genetic(base_sol, population_size,
                                          generations, tournament_size, pm, px);
        int ga_makespan = ga_sol.get_makespan();
        ga_results.push_back(ga_makespan);
        if (ga_makespan < best_ga.get_makespan()) {
            best_ga = ga_sol.copy();
        }

        // Write to CSV
        csvFile << run << "," << rs_makespan << "," << greedy_makespan << ","
                << sa_makespan << "," << ga_makespan << "\n";
    }

    csvFile.close();

    // Compute statistics for each algorithm
    std::vector<AlgorithmStats> all_stats;
    all_stats.push_back(compute_stats("Random Search", rs_results));
    all_stats.push_back(compute_stats("Greedy", greedy_results));
    all_stats.push_back(compute_stats("Simulated Annealing", sa_results));
    all_stats.push_back(compute_stats("Genetic Algorithm", ga_results));

    // Print summary table only
    std::cout << std::fixed << std::setprecision(1);
    std::cout << std::string(100, '=') << "\n";
    std::cout << std::left << std::setw(20) << "Algorithm" << std::right
              << std::setw(10) << "Mean" << std::setw(12) << "Std Dev"
              << std::setw(10) << "Min" << std::setw(10) << "Max"
              << std::setw(12) << "Median" << std::setw(20) << "95% CI"
              << "\n";
    std::cout << std::string(100, '-') << "\n";

    for (const auto& stats : all_stats) {
        std::cout << std::left << std::setw(20) << stats.name << std::right
                  << std::setw(10) << stats.mean << std::setw(12)
                  << stats.std_dev << std::setw(10) << stats.min
                  << std::setw(10) << stats.max << std::setw(12) << stats.median
                  << std::setw(8) << "[" << stats.ci_lower << ", "
                  << stats.ci_upper << "]"
                  << "\n";
    }
    std::cout << std::string(100, '=') << "\n";

    // Save best sequences to file
    std::ofstream bestFile("results/best_sequences(T500-20).txt");
    bestFile << "=== BEST SOLUTIONS FOUND ===\n\n";
    bestFile << "Instance: taiX_X_X.fsp\n";
    bestFile << "Jobs: " << inst.n_jobs << ", Machines: " << inst.n_machines
             << "\n";
    bestFile << "UB: " << inst.UB << ", LB: " << inst.LB << "\n\n";

    bestFile << "Random Search (Makespan: " << best_rs.get_makespan() << "):\n";
    bestFile << "Sequence: ";
    for (int id : best_rs.get_ids()) {
        bestFile << id << " ";
    }
    bestFile << "\n\n";

    bestFile << "Greedy (Makespan: " << best_greedy.get_makespan() << "):\n";
    bestFile << "Sequence: ";
    for (int id : best_greedy.get_ids()) {
        bestFile << id << " ";
    }
    bestFile << "\n\n";

    bestFile << "Simulated Annealing (Makespan: " << best_sa.get_makespan()
             << "):\n";
    bestFile << "Sequence: ";
    for (int id : best_sa.get_ids()) {
        bestFile << id << " ";
    }
    bestFile << "\n\n";

    bestFile << "Genetic Algorithm (Makespan: " << best_ga.get_makespan()
             << "):\n";
    bestFile << "Sequence: ";
    for (int id : best_ga.get_ids()) {
        bestFile << id << " ";
    }
    bestFile << "\n\n";

    bestFile << "=== STATISTICS SUMMARY ===\n\n";
    for (const auto& stats : all_stats) {
        bestFile << stats.name << ":\n";
        bestFile << "  Mean: " << std::fixed << std::setprecision(1)
                 << stats.mean << "\n";
        bestFile << "  Std Dev: " << stats.std_dev << "\n";
        bestFile << "  Min: " << stats.min << "\n";
        bestFile << "  Max: " << stats.max << "\n";
        bestFile << "  Median: " << stats.median << "\n";
        bestFile << "  95% CI: [" << stats.ci_lower << ", " << stats.ci_upper
                 << "]\n\n";
    }

    bestFile.close();
    std::cout << "UB: " << inst.UB << std::endl;
    std::cout << "LB: " << inst.LB << std::endl;
    std::cout << "\nResults saved to:\n";
    std::cout << "  - results/algorithm_comparison.csv (Raw data)\n";
    std::cout
        << "  - results/best_sequences(T500-20-0).txt (Best sequences and "
           "statistics)\n";

    return 0;
}