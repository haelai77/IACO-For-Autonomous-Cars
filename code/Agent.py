import random
import numpy as np
import numpy.typing as npt
from numpy.random import choice
from collections import defaultdict

class Agent:
    def __init__(self, src, grid=None, ID=None, pheromone = 0, alpha = 5, decay=0.9, spread=0.5, p_dropoff = 1) -> None:
        self.pheromone = pheromone
        self.delay = 0
        self.alpha = alpha
        self.decay = decay
        self.spread = spread
        self.spread_decay = p_dropoff

        # grid related attributes
        self.src: tuple = src[:2] # starting coordinates
        self.src_side = src[2] # not to be confused with direction of travel
        
        self.grid = grid # grid with roads representing directions
        self.grid_coord: tuple = self.src # current coordinate in cell
        self.grid.tracker[self.grid_coord] = self

        self.dst: tuple = None # ending coordinates
        self.dst_side = None
        self.final_road_len = grid.BLOCK_SIZE
        self.exit_junc = None
        self._init_dst() # randomly assigns a possible destination

        # agent attributes
        self.ID = ID 
        self.direction = self.grid.grid[self.src] # direction of current cell

        # the number of possible moves to move in each direction
        self.moveset = {
            "n": 0,
            "s": 0,
            "e": 0,
            "w": 0}
        
        # how the grid coordinate is updated when travelling in each of these directions
        self.cardinal_move = {
            "n": (-1,  0),
            "s": ( 1,  0),
            "e": ( 0,  1),
            "w": ( 0, -1)}
        
        self.intercard_move = defaultdict(set)

        # to remove possible moves from self.intercard_move, e.g. if you ran out of north moves, n, you would look in the "ne" and "nw" sections fo intercard_move to remove north from the associated sets
        self.remove_opt = {
            "n": ["ne", "nw"],
            "s": ["se", "sw"],
            "e": ["ne", "se"],
            "w": ["nw", "sw"],}
        
        # determines whether the final stretch of road is self.grid.BLOCK_SIZE or self.grid.BLOCK_SIZE + 1 
        self.alt_dist = {
            ("n", "w"): 1,
            ("e", "n"): 1,
            ("s", "e"): 1,
            ("w", "s"): 1,
            ("n", "s"): self.src[1] < self.dst[1], 
            ("e", "w"): self.src[0] < self.dst[0], 
            ("s", "n"): self.src[1] > self.dst[1], 
            ("w", "e"): self.src[0] > self.dst[0]}
        
        # for calculating which junction is associated with the exit
        self.exit_junc_type = {
            "n": (self.final_road_len, 0),
            "s": (-self.final_road_len, 0),
            "e": (0, -self.final_road_len),
            "w": (0, self.final_road_len)}
        
        # for checking diagonal cell when entering junction
        self.diag_check = {
            "n": (-1,  1),
            "s": ( 1, -1),
            "e": ( 1,  1),
            "w": (-1, -1)}

        self._set_finalroad()
        self._init_moveset() # calculates the moves required to get to destination
        self.exit_junc = (np.add(self.dst, self.exit_junc_type[self.dst_side])) # retrieves element instantiated in loop yikes

    def _set_finalroad(self):
        if (self.src_side, self.dst_side) in self.alt_dist:
            self.final_road_len += self.alt_dist[(self.src_side, self.dst_side)]

    def _init_dst(self):
        '''finds suitable destination and sets current direction'''
        selected = False
        while not selected:
            dst_choice = random.choice(self.grid.exits) # selects random destination  
            if self.src[0] != dst_choice[0] and self.src[1] != dst_choice[1]: # set destination if y and x are not the same
                selected = True
                self.dst = dst_choice[:2]
                self.dst_side = dst_choice[2]
        
    def _init_moveset(self):
        '''sets up moveset and possible intercardinal directions'''
        moves = np.subtract(self.src, self.dst[:2])
        if moves[0] < 0: # if y diff is neg we go south else north
            self.moveset["s"] = abs(moves[0])
            self.intercard_move["se"].add("s")
            self.intercard_move["sw"].add("s")
        else:
            self.moveset["n"] = (moves[0])
            self.intercard_move["ne"].add("n")
            self.intercard_move["nw"].add("n")

        if moves[1] < 0: # if x is negative go east else go west
            self.moveset["e"] = abs(moves[1])
            self.intercard_move["ne"].add("e")
            self.intercard_move["se"].add("e")
        else:
            self.moveset["w"] = (moves[1])
            self.intercard_move["sw"].add("w")
            self.intercard_move["nw"].add("w")

    def possible_move(self, move_result) ->  bool:
        '''
        checks if move is good and updates location in tracking grid
        -> returning false is a good thing i.e. the move is possible
        '''
        next_cell = self.grid.tracker[move_result[0], move_result[1]]
        # if next square is an intercardinal cell we want to check the top right adjacent cell relative to direction of travel of agent
        if self.direction in self.cardinal_move and self.grid.grid[move_result[0], move_result[1]] in self.intercard_move and not next_cell:
            diag = np.add(self.diag_check[self.direction], self.grid_coord)
            if not self.grid.tracker[diag[0], diag[1]]: # if relative top right diagonal cell is empty in junction
                self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
                self.grid.tracker[move_result[0], move_result[1]] = self
                return False
        elif not next_cell: # if next cell is empty and you're on a straight road
            self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
            self.grid.tracker[move_result[0], move_result[1]] = self
            return False
        return True
##############################################################
    def pheromone_choice(self):
        '''only used at junctions, should take into account whether or not you're at exit junction'''
        directions = list(self.intercard_move[self.direction])

        # case 1: theres is only one option in the possible directions to turn (this move should always be possible due to removing turn options at the end of each move if moveset is zero)
        if len(directions) == 1:
            return directions[0]
        
        # case 2: if at edge return exit move if at exit junction else return alternative move
        possible_turns = [self.moveset[move_choice] == self.final_road_len and move_choice == self.dst_side and tuple(self.grid_coord) != tuple(self.exit_junc) for move_choice in directions]
        if sum(possible_turns) == 1: # if sum is 1 then we are at the edge of the grid    
            for index, entry in enumerate(possible_turns):
                if not entry: return directions[index]

        # case 3: you need to look ahead in each direction you are travelling in and determine which option is best for self based on formulas specified in Fabrice's paper
        found_flags = [0] * 2 # will always be 2 options in vanilla version
        pheromones = [None] * len(directions)
        next_check = [np.add(self.grid_coord, self.cardinal_move[direction]) for direction in directions]
        
        while not (found_flags[0] and found_flags[1]):
            for index, direction in enumerate(directions):
                if not found_flags[index] and not (0 <= next_check[index][0] <= self.grid.CELLS_IN_HEIGHT-1 and 0 <= next_check[index][1] <= self.grid.CELLS_IN_WIDTH-1):
                    pheromones[index] = 0
                    found_flags[index] = 1 
                elif not found_flags[index]:
                    cell = self.grid.tracker[next_check[index][0], next_check[index][1]]
                    if cell:
                        pheromones[index] = cell.pheromone
                        found_flags[index] = 1
                    next_check[index] = np.add(next_check[index], self.cardinal_move[direction])
        try:
            weights = [1/((1+pheromone)**self.alpha) for pheromone in pheromones]
        except:
            raise Exception(f"ERROR: phero: {pheromones}, alpha: {self.alpha}")
        probability_A = weights[0]/sum(weights)
        probability_B = 1 - probability_A
        return choice(directions, p=[probability_A, probability_B])
##############################################################
    def spread_helper_1(self):
        '''helper function that looks directly behind agent (one direction)'''
        spread_counter = 0 # counts how far away the cell the agent is checking
        pheromone_spread = self.pheromone * self.spread

        next_check = np.subtract(self.grid_coord, self.cardinal_move[self.direction]) # only need to subtract
        while True:
            spread_counter += 1
            if not (0 <= next_check[0] <= self.grid.CELLS_IN_HEIGHT-1 and 0 <= next_check[1] <= self.grid.CELLS_IN_WIDTH-1): # if not within bounds
                self.pheromone = max(0, self.pheromone - pheromone_spread) # avoids any floating point error going negative
                return []
            else:
                cell = self.grid.tracker[next_check[0], next_check[1]]
                self.pheromone = max(0, self.pheromone - pheromone_spread) # avoids any floating point error going negative
                if cell:
                    return [(cell, pheromone_spread * (self.spread_decay ** spread_counter))] # return agent behind and pheromone it needs to update
                next_check = np.subtract(next_check, self.cardinal_move[self.direction])

    def spread_helper_2(self):
        '''function that helps spread pheromone in 2 directions when at junction i.e. if you are at a NE cell you can spread backwards and west wards as those 2 directions can arrive onto the NE cell'''
        pheromone_spread = self.pheromone * self.spread
        
        spread_counter = 0 # counts how far away the cell the agent is checking
        next_check = [np.subtract(self.grid_coord, self.cardinal_move[direction]) for direction in self.direction] # next cells to check in each direction
        agents_found = []
        found_flags = [0] * 2

        while not (found_flags[0] and found_flags[1]):
                spread_counter += 1
                for index, direction in enumerate(self.direction):
                    # out of bounds = set found flag so you don't have to check / do any more adding, makes use of short circuiting so skips comparisons
                    if not found_flags[index] and not (0 <= next_check[index][0] <= self.grid.CELLS_IN_HEIGHT-1 and 0 <= next_check[index][1] <= self.grid.CELLS_IN_WIDTH-1):
                        found_flags[index] = 1 
                    elif not found_flags[index]:
                        # if cell contains an agent add it to the found agents list
                        cell = self.grid.tracker[next_check[index][0], next_check[index][1]]
                        if cell: 
                            agents_found.append((cell, pheromone_spread * (self.spread_decay ** spread_counter)))
                            found_flags[index] = 1
                        next_check[index] = np.subtract(next_check[index], self.cardinal_move[direction])

        self.pheromone = max(0, self.pheromone - pheromone_spread)
        return agents_found

    def spread_pheromone(self) -> tuple[int]:
        '''returns list of tuple/iterator of (agent, pheromone update value)'''
        # straight road case: you just look in opposite to direction of travel
        if self.direction in self.cardinal_move:
            return self.spread_helper_1()
        
        # junction cell case: you need to spread out in 2 directions, backwards to direction fo travel and opposite to the possible turning direction
        elif self.direction in self.intercard_move:
            return self.spread_helper_2()
    
##############################################################
    def move(self):
        '''currently does move based with a probability of selecting turn randomly -> this will eventually be influenced by pheromones'''
        ###############################################
        # # for bug fixing
        if self.ID == "tracker":
            self.pheromone=1000
            return 1

        ###############################################
        # NOTE: always decay even if waiting (this also occurs after pheromone is updated)
        self.pheromone = self.pheromone * self.decay

        if self.dst == tuple(self.grid_coord):
            self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
            return False
        ###############################################
        # case 1: straight road -> move ahead if possible
        elif self.direction in self.moveset and self.moveset[self.direction] > 0: # if cardinal direction and possible to move
            move_choice = self.direction
        ###############################################
        # case 2: you're at a junction and you need to make a choice based on pheromones
        elif self.direction in self.intercard_move:
            move_choice = self.pheromone_choice()
        ###############################################
        # if proposed move is not blocked by agent car
        if self.possible_move(np.add(self.grid_coord, self.cardinal_move[move_choice])):
            self.delay += 1
            self.pheromone += 1
            return True
        ###############################################
        # update attributes
        self.moveset[move_choice] -= 1 # update moveset
        self.grid_coord = np.add(self.grid_coord, self.cardinal_move[move_choice]) # update grid coordinate
        self.direction = self.grid.grid[self.grid_coord[0], self.grid_coord[1]] # update direction
        ###############################################
        # removes possible move from junction if moveset deems it impossible
        if self.moveset[move_choice] == 0 and tuple(self.grid_coord) != self.dst:
            for junc_cell in self.remove_opt[move_choice]:
                self.intercard_move[junc_cell].remove(move_choice)
        return True
    