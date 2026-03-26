import load
import random as rand
from Subject_solution import Subject_solution, swap, ox, solution
from collections import namedtuple

Job = namedtuple('Job', ['id', 'times'])
jobs, machines, subject, UB, LB = load.load_taillard("tai20_10_0.fsp")
subject = [Job(id=i, times=t) for i, t in enumerate(subject)]
Subject_solution.set_lookup(subject)  # set dictionary


def randomSearch(subject, machines):
    Highest_solution = float('inf')
    Best_subject = None
    temp_subject = subject.copy()
    for i in range(10000):
        rand.shuffle(temp_subject)
        sol = solution(temp_subject, machines)
        if Highest_solution > sol[-1]:
            Highest_solution = sol[-1]
            Best_subject = temp_subject.copy()
    return Best_subject, Highest_solution


def greedy(subject, machines):
    temp_subject = subject.copy()
    Best_subject = [temp_subject.pop(0)]
    rand.shuffle(temp_subject)

    while temp_subject:
        current_sol = float('inf')
        current_job = None

        for s in temp_subject:
            current_step = Best_subject + [s]
            ms = solution(current_step, machines)[-1]
            if ms < current_sol:
                current_sol = ms
                current_job = s

        Best_subject.append(current_job)
        temp_subject.remove(current_job)

    return Best_subject, current_sol


def genetic(subject, machines, population_size=50, generations=100,
            root_parents=20, tournament_size=5, pm=0.1):
    Population = []  # list of Subject_solution objects
    population_makespan = []
    temp_subject = subject.copy()

    for i in range(population_size):
        rand.shuffle(temp_subject)
        # store the last value which is the makespan
        population_makespan.append(solution(temp_subject, machines)[-1])
        Population.append(Subject_solution(
            temp_subject.copy(), population_makespan[i]))
        temp_subject = subject.copy()

    for gen in range(generations):
        Parents = []
        Children = []

        # Tournament selection
        for _ in range(root_parents):
            tournament = rand.sample(Population, tournament_size)
            best_makespan = float('inf')
            best_parent = None
            for individual in tournament:
                if individual.makespan < best_makespan:
                    best_makespan = individual.makespan
                    best_parent = individual
            Parents.append(best_parent)
        # Crossover ox
        for i in range(len(Parents)):
            Children.append(ox(Parents[i].ids, Parents[i-1].ids, machines))
        # Mutation swap
        for child in Children:
            if rand.random() < pm:  # mutation probability
                swap(child, machines)
        Population = Children.copy()
    best = None
    best_ms = float('inf')
    for s in Population:
        if s.makespan < best_ms:
            best_ms = s.makespan
            best = s
    return Population, best


Best_subject, Highest_solution = randomSearch(subject, machines)
print(f"Random Search — Best order: {[job.id for job in Best_subject]}")
print(f"Random Search — Makespan: {Highest_solution}")

Best_subject, Highest_solution = greedy(subject, machines)
print(f"Greedy — Best order: {[job.id for job in Best_subject]}")
print(f"Greedy — Makespan: {Highest_solution}")

Population, Highest_solution = genetic(subject, machines, generations=10)
print(f"Genetic Algorithm — Makespan: {Highest_solution.makespan}")
print(f"Genetic Algorithm — Best order: {Highest_solution.ids}")

# 2. EVALUATE    — compute makespan for each Solution ✅
# 3. SELECT      — pick parents (tournament, roulette wheel, etc.)✅
# 4. CROSSOVER   — combine two parents → child permutation ✅
# 5. MUTATE      — randomly tweak child with probability Pm ✅
# 6. REPEAT 3-5 for gen generations
# 7. TRACK       — best, average, worst makespan per generation
# project/
# ├── load.py
# ├── Solution.py        ← done ✅
# ├── Eda.py             ← your main file, rename to main.py eventually
# │
# │   Algorithms:
# ├── randomSearch()     ← done ✅
# ├── greedy()           ← done ✅
# ├── ga()               ← next to implement
# └── simulatedAnnealing() ← after GA
