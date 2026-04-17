#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

#include "../include/Subject_solution.h"
#include "../include/algo.h"
#include "../include/load.h"

int run_ga_with_seed(const Subject_solution& base_sol, int population_size,
                     int generations, int tournament_size, double pm, double px,
                     unsigned int seed) {
    gen.seed(seed);
    Subject_solution sol = base_sol.copy();
    Subject_solution result =
        genetic(sol, population_size, generations, tournament_size, pm, px);
    return result.get_makespan();
}

struct Statistics {
    double mean, std_dev, min, max, median, ci_lower, ci_upper;
};

Statistics compute_statistics(const std::vector<int>& values) {
    Statistics stats;
    int n = values.size();
    stats.min = *std::min_element(values.begin(), values.end());
    stats.max = *std::max_element(values.begin(), values.end());
    double sum = 0;
    for (int val : values)
        sum += val;
    stats.mean = sum / n;
    double sq_sum = 0;
    for (int val : values)
        sq_sum += (val - stats.mean) * (val - stats.mean);
    stats.std_dev = std::sqrt(sq_sum / n);
    std::vector<int> sorted = values;
    std::sort(sorted.begin(), sorted.end());
    stats.median = (n % 2 == 0) ? (sorted[n / 2 - 1] + sorted[n / 2]) / 2.0
                                : sorted[n / 2];
    double se = stats.std_dev / std::sqrt(n);
    stats.ci_lower = stats.mean - 1.96 * se;
    stats.ci_upper = stats.mean + 1.96 * se;
    return stats;
}

int main() {
    std::string instance_path = "tai500_20_0";
    TaillardInstance inst = load_taillard("../../" + instance_path + ".fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    const int RUNS_PER_CONFIG = 20;
    const int POPULATION_SIZE = 360;
    const int GENERATIONS = 50;
    const int TOURNAMENT_SIZE = 5;
    const double FIXED_PX = 1;
    const double FIXED_PM = 0.85;
    const int EVAL_BUDGET = POPULATION_SIZE * GENERATIONS; // 18,000
    const unsigned int base_seed = 12345;

    const std::string results_dir = "../main/results/";

    std::cout << "========================================\n";
    std::cout << "GA Parameter Sensitivity Analysis\n";
    std::cout << "========================================\n";
    std::cout << "Instance: " << inst.n_jobs << " jobs, " << inst.n_machines
              << " machines\n";
    std::cout << "Defaults: pop=" << POPULATION_SIZE << ", gens=" << GENERATIONS
              << ", ts=" << TOURNAMENT_SIZE << ", px=" << FIXED_PX
              << ", pm=" << FIXED_PM << "\n";
    std::cout << "Runs per configuration: " << RUNS_PER_CONFIG << "\n\n";
    std::cout << std::fixed << std::setprecision(3);

    // ── 1. Mutation probability (pm) ─────────────────────────────────────────
    std::cout << "Testing Mutation Probability (pm)...\n";
    std::vector<double> pm_values = {0.01, 0.05, 0.10, 0.15,
                                     0.20, 0.30, 0.40, 0.50};

    std::ofstream pmRaw(results_dir + "pm_raw_" + instance_path + ".csv");
    pmRaw << "pm,run,makespan\n";
    std::ofstream pmSummary(results_dir + "pm_summary_" + instance_path +
                            ".csv");
    pmSummary << "pm,runs,mean,std_dev,min,max,median,ci_lower,ci_upper\n";

    for (double pm : pm_values) {
        std::vector<int> makespans;
        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed =
                base_seed + run * 100 + static_cast<int>(pm * 1000);
            int makespan =
                run_ga_with_seed(base_sol, POPULATION_SIZE, GENERATIONS,
                                 TOURNAMENT_SIZE, pm, FIXED_PX, seed);
            makespans.push_back(makespan);
            pmRaw << pm << "," << run << "," << makespan << "\n";
        }
        Statistics stats = compute_statistics(makespans);
        pmSummary << pm << "," << RUNS_PER_CONFIG << "," << stats.mean << ","
                  << stats.std_dev << "," << stats.min << "," << stats.max
                  << "," << stats.median << "," << stats.ci_lower << ","
                  << stats.ci_upper << "\n";
        std::cout << "  pm = " << std::setw(5) << pm
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }
    pmRaw.close();
    pmSummary.close();

    // ── 2. Crossover probability (px) ────────────────────────────────────────
    std::cout << "\nTesting Crossover Probability (px)...\n";
    std::vector<double> px_values = {0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0};

    std::ofstream pxRaw(results_dir + "px_raw_" + instance_path + ".csv");
    pxRaw << "px,run,makespan\n";
    std::ofstream pxSummary(results_dir + "px_summary_" + instance_path +
                            ".csv");
    pxSummary << "px,runs,mean,std_dev,min,max,median,ci_lower,ci_upper\n";

    for (double px : px_values) {
        std::vector<int> makespans;
        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed =
                base_seed + run * 100 + static_cast<int>(px * 1000);
            int makespan =
                run_ga_with_seed(base_sol, POPULATION_SIZE, GENERATIONS,
                                 TOURNAMENT_SIZE, FIXED_PM, px, seed);
            makespans.push_back(makespan);
            pxRaw << px << "," << run << "," << makespan << "\n";
        }
        Statistics stats = compute_statistics(makespans);
        pxSummary << px << "," << RUNS_PER_CONFIG << "," << stats.mean << ","
                  << stats.std_dev << "," << stats.min << "," << stats.max
                  << "," << stats.median << "," << stats.ci_lower << ","
                  << stats.ci_upper << "\n";
        std::cout << "  px = " << std::setw(5) << px
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }
    pxRaw.close();
    pxSummary.close();

    // ── 3. Population size (generations scaled, fixed eval budget) ───────────
    std::cout << "\nTesting Population Size (fixed eval budget = "
              << EVAL_BUDGET << ")...\n";
    std::vector<int> pop_sizes = {45, 90, 180, 360};

    std::ofstream popRaw(results_dir + "population_raw_" + instance_path +
                         ".csv");
    popRaw << "population_size,generations,run,makespan\n";
    std::ofstream popSummary(results_dir + "population_summary_" +
                             instance_path + ".csv");
    popSummary << "population_size,generations,runs,mean,std_dev,min,max,"
                  "median,ci_lower,ci_upper\n";

    for (int pop_size : pop_sizes) {
        int scaled_gens = EVAL_BUDGET / pop_size;
        std::vector<int> makespans;
        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed = base_seed + run * 100 + pop_size;
            gen.seed(seed);
            Subject_solution sol = base_sol.copy();
            Subject_solution result =
                genetic(sol, pop_size, scaled_gens, TOURNAMENT_SIZE, FIXED_PM,
                        FIXED_PX);
            makespans.push_back(result.get_makespan());
            popRaw << pop_size << "," << scaled_gens << "," << run << ","
                   << result.get_makespan() << "\n";
        }
        Statistics stats = compute_statistics(makespans);
        popSummary << pop_size << "," << scaled_gens << "," << RUNS_PER_CONFIG
                   << "," << stats.mean << "," << stats.std_dev << ","
                   << stats.min << "," << stats.max << "," << stats.median
                   << "," << stats.ci_lower << "," << stats.ci_upper << "\n";
        std::cout << "  Pop = " << std::setw(4) << pop_size
                  << " | Gens = " << std::setw(4) << scaled_gens
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }
    popRaw.close();
    popSummary.close();

    // ── 4. Tournament size ───────────────────────────────────────────────────
    std::cout << "\nTesting Tournament Size...\n";
    std::vector<int> tournament_sizes = {2, 3, 4, 5, 6, 7, 8, 10};

    std::ofstream tourRaw(results_dir + "tournament_raw_" + instance_path +
                          ".csv");
    tourRaw << "tournament_size,run,makespan\n";
    std::ofstream tourSummary(results_dir + "tournament_summary_" +
                              instance_path + ".csv");
    tourSummary << "tournament_size,runs,mean,std_dev,min,max,median,ci_lower,"
                   "ci_upper\n";

    for (int t_size : tournament_sizes) {
        std::vector<int> makespans;
        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed = base_seed + run * 100 + t_size;
            int makespan =
                run_ga_with_seed(base_sol, POPULATION_SIZE, GENERATIONS, t_size,
                                 FIXED_PM, FIXED_PX, seed);
            makespans.push_back(makespan);
            tourRaw << t_size << "," << run << "," << makespan << "\n";
        }
        Statistics stats = compute_statistics(makespans);
        tourSummary << t_size << "," << RUNS_PER_CONFIG << "," << stats.mean
                    << "," << stats.std_dev << "," << stats.min << ","
                    << stats.max << "," << stats.median << "," << stats.ci_lower
                    << "," << stats.ci_upper << "\n";
        std::cout << "  T Size = " << std::setw(2) << t_size
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }
    tourRaw.close();
    tourSummary.close();

    std::cout << "\n========================================\n";
    std::cout << "Experiment Complete!\n";
    std::cout << "CSV files saved to " << results_dir << "\n";
    std::cout << "========================================\n";

    return 0;
}
