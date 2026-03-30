#include "algo.h"

#include <algorithm>
#include <cmath>
#include <random>
std::uniform_real_distribution<double> prob_dist(0.0, 1.0);

Subject_solution randomSearch(const Subject_solution& solution,
                              int iterations) {
    Subject_solution Best_solution = solution.copy();
    Subject_solution Temporary_solution = solution.copy();
    for (int i = 0; i < iterations; i++) {
        Temporary_solution = solution.copy();
        Temporary_solution.shuffle_permutation(gen);
        Temporary_solution.compute_makespan();
        if (Temporary_solution.get_makespan() < Best_solution.get_makespan()) {
            Best_solution = Temporary_solution.copy();
        }
    }
    return Best_solution;
}

Subject_solution greedy(const Subject_solution& solution) {
    Subject_solution remaining = solution.copy();
    remaining.shuffle_permutation(gen);
    Subject_solution scheduled({remaining.pop_front()});

    while (!remaining.empty()) {
        int current_sol = 99999;
        Job best_candidate = remaining.get_permutation()[0];
        for (const auto& job : remaining.get_permutation()) {
            Subject_solution trial = scheduled.copy();
            trial.append_job(job);
            if (trial.get_makespan() < current_sol) {
                current_sol = trial.get_makespan();
                best_candidate = job;
            }
        }
        scheduled.append_job(best_candidate);
        remaining.remove_job(best_candidate);
    }
    return scheduled;
}

Subject_solution ox(const Subject_solution& parent1,
                    const Subject_solution& parent2) {
    std::vector<int> ids1 = parent1.get_ids();
    std::vector<int> ids2 = parent2.get_ids();
    int n = (int)ids1.size();

    std::uniform_int_distribution<int> dist(0, n - 1);
    int i = dist(gen);
    int j = dist(gen);
    if (i > j) std::swap(i, j);

    std::vector<int> child_ids(n, -1);
    for (int k = i; k < j; k++) {
        child_ids[k] = ids1[k];
    }

    int pos = 0;
    for (int gene : ids2) {
        if (std::find(child_ids.begin(), child_ids.end(), gene) ==
            child_ids.end()) {
            while (child_ids[pos] != -1) pos++;
            child_ids[pos] = gene;
        }
    }
    return Subject_solution::from_ids(child_ids);
}
Subject_solution pmx(const Subject_solution& parent1,
                     const Subject_solution& parent2) {
    std::vector<int> p1 = parent1.get_ids();
    std::vector<int> p2 = parent2.get_ids();
    int n = (int)p1.size();

    std::uniform_int_distribution<int> dist(0, n - 1);
    int i = dist(gen);
    int j = dist(gen);
    if (i > j) std::swap(i, j);

    std::vector<int> child(n, -1);

    // Step 1: Copy segment from parent1
    for (int k = i; k <= j; k++) {
        child[k] = p1[k];
    }

    // Step 2: Create mapping (p2 -> p1 in segment)
    std::unordered_map<int, int> mapping;
    for (int k = i; k <= j; k++) {
        mapping[p2[k]] = p1[k];
    }

    // Step 3: Fill remaining positions
    for (int k = 0; k < n; k++) {
        if (k >= i && k <= j) continue;

        int gene = p2[k];

        // Resolve conflicts using mapping
        while (mapping.find(gene) != mapping.end()) {
            gene = mapping[gene];
        }

        child[k] = gene;
    }

    return Subject_solution::from_ids(child);
}
Subject_solution simulatedAnnealing(const Subject_solution& solution,
                                    double temp, double cooling_rate,
                                    int iterations) {
    Subject_solution current = solution.copy();
    current.shuffle_permutation(gen);
    current.compute_makespan();

    for (int i = 0; i < iterations; i++) {
        Subject_solution neighbor = current.copy();
        neighbor.swap_jobs(gen);

        double delta = neighbor.get_makespan() - current.get_makespan();
        if (delta < 0) {
            current = neighbor.copy();
        } else if (std::uniform_real_distribution<double>(0.0, 1.0)(gen) <
                   std::exp(-delta / temp)) {
            current = neighbor.copy();
        }
        temp *= cooling_rate;
    }
    return current;
}

Subject_solution genetic(const Subject_solution& solution, int population_size,
                         int generations, int tournament_size, double pm,
                         double px) {
    std::vector<Subject_solution> population;
    for (int i = 0; i < population_size; i++) {
        Subject_solution temp = solution.copy();
        temp.shuffle_permutation(gen);
        temp.compute_makespan();
        population.push_back(temp);
    }
    Subject_solution global_best = population[0];

    for (int g = 0; g < generations; g++) {
        std::vector<Subject_solution> parents;
        std::vector<Subject_solution> children;

        std::uniform_int_distribution<int> dist(0, (int)population.size() - 1);
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

        // 2. Update Global Best (The "Memory" of the GA)
        if (population[0] < global_best) {
            global_best = population[0];
        }

        // 3. Elitism: Keep the 20% absolute best from the OLD population
        std::vector<Subject_solution> new_pop;
        int elite_count = population_size / 5;
        for (int i = 0; i < elite_count; i++) {
            new_pop.push_back(population[i]);
        }

        // 4. Fill the rest with children
        for (int i = 0;
             i < population_size - elite_count && i < children.size(); i++) {
            new_pop.push_back(children[i]);
        }

        population = new_pop;  // always exactly population_size
    }
    return global_best;
}
std::pair<Subject_solution, std::vector<GenerationStats>> genetic_tracked(
    const Subject_solution& solution, int population_size, int generations,
    int root_parents, int tournament_size, double pm) {
    std::vector<GenerationStats> stats;

    // --- Initialize population ---
    std::vector<Subject_solution> population;
    for (int i = 0; i < population_size; i++) {
        Subject_solution temp = solution.copy();
        temp.shuffle_permutation(gen);
        temp.compute_makespan();
        population.push_back(temp);
    }

    // --- Generational loop ---
    for (int g = 0; g < generations; g++) {
        std::vector<Subject_solution> parents;
        std::vector<Subject_solution> children;

        // Tournament selection
        std::uniform_int_distribution<int> dist(0, (int)population.size() - 1);
        for (int p = 0; p < root_parents; p++) {
            Subject_solution best = population[dist(gen)];
            for (int t = 1; t < tournament_size; t++) {
                Subject_solution candidate = population[dist(gen)];
                if (candidate < best) best = candidate;
            }
            parents.push_back(best);
        }

        // Crossover
        for (int i = 0; i < (int)parents.size(); i++) {
            int prev = (i == 0) ? (int)parents.size() - 1 : i - 1;
            children.push_back(ox(parents[i], parents[prev]));
        }

        // Mutation
        std::uniform_real_distribution<double> prob(0.0, 1.0);
        for (auto& child : children) {
            if (prob(gen) < pm) child.swap_jobs(gen);
        }
        population = children;

        // --- track stats for this generation ---
        int best_ms = std::min_element(population.begin(), population.end())
                          ->get_makespan();
        int worst_ms = std::max_element(population.begin(), population.end())
                           ->get_makespan();
        double avg_ms = 0;
        for (const auto& s : population) avg_ms += s.get_makespan();
        avg_ms /= population.size();

        stats.push_back({best_ms, worst_ms, avg_ms});
    }

    Subject_solution best =
        *std::min_element(population.begin(), population.end());
    return {best, stats};
}