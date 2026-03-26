import random as rand
import load

# subject = [[1, 2, 3], [2, 3, 4], ...], where each is job time per Machine
# each inner list is a Machine: [J1([M1,M2,M3]), J2([M1,M2,M3]), ...]
jobs, machines, subject, UB, LB = load.load_taillard("tai20_10_0.fsp")
subject_ids = list(enumerate(subject))


def solution(subject, machines):
    time = [0 for _ in range(machines)]
    for jb in subject:
        for i in range(len(time)):
            if i == 0:
                time[i] += jb[i]
            else:
                time[i] = max(time[i], time[i-1]) + jb[i]
                continue
    return time


def randomSearch(subject, machines):
    Highest_solution = 10000000
    Best_subject = None
    temp_subject_ids = subject_ids.copy()
    for i in range(10000):
        rand.shuffle(temp_subject_ids)
        selected_subject = [job for idx, job in temp_subject_ids]
        sol = solution(selected_subject, machines)
        if Highest_solution > sol[-1]:
            Highest_solution = sol[-1]
            Best_subject = [(idx, job[:]) for idx, job in temp_subject_ids]
    return Best_subject, Highest_solution


def greedy(subject_ids, machines):
    temp_subject_ids = subject_ids.copy()  # remaining jobs to schedule
    Best_subject = [temp_subject_ids.pop(0)]  # start with first job
    rand.shuffle(temp_subject_ids)  # randomize order of remaining jobs
    while temp_subject_ids:
        current_sol = float('inf')  # best makespan found in this round
        current_job = None          # best candidate job found in this round

        for s in temp_subject_ids:  # s is (idx, job)
            current_step = [job for _, job in Best_subject] + [s[1]]
            ms = solution(current_step, machines)[-1]
            if ms < current_sol:
                current_sol = ms
                current_job = s  # remember best candidate

        # commit the winner of this round
        Best_subject.append(current_job)
        temp_subject_ids.remove(current_job)

    return Best_subject, current_sol


Best_subject, Highest_solution = randomSearch(subject, machines)
print(f"Best subject: {[idx for idx, job in Best_subject]}")
print(Highest_solution)
Best_subject, Highest_solution = None, None
Best_subject, Highest_solution = greedy(subject_ids, machines)
print(f"Best subject: {[idx for idx, job in Best_subject]}")
print(Highest_solution)
