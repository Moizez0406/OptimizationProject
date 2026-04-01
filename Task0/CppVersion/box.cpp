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

int run_ga_with_seed(const Subject_solution& base_sol, int population_size,
                     int generations, int tournament_size, double pm, double px,
                     unsigned int seed) {
    // Seed the random generator
    gen.seed(seed);

    Subject_solution sol = base_sol.copy();
    Subject_solution result =
        genetic(sol, population_size, generations, tournament_size, pm, px);

    return result.get_makespan();
}

struct Statistics {
    double mean;
    double std_dev;
    double min;
    double max;
    double median;
    double ci_lower;
    double ci_upper;
};

Statistics compute_statistics(const std::vector<int>& values) {
    Statistics stats;
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

    double standard_error = stats.std_dev / std::sqrt(n);
    stats.ci_lower = stats.mean - 1.96 * standard_error;
    stats.ci_upper = stats.mean + 1.96 * standard_error;

    return stats;
}

int main() {
    system("mkdir -p results");

    TaillardInstance inst = load_taillard("../tai20_20_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    const int RUNS_PER_CONFIG = 30;
    int default_population_size = 180;
    int default_generations = 100;
    int default_tournament_size = 5;
    double default_px = 0.85;
    double default_pm = 0.10;

    unsigned int base_seed = 12345;

    std::cout << "========================================\n";
    std::cout << "GA Parameter Sensitivity Analysis\n";
    std::cout << "========================================\n";
    std::cout << "Instance: " << inst.n_jobs << " jobs, " << inst.n_machines
              << " machines\n";
    std::cout << "Runs per configuration: " << RUNS_PER_CONFIG << "\n\n";

    // Set precision for output
    std::cout << std::fixed << std::setprecision(3);

    // ==================== 1. Mutation Probability (pm) ====================
    std::cout << "Testing Mutation Probability (pm)...\n";
    std::vector<double> pm_values = {0.01, 0.05, 0.10, 0.15,
                                     0.20, 0.30, 0.40, 0.50};

    std::ofstream pmFile("results/pm_analysis.csv");
    pmFile << "pm,run,makespan\n";

    std::ofstream pmSummary("results/pm_summary.csv");
    pmSummary << "pm,runs,mean,std_dev,min,max,median,ci_lower,ci_upper\n";

    for (double pm : pm_values) {
        std::vector<int> makespans;

        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed =
                base_seed + run * 100 + static_cast<int>(pm * 1000);
            int makespan = run_ga_with_seed(
                base_sol, default_population_size, default_generations,
                default_tournament_size, pm, default_px, seed);
            makespans.push_back(makespan);
            pmFile << pm << "," << run << "," << makespan << "\n";
        }

        Statistics stats = compute_statistics(makespans);
        pmSummary << pm << "," << RUNS_PER_CONFIG << "," << stats.mean << ","
                  << stats.std_dev << "," << stats.min << "," << stats.max
                  << "," << stats.median << "," << stats.ci_lower << ","
                  << stats.ci_upper << "\n";

        std::cout << "  pm = " << std::setw(6) << pm
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }
    pmFile.close();
    pmSummary.close();

    // ==================== 2. Crossover Probability (px) ====================
    std::cout << "\nTesting Crossover Probability (px)...\n";
    std::vector<double> px_values = {0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0};

    std::ofstream pxFile("results/px_analysis.csv");
    pxFile << "px,run,makespan\n";

    std::ofstream pxSummary("results/px_summary.csv");
    pxSummary << "px,runs,mean,std_dev,min,max,median,ci_lower,ci_upper\n";

    for (double px : px_values) {
        std::vector<int> makespans;

        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed =
                base_seed + run * 100 + static_cast<int>(px * 1000);
            int makespan = run_ga_with_seed(
                base_sol, default_population_size, default_generations,
                default_tournament_size, default_pm, px, seed);
            makespans.push_back(makespan);
            pxFile << px << "," << run << "," << makespan << "\n";
        }

        Statistics stats = compute_statistics(makespans);
        pxSummary << px << "," << RUNS_PER_CONFIG << "," << stats.mean << ","
                  << stats.std_dev << "," << stats.min << "," << stats.max
                  << "," << stats.median << "," << stats.ci_lower << ","
                  << stats.ci_upper << "\n";

        std::cout << "  px = " << std::setw(6) << px
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }
    pxFile.close();
    pxSummary.close();

    // ==================== 3. Population Size ====================
    std::cout << "\nTesting Population Size...\n";
    std::vector<int> pop_sizes = {50, 100, 150, 180, 200, 250, 300, 400};

    std::ofstream popFile("results/population_analysis.csv");
    popFile << "population_size,run,makespan\n";

    std::ofstream popSummary("results/population_summary.csv");
    popSummary << "population_size,runs,mean,std_dev,min,max,median,ci_lower,"
                  "ci_upper\n";

    for (int pop_size : pop_sizes) {
        std::vector<int> makespans;

        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed = base_seed + run * 100 + pop_size;
            gen.seed(seed);

            Subject_solution sol = base_sol.copy();
            Subject_solution result =
                genetic(sol, pop_size, default_generations,
                        default_tournament_size, default_pm, default_px);
            int makespan = result.get_makespan();
            makespans.push_back(makespan);
            popFile << pop_size << "," << run << "," << makespan << "\n";
        }

        Statistics stats = compute_statistics(makespans);
        popSummary << pop_size << "," << RUNS_PER_CONFIG << "," << stats.mean
                   << "," << stats.std_dev << "," << stats.min << ","
                   << stats.max << "," << stats.median << "," << stats.ci_lower
                   << "," << stats.ci_upper << "\n";

        std::cout << "  Pop Size = " << std::setw(4) << pop_size
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }
    popFile.close();
    popSummary.close();

    // ==================== 4. Tournament Size ====================
    std::cout << "\nTesting Tournament Size...\n";
    std::vector<int> tournament_sizes = {2, 3, 4, 5, 6, 7, 8, 10};

    std::ofstream tourFile("results/tournament_analysis.csv");
    tourFile << "tournament_size,run,makespan\n";

    std::ofstream tourSummary("results/tournament_summary.csv");
    tourSummary << "tournament_size,runs,mean,std_dev,min,max,median,ci_lower,"
                   "ci_upper\n";

    for (int t_size : tournament_sizes) {
        std::vector<int> makespans;

        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed = base_seed + run * 100 + t_size;
            gen.seed(seed);

            Subject_solution sol = base_sol.copy();
            Subject_solution result =
                genetic(sol, default_population_size, default_generations,
                        t_size, default_pm, default_px);
            int makespan = result.get_makespan();
            makespans.push_back(makespan);
            tourFile << t_size << "," << run << "," << makespan << "\n";
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
    tourFile.close();
    tourSummary.close();

    std::cout << "\n========================================\n";
    std::cout << "Experiment Complete!\n";
    std::cout << "CSV files saved to results/ directory\n";
    std::cout << "========================================\n";

    return 0;
}