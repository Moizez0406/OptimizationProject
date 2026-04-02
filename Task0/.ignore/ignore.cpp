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

    TaillardInstance inst = load_taillard("../tai500_20_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    // Fixed configuration from your optimal parameters
    const int RUNS_PER_CONFIG = 10;
    int population_size = 400;  // Fixed: optimal from analysis
    int generations = 100;      // Fixed
    int tournament_size = 2;    // Fixed: optimal from analysis
    double px = 1.0;            // Fixed: optimal from analysis

    unsigned int base_seed = 12345;

    std::cout << "========================================\n";
    std::cout << "GA Mutation Probability Test\n";
    std::cout << "========================================\n";
    std::cout << "Instance: " << inst.n_jobs << " jobs, " << inst.n_machines
              << " machines\n";
    std::cout << "Fixed Configuration:\n";
    std::cout << "  Population Size: " << population_size << "\n";
    std::cout << "  Generations: " << generations << "\n";
    std::cout << "  Tournament Size: " << tournament_size << "\n";
    std::cout << "  Crossover Probability (px): " << px << "\n";
    std::cout << "Runs per configuration: " << RUNS_PER_CONFIG << "\n\n";

    // Set precision for output
    std::cout << std::fixed << std::setprecision(3);

    // ==================== Test Mutation Probability (pm) ====================
    std::cout
        << "Testing Mutation Probability (pm) with optimal fixed params...\n";
    std::vector<double> pm_values = {0.50, 0.666, 0.8632, 1};

    std::ofstream pmFile("results/ignore.csv");
    pmFile << "pm,run,makespan\n";

    std::ofstream pmSummary("results/ignore_summary.csv");
    pmSummary << "pm,runs,mean,std_dev,min,max,median,ci_lower,ci_upper\n";

    for (double pm : pm_values) {
        std::vector<int> makespans;

        for (int run = 0; run < RUNS_PER_CONFIG; run++) {
            unsigned int seed =
                base_seed + run * 100 + static_cast<int>(pm * 1000);
            int makespan =
                run_ga_with_seed(base_sol, population_size, generations,
                                 tournament_size, pm, px, seed);
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
                  << " | Best: " << std::setw(5) << stats.min
                  << " | Worst: " << std::setw(5) << stats.max << "\n";
    }
    pmFile.close();
    pmSummary.close();

    std::cout << "\n========================================\n";
    std::cout << "Experiment Complete!\n";
    std::cout << "Results saved to:\n";
    std::cout << "  - results/ignore.csv (Raw data for pm test)\n";
    std::cout << "  - results/ignore_summary.csv (Statistics summary)\n";
    std::cout << "========================================\n";

    return 0;
}