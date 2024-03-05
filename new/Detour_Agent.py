import random
import numpy as np
import numpy.typing as npt
from numpy.random import choice
from collections import deque

class Detour_Agent:
    def __init__(self, src, grid=None, ID=None, pheromone = 0, alpha = 5, decay=0.9, spread=0.5, spread_decay = 0.03333) -> None:
        self.pheromone = pheromone
        self.delay = 0
        self.alpha = alpha
        self.decay = decay
        self.spread = spread
        self.spread_decay = spread_decay

        # grid related attributes
        self.src: tuple = src[:2] # starting coordinates
        self.src_side = src[2] # not to be confused with direction of travel
        
        self.grid = grid # grid with roads representing directions
        self.grid_coord: tuple = self.src # current coordinate in cell
        self.grid.tracker[self.grid_coord] = self

        self.dst: tuple = None # ending coordinates
        self.dst_side = None
        self.exit_junc = None
        self._init_dst() # randomly assigns a possible destination

        # agent attributes
        self.ID = ID 
        self.direction = self.grid.grid[self.src] # direction of current cell

        self.steps = 0 # number of steps taken

        self.move_buffer = deque()

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
        
        # holds the possible move at each junction
        self.intercard_move = {
            "ne": set(), # "n", "e"
            "nw": set(), # "n", "w"
            "se": set(), # "s", "e"
            "sw": set()} # "s", "w"
        
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
        
        # for checking diagonal cell when entering junction
        self.diag_check = {
            "n": (-1,  1),
            "s": ( 1, -1),
            "e": ( 1,  1),
            "w": (-1, -1)}
        # calculates the length of the final stretch of "road"
        self.final_road_len = grid.BLOCK_SIZE
        if (self.src_side, self.dst_side) in self.alt_dist: self.final_road_len += self.alt_dist[(self.src_side, self.dst_side)]

        # for calculating which junction is associated with the exit
        self.exit_junc_type = {
            "n": (self.final_road_len, 0),
            "s": (-self.final_road_len, 0),
            "e": (0, -self.final_road_len),
            "w": (0, self.final_road_len)}
        
        self._init_moveset() # calculates the moves required to get to destination
        self.exit_junc = (np.add(self.dst, self.exit_junc_type[self.dst_side])) 

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
##############################################################
    def phero_dist_choice(self):
        '''returns immediate move and stores rest in move buffer'''
        dirs_to_check = [] # shouldn't contain direction which exits early 

        # check in all 4 directions
        for direction in "nsew":
            # if direction not going to lead to wrong exit

            # if direction in corresponding detour direction mapping
                # calculate minimum extra distance required to travel and take that into account
            # else calculate weight corresponding to direction as normal
        pass

##############################################################
    def possible_move(self, move_result) ->  bool:
        '''
        checks if move is good and updates location in tracking grid
        -> returning false is a good thing i.e. the move is possible
        '''
        next_cell = self.grid.tracker[move_result[0], move_result[1]]
        # if next square is an intercardinal cell we want to check the top right adjacent cell relative to direction of travel of agent
        # (only if current cell is a regular cell)
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
    def move(self):
        # dummy agent check
        if self.ID == "tracker":
            return 1
        ###############################################
        if self.dst == tuple(self.grid_coord):
            self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
            return False
        ###############################################
        # move buffer must be empty before any other move considered
        elif self.move_buffer:
            return self.move_buffer.popleft()
        ###############################################
        # case 1: straight road -> move ahead if possible
        elif self.direction in self.moveset and self.moveset[self.direction] > 0: # if cardinal direction and possible to move
            move_choice = self.direction
        ###############################################
        # case 2: you're at a junction and need to compare 4 directions, 2 of which will be detours
        elif self.direction in self.intercard_move:
            move_choice = self.phero_dist_choice()
        ###############################################
        # if proposed move is not blocked by agent car
        if self.possible_move(np.add(self.grid_coord, self.cardinal_move[move_choice])):
            self.delay += 1
            self.pheromone += 1
            return True
        else: # pheromone only decays if a move has been made
            self.pheromone = self.pheromone * self.decay