#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#include "Subject_solution.h"
#include "algo.h"
#include "load.h"

int main() {
    std::ofstream outFile("ga_param_study.csv");
    outFile << "Population,Generations,Tournament,Mutation,Run,Makespan\n";

    TaillardInstance inst = load_taillard("../tai100_20_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution base(inst.jobs);

    const int RUNS = 10;

    // --- Parameter ranges ---
    std::vector<int> population_sizes = {100, 150, 180};
    std::vector<int> generations_list = {100, 150};
    std::vector<int> tournament_sizes = {5};
    std::vector<double> mutation_rates = {0.05, 0.5, 1};

    // --- Grid search ---
    for (int pop : population_sizes) {
        for (int gen : generations_list) {
            for (int tour : tournament_sizes) {
                for (double pm : mutation_rates) {
                    std::cout << "Running: pop=" << pop << " gen=" << gen
                              << " tour=" << tour << " pm=" << pm << "\n";

                    for (int run = 0; run < RUNS; run++) {
                        Subject_solution result =
                            genetic(base, pop, gen, tour, pm);

                        int makespan = result.get_makespan();

                        outFile << pop << "," << gen << "," << tour << "," << pm
                                << "," << run << "," << makespan << "\n";
                    }
                }
            }
        }
    }

    outFile.close();

    std::cout << "Parameter study completed.\n";
    return 0;
}