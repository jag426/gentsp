from itertools import product, tee
from math import sqrt
from random import random, randrange


def distance(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def pairwise(i):
    a, b = tee(i)
    next(b, None)
    return zip(a, b)


class Graph:
    def __init__(self, nodes=None, n=100):
        if not nodes:
            nodes = [(random(), random()) for _ in range(n)]
        self.nodes = nodes

    def evaluate(self, sol):
        order = list(map(
            lambda pair: pair[0],
            sorted(enumerate(sol.weights), key=lambda pair: pair[1])))
        path = map(lambda i: self.nodes[i], order)
        legs = pairwise(path)
        costs = map(lambda ps: distance(*ps), legs)
        return sum(costs)


class Sol:
    def __init__(self, mom=None, dad=None, n=100):
        if mom and dad:
            pivot = randrange(len(mom.weights))
            self.weights = mom.weights[:pivot] + dad.weights[pivot:]
        else:
            self.weights = [random() for _ in range(n)]


class Generation:
    def __init__(self, individuals=None, n=100):
        if not individuals:
            individuals = [Sol(n=n) for _ in range(100)]
        self.individuals = individuals
    
    def reproduce(self, graph):
        ordered = sorted(self.individuals, key=lambda s: graph.evaluate(s))
        chosen = ordered[:10]

        for s in chosen:
            print(graph.evaluate(s))

        pairings = product(chosen, repeat=2)
        offspring = [Sol(mom, dad) for mom, dad in pairings]

        print()
        print()
        return Generation(offspring)


if __name__ == "__main__":
    generations = 10
    n = 10000
    g = Graph(n=n)
    G = Generation(n=n)
    for _ in range(generations):
        G = G.reproduce(g)
