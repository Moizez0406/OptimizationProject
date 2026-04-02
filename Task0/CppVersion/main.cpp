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

struct AlgorithmStats {
    std::string name;
    std::vector<int> makespans;
    double mean;
    double std_dev;
    double min;
    double max;
    double median;
    // double ci = mean -+ 1.96 * (std_dev / sqrt(RUNS))
};
AlgorithmStats compute_stats(const std::string& name,
                             const std::vector<int>& values) {
    AlgorithmStats stats;
    stats.name = name;
    stats.makespans = values;

    int n = values.size();

    stats.min = *std::min_element(values.begin(), values.end());
    stats.max = *std::max_element(values.begin(), values.end());

    double sum = 0;
    for (int val : values) {
        sum += val;
    }
    stats.mean = sum / n;

    double sq_sum = 0;
    for (int val : values) {
        sq_sum += (val - stats.mean) * (val - stats.mean);
    }
    stats.std_dev = std::sqrt(sq_sum / n);

    std::vector<int> sorted = values;
    std::sort(sorted.begin(), sorted.end());
    if (n % 2 == 0) {
        stats.median = (sorted[n / 2 - 1] + sorted[n / 2]) / 2.0;
    } else {
        stats.median = sorted[n / 2];
    }

    return stats;
}

int main() {
    std::string dataset = "tai20_10_0";

    std::string file_path = "../" + dataset + ".fsp";
    std::string results_dir = "results/";

    TaillardInstance inst = load_taillard(file_path.c_str());
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    system(("mkdir -p " + results_dir).c_str());

    const int RUNS = 20;
    unsigned int base_seed = 12345;

    // GA Parameters
    int population_size = 180;
    int generations = 100;
    int tournament_size = 2;
    double pm = 0.85;
    double px = 1;

    int ga_total_evaluations = population_size * generations;

    double initial_temp = 100.0;
    double cooling_rate = 0.95;
    int sa_iterations = ga_total_evaluations;
    int rs_iterations = ga_total_evaluations;
    int greedy_evaluation_budget = ga_total_evaluations;

    std::cout << "Dataset: " << dataset << "\n";
    std::cout << "Instance: " << inst.n_jobs << " jobs, " << inst.n_machines
              << " machines\n";
    std::cout << "Runs per algorithm: " << RUNS << "\n\n";

    std::vector<int> rs_results;
    std::vector<int> greedy_results;
    std::vector<int> sa_results;
    std::vector<int> ga_results;

    Subject_solution best_rs = base_sol.copy();
    Subject_solution best_greedy = base_sol.copy();
    Subject_solution best_sa = base_sol.copy();
    Subject_solution best_ga = base_sol.copy();

    // Use dataset name for all generated files
    std::string csv_filename = results_dir + dataset + "_comparison.csv";
    std::ofstream csvFile(csv_filename);
    csvFile
        << "run,random_search,greedy,simulated_annealing,genetic_algorithm\n";

    for (int run = 0; run < RUNS; run++) {
        unsigned int seed_rs = base_seed + run * 100 + 1;
        unsigned int seed_greedy = base_seed + run * 100 + 2;
        unsigned int seed_sa = base_seed + run * 100 + 3;
        unsigned int seed_ga = base_seed + run * 100 + 4;

        gen.seed(seed_rs);
        Subject_solution rs_sol = randomSearch(base_sol, rs_iterations);
        int rs_makespan = rs_sol.get_makespan();
        rs_results.push_back(rs_makespan);
        if (rs_makespan < best_rs.get_makespan()) {
            best_rs = rs_sol.copy();
        }

        gen.seed(seed_greedy);
        Subject_solution greedy_sol =
            greedy_with_budget(base_sol, greedy_evaluation_budget);
        int greedy_makespan = greedy_sol.get_makespan();
        greedy_results.push_back(greedy_makespan);
        if (greedy_makespan < best_greedy.get_makespan()) {
            best_greedy = greedy_sol.copy();
        }

        gen.seed(seed_sa);
        Subject_solution sa_sol = simulatedAnnealing(
            base_sol, initial_temp, cooling_rate, sa_iterations);
        int sa_makespan = sa_sol.get_makespan();
        sa_results.push_back(sa_makespan);
        if (sa_makespan < best_sa.get_makespan()) {
            best_sa = sa_sol.copy();
        }
        gen.seed(seed_ga);
        Subject_solution ga_sol = genetic(base_sol, population_size,
                                          generations, tournament_size, pm, px);
        int ga_makespan = ga_sol.get_makespan();
        ga_results.push_back(ga_makespan);
        if (ga_makespan < best_ga.get_makespan()) {
            best_ga = ga_sol.copy();
        }

        csvFile << run << "," << rs_makespan << "," << greedy_makespan << ","
                << sa_makespan << "," << ga_makespan << "\n";

        if ((run + 1) % 5 == 0) {
            std::cout << "Completed " << (run + 1) << " runs\n";
        }
    }

    csvFile.close();

    std::vector<AlgorithmStats> all_stats;
    all_stats.push_back(compute_stats("Random Search", rs_results));
    all_stats.push_back(compute_stats("Greedy (w/ budget)", greedy_results));
    all_stats.push_back(compute_stats("Simulated Annealing", sa_results));
    all_stats.push_back(compute_stats("Genetic Algorithm", ga_results));

    // Print summary table
    std::cout << "\n" << std::fixed << std::setprecision(1);
    std::cout << std::string(85, '=') << "\n";
    std::cout << std::left << std::setw(25) << "Algorithm" << std::right
              << std::setw(10) << "Mean" << std::setw(12) << "Std Dev"
              << std::setw(10) << "Min" << std::setw(10) << "Max"
              << std::setw(12) << "Median" << "\n";
    std::cout << std::string(85, '-') << "\n";

    for (const auto& stats : all_stats) {
        std::cout << std::left << std::setw(25) << stats.name << std::right
                  << std::setw(10) << stats.mean << std::setw(12)
                  << stats.std_dev << std::setw(10) << stats.min
                  << std::setw(10) << stats.max << std::setw(12) << stats.median
                  << "\n";
    }
    std::cout << std::string(85, '=') << "\n";

    // Save to file using dataset name
    std::string best_filename = results_dir + dataset + "_best_sequences.txt";
    std::ofstream bestFile(best_filename);
    bestFile << "=== BEST SOLUTIONS FOUND (Equal Evaluation Budget) ===\n\n";
    bestFile << "Dataset: " << dataset << "\n";
    bestFile << "File: " << file_path << "\n";
    bestFile << "Jobs: " << inst.n_jobs << ", Machines: " << inst.n_machines
             << "\n";
    bestFile << "UB: " << inst.UB << ", LB: " << inst.LB << "\n";
    bestFile << "Evaluation Budget: " << ga_total_evaluations
             << " per algorithm\n\n";
    bestFile << "Number of runs: " << RUNS << "\n\n";

    bestFile << "GA Configuration (Baseline):\n";
    bestFile << "  Population Size: " << population_size << "\n";
    bestFile << "  Generations: " << generations << "\n";
    bestFile << "  Tournament Size: " << tournament_size << "\n";
    bestFile << "  Mutation Probability (pm): " << pm << "\n";
    bestFile << "  Crossover Probability (px): " << px << "\n\n";

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

    for (const auto& stats : all_stats) {
        bestFile << stats.name << ":\n";
        bestFile << "  Mean: " << std::fixed << std::setprecision(1)
                 << stats.mean << "\n";
        bestFile << "  Std Dev: " << stats.std_dev << "\n";
        bestFile << "  Min: " << stats.min << "\n";
        bestFile << "  Max: " << stats.max << "\n";
        bestFile << "  Median: " << stats.median << "\n";
        bestFile << "\n";
    }

    bestFile.close();

    std::cout << "\nUB: " << inst.UB << std::endl;
    std::cout << "LB: " << inst.LB << std::endl;
    std::cout << "\nResults saved to:\n";
    std::cout << "  - " << csv_filename << " (Raw data)\n";
    std::cout << "  - " << best_filename
              << " (Best sequences and statistics)\n";

    return 0;
}
