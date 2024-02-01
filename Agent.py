
import numpy.typing as npt
import numpy as np
import pygame as pg
import networkx as nx

class Agent:
    def __init__(self, grid: npt.NDArray[np.int64],
                 grid_coord: tuple,
                 graph, graph_coord: tuple,
                 ID: int) -> None: #TODO add type for graph
        self.env = grid, # environment to move around in
        self.grid_coord =  grid_coord
        self.p_val = None # for picking which junction to move to based on pheremonve value
        self.ID = ID
        self.route = None

    def move(self): # caluclates next move based on pheremones and the next local best step 
        # check if at junction
        # 

        return
    