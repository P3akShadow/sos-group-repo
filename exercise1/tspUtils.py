import random
import math

def generateInstance(size):
    firstCities = [(random.uniform(-3,0), random.uniform(-3,0)) for _ in range(math.floor(size/2))]
    secondCities = [(random.uniform(0,3), random.uniform(0,3)) for _ in range(math.ceil(size/2))]
    return firstCities + secondCities

def evaluate(instance, ordering):
    sum = 0
    for i in range(len(ordering)):
        dx = instance[ordering[i]][0] - instance[ordering[(i+1)%len(ordering)]][0]
        dy = instance[ordering[i]][1] - instance[ordering[(i+1)%len(ordering)]][1]
        sum += math.sqrt(dx*dx + dy*dy)

    return sum
