from math import cos, pi

def rastrigin(values):
    a = 10
    n = len(values)

    factors = [(x*x-a*cos(2*pi*x)) for x in values]
    return a*n + sum(factors)
