#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#include "../include/Subject_solution.h"
#include "../include/algo.h"
#include "../include/load.h"

int main() {
    std::string instance_path = "tai500_20_0";
    TaillardInstance inst = load_taillard("../../" + instance_path + ".fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution sol(inst.jobs);

    std::ofstream convergenceFile("../main/results/convergence_ga_" +
                                  instance_path + ".csv");
    convergenceFile << "generation,best_makespan,avg_makespan,worst_makespan\n";

    int population_size = 360;
    int generations = 50;
    int tournament_size = 6;
    double pm = 1;    // mutation probability
    double px = 0.9; // crossover probability

    std::vector<int> best_per_gen(generations);
    std::vector<double> avg_per_gen(generations);
    std::vector<int> worst_per_gen(generations);

    std::vector<Subject_solution> population;
    for (int i = 0; i < population_size; i++) {
        Subject_solution temp = sol.copy();
        temp.shuffle_permutation(gen);
        temp.compute_makespan();
        population.push_back(temp);
    }

    std::uniform_real_distribution<double> prob_dist(0.0, 1.0);
    std::uniform_int_distribution<int> dist(0, population_size - 1);

    for (int g = 0; g < generations; g++) {
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

        std::uniform_real_distribution<double> prob(0.0, 1.0);
        for (auto& child : children) {
            if (prob(gen) < pm) {
                child.swap_jobs(gen);
                child.compute_makespan();
            }
        }

        std::sort(children.begin(), children.end());
        std::sort(population.begin(), population.end());

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

        convergenceFile << g << "," << gen_best << "," << gen_avg << ","
                        << gen_worst << "\n";

        std::vector<Subject_solution> new_pop;
        int elite_count = population_size / 5;
        for (int i = 0; i < elite_count; i++) {
            new_pop.push_back(population[i]);
        }

        for (int i = 0;
             i < population_size - elite_count && i < children.size(); i++) {
            new_pop.push_back(children[i]);
        }

        population = new_pop;

        if ((g + 1) % 10 == 0 || g == 0) {
            std::cout << "Generation " << g << ": Best = " << gen_best
                      << ", Avg = " << gen_avg << ", Worst = " << gen_worst
                      << "\n";
        }
    }

    convergenceFile.close();

    std::ofstream summaryFile("../main/results/convergence_summary_" +
                              instance_path + ".txt");
    summaryFile << "GA Convergence Summary\n";
    summaryFile << "-------------------------------------------\n\n";
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

    std::cout << "\nConvergence data saved to convergence_ga_" << instance_path
              << ".csv\n";
    std::cout << "Summary saved to convergence_summary_" << instance_path
              << ".txt\n";

    return 0;
}
