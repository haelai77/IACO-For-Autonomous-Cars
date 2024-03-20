import numpy as np
import numpy.typing as npt
from Agent import Agent
from Detour_Agent import Detour_Agent
import random

class Grid():
    def __init__(self,
                 cell_size_px = 5, # pixel size of a cell in the grid
                 grey_block_size = 15, # number of cells a grey block should be 
                 num_roads_on_axis = 5,
                 margin = 1) -> None:
        self.test = False
        self.CELL_SIZE: int = cell_size_px
        self.BLOCK_SIZE: int = grey_block_size
        self.NUM_ROADS_ON_AXIS: int = num_roads_on_axis
        self.CELLS_IN_WIDTH = self.CELLS_IN_HEIGHT = grey_block_size * (num_roads_on_axis + 1) + 2 * num_roads_on_axis

        self.MARGIN = margin
        self.WINDOW_SIZE = [self.CELLS_IN_WIDTH * self.CELL_SIZE + self.MARGIN*self.CELLS_IN_WIDTH, # GRID_WIDTH * CELL_PX + MARGIN* GRID_WIDTH
                            self.CELLS_IN_HEIGHT * self.CELL_SIZE + self.MARGIN*self.CELLS_IN_HEIGHT]

        self.grid: npt.NDArray[np.int64] = self.init_grid()
        self.tracker: npt.NDArray[np.int64] = np.full(shape=(self.CELLS_IN_WIDTH, self.CELLS_IN_HEIGHT), dtype=object, fill_value=None) # keeps track of agent objects
        self.entrances: list[tuple] = []
        self.exits: list[tuple] = []

        self.generate_accessways()
        
    def init_grid(self):
        '''MAKES MANHATTAN STYLE GRID'''
        grid = np.full(shape=(self.CELLS_IN_WIDTH, self.CELLS_IN_HEIGHT), dtype=object, fill_value="")

        for idx in range(self.BLOCK_SIZE, self.CELLS_IN_WIDTH, self.BLOCK_SIZE): # for vertical roads
            road_x = idx + 2*(idx//self.BLOCK_SIZE-1) # 

            if road_x >= self.CELLS_IN_WIDTH: continue
            grid[:, road_x] += "n" # going north
            grid[:, road_x+1] += "s" # going south

        for idx in range(self.BLOCK_SIZE, self.CELLS_IN_HEIGHT, self.BLOCK_SIZE): # for horizontal roads
            road_y = idx + 2*(idx//self.BLOCK_SIZE-1)

            if road_y >= self.CELLS_IN_WIDTH: continue
            grid[road_y, :] += "e" # going east 
            grid[road_y+1, :] += "w" # going west

        return grid

    def generate_agents(self, round_density = 2.3, alpha = 0, p_dropoff = 0, detours=False, test=False, signalling_toggle=False):
        '''generates agents at every time step and intialises them with a source'''

        if test:
            self.test = True
            if detours: 
                agents = [Detour_Agent(self.entrances[0], grid=self, ID=1, alpha=alpha, p_dropoff=p_dropoff, signalling_toggle=signalling_toggle)]
            else:
                agents = [Agent(self.entrances[0], grid=self, ID=1, alpha=alpha, p_dropoff=p_dropoff)]

            return agents

        sources = []
        probability = round_density/len(self.entrances) 

        for source in self.entrances:
            k = random.uniform(0,1)
            if k <= probability:
                sources.append(source)

        if not detours:
            agents = [Agent(src, grid=self, ID = i+1, alpha=alpha, p_dropoff=p_dropoff) for i, src in enumerate(sources)]
        else:
            agents = [Detour_Agent(src, grid=self, ID = i+1, alpha=alpha, p_dropoff=p_dropoff, signalling_toggle=signalling_toggle) for i, src in enumerate(sources)]
        return agents

    def generate_accessways(self):
        '''stores all possible exits and entrances'''

        for k in range(self.NUM_ROADS_ON_AXIS):
            # calculates entrance coordinates based on k            
            i = self.BLOCK_SIZE + k*(self.BLOCK_SIZE + 2)
            j = i + 1 

            self.entrances.append( (0, j, "n") ) # top entrance
            self.entrances.append( (j, self.CELLS_IN_WIDTH-1, "e") ) # right entrance
            self.entrances.append( (i, 0, "w") ) # left entrance
            self.entrances.append( (self.CELLS_IN_HEIGHT-1, i, "s") ) # bottom entrance

            self.exits.append( (0, i, "n") ) # top exit
            self.exits.append( (i, self.CELLS_IN_WIDTH-1, "e") ) # right exit
            self.exits.append( (j, 0, "w") ) # left exit
            self.exits.append( (self.CELLS_IN_HEIGHT-1, j, "s") ) # bottom exit
