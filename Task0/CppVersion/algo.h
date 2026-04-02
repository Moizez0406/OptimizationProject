#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "Subject_solution.h"
struct GenerationStats {
    int best;
    int worst;
    double avg;
};

Subject_solution randomSearch(const Subject_solution& solution,
                              int iterations = 10000);
Subject_solution greedy(const Subject_solution& solution);
Subject_solution greedy_with_budget(const Subject_solution& base_sol,
                                    int max_evaluations);
Subject_solution ox(const Subject_solution& parent1,
                    const Subject_solution& parent2);
Subject_solution simulatedAnnealing(const Subject_solution& solution,
                                    double temp = 500.0,
                                    double cooling_rate = 0.999,
                                    int iterations = 10000);
Subject_solution genetic(const Subject_solution& solution,
                         int population_size = 100, int generations = 100,
                         int tournament_size = 10, double pm = 0.1,
                         double px = 0.7);

#endif  // ALGORITHMS_H