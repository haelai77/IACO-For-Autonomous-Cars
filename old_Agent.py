import numpy.typing as npt
import numpy as np
import pygame as pg
import networkx as nx
from Pheromone_graph import Pheromone_graph


class Agent:
    def __init__(self,
                 ID: int,
                 direction: str,
                 graph,
                 src,
                 dst) -> None:
        
        self.graph_env: Pheromone_graph = graph
        self.grid_coord =  src

        self.ID = ID
        self.curr_direction = direction
        self.pheremone = 10 # for picking which junction to move to based on pheremonve value
        
        self.prev_dir = None
        self.src = src # starting node
        self.dst = dst # ending node
        
        self.coord_route = self.graph_env.shortest_path()
        self.moveset, self.cardinal_route = self.decode_coordinates_to_directions(self.coord_route)
        self.grey_size = 15
        print(self.moveset, "\n", self.cardinal_route)
        print(self.dst)



    def decode_coordinates_to_directions(self, coordinates):
        '''decodes a list of coords into cardinal directions'''
        moveset = {"n": 0,
                   "s": 0,
                   "e": 0,
                   "w": 0}

        tmp = []
        for i in range(len(coordinates) - 1):
            curr_y, curr_x = coordinates[i]
            next_y, next_x = coordinates[i + 1]

            if curr_x == next_x:
                if next_y < curr_y:
                    tmp.append("n")
                    moveset["n"] += 1
                elif next_y > curr_y:
                    tmp.append("s")
                    moveset["s"] += 1
            elif curr_y == next_y:
                if next_x < curr_x:
                    tmp.append("w")
                    moveset["w"] += 1
                elif next_x > curr_x:
                    tmp.append("e")
                    moveset["e"] += 1
            else:
                raise ValueError("Coordinates must be consecutive and either vertically or horizontally adjacent")

        # for move in moveset:
        #     if moveset[move] > 0: moveset[move] -= 1
        
        return moveset, tmp

    def check_move(self, grid, next_direction, junction=False) -> int | bool:
        '''Checks if move satisfies conditions:
            1. no other car up-diagonal-right to direction of travel if next move is into junction
            2. the space ahead is not obstructed
            *** will need to eventually add in pheremone considerations
        '''
        # temp function that always returns true
        # match next_direction:
        #     case "n":
        #         return True
            
        #     case "e":
        #         return True
            
        #     case "s":
        #         return True
            
        #     case "w":
        #         return True
        return True

    def update_curr_direction(self, next_dir):
        #update current direction and previous direction
        self.prev_dir = self.curr_direction
        self.curr_direction = next_dir

    def move(self, grid) -> tuple: # caluclates next move based on pheremones and the next local best step 
        ''' Decides which move to take based on pheremone at junction and shortest route '''
        # todo CURRENT MOVES ARE JUST AN ARBITRARY SHORTEST PATH

        #TODO REFACTOR THIS,ITS SOOO BADDDSDJFLKASDJFKOUIRHGFSNKMREIUHJAHAFEIRVAFOEJRAFJCVEAFOJCIIOAPJFSDIOJFIOSMCDKLSSAOIDFJCMIO
        
        if self.grid_coord == self.dst:
            return self.grid_coord

        match self.curr_direction:
            case "n":
                next_dir = grid[self.grid_coord[0] - 1, self.grid_coord[1]] # move to N or NW
                junction = True if next_dir == "nw" else False

                if self.check_move(grid, next_dir, junction):
                    self.update_curr_direction(next_dir)
                    # relay next move to grid
                    self.grid_coord = (self.grid_coord[0] - 1, self.grid_coord[1])
                    return self.grid_coord # return move up north

            case "e":
                next_dir = grid[self.grid_coord[0], self.grid_coord[1] + 1] # move to E or NE
                junction = True if next_dir == "ne" else False

                if self.check_move(grid, next_dir, junction):
                    self.update_curr_direction(next_dir)
                    # relay next move to grid
                    self.grid_coord = (self.grid_coord[0], self.grid_coord[1] + 1)
                    return self.grid_coord # return reutrn move to east
            
            case "s":
                next_dir = grid[self.grid_coord[0] + 1, self.grid_coord[1]] # move to S or SE
                junction = True if next_dir == "se" else False

                if self.check_move(grid, next_dir, junction):
                    self.update_curr_direction(next_dir)
                    # relay next move to grid
                    self.grid_coord = (self.grid_coord[0] + 1, self.grid_coord[1])
                    return self.grid_coord # return reutrn move to east
                return
            
            case "w":
                next_dir = grid[self.grid_coord[0], self.grid_coord[1] - 1] # move to W or SW
                junction = True if next_dir == "sw" else False

                if self.check_move(grid, junction):
                    self.update_curr_direction(next_dir)
                    # relay next move to grid
                    self.grid_coord = (self.grid_coord[0], self.grid_coord[1] - 1)
                    return self.grid_coord # return reutrn move to east
                return
            ########################## intercardinal directions ##########################
            case "nw":
 
                # if possible to move west 
                # todo throw away - (self.grey_size + 2)
                if self.moveset["w"] > 1 or (self.moveset["w"] == 1 and self.grid_coord[0] - (self.grey_size + 2) == self.dst[0]):
                    next_dir = grid[self.grid_coord[0], self.grid_coord[1] - 1] # move to W
                    # if move is valid
                    if self.check_move(grid, next_dir):
                        self.update_curr_direction(next_dir)
                        # relay next move to grid
                        self.grid_coord = (self.grid_coord[0], self.grid_coord[1] - 1)
                        self.moveset["w"] -= 1
                        return self.grid_coord # return move left west
                else:
                    if self.check_move(grid, "n"):
                        self.update_curr_direction(grid[self.grid_coord[0] - 1, self.grid_coord[1]])
                        self.grid_coord = (self.grid_coord[0] - 1, self.grid_coord[1])
                        return self.grid_coord # return move up north because can't take left
                    
            case "ne":

                # if possible move north
                if self.moveset["n"] > 1 or (self.moveset["n"] == 1 and self.grid_coord[1] == self.dst[1]):
                    next_dir = grid[self.grid_coord[0] - 1, self.grid_coord[1]] # move to N
                    # if move is valid
                    if self.check_move(grid,  next_dir):
                        self.update_curr_direction(next_dir)

                        # relay next move to grid
                        self.grid_coord = (self.grid_coord[0] - 1, self.grid_coord[1])
                        self.moveset["n"] -= 1
                        return self.grid_coord # return move to up north 
                else:
                    if self.check_move(grid, "e"): # return move right east because can't take move up north
                        self.update_curr_direction(grid[self.grid_coord[0], self.grid_coord[1] + 1])
                        self.grid_coord = (self.grid_coord[0], self.grid_coord[1] + 1)
                        return self.grid_coord
            case "se":

                # take forwards path if possible
                if self.moveset["e"] > 1 or (self.moveset["e"] == 1 and self.grid_coord[0] == self.dst[0]):
                    next_dir = grid[self.grid_coord[0], self.grid_coord[1] + 1] # move to E
                    # if move is valid
                    if self.check_move(grid,  next_dir):
                        self.update_curr_direction(next_dir)

                        # relay next move to grid
                        self.grid_coord = (self.grid_coord[0], self.grid_coord[1] + 1)
                        self.moveset["e"] -= 1
                        return self.grid_coord # return move to up north 
                else:
                    if self.check_move(grid, "s"): # return move down south because can't make east move
                        self.update_curr_direction(grid[self.grid_coord[0] + 1, self.grid_coord[1]])
                        self.grid_coord = (self.grid_coord[0] + 1, self.grid_coord[1])
                        return self.grid_coord
                    
            case "sw":
       
                # take forwards path if possible
                if self.moveset["s"] > 1 or (self.moveset["s"] == 1 and self.grid_coord[1] == self.dst[1]):
                    next_dir = grid[self.grid_coord[0] + 1, self.grid_coord[1]] # move to E
                    # if move is valid
                    if self.check_move(grid,  next_dir):
                        self.update_curr_direction(next_dir)

                        # relay next move to grid
                        self.grid_coord = (self.grid_coord[0] + 1, self.grid_coord[1])
                        self.moveset["s"] -= 1
                        return self.grid_coord # return move down south
                else:
                    if self.check_move(grid, "w"): # return move left west because can't take move down south
                        self.update_curr_direction(grid[self.grid_coord[0], self.grid_coord[1] - 1])
                        self.grid_coord = (self.grid_coord[0], self.grid_coord[1] - 1)
                        return self.grid_coord
        # default return
        return self.grid_coord # default return current coord
    

    