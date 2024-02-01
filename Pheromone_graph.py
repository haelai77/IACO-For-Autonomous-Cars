import networkx as nx

class Pheromone_graph:
    #TODO  singleton?
    def __init__(self, NUMB_X_CELLS: int, NUMB_Y_CELLS: int) -> None:
        self.NUMB_X_CELLS = NUMB_X_CELLS
        self.NUMB_Y_CELLS = NUMB_Y_CELLS
        self.graph = None
        
    def build_graph(self): # makes graph based on dimensions passed in (simple grid)
        
        return 
    
    def update_weight(self,coord):
        return
    
    def subscribe_agent(self, coord):
        return
    
p = Pheromone_graph(NUMB_X_CELLS=1, NUMB_Y_CELLS=2)
p.build_graph()
