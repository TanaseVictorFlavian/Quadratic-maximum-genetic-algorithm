import math
from chromosome import Chromosome
import random
from typing import List


def calculate_l(a, b, p):
    # calculates the number of bits needed to represent
    # a number from the [a, b] interval
    # with precision p
    return math.ceil(math.log2((b - a) * 10 ** p))


def calculate_d(a, b, l):
    # calculates the step between intervals
    return (b - a) / (2 ** l)


def calculate_interval_start(a, d, nr):
    # find the left end of the interval that contains nr
    return int((nr - a) // d)


def binary_to_number(a, d, bin_num):
    # returns the decimal value of a binary number
    return a + d * int(bin_num, 2)


def quadratic(a, b, c, x):
    # return f(x) where f is the quadratic function
    return a * x ** 2 + b * x + c


def encode(a, b, p, number):
    # returns the binary representation of number
    l = calculate_l(a, b, p)
    d = calculate_d(a, b, l)
    return '{:0{}b}'.format(calculate_interval_start(a, d, number), l)


def decode(a, b, p, bitString):
    # gets a binary representation of a number
    # and returns its decimal value
    l = calculate_l(a, b, p)
    d = calculate_d(a, b, l)
    return binary_to_number(a, d, bitString)


def print_intervals(intervals: list):
    # prints intervals from a list of interval ends
    for i in range(len(intervals) - 2):
        print("\t[{:<20}, {:<20}]".format(intervals[i], intervals[i + 1]))
    print("\t[{:<20}, {:<20}]".format(intervals[i + 1], 1))


def get_intervals(probabilities):
    # calculates the ends of the selection intervals
    intervals = [0]
    p_sum = 0
    for p in probabilities:
        p_sum += p
        intervals.append(p_sum)

    return intervals


def binary_crossover(ch1: Chromosome, ch2: Chromosome, i):
    # returns a tuple with the new binary representation
    # of the two chromosomes
    return(ch1.binary[: i] + ch2.binary[i:], ch2.binary[: i] + ch1.binary[i:])


def crossover(ch1: Chromosome, ch2: Chromosome, a, b, c, p, gen_counter, c1, c2):
    l = calculate_l(a, b, p)
    breaking_point = random.randint(0, l)

    # each child inherits one of its parent's index
    child1 = Chromosome(index=ch1.index)
    child2 = Chromosome(index=ch2.index)

    # get the children binary strings
    child1.binary, child2.binary = binary_crossover(ch1, ch2, breaking_point)

    # calculate children's value
    child1.value = decode(c1, c2, p, child1.binary)
    child2.value = decode(c1, c2, p, child2.binary)

    # calculate children's fitness
    child1.fitness = quadratic(a, b, c, child1.value)
    child2.fitness = quadratic(a, b, c, child2.value)

    # log the changes only for the first generation
    if gen_counter == 1:
        print(
            f"\t Recombinare intre cromozomul {ch1.index} si cromozomul {ch2.index}")
        print(f"\t {ch1.binary} {ch2.binary} punct {breaking_point}")
        print(f"Rezultat {child1.binary} {child2.binary}\n")

    return (child1, child2)


def mutation(ch: Chromosome, mutation_p: float, a, b, c, p, gen_counter, c1, c2):
    new_binary = list(ch.binary)
    mutation_checker = False
    for bit in new_binary:
        u = random.uniform(0, 1)
        if u < mutation_p:
            mutation_checker = True
            if bit == '0':
                bit = '1'
            else:
                bit = '0'

    if mutation_checker:
        new_binary = "".join(new_binary)
        new_chromosome = Chromosome(index=ch.index, binary=new_binary)
        new_chromosome.value = decode(c1, c2, p, new_chromosome.binary)
        new_chromosome.fitness = quadratic(a, b, c, new_chromosome.value)

        # log the changes only for the first generation
        if gen_counter == 1:
            print(f"\t{new_chromosome.index}")
        
        return new_chromosome

    return ch

def maxFitness(popultion : List[Chromosome]):
    return max(popultion, key= lambda x : x.fitness).fitness

def meanFitness(population : List[Chromosome]):
    return (sum (x.fitness for x in population) / len(population))