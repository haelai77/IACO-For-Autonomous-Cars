from networkx import grid_graph
from collections import deque
from networkx import grid_graph, MultiDiGraph, get_edge_attributes, shortest_path

class Pheromone_graph:
    def __init__(self, roads, grey_size=15) -> None:
        # assumes that the environment is a square grid not a rectangle
        self.num_nodes_on_axis = roads
        self.grey_size = grey_size
        self.graph = self.build_graph(dim=self.num_nodes_on_axis)
        
    def build_graph(self, dim):
        '''builds a graph where each node represents a junction in the grid environment and edges have 2 queue attributes representing the carriageway'''
        dim1 = dim
        dim2 = dim
        G = grid_graph(dim=(dim1, dim2))
        G.remove_node((0,0))
        G.remove_node((0, dim1-1))
        G.remove_node((dim2-1, 0))
        G.remove_node((dim1-1, dim2-1))

        for u,v in G.edges():
            G.edges[u, v]["left"] = deque(maxlen=self.grey_size + 2) # queue edges in direction of n, e 
            G.edges[u, v]["right"] = deque(maxlen=self.grey_size + 2) # queue edges in direction of s, w

        return G
    
    def entrance_mapping(self, src, dst) -> tuple:
        convert = lambda node: ((node[0]+2)/(self.grey_size+2), (node[1]+2)/(self.grey_size+2))

        src_node = convert(src)
        dst_node = convert(dst)

        return (src_node, dst_node)

    def shortest_path(self, source=(0,1), target=(5,6)):
        '''gets shortest path between 2 nodes as coordinates in coordinates'''
        return shortest_path(self.graph, source = source, target = target, method="dijkstra")
        
    
    def update_pheromones(self, coord): # network
        return
    
    def add_agent(self, entrance_coord):
        '''adds and agent to one of the possible entrances'''
        return
    

