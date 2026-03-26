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
            root_parents=20, tournament_size=10, pm=0.1):
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

def simulatedAnnealing(subject, machines, temp=1000, cooling_rate=0.999, 
                       iterations=50000):
    rand.shuffle(subject)
    current_sol = solution(subject, machines)[-1]
    current_subject = Subject_solution(subject, current_sol)
    temp_subject = current_subject.copy()
    for _ in range(iterations):
        swap(temp_subject, machines)
        if temp_subject.makespan < current_sol:
            current_sol = temp_subject.makespan
            current_subject = temp_subject.copy()
        elif rand.random() < 2.71828 ** ((current_sol - temp_subject.makespan) / temp):
                current_sol = temp_subject.makespan
                current_subject = temp_subject.copy()
        temp *= cooling_rate
    return current_subject

simulatedAnnealing_solution = simulatedAnnealing(subject, machines)
print(f"Simulated Annealing — Makespan: {simulatedAnnealing_solution.makespan}")
# print(f"Simulated Annealing — Best order: {simulatedAnnealing_solution.ids}")
Best_subject, Highest_solution = randomSearch(subject, machines)
print(f"Random Search — Makespan: {Highest_solution}")
# print(f"Random Search — Best order: {[job.id for job in Best_subject]}")

Best_subject, Highest_solution = greedy(subject, machines)
print(f"Greedy — Makespan: {Highest_solution}")
# print(f"Greedy — Best order: {[job.id for job in Best_subject]}")

Population, Highest_solution = genetic(subject, machines, generations=10)
print(f"Genetic Algorithm — Makespan: {Highest_solution.makespan}")
# print(f"Genetic Algorithm — Best order: {Highest_solution.ids}")

