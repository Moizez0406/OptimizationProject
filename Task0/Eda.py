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
    best = None

    for _ in range(10000):
        perm = subject.copy()
        rand.shuffle(perm)

        ms = solution(perm, machines)[-1]
        sol = Subject_solution(perm, ms)

        if best is None or sol.makespan < best.makespan:
            best = sol

    return best


def greedy(subject, machines):
    temp = subject.copy()
    result = [temp.pop(0)]
    rand.shuffle(temp)

    while temp:
        best_job = None
        best_ms = float("inf")

        for job in temp:
            trial = result + [job]
            ms = solution(trial, machines)[-1]

            if ms < best_ms:
                best_ms = ms
                best_job = job

        result.append(best_job)
        temp.remove(best_job)

    return Subject_solution(result, solution(result, machines)[-1])


def genetic(
    subject,
    machines,
    population_size=180,
    generations=100,
    tournament_size=5,
    pm=0.1,
    px=0.8,
):
    Population = []

    # --- Initial population ---
    for _ in range(population_size):
        temp = subject.copy()
        rand.shuffle(temp)
        ms = solution(temp, machines)[-1]
        Population.append(Subject_solution(temp.copy(), ms))

    global_best = min(Population, key=lambda s: s.makespan)

    for _ in range(generations):
        Parents = []
        Children = []

        # --- Tournament selection (FIXED: population_size, not generations) ---
        for _ in range(population_size):
            tournament = rand.sample(Population, tournament_size)
            best = min(tournament, key=lambda s: s.makespan)
            Parents.append(best)

        # --- Crossover with probability px ---
        for i in range(0, len(Parents), 2):
            if i + 1 < len(Parents):
                p1 = Parents[i]
                p2 = Parents[i + 1]

                if rand.random() < px:
                    c1 = ox(p1.ids, p2.ids, machines)
                    c2 = ox(p2.ids, p1.ids, machines)
                    # recompute makespan
                    c1.makespan = solution(c1.permutation, machines)[-1]
                    c2.makespan = solution(c2.permutation, machines)[-1]
                    Children.extend([c1, c2])
                else:
                    # copy parents (like C++)
                    Children.extend([p1.copy(), p2.copy()])
        # --- Mutation ---
        for child in Children:
            if rand.random() < pm:
                swap(child, machines)
                # child.makespan = solution(child.permutation, machines)[-1]

        # --- Sort population & children ---
        Population.sort(key=lambda s: s.makespan)
        Children.sort(key=lambda s: s.makespan)

        # --- Elitism (top 20%) ---
        elite_count = population_size // 5
        new_pop = Population[:elite_count]

        # --- Fill rest with best children ---
        needed = population_size - elite_count
        new_pop.extend(Children[:needed])

        Population = new_pop

        # --- Update global best ---
        if Population[0].makespan < global_best.makespan:
            global_best = Population[0]
    return Population, global_best


def simulatedAnnealing(
    subject, machines, temp=500, cooling_rate=0.999, iterations=10000
):
    perm = subject.copy()
    rand.shuffle(perm)

    current = Subject_solution(perm, solution(perm, machines)[-1])
    best = current.copy()

    for _ in range(iterations):
        candidate = current.copy()
        swap(candidate, machines)

        delta = candidate.makespan - current.makespan

        if delta < 0 or rand.random() < pow(2.71828, -delta / temp):
            current = candidate

            if current.makespan < best.makespan:
                best = current.copy()

        temp *= cooling_rate

    return best


def run_comparison(subject, machines, runs=20, algorithms=None):
    # default to all algorithms if none specified
    if algorithms is None:
        algorithms = ["Random Search", "Greedy", "GA", "SA"]

    results = {name: [] for name in algorithms}

    algo_map = {
        "Random Search": lambda: randomSearch(subject, machines).makespan,
        "Greedy": lambda: greedy(subject, machines).makespan,
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
