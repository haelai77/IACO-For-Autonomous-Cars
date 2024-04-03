from numpy.random import normal
from Simulation import simulation
import random
from multiprocessing import Pool
import os

class GA:
    def __init__(self, max_gen, pop_size, roads, t_max, mutation_chance, density=3, lookahead=False, detouring=False, p_dropoff=1, signalling=False, tourney_size=2) -> None:
        """current evolves individuals"""
        
        self.max_gen = max_gen
        self.pop_size = pop_size
        self.t_max = t_max
        self.mutation_chance = mutation_chance
        self.roads = roads

        self.density = density
        self.lookahead = lookahead
        self.detouring = detouring
        self.p_dropoff = p_dropoff
        self.signal = signalling
        self.tourney_size = tourney_size

        self.simulation = simulation()

    def initialise_pop(self, pop_size = 100):
        # generate inital population with random paramenters
        pop = [None] * pop_size
        
        init_vals = {
            "spread_pct" : 0.5,
            "p_dropoff"  : 1, # 1 = no dropoff
            "p_weight"   : 1,
            "d_weight"   : 10,
            "alpha"      : 5}
        
        for i in range(pop_size):
            genome = {
                "spread_pct" : max(0,init_vals["spread_pct"] + round(normal(loc=0, scale=0.075),3   )),
                "p_dropoff"  : min(1, init_vals["p_dropoff"] + round(normal(loc=0, scale=0.05)      )),
                "p_weight"   : max(0, init_vals["p_weight"]  + round(normal(loc=0, scale=5)         )),
                "d_weight"   : max(0, init_vals["p_weight"]  + round(normal(loc=0, scale=5)         )),
                "alpha"      : max(0, init_vals["p_weight"]  + round(normal(loc=0, scale=0.4)       )),
                "fitness"    : 0
            }

            pop[i] = genome

        return pop
    
    def sim_wrapper(self, kwargs):
        return self.simulation.env_loop(**kwargs)

    def assess_fitness(self, population):
        # take mean of last 1000 time step delay
        # run all simulations
        assessed_pop = []

        # for individual in population:
        template = {
            "GA":True,
            "t_max":self.t_max,
            "roads":self.roads,
            "round_density":self.density,
            "lookahead":self.lookahead, 
            "detouring":self.detouring, 
            "signalling_toggle":self.signal,}
        inputs = [ {**template.copy(), **(dict(list(individual.items())[:-1]))} for individual in population]
        
        # startime=time.time()
        with Pool(processes=self.pop_size) as individual_pool:
            average_delays = individual_pool.starmap(self.sim_wrapper, [(kwarg_set,) for kwarg_set in inputs])
        # average_delays = [self.sim_wrapper(i) for i in inputs]
        # endtime=time.time()
        # print(endtime-startime, "s")

        for i, individual in enumerate(population):
            individual["fitness"] = average_delays[i] * -1
            
        assessed_pop.append(individual)
        return sorted(assessed_pop, key= lambda d: d["fitness"], reverse=True) 

    def tournament(self, population, tournament_size):

        competitors = random.sample(population, tournament_size)

        winner = competitors.pop()
        while competitors:
            i = competitors.pop()
            if i["fitness"] > winner["fitness"]:
                winner = i
        return winner

    def cross(self, p1, p2):
        """2 point crossover"""
        keys = ["spread_pct", "p_dropoff", "p_weight", "d_weight", "alpha"]
        idx1 = random.choice(range(len(keys)))

        offspring = p1.copy()
        if idx1 == len(keys)-1: # in the case that an identical clone is spawned
            offspring["fitness"] = None
            return offspring

        idx2 = random.choice(range(idx1 + 1, len(keys)))

        for key in keys[idx1:idx2+1]:
            offspring[key] = p2[key]

        offspring["fitness"] = None # unassessed
        return offspring

    def breed(self, population, tournament_size, elitism, crossover=0.5):
        # cross over attributes of parents
        offspring = []
        if elitism:
            offspring.append(population[0])
        
        while len(offspring) < len(population):
            parent1 = self.tournament(population, tournament_size=tournament_size)
            parent2 = self.tournament(population, tournament_size=tournament_size)
            offspring.append(self.cross(parent1, parent2))


        return offspring    

    def mutate(self, population, mutation_chance, elitism=True):
        # applied to population after breading
        mutation_rates = {
            "spread_pct": round(normal(loc=0, scale=0.075),3   ), #95% within 1.5% change
            "p_dropoff" : round(normal(loc=0, scale=0.05)      ), #95% within 1.5 change
            "p_weight"  : round(normal(loc=0, scale=5)         ), 
            "d_weight"  : round(normal(loc=0, scale=5)         ),
            "alpha"     : round(normal(loc=0, scale=0.4)       ),
        }

        for individual in population[elitism:]:
            for key in mutation_rates:
                if random.random() < mutation_chance:
                    individual[key] += mutation_rates[key]
        
        return population

    def run(self):

        gen = 0

        #1 initialise population
        population = self.initialise_pop(pop_size=self.pop_size)

        #2 run simulations 5000 time steps each assess population
        assessed_pop = self.assess_fitness(population=population)
        best = assessed_pop[0]

        # while not max getneration:
        while gen < self.max_gen:
            gen += 1

            # breed
            offspring = self.breed(population=assessed_pop, tournament_size=self.tourney_size , elitism=True)
            # mutate
            mutants = self.mutate(population=offspring, elitism=True, mutation_chance=self.mutation_chance)
            # assess
            assessed_pop = self.assess_fitness(population=mutants)

            best = assessed_pop[0]
            print(best)
    