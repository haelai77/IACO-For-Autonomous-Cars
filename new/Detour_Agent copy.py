import random
import numpy as np
import numpy.typing as npt
from numpy.random import choice
from collections import defaultdict, deque

class Detour_Agent:
    def __init__(self, src, grid=None, ID=None, pheromone = 0, alpha = 5, decay=0.9, spread=0.5, spread_decay = 0, p_weight = 1, d_weight = 1.5) -> None:
        self.pheromone = pheromone
        self.delay = 0
        self.alpha = alpha
        self.decay = decay
        self.spread = spread
        self.spread_decay = spread_decay

        # move buffer for executive moves where agent doesn't get to choose
        self.move_buffer = deque()
        self.buffered_move_flag = False
        self.p_weight = p_weight
        self.d_weight = d_weight

        # grid related attributes
        self.src: tuple = src[:2] # starting coordinates
        self.src_side = src[2] # not to be confused with direction of travel
        
        self.grid = grid # grid with roads representing directions
        self.grid_coord = self.src # current coordinate in cell
        self.grid.tracker[self.grid_coord] = self

        self.dst: tuple = None # ending coordinates
        self.dst_side = None
        self.final_road_len = grid.BLOCK_SIZE
        self.exit_junc = None
        self._init_dst() # randomly assigns a possible destination

        # agent attributes
        self.ID = ID 
        self.direction = self.grid.grid[self.src] # direction of current cell
        self.prev_direction = self.direction

        # the number of possible moves to move in each direction
        self.moveset = defaultdict(int)
        
        # how the grid coordinate is updated when travelling in each of these directions
        self.cardinal_move = {
            "n": (-1,  0),
            "s": ( 1,  0),
            "e": ( 0,  1),
            "w": ( 0, -1)}
        
        # holds the possible move at each junction
        # self.intercard_move: dict = None
        self.intercard_move = {"se", "sw", "ne", "nw"}
        
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

        # to calculate the relative cell required to check in each direction at a junction e.g. if you are entering at NW to check westwards from that junction you need to start from NE
        self.root_cell = {
            "nww" : ( 0,  0, "w"), # ""
            "nwn" : (-1,  0, "nn"), # "n"
            "nwe" : (-1,  1, "nee"), # "ne"
            "nws" : ( 0,  1, "ness"), # "e"

            "sew" : ( 1, -1, "sww"), # "sw"
            "sen" : ( 0, -1, "senn"), # "w"
            "see" : ( 0,  0, "e"), # ""
            "ses" : ( 1,  0, "ss"), # "s"

            "sww" : ( 0, -1, "ww"), # "w",
            "swn" : (-1, -1, "wnn"), # "nw",
            "swe" : (-1,  0, "wnee"), # "n",
            "sws" : ( 0,  0, "s"), # "",

            "new" : ( 1,  0, "esww"), # "s",
            "nen" : ( 0,  0, "n"), # "",
            "nee" : ( 0,  1, "ee"), # "e",
            "nes" : ( 1,  1, "ess")} # "se"

     
        self._init_moveset(self.src, self.dst) # calculates the moves required to get to destination
        self.exit_junc = (np.add(self.dst, self.exit_junc_type[self.dst_side])) # retrieves element instantiated in loop yikes

    def _init_dst(self):
        '''finds suitable destination and sets current direction'''
        selected = False
        while not selected:
            dst_choice = random.choice(self.grid.exits) # selects random destination  
            if self.src[0] != dst_choice[0] and self.src[1] != dst_choice[1]: # set destination if y and x are not the same
                selected = True
                self.dst = dst_choice[:2]
                self.dst_side = dst_choice[2]
        self.dst_side ="w"
        
    def _init_moveset(self, src, dst): # hack modify to have intercard_move as a immutable array-like holding junction cell labels
        '''sets up moveset and possible intercardinal directions'''
        print("new moveset")
        moves = np.subtract(src, dst)
        if moves[0] < 0: # if y diff is neg we go south else north
            self.moveset["s"] = abs(moves[0])
        else:
            self.moveset["n"] = (moves[0])
        if moves[1] < 0: # if x is negative go east else go west
            self.moveset["e"] = abs(moves[1])
        else:
            self.moveset["w"] = (moves[1])
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
                self.pheromone = max(0, self.pheromone - pheromone_spread) # decreases agent's pheromone pool
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
    def buffer_moves(self, pheromone, endpoint):
        '''buffers junction moves and returns first initial move'''
        _, direction = pheromone
        current_cell = self.grid.grid[tuple(self.grid_coord)]
        junc_moves = self.root_cell[f"{current_cell}{direction}"][2]
        print(f"decision: {direction}, junc_moves: {junc_moves}, endpoint: {endpoint}")
        # NOTE don't need to account for junc_moves[0] here because it is accounted for in self.update_attributes

        if endpoint:
            print("buffering to endpoint and calculating move ")
            # buffer junction moves
            self.move_buffer.extend(junc_moves[1:])
            # buffer road moves in calculated direction (different from self.direction)
            for _ in range(self.grid.BLOCK_SIZE): # NOTE the reason why I'm not buffering to +1 if right turn is because you may need to make a new decision 
                self.move_buffer.append(direction)

            # need to calculate new move set as well
            self._init_moveset(src=endpoint, dst=self.dst)
        else:
            # buffer moves and remove from moveset
            print("buffering typical junction moves")
            for move in junc_moves[1:]:
                self.move_buffer.append(move)
                self.moveset[move] -= 1

        return junc_moves[0]

    def search_pheromones(self):
        '''finds a agents on out-roads of current junction, guaranteed to not return agents on exit roads'''
        pheromones = [] # [ (pheromone_found, direction) ]
        curr_junc_cell = self.grid.grid[tuple(self.grid_coord)]

        # check in all 4 directions
        for direction in "nsew":
            branch_cell = self.grid_coord # cell to branch from when checking in each out-road from a junction
            branch_cell = np.add(self.grid_coord, self.root_cell[f"{curr_junc_cell}{direction}"][:2])
            
            road_len = np.multiply(self.cardinal_move[direction], self.grid.BLOCK_SIZE)
            exit_check = np.add(branch_cell, road_len)

            # we will always take exit if at exit junction
            if self.dst == tuple(exit_check):
                current_cell = self.grid.grid[tuple(self.grid_coord)]
                junc_move = self.root_cell[f"{current_cell}{direction}"][2]
                self.move_buffer.extend(junc_move[:2])
                self.move_buffer.extend(direction * self.grid.BLOCK_SIZE) # buffer final road
                return [junc_move[0]]
            # if direction is going to lead to the wrong exit skip
            elif exit_check[0] in {0, self.grid.CELLS_IN_HEIGHT-1} or exit_check[1] in {0,self.grid.CELLS_IN_WIDTH-1}:
                continue
            else: # if not incorrect or correct exit search for agent
                found_flag = False
                while not found_flag:
                    branch_cell = np.add(branch_cell, self.cardinal_move[direction])
                    # if out of bounds set found to true
                    if not (0 <= branch_cell[0] <= self.grid.CELLS_IN_HEIGHT-1 and 0 <= branch_cell[1] <= self.grid.CELLS_IN_WIDTH-1):
                        pheromones.append((0, direction))
                        found_flag = True
                    # if agent found in direction store it and set found to true
                    elif self.grid.tracker[tuple(branch_cell)]:
                        pheromones.append((self.grid.tracker[tuple(branch_cell)].pheromone, direction))
                        found_flag = True
        return pheromones
        
    def phero_dist_choice(self):
        '''returns immediate move and stores rest in move buffer'''
        pheromones = self.search_pheromones() # [ (pheromone, direction) ]
        if len(pheromones) == 1 and pheromones[0] in self.cardinal_move:
            return pheromones[0]
        
        endpoints = []
        weights = []
        distances = [] #todo remove

        extra_dist = {# extra cell if a right turn is required at the end of calculated distance
            "ne" : (2, 0),
            "nn" : ((self.grid_coord[1] < self.dst[1]), 0),
            "ns" : ((self.grid_coord[1] < self.dst[1]), 0),

            "sw" : (2, 0), 
            "sn" : ((self.grid_coord[1] > self.dst[1]), 0),
            "ss" : ((self.grid_coord[1] > self.dst[1]), 0),      

            "es" : (0, 2), 
            "ee" : (0, (self.grid_coord[0] < self.dst[0])),
            "ew" : (0, (self.grid_coord[0] < self.dst[0])), 

            "wn" : (0, 2),
            "we" : (0, (self.grid_coord[0] > self.dst[0])),
            "we" : (0, (self.grid_coord[0] > self.dst[0]))}

        # NOTE: if detour not taken moves taken from moveset and put onto buffer, else detour then generate new move set and buffer and extra row
        for pheromone, direction in pheromones:
            distance = sum(self.moveset.values())
            extra_distance = (0, 0) if f"{direction}{self.dst_side}" not in extra_dist else extra_dist[f"{direction}{self.dst_side}"]
            if self.moveset[direction] == 0: # if detour (not on shortest route) calculate new minimum distance
                current_cell = self.grid.grid[tuple(self.grid_coord)]
                branch_start = np.add(self.grid_coord, self.root_cell[f"{current_cell}{direction}"][:2])
                branch_endpoint = np.sum([branch_start, np.multiply(self.cardinal_move[direction], self.grid.BLOCK_SIZE), extra_distance], axis = 0) # coordinate to calculate new distance from (branch_cell + block size + extra distance due to right turn)
                distance = np.sum(np.abs(np.subtract(branch_endpoint, self.dst))) # sum of absolute manhattan distance
                endpoints.append(tuple(branch_endpoint)) 
                distances.append(distance)# todo remove
            else:
                distances.append(distance)# todo remove
                endpoints.append(None)

            lin_comb_p_d = (1+(self.p_weight * pheromone) + (self.d_weight * distance)) # linear combo of pheromone and distance
            weights.append( (1/((1+lin_comb_p_d)**self.alpha)) ) # calculate weight as before in Agent.py

        # choose move based on probabilities
        sum_of_weights = np.sum(weights)
        probabilities = [weight/sum_of_weights for weight in weights]
        print(list(zip(probabilities, pheromones, distances)))
        move_choice = choice(len(pheromones), p=probabilities) # index

        # calculate new move set and buffer required moves
        return self.buffer_moves(pheromones[move_choice], endpoints[move_choice])
##############################################################
    def possible_move(self, move_result) ->  bool:
        '''
        checks if move is good and updates location in tracking grid
        -> returning false is a good thing i.e. the move is possible
        '''
        next_cell = self.grid.tracker[move_result[0], move_result[1]]
        # if current cell is cardinal and next cell is intercarinal and next cell is empty
        if self.direction in self.cardinal_move and self.grid.grid[move_result[0], move_result[1]] in self.intercard_move and not next_cell:
            diag = np.add(self.diag_check[self.direction], self.grid_coord)
            diag_cell = self.grid.tracker[diag[0], diag[1]]

            # if diagonally relative cell is empty or contains and agent where it's next move won't be next cell
            if not diag_cell or not tuple(np.add(diag_cell.grid_coord, self.cardinal_move[diag_cell.move_buffer[0]])) == next_cell:
                self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
                self.grid.tracker[move_result[0], move_result[1]] = self
                return False
            
        elif not next_cell: # if next cell is empty and you're on a straight road
            self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
            self.grid.tracker[move_result[0], move_result[1]] = self
            return False
        return True
##############################################################

    def update_attributes(self, move_choice, buffered):
        '''updates grid coordinate in tracker and current direciton of travel, optionally decrements item in moveset if buffer move not selected'''
        if not buffered:
            self.moveset[move_choice] -= 1 # update moveset
        else:
            self.move_buffer.popleft()
            self.buffered_move_flag = False

        self.grid_coord = np.add(self.grid_coord, self.cardinal_move[move_choice]) # update grid coordinate
        self.prev_direction = self.direction
        self.direction = self.grid.grid[self.grid_coord[0], self.grid_coord[1]] # update direction
    
    def move(self):
        self.pheromone = self.pheromone * self.decay

        # dummy agent check
        if self.ID == "tracker":
            return 1
        ###############################################
        # case 1: if destination has been reached
        if self.dst == tuple(self.grid_coord):
            self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
            return False
        ###############################################
        # case 2: move on executive buffer
        elif self.move_buffer:
            print("move_buffer case")
            move_choice = self.move_buffer[0]
            self.buffered_move_flag = True
        ###############################################
        # case 3: straight road -> move ahead if possible
        elif self.direction in self.cardinal_move and self.moveset[self.direction] > 0: # if cardinal direction and possible to move
            move_choice = self.direction
        ###############################################
        # case 4: you're at a junction and need to compare 4 directions, 2 of which will be detours
        elif self.direction in self.intercard_move and self.prev_direction in self.cardinal_move:
            print(f"junction case, current cell:{self.grid.grid[tuple(self.grid_coord)]}")
            move_choice = self.phero_dist_choice()
        else:
            raise Exception("no choices oh no")
        ###############################################
        print(move_choice, self.move_buffer, self.moveset, self.grid_coord)
        # possible move check
        if self.possible_move(np.add(self.grid_coord, self.cardinal_move[move_choice])):
            self.delay += 1
            self.pheromone += 1
            return True
        ###############################################
        self.update_attributes(move_choice, buffered=self.buffered_move_flag)
        return True
    