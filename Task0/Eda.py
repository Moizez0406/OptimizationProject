import statistics
import load
import random as rand
from Subject_solution import Subject_solution, swap, ox, solution
from collections import namedtuple

Job = namedtuple("Job", ["id", "times"])
jobs, machines, subject, UB, LB = load.load_taillard("tai500_20_0.fsp")
subject = [Job(id=i, times=t) for i, t in enumerate(subject)]
Subject_solution.set_lookup(subject)


def randomSearch(subject, machines):
    Highest_solution = float("inf")
    Best_subject = None
    for i in range(10000):
        rand.shuffle(subject)
        sol = solution(subject, machines)
        if Highest_solution > sol[-1]:
            Highest_solution = sol[-1]
            Best_subject = subject.copy()
    return Best_subject, Highest_solution


def greedy(subject, machines):
    temp_subject = subject.copy()
    Best_subject = [temp_subject.pop(0)]  # Take 1st job ((0)(1,2,3,..))
    rand.shuffle(temp_subject)

    while temp_subject:
        current_sol = float("inf")
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


def genetic(
    subject,
    machines,
    population_size=100,
    generations=100,
    root_parents=20,
    tournament_size=10,
    pm=0.1,
):
    Population = []  # list of Subject_solution objects
    population_makespan = []
    temp_subject = subject.copy()

    for i in range(population_size):
        rand.shuffle(temp_subject)
        # store the last value which is the makespan
        population_makespan.append(solution(temp_subject, machines)[-1])
        Population.append(Subject_solution(temp_subject.copy(), population_makespan[i]))
        temp_subject = subject.copy()

    for gen in range(generations):
        Parents = []
        Children = []

        # Tournament selection
        for _ in range(root_parents):
            tournament = rand.sample(Population, tournament_size)
            best_makespan = float("inf")
            best_parent = None
            for individual in tournament:
                if individual.makespan < best_makespan:
                    best_makespan = individual.makespan
                    best_parent = individual
            Parents.append(best_parent)
        # Crossover ox
        for i in range(0, len(Parents), 2):
            if i + 1 < len(Parents):
                Children.append(ox(Parents[i].ids, Parents[i + 1].ids, machines))
                Children.append(ox(Parents[i + 1].ids, Parents[i].ids, machines))
        # for i in range(len(Parents)):
        #     Children.append(ox(Parents[i].ids, Parents[i - 1].ids, machines))
        # Mutation swap
        for child in Children:
            if rand.random() < pm:  # mutation probability
                swap(child, machines)
        Population = Children.copy()
    best = None
    best_ms = float("inf")
    for s in Population:
        if s.makespan < best_ms:
            best_ms = s.makespan
            best = s
    return Population, best


def simulatedAnnealing(
    subject, machines, temp=500, cooling_rate=0.999, iterations=10000
):
    rand.shuffle(subject)
    current_sol = solution(subject, machines)[-1]
    current_subject = Subject_solution(subject, current_sol)
    for _ in range(iterations):
        temp_subject = current_subject.copy()
        swap(temp_subject, machines)
        if temp_subject.makespan < current_sol:
            current_sol = temp_subject.makespan
            current_subject = temp_subject.copy()
        elif rand.random() < 2.71828 ** ((current_sol - temp_subject.makespan) / temp):
            current_sol = temp_subject.makespan
            current_subject = temp_subject.copy()
        temp *= cooling_rate
    return current_subject


def run_comparison(subject, machines, runs=10, algorithms=None):
    # default to all algorithms if none specified
    if algorithms is None:
        algorithms = ["Random Search", "Greedy", "GA", "SA"]

    results = {name: [] for name in algorithms}

    algo_map = {
        "Random Search": lambda: randomSearch(subject, machines)[1],
        "Greedy": lambda: greedy(subject, machines)[1],
        "GA": lambda: genetic(subject, machines, generations=100)[1].makespan,
        "SA": lambda: simulatedAnnealing(subject, machines).makespan,
    }

    for _ in range(runs):
        for name in algorithms:
            results[name].append(algo_map[name]())

    print(f"{'Algorithm':<20} {'Best':>8} {'Worst':>8} {'Avg':>8} {'Std':>8}")
    print("-" * 56)
    for name, data in results.items():
        std = statistics.stdev(data) if len(data) > 1 else 0
        print(
            f"{name:<20} {min(data):>8} {max(data):>8} {statistics.mean(data):>8.1f} {std:>8.2f}"
        )
    print(f"\nKnown UB: {UB} | Known LB: {LB}")


# all algorithms
run_comparison(subject, machines)

# just SA and Random Search
# run_comparison(subject, machines, algorithms=["Greedy", "Random Search"])
