import random as rand


class Subject_solution:
    job_lookup = {}

    def __init__(self, permutation, makespan):
        self.permutation = permutation
        self.makespan = makespan

    def copy(self):
        return Subject_solution(self.permutation.copy(), self.makespan)

    @classmethod
    def set_lookup(cls, subject):
        cls.job_lookup = {job.id: job for job in subject}

    @classmethod
    def from_ids(cls, child_ids, machines):
        """Alternative constructor — build from a list of ids"""
        perm = [cls.job_lookup[id] for id in child_ids]
        ms = solution(perm, machines)[-1]
        return cls(perm, ms)

    @property
    def ids(self):
        return [job.id for job in self.permutation]

    def __repr__(self):
        return f"Subject_solution(makespan={self.makespan}, order={self.ids})"


# Subject_solution = S
# S[i] = (makespan=2103, order=[17, 8, ..., 11])
# S[i][1] = [17, 8, ..., 11]


def solution(jobs, machines):
    time = [0] * machines
    for jb in jobs:
        time[0] += jb.times[0]
        for i in range(1, machines):
            time[i] = max(time[i], time[i - 1]) + jb.times[i]
    return time


def swap(subject, machines):
    n = len(subject.permutation)
    i, j = rand.sample(range(n), 2)

    subject.permutation[i], subject.permutation[j] = (
        subject.permutation[j],
        subject.permutation[i],
    )

    subject.makespan = solution(subject.permutation, machines)[-1]


def ox(parent1, parent2, machines):
    child_ids = [None for _ in range(len(parent1))]
    i = rand.randint(0, len(parent1) - 1)
    j = rand.randint(0, len(parent1) - 1)
    if i > j:
        i, j = j, i
    child_ids[i:j] = parent1[i:j]
    for gene in parent2:
        if gene not in child_ids:
            for k in range(len(child_ids)):
                if child_ids[k] is None:
                    child_ids[k] = gene
                    break
    return Subject_solution.from_ids(child_ids, machines)
