import random, math
from sudoku import Sudoku


# Student TODO: Modify This (optional)
#
# This is the function that will be used by the genetic algorithm as the fitness function
# As I have implemented it, it counts up the number of unique integers on each row, each
# column, and each square, and sums them. The maximum possible fitness of a solved sudoku
# board given this evaluation function is 81*3 = 243. 
#
# You can change this function if you want (and probably should) to something more clever.
# Even though it works as-is, genetic algorithms tend to work better if the difference in
# fitness between good individuals and poor ones is much larger than this linear function.
#
# In your testing, try out different fitness functions to see if your genetic algorithm is
# able to solve all of them! For example, try returning sum(array) as the fitness and watch
# as your GA turns all the values to 9 (try with the the solution). Or, change the fitness
# function so that it only cares about unique values in the columns, and watch it solve that
# quite quickly. Your GA should be able to solve trivial fitness functions to get full marks
# on the assignment. Some examples I will be using are:
#
# sum(array)    (maximize sum)
# -sum(array)   (minimize sum)
# sudoku rows only
# sudoku columns only
# full sudoku board (get close to solution)
#
def eval_sudoku(array):
    # return sum(array)  # un-comment this line and watch the GA optimize to all max numbers
    # return -sum(array) # un-comment this line and watch the GA optimize to all ones
    s = Sudoku(0)
    size = int(math.sqrt(len(array)))
    s.set_arr(array)
    fitness = 0
    # count unique values in each row
    for r in range(s.size()):
        vals = set()
        for c in range(s.size()):
            vals.add(s.get(r, c))
        fitness += len(vals)
    # count unique values in each column
    for c in range(s.size()):
        vals = set()
        for r in range(s.size()):
            vals.add(s.get(r, c))
        fitness += len(vals)
    # count unique values in each square
    sqsize = int(math.sqrt(s.size()))
    for sr in range(sqsize):
        for sc in range(sqsize):
            vals = set()
            for r in range(sqsize):
                for c in range(sqsize):
                    vals.add(s.get(sr * sqsize + r, sc * sqsize + c))
            fitness += len(vals)
    return fitness


# the class that stores the genetic algorithm settings
class GASettings:
    # we need something in here so that python doesn't complain about blank classes
    description = 'Blank struct to hold our GA settings in'


# TODO: Modify this function (optional)
#
# The function which returns the settings you will use back to the main function,
# these will then be used by evolve() below. Try and tweak the settings so that 
# you get better solutions to the sudoku puzzle it's not necessary for most marks, 
# but better settings probably exist. 
def get_ga_settings(sudoko_size):
    settings = GASettings()
    settings.individual_values = [(i + 1) for i in range(sudoko_size)]  # list of possible values individuals can take
    settings.individual_size = sudoko_size * sudoko_size  # length of an individual
    settings.fitness_function = eval_sudoku  # the fitness function of an individual
    settings.population_size = 100  # total size of each population                             (experiment with this)
    settings.elitism_ratio = 0.2  # select top x% of individuals to survive                   (experiment with this)
    settings.parent_roulette_ratio = 0.2  # select x% of population as parents via roulette wheel     (experiment
    # with this)
    settings.mutation_rate = 0.2  # mutation rate percentage                                  (experiment with this)
    settings.crossover_index = settings.individual_size // 2  # the index to split parents for recombination

    return settings


# Student TODO: Implement This Function (required)
#
# This is the main function that you must implement for Assignment 4
# Follow the class notes and the pseudocode below to implement a one-generation update
# of a genetic algorithm. What you must include is listed in the algorithm below.
#
# args:
#
#   population - A list of individuals, each of which are a 1D list representing a 'flattened'
#                sudoku candidate solution. 
#
#   settings   - An instance of a GAsettings object which uses the settings within it to compute
#                the next generation's population
#
# returns:
#
#   next_population - The next population after a one-generation genetic algorithm evolution
#
def roulette_select(population):
    max = sum(population)
    select = random.uniform(0, max)
    current = 0
    for i, p in enumerate(population):
        current += p
        if current > select:
            return i


def evolve(population, settings):
    # 1. First, it is very useful to store the fitness of each of the individuals in a separate
    # array, pop_fitness, such that pop_fitness[i] = fitness(population[i])
    #
    # pop_fitness = [calculate fitnesses of population]
    pop_fitness = [settings.fitness_function(x) for x in population]

    # 2. The next step is to select the parents that will be used to generate the next generation's
    # offspring. This will be done via roulette wheel selection, covered in class. You should
    # store these parents in a list called 'parents'. The number of parents P you should select:
    P = int(settings.parent_roulette_ratio * len(population))

    parents = []
    while len(parents) < P:
        parents.append(population[roulette_select(pop_fitness)])
    #
    #
    # 3. Let's now define a blank list which will hold the next population's individuals. At the
    # end of this function, it should be the same size as the previous population.
    #
    next_population = []
    #
    #
    # 4. The next step is elite individual selection. You will select the top E fitness individuals
    # from input population and insert them into next_population, since they are elite, and chosen
    # to survive. The number E is equal to int(settings.elitism_ratio * len(population))
    # For example, if E is 2, and pop_fitness = [5, 3, 1, 7] then you will choose the first and last
    # individuals as the elite ones to add to the next population, since they have the top 2 fitnesses.
    E = int(settings.elitism_ratio * len(population))
    elite = sorted(range(len(pop_fitness)), key=lambda x: pop_fitness[x])[-E:]
    next_population.extend(elite)
    #
    # 5. Step 5 is the offspring generation (recombination) step. You will generate offspring until
    # you have enough to fill next_population to the size of the previous population. You will generate
    # offspring via crossover, with the # crossover index being defined in settings.crossover_index.
    # Pseudocode for generating children:
    #
    offspring = []
    while len(next_population) < len(population):
        mother = random.choice(parents)
        father = random.choice(parents)

        if mother == father:
            continue

        child1 = mother[:settings.crossover_index] + father[settings.crossover_index:]
        child2 = father[:settings.crossover_index] + mother[settings.crossover_index:]

        offspring.extend([child1, child2])

        # mother = choose random parent from parent list
        # father = choose random parent from parent list
        #   if (mother == father): continue
        #   child1 = crossover 1st part of mother with 2nd part of father
        #   child2 = crossover 2nd part of father with 1st part of mother
        #   add children to the offspring list


        #
        # 6. Step 6 is to mutate the offspring. You will mutate M of the offpspring, where M is defined
        # as int(settings.mutation_rate * len(offspring)). Do not mutate a single offspring twice. You
        # will perform mutation by changing a single element of the individual's array to a random legal
        # sudoku number, which are given in settings.individual_values
        M = int(settings.mutation_rate * len(offspring))
        mutated = set()

        for _ in range(M):
            i = random.randint(0, len(offspring) - 1)
            child = offspring[i]
            j = random.randint(0, len(child) - 1)

            if tuple(child) in mutated:
                continue

            child[j] = random.choice(settings.individual_values)

            offspring[i] = child

            mutated.add(tuple(child))

        next_population.append(offspring)
    # As a possible optimization, you can experiment with performing different types of mutations
    # here, but please add that as an option in your settings file, and explain it in your README.txt
    #
    # 7. Finally, you should combine your elite individual selection with your offspring to form
    # the next population, and return it as a single list. This function will then be called iteratively
    # which each new population. Each iteration is one generation.
    return next_population
