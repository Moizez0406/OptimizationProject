import random as rand

def shuffle(lst):
    rand.shuffle(lst)

class RNG:
    def __init__(self, seed=42):
        self.state = seed
    def next(self):
        self.state = (1664525 * self.state + 1013904223) % (2**32)
        return self.state / (2**32)

rng = RNG()

def shuffle(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = int(rng.next() * (i + 1))
        lst[i], lst[j] = lst[j], lst[i]
