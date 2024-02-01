import pygame as pg
import numpy as np
import numpy.typing as npt
import networkx as nx

###### GLOBAL VARIABLES ######

#COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGREY = (211, 211, 211)
GREY = (128, 128, 128)

#AGENT COLOURS
#TODO COLOUR interpolation?
DEEP_GREEN = (0, 255, 0)
GREEN = (153, 255, 0)
GREEN_YELLOW = (223, 254, 0)

LIGHT_ORANGE = (254, 208, 0)
ORANGE = (255, 179, 0)
DARK_ORANGE = (255, 158, 0)

RED = (255, 0, 0)


# CELL SIZE
WIDTH = 5
HEIGHT = 5

# no. cells in width and height
NUMB_X_CELLS = NUMB_Y_CELLS = 100
# MARGIN BETWEEN CELLS
MARGIN = 1

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [NUMB_X_CELLS*WIDTH + MARGIN*NUMB_X_CELLS, NUMB_Y_CELLS*HEIGHT + MARGIN*NUMB_Y_CELLS]
##############################


def isroad(row_index: int, column_index: int) -> bool:

    # Calculate the adjusted row and column indices (accounts for an offset of 2 cells for every row/column)
    adjusted_row = row_index - 2 * max(row_index // 15 - 1, 0)
    adjusted_column = column_index - 2 * max(column_index // 15 - 1, 0)

    # Check if the cell is white
    is_white_row = adjusted_row % 15 in {0, 1} and row_index not in {0, 1}
    is_white_column = adjusted_column % 15 in {0, 1} and column_index not in {0, 1}

    # Return True if either the row or column satisfies the condition
    return is_white_row or is_white_column

# MAKES GAME GRID
def make_grid(NUMB_X_CELLS: int, NUMB_Y_CELLS: int) -> npt.NDArray[np.int64]:
    grid = np.zeros((NUMB_X_CELLS, NUMB_Y_CELLS), dtype=int)

    for idx in range(15, NUMB_X_CELLS, 15):
        idx_adj = idx + 2*(idx//15-1)
        if idx_adj >= NUMB_X_CELLS: continue
        grid[:, idx_adj] += 1
        grid[:, idx_adj+1] += 1
        grid[idx_adj, :] += 1
        grid[idx_adj+1, :] += 1
    return grid

def game_loop(grid: npt.NDArray[np.int64]) -> None:
    pg.init()
    end = False
    screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE) # surface
    pg.display.set_caption("simple traffic simulation") # set window title
    
    clock = pg.time.Clock() # Used to manage how fast the screen updates
    
    # -------- Main Game Loop -----------
    while not end:
        for event in pg.event.get():  # User did something
            if event.type == pg.QUIT:  # If user clicked close
                end = True  # Flag that we are done so we exit this loop
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
        # TODO remove this code (it's for just clicking cells for fun)
            elif event.type == pg.MOUSEBUTTONDOWN: # clicked cells turn green
                # User clicks the mouse. Get the position
                pos = pg.mouse.get_pos()
                # gets discrete coordinate of mouse click pos
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one

                grid[row][column] = 1
                print("Click ", pos, "Grid coordinates: ", row, column)
        # TODO remove this code                                        

        screen.fill(GREY)
    
        # Draw the grid
        for row in range(NUMB_X_CELLS):
            for column in range(NUMB_Y_CELLS):

                colour = GREY # default colour
                if grid[row][column] == 1: colour = WHITE
                elif grid[row][column] == 2: colour = LIGHTGREY

                pg.draw.rect(screen, colour,
                             [(MARGIN + WIDTH) * column + MARGIN, # left
                              (MARGIN + HEIGHT) * row + MARGIN, # top
                              WIDTH, # width
                              HEIGHT]) # height     
                
        clock.tick(60) # fps
        pg.display.flip() # updates frame / draws new frame
    pg.quit()

def no_vis_loop(grid: npt.NDArray[np.int64]) -> None:
    return

grid = make_grid(NUMB_X_CELLS, NUMB_Y_CELLS)
grid[NUMB_Y_CELLS-1, NUMB_X_CELLS-1] = 1
game_loop(grid)




