#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#include "Subject_solution.h"
#include "algo.h"
#include "load.h"

int main() {
    // Open CSV file for convergence data
    std::ofstream convergenceFile("convergence_ga.csv");
    convergenceFile << "generation,best_makespan,avg_makespan,worst_makespan\n";

    TaillardInstance inst = load_taillard("../tai500_20_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution sol(inst.jobs);

    // GA Parameters
    int population_size = 180;
    int generations = 100;
    int tournament_size = 5;
    double pm = 1;     // mutation probability
    double px = 0.85;  // crossover probability

    // Track convergence data
    std::vector<int> best_per_gen(generations);
    std::vector<double> avg_per_gen(generations);
    std::vector<int> worst_per_gen(generations);

    // Initialize population
    std::vector<Subject_solution> population;
    for (int i = 0; i < population_size; i++) {
        Subject_solution temp = sol.copy();
        temp.shuffle_permutation(gen);
        temp.compute_makespan();
        population.push_back(temp);
    }

    std::uniform_real_distribution<double> prob_dist(0.0, 1.0);
    std::uniform_int_distribution<int> dist(0, population_size - 1);

    // Main GA loop with convergence tracking
    for (int g = 0; g < generations; g++) {
        // Tournament Selection
        std::vector<Subject_solution> parents;
        for (int p = 0; p < population_size; p++) {
            Subject_solution best = population[dist(gen)];
            for (int t = 1; t < tournament_size; t++) {
                Subject_solution candidate = population[dist(gen)];
                if (candidate < best) {
                    best = candidate;
                }
            }
            parents.push_back(best);
        }

        // Crossover
        std::vector<Subject_solution> children;
        for (int i = 0; i < (int)parents.size(); i += 2) {
            if (i + 1 < (int)parents.size()) {
                Subject_solution p1 = parents[i];
                Subject_solution p2 = parents[i + 1];
                if (prob_dist(gen) < px) {
                    Subject_solution child1 = ox(p1, p2);
                    Subject_solution child2 = ox(p2, p1);
                    child1.compute_makespan();
                    child2.compute_makespan();
                    children.push_back(child1);
                    children.push_back(child2);
                } else {
                    children.push_back(p1);
                    children.push_back(p2);
                }
            }
        }

        // Mutation
        std::uniform_real_distribution<double> prob(0.0, 1.0);
        for (auto& child : children) {
            if (prob(gen) < pm) {
                child.swap_jobs(gen);
                child.compute_makespan();
            }
        }

        // Sort populations
        std::sort(children.begin(), children.end());
        std::sort(population.begin(), population.end());

        // Track statistics for current generation
        int gen_best = population[0].get_makespan();
        int gen_worst = population.back().get_makespan();

        double gen_avg = 0.0;
        for (const auto& ind : population) {
            gen_avg += ind.get_makespan();
        }
        gen_avg /= population_size;

        best_per_gen[g] = gen_best;
        avg_per_gen[g] = gen_avg;
        worst_per_gen[g] = gen_worst;

        // Write to CSV file
        convergenceFile << g << "," << gen_best << "," << gen_avg << ","
                        << gen_worst << "\n";

        // Elitism: Keep the 20% absolute best from the OLD population
        std::vector<Subject_solution> new_pop;
        int elite_count = population_size / 5;
        for (int i = 0; i < elite_count; i++) {
            new_pop.push_back(population[i]);
        }

        // Fill the rest with children
        for (int i = 0;
             i < population_size - elite_count && i < children.size(); i++) {
            new_pop.push_back(children[i]);
        }

        population = new_pop;

        // Optional: Print progress
        if ((g + 1) % 10 == 0 || g == 0) {
            std::cout << "Generation " << g << ": Best = " << gen_best
                      << ", Avg = " << gen_avg << ", Worst = " << gen_worst
                      << "\n";
        }
    }

    convergenceFile.close();

    // Also create a separate file with summary statistics
    std::ofstream summaryFile("convergence_summary.txt");
    summaryFile << "GA Convergence Summary\n";
    summaryFile << "======================\n\n";
    summaryFile << "Population Size: " << population_size << "\n";
    summaryFile << "Generations: " << generations << "\n";
    summaryFile << "Tournament Size: " << tournament_size << "\n";
    summaryFile << "Mutation Probability: " << pm << "\n";
    summaryFile << "Crossover Probability: " << px << "\n\n";

    summaryFile << "Final Best Makespan: " << best_per_gen.back() << "\n";
    summaryFile << "Final Average Makespan: " << avg_per_gen.back() << "\n";
    summaryFile << "Final Worst Makespan: " << worst_per_gen.back() << "\n\n";

    summaryFile << "Best Improvement: " << best_per_gen[0] - best_per_gen.back()
                << "\n";

    summaryFile.close();

    std::cout << "\nConvergence data saved to convergence_ga.csv\n";
    std::cout << "Summary saved to convergence_summary.txt\n";
    std::cout << "Run the Python script to generate the convergence graph\n";

    return 0;
}