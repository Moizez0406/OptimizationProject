#include <fstream>
#include <iostream>

#include "Subject_solution.h"
#include "algo.h"
#include "load.h"

int main() {
    TaillardInstance inst = load_taillard("../tai500_20_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution sol(inst.jobs);

    int population_size = 400;
    int generations = 1000;
    int tournament_size = 5;
    double pm = 0.01;

    auto [ga_best, ga_stats] =
        genetic_tracked(sol, population_size, generations, tournament_size, pm);

    // write convergence CSV
    std::ofstream convFile("convergence.csv");
    convFile << "Generation,Best,Worst,Avg\n";
    for (int g = 0; g < (int)ga_stats.size(); g++) {
        convFile << g << "," << ga_stats[g].best << "," << ga_stats[g].worst
                 << "," << ga_stats[g].avg << "\n";
    }
    convFile.close();

    std::cout << "GA Best: " << ga_best.get_makespan() << "\n";
    std::cout << "Generations: " << generations << "\n";
    std::cout << "Population: " << population_size << "\n";
    std::cout << "UB: " << inst.UB << "\n";
    std::cout << "LB: " << inst.LB << "\n";
    std::cout << "Convergence data written to convergence.csv\n";

    return 0;
}