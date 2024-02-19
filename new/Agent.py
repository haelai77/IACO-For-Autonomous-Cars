import random
import numpy as np
import numpy.typing as npt

class Agent:
    def __init__(self, src, grid=None, ID=None) -> None:

        # grid related attributes
        self.src: tuple = src[:2] # starting coordinates
        self.src_side = src[2] # not to be confused with direction of travel
        self.dst: tuple = None # ending coordinates
        self.dst_side = None
        self.exit_junc = None
        
        self.grid = grid # grid with roads representing directions
        self.grid_coord: tuple = self.src # current coordinate in cell

        # agent attributes
        self.ID = ID 
        self.direction = self.grid.grid[self.src] # direction of current cell
        self.steps = 0 # number of steps taken

        # number of possible steps able to be taken
        self.moveset = {
            "n": 0,
            "s": 0,
            "e": 0,
            "w": 0}
        # determines how coord is updated after move
        self.cardinal_move = {
            "n": (-1,  0),
            "s": ( 1,  0),
            "e": ( 0,  1),
            "w": ( 0, -1)}
        # determines possible moves at junction
        self.intercard_move = {
            "ne": set(), # "n", "e"
            "nw": set(), # "n", "w"
            "se": set(), # "s", "e"
            "sw": set()} # "s", "w"
        # determines which possible moves at junction are available
        self.remove_opt = {
            "n": ["ne", "nw"],
            "s": ["se", "sw"],
            "e": ["ne", "se"],
            "w": ["nw", "sw"],}
        
        self._init_dst() # randomly assigns a possible destination

        self._init_moveset() # calculates the moves required to get to destination

        self.alt_dist = {
            ("n", "w"): 1,
            ("e", "n"): 1,
            ("s", "e"): 1,
            ("w", "s"): 1,
            ("n", "s"): self.src[1] < self.dst[1], 
            ("e", "w"): self.src[0] < self.dst[0], 
            ("s", "n"): self.src[1] > self.dst[1], 
            ("w", "e"): self.src[0] > self.dst[0]}

        self.final_road_len = grid.BLOCK_SIZE
        if (self.src_side, self.dst_side) in self.alt_dist:
            self.final_road_len += self.alt_dist[(self.src_side, self.dst_side)]
                
        # determines how which junction associated with the exit is calculated
        self.exit_junc_type = {
            "n": (self.final_road_len, 0),
            "s": (-self.final_road_len, 0),
            "e": (0, -self.final_road_len),
            "w": (0, self.final_road_len)}
        
        self.exit_junc = (np.add(self.dst, self.exit_junc_type[self.dst_side])) # retrieves element instantiated in loop yikes

        self.diag_check = {
            "n": (-1,  1),
            "s": ( 1, -1),
            "e": ( 1,  1),
            "w": (-1, -1)}

    def _init_dst(self):
        '''finds suitable destination and sets current direction'''
        selected = False
        while not selected:
            dst_choice = random.choice(self.grid.exits) # selects random destination  
            if self.src[0] != dst_choice[0] and self.src[1] != dst_choice[1]: # set destination if y and x are not the same
                selected = True
                self.dst = dst_choice[:2]
                self.direction = self.grid.grid[self.src]
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
        '''checks if move is good and updates location in tracking grid'''

        next_cell = self.grid.tracker[move_result[0], move_result[1]]
        
        # if next square is an intercardinal cell we want to check the top right adjacent cell relative to direction of travel of agent
        #todo need to keep track of previous one as well to tell if you're just entering the junction
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

    def move(self):
        '''currently does move based with a probability of selecting turn randomly -> this will eventually be influenced by pheromones'''

        #todo make this return an event that removes this agent
        if self.dst == tuple(self.grid_coord):
            return
        move_choice = None
        # case 1: straight road -> move ahead if possible
        if self.direction in self.moveset and self.moveset[self.direction] > 0: # if cardinal direction and possible to move
            move_choice = self.direction

        # case 2: you're in a junction select a direction at random, if choice is wrong exit change choice
        elif self.direction in self.intercard_move:
            # todo current randomly choice needs permutations
            move_choice = random.choice(list(self.intercard_move[self.direction]))
            # if move_choice can't be done yet i.e. at edge of grid
            if self.moveset[move_choice] == self.final_road_len and move_choice == self.dst_side and tuple(self.grid_coord) != tuple(self.exit_junc): #todo what is this monstrosity, short-circuiting so its alright?  //// and self.dst_side == move_choice
                print("##############")
                print(f"move_set: {self.moveset}")
                print(f"currnt dirction:{self.direction}")
                print(f"attempted move: {move_choice}")
                print(f"final road len: {self.final_road_len}")
                print(f"src {self.src} {self.src_side}, dst {self.dst} {self.dst_side}")
                print(f"card dict: {self.intercard_move}")
                print(f"grid coord: {self.grid_coord}")
                print("##############")
                copy_moveset  = self.intercard_move[self.direction].copy()
                copy_moveset.remove(move_choice)
                move_choice = copy_moveset.pop() 
                
        if self.possible_move(np.add(self.grid_coord, self.cardinal_move[move_choice])): return
        if move_choice == None: # todo remove
            print(f"move choice is none, moveset: {self.moveset}")
            return

        self.moveset[move_choice] -= 1 # update moveset
        self.grid_coord = np.add(self.grid_coord, self.cardinal_move[move_choice]) # update grid coordinate
        self.direction = self.grid.grid[self.grid_coord[0], self.grid_coord[1]] # update direction
        self.steps += 1
        
        # removes possible move from junction if moveset deems it impossible
        if self.moveset[move_choice] == 0 and tuple(self.grid_coord) != self.dst:
            print("popped option")
            for junc_cell in self.remove_opt[move_choice]:
                self.intercard_move[junc_cell].remove(move_choice)



            

        
    