import random
import numpy as np
import numpy.typing as npt

class Agent:
    def __init__(self, src, grid=None, ID=None, ) -> None:
        self.pheromone = 0
        self.delay = 0

        self.edge_junc: list[tuple] = [] #todo tmp? edge junc? huh?

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
        self.prev_direction = self.direction
        self.prev_direction = "s"#todo remove

        self.steps = 0 # number of steps taken

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
        
        # calculates the length of the final stretch of "road"
        self.final_road_len = grid.BLOCK_SIZE
        if (self.src_side, self.dst_side) in self.alt_dist: self.final_road_len += self.alt_dist[(self.src_side, self.dst_side)]

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
        
        self._init_moveset() # calculates the moves required to get to destination
                
        self.exit_junc = (np.add(self.dst, self.exit_junc_type[self.dst_side])) # retrieves element instantiated in loop yikes

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

    def pheromone_lft(self):
        #todo
        pass

    def pheromone_fwd(self):
        #todo
        pass

    def compare_pheronomes(self, ag1, ag2):
        '''returns a direction based on either agent or random '''
        #todo
        pass

    def pheromone_choice(self):
        '''only used at junctions, should take into account whether or not you're at exit junction'''
        # todo should also update
        #####################
        # if current direction is in intercard
            # based on intercard iterate in different diretions
                # take first 2 agents on either choice and make decision considering either
        ##################### 
        if tuple(self.grid_coord) in self.edge_junc: #todo needs function for calculating edge junctions that aren't the exit junction can be done in the grid obj and the exit junc just removed from the list
            # return the other option
            #todo
            pass
        elif self.direction in self.intercard_move:
            left_agent = self.pheromone_lft()
            fwd_agent = self.pheromone_fwd()
            
            if left_agent and fwd_agent: # return better of 2 paths
                return self.compare_pheromones()
            else: # return random choice if no agents in adjacent roads
                return random.choice(list(self.intercard_move[self.direction]))
            
    def spread_pheromone(self) -> tuple[int]:
        '''returns list of tuple/iterator of (agent, pheromone update value)'''
        pheromone = 1 #todo calculate pheromone
        

        if self.direction in self.cardinal_move: # if on straight road
            next_check = np.subtract(self.grid_coord, self.cardinal_move[self.direction]) # only need to subtract
            while True:
                if not (0 <= next_check[0] <= self.grid.CELLS_IN_HEIGHT-1 and 0 <= next_check[1] <= self.grid.CELLS_IN_WIDTH-1): # if not within bounds
                    return []
                else:
                    cell = self.grid.tracker[next_check[0], next_check[1]]
                    if cell: return [(cell.ID, pheromone)] # return agent behind and pheromone it needs to update
                    next_check = np.subtract(next_check, self.cardinal_move[self.direction])

        elif self.direction in self.intercard_move:
            found_counter = 0
            # WHEN CHECKING BEHIND YOU SUBSTRACT BUT WHEN CHECKING ADJACENTLY YOU ADD
            next_check = [np.subtract(self.grid_coord, self.cardinal_move[direction]) if direction == self.prev_direction else np.add(self.grid_coord, self.cardinal_move[direction]) for direction in self.direction] # next cells to check in each direction
            agents_found = []
            flags = [0] * 2

            while not (flags[0] and flags[1]):
                for index, direction in enumerate(self.direction):
                    # set out of bounds flag
                    if not flags[index] and not (0 <= next_check[index][0] <= self.grid.CELLS_IN_HEIGHT-1 and 0 <= next_check[index][1] <= self.grid.CELLS_IN_WIDTH-1):
                        flags[index] = 1 
                    else:
                        # if contains an agent add it to the found agents list
                        cell = self.grid.tracker[next_check[index][0], next_check[index][1]]
                        if cell: 
                            agents_found.append(cell) 
                            found_counter += 1
                        
                        next_check[index] = np.subtract(next_check[index], self.cardinal_move[direction]) if direction == self.prev_direction else np.add(next_check[index], self.cardinal_move[direction])
            return [(agent.ID, pheromone/len(agents_found)) for agent in agents_found] # todo may need to fix "pheromon/len..."

    def move(self):
        '''currently does move based with a probability of selecting turn randomly -> this will eventually be influenced by pheromones'''
        if self.dst == tuple(self.grid_coord):
            self.grid.tracker[self.grid_coord[0], self.grid_coord[1]] = None
            return False
        # case 1: straight road -> move ahead if possible
        elif self.direction in self.moveset and self.moveset[self.direction] > 0: # if cardinal direction and possible to move
            move_choice = self.direction
        # case 2: you're in a junction select a direction at random, if choice is wrong exit change choice
        elif self.direction in self.intercard_move:
            # todo current randomly choice will eventually include pheromone 
            move_choice = random.choice(list(self.intercard_move[self.direction]))
            # if move_choice can't be done yet i.e. at edge of grid
            if self.moveset[move_choice] == self.final_road_len and move_choice == self.dst_side and tuple(self.grid_coord) != tuple(self.exit_junc): # short circiting makes this alright right?
                copy_moveset  = self.intercard_move[self.direction].copy()
                copy_moveset.remove(move_choice)
                move_choice = copy_moveset.pop() 
        else:
            move_choice = None
                
        if self.possible_move(np.add(self.grid_coord, self.cardinal_move[move_choice])):
            return True

        self.moveset[move_choice] -= 1 # update moveset
        self.grid_coord = np.add(self.grid_coord, self.cardinal_move[move_choice]) # update grid coordinate
        self.prev_direction = self.direction
        self.direction = self.grid.grid[self.grid_coord[0], self.grid_coord[1]] # update direction
        self.steps += 1
        
        # removes possible move from junction if moveset deems it impossible
        if self.moveset[move_choice] == 0 and tuple(self.grid_coord) != self.dst:
            for junc_cell in self.remove_opt[move_choice]:
                self.intercard_move[junc_cell].remove(move_choice)
        return True


            

        
    