# import geopandas as gpd 
import networkx as nx
from networkx import grid_graph, MultiDiGraph, get_edge_attributes, shortest_path
from collections import deque # popleft and append

import osmnx as ox 
import numpy as np
import matplotlib.pyplot as plt
# average car length = 4m

dim1 = dim2 = 7

node_size = 70

G = grid_graph(dim=(dim1, dim2))
G.remove_node((0,0))
G.remove_node((0, dim1-1))
G.remove_node((dim2-1, 0))
G.remove_node((dim1-1, dim2-1))
# G = MultiDiGraph(G)

grey_size = 15

for u,v in G.edges():
    print("#####", u, v)
    G.edges[u, v]["left"] = deque(maxlen=grey_size + 2) # n, e 
    G.edges[u, v]["right"] = deque(maxlen=grey_size + 2) # s, w

G.edges[(0, 1), (1, 1)]["left"].append(1)
G.edges[(0, 1), (1, 1)]["left"].append(2)
G.edges[(0, 1), (1, 1)]["left"].popleft()

print(G.edges[(0, 1), (1, 1)])
print("###########")

plt.figure(1, figsize=(8,8))

pos = {(x,y):(y,-x) for x,y in G.nodes()}
labels = {(x, y): f"{x}, {y}" for x, y in G.nodes()}  # Use the node coordinates as labels

def decode_coordinates_to_directions(coordinates):
    directions = []
    for i in range(len(coordinates) - 1):
        curr_y, curr_x = coordinates[i]
        next_y, next_x = coordinates[i + 1]

        if curr_x == next_x:
            if next_y < curr_y:
                directions.append("N")
            elif next_y > curr_y:
                directions.append("S")
        elif curr_y == next_y:
            if next_x < curr_x:
                directions.append("E")
            elif next_x > curr_x:
                directions.append("W")
        else:
            raise ValueError("Coordinates must be consecutive and either vertically or horizontally adjacent")
    return directions

# path = shortest_path(G, source = (0,1), target = (5,6), method="dijkstra")
# print("###########shortest path:\n", path)
# print(decode_coordinates_to_directions(path))


nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black', font_weight='bold')
# nx.draw(G, pos=pos, node_size=node_size, node_color="blue", node_shape="s")
# nx.draw_networkx_nodes(G, pos=pos, node_size=node_size, node_color="blue", node_shape="s")
nx.draw_networkx_edges(G, pos, edgelist=G.edges, node_size=node_size)

# print(G.nodes)
# print("##########")
# print(G.edges)

plt.show()

