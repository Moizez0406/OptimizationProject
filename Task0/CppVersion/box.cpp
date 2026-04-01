#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#include "Subject_solution.h"
#include "algo.h"
#include "load.h"

int main() {
    std::ofstream outFile("ga_pm_results.csv");

    // CSV header (IMPORTANT for pandas)
    outFile << "Algorithm,pm,Run,Makespan\n";

    // Load instance
    TaillardInstance inst = load_taillard("../tai100_20_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base_sol(inst.jobs);

    // Parameters
    const int RUNS = 20;
    int population_size = 180;
    int generations = 100;
    int tournament_size = 5;
    int pm = 1;
    // Mutation probabilities to test
    std::vector<double> pms = {20, 60, 100, 140, 180, 220, 260};

    // ---- Experiment loop ----
    for (double pm : pms) {
        std::cout << "Running experiments for pm = " << pm << std::endl;

        for (int run = 0; run < RUNS; run++) {
            Subject_solution result =
                genetic(base_sol, population_size, generations, tournament_size,
                        0.85, 1);

            int makespan = result.get_makespan();

            // Write to CSV
            outFile << "GA," << pm << "," << run << "," << makespan << "\n";
        }
    }

    outFile.close();

    // Basic info (optional)
    std::cout << "\nInstance info:\n";
    std::cout << "Jobs: " << inst.n_jobs << "\n";
    std::cout << "Machines: " << inst.n_machines << "\n";
    std::cout << "UB: " << inst.UB << "\n";
    std::cout << "LB: " << inst.LB << "\n";

    std::cout << "\nResults written to ga_pm_results.csv\n";

    return 0;
}