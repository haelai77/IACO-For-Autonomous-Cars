from Grid import Grid
import argparse
from numpy.random import normal
from main import env_loop
import random

parser = argparse.ArgumentParser()
parser.add_argument("-max_gen", default=1000, type=int)
parser.add_argument("-pop_size", default=100, type=int)
parser.add_argument("-roads", default=5, type=int)
parser.add_argument("-density", default=2.3, type=float)
parser.add_argument("-t_max", default=5000, type=int)
args = parser.parse_args()

Lookahead_Agent = True
detouring = True
signalling_toogle = True
round_density = 3

def initialise_pop(pop_size = 100):
    # generate inital population with random paramenters
    pop = [None] * pop_size
     
    init_vals = {
        "spread_pct" : 0.5,
        "p_dropoff"  : 1, # 1 = no dropoff
        "p_weight"   : 1,
        "d_weight"   : 10,
        "alpha"      : 1}
    
    for i in range(pop_size):
        genome = {
            "spread_pct" : max(0,init_vals["spread_pct"] + round(normal(loc=0, scale=0.075),3)),
            "p_dropoff"  : min(1, init_vals["p_dropoff"] + round(normal(loc=0, scale=0.05))),
            "p_weight"   : max(0, init_vals["p_weight"] + round(normal(loc=0, sacle=5))),
            "d_weight"   : max(0, init_vals["p_weight"] + round(normal(loc=0, sacle=5))),
            "alpha"      : max(0, init_vals["p_weight"] + round(normal(loc=0, sacle=0.4))),
            "fitness"    : 0
        }
        pop[i] = genome

    return pop

def assess_fitness(population):
    # take mean of last 1000 time step delay
    # run all simulations
    assessed_pop = []

    for individual in population:
        grid = Grid(num_roads_on_axis = args.roads)

        agents = grid.generate_agents(round_density=round_density,
                                      lookahead_agent=Lookahead_Agent,
                                      detouring=detouring,
                                      signalling_toggle=signalling_toogle,
                                      **individual)
        
        average_delay = env_loop(grid=grid,
                                       agents=agents,
                                       GA=True,
                                       t_max=args.t_max,

                                       round_density=round_density,
                                       lookahead_agent=Lookahead_Agent, 
                                       detouring=detouring, 
                                       signalling_toggle=signalling_toogle,
                                       **individual)
        individual["fitness"] = average_delay * -1

    return sorted(assessed_pop, key= lambda d: d["fitness"], reverse=True) 

def tournament(population, tournament_size):
    competitors = random.sample(population, tournament_size)

    winner = competitors.pop()
    while competitors:
        i = competitors.pop()
        if i["fitness"] > winner["fitness"]:
            winner = i
    return winner

def cross(p1, p2):
    pass

def breed(population, tournament_size, elitism, crossover=0.5):
    # cross over attributes of parents
    offspring = []

    if elitism:
        offspring.append(population[0])
    
    while len(offspring) < len(population):
        parent1 = tournament(population, tournament_size=tournament_size)
        # if random.random() < crossover:
        parent2 = tournament(population, tournament_size=tournament_size)
        offspring.append(cross(parent1, parent2))

    return offspring    

def mutate():
    # applied to population after breading
    mutation_rates = {
        "spread_pct": 0.1,
        "p_dropoff": 0.05,
        "p_weight": 1,
        "d_weight": 1,
        "alpha": 1}
    

def run_ga():
    max_gen = args.max_gen
    gen = 0
    pop_size = 100

    #1 initialise population
    population = initialise_pop(pop_size=pop_size)

    #2 run simulations 5000 time steps each assess population
    assessed_pop = assess_fitness(population=population)

    # while not max getneration:
    while gen < max_gen:
        # breed
        breed(population=assessed_pop, tournament_size=5 , elitism=True)
        # mutate
        # assess
        gen += 1
