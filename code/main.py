import argparse
from Simulation import simulation
from Grid import Grid
from GA import GA

parser = argparse.ArgumentParser()
parser.add_argument("-vis", action="store_true")
parser.add_argument("-test", action="store_true")

# agent types
parser.add_argument("-lookahead", action="store_true")
parser.add_argument("-detouring", action="store_true")
parser.add_argument("-signalling", action="store_true")

# chance for agent to spawn
parser.add_argument("-density", default=2.3, type=float)

# how much pheromone / pheromone & distance is taken into account
parser.add_argument("-alpha", default=0, type=int)

# simulation attributes
parser.add_argument("-t_max", default=20000, type=int)
parser.add_argument("-roads", default=5, type=int)
parser.add_argument("-speed", default=50, type=int)

# detouring attributes
parser.add_argument("-spread_pct", default=0.5, type=float)
parser.add_argument("-p_dropoff", default=1, type=float)
parser.add_argument("-p_weight", default=1, type=int)
parser.add_argument("-d_weight", default=1, type=int)

# genetic algorithm parameters
parser.add_argument("-ga", action="store_true")
parser.add_argument("-max_gen", default=1000, type=int)
parser.add_argument("-pop_size", default=100, type=int)
parser.add_argument("-mutation_chance", default=2/5, type=float)
parser.add_argument("-tourney_size", default=5, type=int)

args = parser.parse_args()

if not args.lookahead and (args.signalling or args.detouring):
    raise Exception("can't have signalling without look ahead")

if not args.ga:

    # agents = grid.generate_agents(round_density=args.density, 
    #                             alpha=args.alpha, 
    #                             p_dropoff=args.p_dropoff,
    #                             p_weight=args.p_weight,
    #                             d_weight=args.d_weight,
    #                             spread_pct=args.spread_pct,
    #                             lookahead=args.lookahead,
    #                             detouring = args.detouring,
    #                             signalling_toggle=args.signalling)

    simulation = simulation()
    simulation.env_loop(round_density=args.density, 
                        alpha=args.alpha, 
                        t_max=args.t_max, 
                        vis=args.vis,
                        speed=args.speed,
                        roads=args.roads,

                        p_dropoff=args.p_dropoff,
                        p_weight=args.p_weight,
                        d_weight=args.d_weight,
                        spread_pct=args.spread_pct,
                        lookahead=args.lookahead,
                        detouring = args.detouring,
                        signalling_toggle=args.signalling)
    
elif args.ga:
    if __name__ == "__main__":
        genetic_algorithm = GA(max_gen=args.max_gen,
                            pop_size=args.pop_size,
                            roads=args.roads,
                            t_max=args.t_max,
                            mutation_chance=args.mutation_chance,
                            density=args.density,
                            lookahead=args.lookahead,
                            detouring=args.detouring,
                            p_dropoff=args.p_dropoff,
                            signalling=args.signalling,
                            tourney_size = args.tourney_size)
        genetic_algorithm.run()
