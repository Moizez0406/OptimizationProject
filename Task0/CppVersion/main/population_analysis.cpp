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
    std::string instance_path = "tai20_20_0";
    TaillardInstance inst = load_taillard("../../" + instance_path + ".fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    const int RUNS_PER_CONFIG = 20;
    const int TOURNAMENT_SIZE = 5;
    const double FIXED_PM = 0.85;
    const double FIXED_PX = 1;
    // Budget fixed at 360 * 50 = 18,000 evaluations
    const int EVAL_BUDGET = 360 * 50;
    const unsigned int base_seed = 12345;

    std::cout << "========================================\n";
    std::cout << "Population Size Analysis\n";
    std::cout << "========================================\n";
    std::cout << "Instance: " << inst.n_jobs << " jobs, " << inst.n_machines
              << " machines\n";
    std::cout << "Fixed: eval_budget=" << EVAL_BUDGET
              << ", ts=" << TOURNAMENT_SIZE << ", pm=" << FIXED_PM
              << ", px=" << FIXED_PX << "\n";
    std::cout << "Runs per config: " << RUNS_PER_CONFIG << "\n\n";
    std::cout << std::fixed << std::setprecision(3);

    std::vector<int> pop_sizes = {45, 90, 180, 360};

    std::ofstream rawFile("../main/results/population_raw_" + instance_path +
                          ".csv");
    rawFile << "population_size,generations,run,makespan\n";

    std::ofstream summaryFile("../main/results/population_summary_" +
                              instance_path + ".csv");
    summaryFile << "population_size,generations,runs,mean,std_dev,min,max,"
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
            int makespan = result.get_makespan();
            makespans.push_back(makespan);
            rawFile << pop_size << "," << scaled_gens << "," << run << ","
                    << makespan << "\n";
        }

        Statistics stats = compute_statistics(makespans);
        summaryFile << pop_size << "," << scaled_gens << "," << RUNS_PER_CONFIG
                    << "," << stats.mean << "," << stats.std_dev << ","
                    << stats.min << "," << stats.max << "," << stats.median
                    << "," << stats.ci_lower << "," << stats.ci_upper << "\n";
        std::cout << "  Pop = " << std::setw(4) << pop_size
                  << " | Gens = " << std::setw(4) << scaled_gens
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }

    rawFile.close();
    summaryFile.close();
    std::cout << "\nDone. Results saved.\n";
    return 0;
}
