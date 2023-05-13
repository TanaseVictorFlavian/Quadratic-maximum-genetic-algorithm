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

# generation counter
gen_counter = 1

# initial population
initial_population = [Chromosome(value=round(random.uniform(
    c1, c2 + 10 ** (-p)), p), index=i + 1) for i in range(pop_dimension)]

g.write("Populatia initiala\n\n")

for i, ch in enumerate(initial_population):
    ch.fitness = fc.quadratic(a, b, c, ch.value)
    ch.binary = fc.encode(c1, c2, p, ch.value)
    g.write(f"{str(ch)}\n")

"""SELECTION STEP"""

# sum of all fitnesses
F = sum(ch.fitness for ch in initial_population)

g.write("\nProbabilitati selectie\n\n")


for ch in (initial_population):
    ch.probability = ch.fitness / F
    g.write(f"\tcromozom {ch.index:4} P({ch.index}) = {ch.probability}\n")

g.write("\nIntervale probabilitati selectie\n\n")

# selection intervals
intervals = fc.get_intervals([ch.probability for ch in initial_population])

# prints the intervals
fc.print_intervals(intervals, g)

g.write("\nSelectia indivizilor\n\n")

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
    g.write(f"\tu = {u : <20} selectam cromozomul {interval_index :4}\n")

g.write("\nDupa selectie\n\n")

for ch in new_population:
    g.write(f"{str(ch)}\n")


"""CROSSOVER STEP"""

g.write(f"\nProbabilitatea de incrucisare {crossover_p}\n\n")

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

    g.write(f"{print_string}\n")

g.write(f"\nIncrucisare\n\n")

m //= 2

for i in range(m):
    child1, child2 = fc.crossover(
        breeding[i], breeding[i + m], a, b, c, p, gen_counter, c1, c2, g)
    # we saved the parent's index so we know where to replace them
    new_population[child1.index - 1] = child1
    new_population[child2.index - 1] = child2

g.write("Dupa recombinare\n\n")

for ch in new_population:
    g.write(f"{str(ch)}\n")

"""MUTATION STEP"""

g.write(f"\nProbabilitatea de mutatie pentru fiecare gena {mutation_p}\n\n")
g.write("\nAu fost modificati urmatorii cromozomi:\n\n")

for ch in new_population:
    new_ch = fc.mutation(ch, mutation_p, a, b, c, p, gen_counter, c1, c2, g)
    new_population[new_ch.index - 1] = new_ch

g.write("\nDupa mutatie\n\n")

for ch in new_population:
    g.write(f"{str(ch)}\n")

g.write("\nEvolutia maximului\n\n")
g.write(f"    Generatia {gen_counter}\n")
g.write(f"\tMax fitness = {fc.maxFitness(new_population)}\n")
g.write(f"\tMean fitnes = {fc.meanFitness(new_population)}\n\n")

# we pass to the next generation and repeat the process

gen_counter += 1

while(gen_counter <= num_gen):
    initial_population = new_population

    """SELECTION STEP"""

    # sum of all fitnesses

    F = sum(ch.fitness for ch in initial_population)

    for ch in (initial_population):
        ch.probability = ch.fitness / F

    # selection intervals
    intervals = fc.get_intervals([ch.probability for ch in initial_population])

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

    """CROSSOVER STEP"""

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

    m //= 2

    for i in range(m):
        child1, child2 = fc.crossover(
            breeding[i], breeding[i + m], a, b, c, p, gen_counter, c1, c2, g)
        # we saved the parent's index so we know where to replace them
        new_population[child1.index - 1] = child1
        new_population[child2.index - 1] = child2

    """MUTATION STEP"""

    for ch in new_population:
        new_ch = fc.mutation(ch, mutation_p, a, b, c,
                             p, gen_counter, c1, c2, g)
        new_population[new_ch.index - 1] = new_ch

    g.write(f"    Generatia {gen_counter}\n")
    g.write(f"\tMax fitness = {fc.maxFitness(new_population)}\n")
    g.write(f"\tMean fitnes = {fc.meanFitness(new_population)}\n")

    gen_counter += 1
