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
    std::string instance_path = "tai20_20_0";
    TaillardInstance inst = load_taillard("../../" + instance_path + ".fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    const int RUNS_PER_CONFIG = 20;
    const int POPULATION_SIZE = 360;
    const int GENERATIONS = 50;
    const double FIXED_PM = 0.85;
    const double FIXED_PX = 1;
    const unsigned int base_seed = 12345;

    std::cout << "========================================\n";
    std::cout << "Tournament Size Analysis\n";
    std::cout << "========================================\n";
    std::cout << "Instance: " << inst.n_jobs << " jobs, " << inst.n_machines
              << " machines\n";
    std::cout << "Fixed: pop=" << POPULATION_SIZE << ", gens=" << GENERATIONS
              << ", pm=" << FIXED_PM << ", px=" << FIXED_PX << "\n";
    std::cout << "Runs per config: " << RUNS_PER_CONFIG << "\n\n";
    std::cout << std::fixed << std::setprecision(3);

    std::vector<int> tournament_sizes = {2, 3, 4, 5, 6, 7, 8, 10};

    std::ofstream rawFile("../main/results/tournament_raw_" + instance_path +
                          ".csv");
    rawFile << "tournament_size,run,makespan\n";

    std::ofstream summaryFile("../main/results/tournament_summary_" +
                              instance_path + ".csv");
    summaryFile << "tournament_size,runs,mean,std_dev,min,max,median,ci_lower,"
                   "ci_upper\n";

    for (int t_size : tournament_sizes) {
        std::vector<int> makespans;
        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed = base_seed + run * 100 + t_size;
            int makespan =
                run_ga_with_seed(base_sol, POPULATION_SIZE, GENERATIONS, t_size,
                                 FIXED_PM, FIXED_PX, seed);
            makespans.push_back(makespan);
            rawFile << t_size << "," << run << "," << makespan << "\n";
        }
        Statistics stats = compute_statistics(makespans);
        summaryFile << t_size << "," << RUNS_PER_CONFIG << "," << stats.mean
                    << "," << stats.std_dev << "," << stats.min << ","
                    << stats.max << "," << stats.median << "," << stats.ci_lower
                    << "," << stats.ci_upper << "\n";
        std::cout << "  T Size = " << std::setw(2) << t_size
                  << " | Mean: " << std::setw(8) << stats.mean
                  << " | Std: " << std::setw(6) << stats.std_dev
                  << " | Best: " << std::setw(5) << stats.min << "\n";
    }

    rawFile.close();
    summaryFile.close();
    std::cout << "\n Results saved.\n";
    return 0;
}
