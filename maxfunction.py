import random
import math
import functions as fc
import bisect
from chromosome import Chromosome
g = open("evolutie.txt", 'w')

with open("date.in", 'r') as f:
    file_lines = list(map(str.split, f.readlines()))
    # population dimension
    pop_dimension = int(file_lines[0][0])

    # domain interval ends
    c1, c2 = map(int, file_lines[1])

    # quadratic function coefficients
    a, b, c = map(int, file_lines[2])

    # precision
    p = int(file_lines[3][0])

    # crossover and mutation probabilities
    crossover_p, mutation_p = map(float, file_lines[4] + file_lines[5])

    # number of generations
    num_gen = int(file_lines[-1][0])

# initial population
initial_population = [Chromosome(value=round(random.uniform(
    c1, c2 + 10 ** (-p)), p), index=i + 1) for i in range(pop_dimension)]

print("Populatia initiala\n")

for i, ch in enumerate(initial_population):
    ch.fitness = fc.quadratic(a, b, c, ch.value)
    ch.binary = fc.encode(c1, c2, p, ch.value)
    print(ch)

# sum of all fitnesses
F = sum(ch.fitness for ch in initial_population)

print("\nProbabilitati selectie\n")


""" here e loop """


for ch in (initial_population):
    ch.probability = ch.fitness / F
    print(f"\tcromozom {ch.index:4} P({ch.index}) = {ch.probability}")

print("\nIntervale probabilitati selectie\n")

# selection intervals
intervals = fc.get_intervals([ch.fitness for ch in initial_population], F)

# prints the intervals
fc.print_intervals(intervals)

print("\nSelectia indivizilor\n")

# here will be stored the new population
new_population = []

for i in range(pop_dimension):
    u = random.uniform(0, 1)
    # performs a binary search in the intervals list
    # and finds the index of the interval u belongs to
    interval_index = bisect.bisect_left(intervals, u)

    # the selected chromosome that will be selected
    old_chromosome = initial_population[interval_index - 1]

    # the "new" chromosome that will have a new index in the new population
    new_chromosome = Chromosome(i + 1, old_chromosome.value, old_chromosome.binary,
                                old_chromosome.fitness, old_chromosome.probability)

    new_population.append(new_chromosome)
    print(f"\tu = {u : <20} selectam cromozomul {interval_index :4}")

print("\nDupa selectie\n")

for ch in new_population:
    print(ch)

print(f"\nProbabilitatea de incrucisare {crossover_p}\n")

breeding = []

# we'll use this variable to easily form disjoint pairs
m = 0

for ch in new_population:
    u = random.uniform(0, 1)
    print_string = f"\t{ch.index :4}: {ch.binary} u = {u : <20}"
    if u < crossover_p:
        breeding.append(ch)
        m += 1
        print_string += " < 0.25 participa la crossover"

    print(print_string)

print(f"\nIncrucisare\n")

m //= 2

for i in range(m):
    child1, child2 = fc.crossover(breeding[i], breeding[i + m], a, b, c, p)
    # we saved the parent's index so we know where to replace them
    new_population[child1.index - 1] = child1
    new_population[child2.index - 1] = child2

print("Dupa recombinare\n")

for ch in new_population:
    print(ch)

print(f"\nProbabilitatea de mutatie pentru fiecare gena {mutation_p}\n")

# to do functie pentru mutatie 
# mutation(new_population)
# l il scot din lungimea chromosome.binary

print("\nEvolutia maximului\n")