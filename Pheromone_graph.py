import networkx as nx
from networkx import grid_graph, MultiDiGraph

class Pheromone_graph:
    #TODO  singleton?
    def __init__(self, NUMB_X_CELLS: int, NUMB_Y_CELLS: int) -> None:
        self.NUMB_X_CELLS = NUMB_X_CELLS
        self.NUMB_Y_CELLS = NUMB_Y_CELLS
        self.graph = None
        
    def build_graph(self): # makes graph based on dimensions passed in (simple grid)
        dim1 = self.NUMB_X_CELLS
        dim2 = self.NUMB_Y_CELLS
        G = grid_graph(dim=(dim1, dim2))
        G.remove_node((0,0))
        G.remove_node((0, dim1-1))
        G.remove_node((dim2-1, 0))
        G.remove_node((dim1-1, dim2-1))
        self.graph = MultiDiGraph(G)
    
    def update_weight(self, coord): # network 
        return
    
    def subscribe_agent(self, coord):
        return
    
p = Pheromone_graph(NUMB_X_CELLS=1, NUMB_Y_CELLS=2)
p.build_graph()
