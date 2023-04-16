import random
from deap import base, creator, tools

# Define the fitness function
def my_fitness(individual):
    a, b, c, d, e, f, g, h = individual
    return (a + b) - (c + d) + (e + f) - (g + h),

# Set up the DEAP framework for the problem
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 0, 9)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=8)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", my_fitness)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=9, indpb=0.1)
toolbox.register("select", tools.selBest)

# Initialize the population
initial_population = [
    [6, 5, 4, 1, 3, 5, 3, 2],
    [8, 7, 1, 2, 6, 6, 0, 1],
    [2, 3, 9, 2, 1, 2, 8, 5],
    [4, 1, 8, 5, 2, 0, 9, 4]
]

# Set up the genetic algorithm parameters
pop = toolbox.population(n=len(initial_population))
pop[:] = [creator.Individual(ind) for ind in initial_population]

ngen = 100  # Number of generations
cxpb = 0.5  # Crossover probability
mutpb = 0.2  # Mutation probability

# Run the genetic algorithm
for gen in range(ngen):
    offspring = toolbox.select(pop, len(pop))
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < cxpb:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < mutpb:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluate the individuals with invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Replace the old population with the offspring
    pop[:] = offspring

# Get the best individual from the final population
best_ind = tools.selBest(pop, 1)[0]
print("Best individual is %s with fitness %s" % (best_ind, best_ind.fitness.values[0]))
