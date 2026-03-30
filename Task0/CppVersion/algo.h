#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include "Subject_solution.h"
<<<<<<< HEAD

=======
struct GenerationStats {
    int best;
    int worst;
    double avg;
};

// update GA signature to return stats too
std::pair<Subject_solution, std::vector<GenerationStats>> genetic_tracked(
    const Subject_solution& solution, int population_size = 100,
    int generations = 100, int root_parents = 20, int tournament_size = 10,
    double pm = 0.1);
>>>>>>> 83805ac (Small fixes across all the project)
Subject_solution randomSearch(const Subject_solution& solution,
                              int iterations = 10000);
Subject_solution greedy(const Subject_solution& solution);
Subject_solution ox(const Subject_solution& parent1,
                    const Subject_solution& parent2);
Subject_solution simulatedAnnealing(const Subject_solution& solution,
                                    double temp = 500.0,
                                    double cooling_rate = 0.999,
                                    int iterations = 10000);
Subject_solution genetic(const Subject_solution& solution,
                         int population_size = 100, int generations = 100,
<<<<<<< HEAD
                         int root_parents = 20, int tournament_size = 10,
                         double pm = 0.1);
=======
                         int tournament_size = 10, double pm = 0.1,
                         double px = 0.7);
>>>>>>> 83805ac (Small fixes across all the project)

#endif  // ALGORITHMS_H