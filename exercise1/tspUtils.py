import random
import math

def generateInstance(size, seed=1):
    rd = random.Random(seed)
    firstCities = [(rd.uniform(-3,0), rd.uniform(-3,0)) for _ in range(math.floor(size/2))]
    secondCities = [(rd.uniform(0,3), rd.uniform(0,3)) for _ in range(math.ceil(size/2))]
    return firstCities + secondCities

def evaluate(instance, ordering):
    sum = 0
    for i in range(len(ordering)):
        dx = instance[ordering[i]][0] - instance[ordering[(i+1)%len(ordering)]][0]
        dy = instance[ordering[i]][1] - instance[ordering[(i+1)%len(ordering)]][1]
        sum += math.sqrt(dx*dx + dy*dy)

    return sum
