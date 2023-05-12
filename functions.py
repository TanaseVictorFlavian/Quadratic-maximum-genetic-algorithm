import math
from chromosome import Chromosome
import random


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
    print("\t[{:<20}, {:<20}]".format(intervals[i], 1))


def get_intervals(fitness, F):
    # calculates the ends of the selection intervals
    intervals = [0]
    p_sum = 0
    for fit in fitness:
        p_sum += fit
        intervals.append(p_sum / F)

    return intervals


def binary_crossover(ch1, ch2, i):
    # returns a tuple with the new binary representation
    # of the two chromosomes
    return(ch1.binary[: i] + ch2.binary[i:], ch2.binary[: i] + ch1.binary[i:])


def crossover(ch1: Chromosome, ch2: Chromosome, a, b, c, p):
    print(
        f"\t Recombinare intre cromozomul {ch1.index} si cromozomul {ch2.index}")
    l = calculate_l(a, b, p)
    breaking_point = random.randint(0, l)
    print(f"\t {ch1.binary} {ch2.binary} punct {breaking_point}")

    # each child inherits one of its parent's index
    child1 = Chromosome(index=ch1.index)
    child2 = Chromosome(index=ch2.index)

    # get the children binary strings
    child1.binary, child2.binary = binary_crossover(ch1, ch2, breaking_point)

    print(f"Rezultat {child1.binary} {child2.binary}\n")

    # calculate children's value
    child1.value = decode(a, b, p, child1.binary)
    child2.value = decode(a, b, p, child2.binary)

    # calculate children's fitness
    child1.fitness = quadratic(a, b, c, child1.value)
    child2.fitness = quadratic(a, b, c, child2.value)

    return (child1, child2)
