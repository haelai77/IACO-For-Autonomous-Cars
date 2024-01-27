import pygame as pg
import numpy as np
import networkx as nx

#COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (124, 125, 125)
#AGENT COLOURS
GREEN = (0, 255, 0)
ORANGE = (255, 148, 82)
RED = (255, 0, 0)
# CELL SIZE
WIDTH = 5
HEIGHT = 5

# no. cells in width and height
NUMB_X_CELLS = NUMB_Y_CELLS = 140
# MARGIN BETWEEN CELLS
MARGIN = 1

def isroad(row_index, column_index):

    # Calculate the adjusted row and column indices (accounts for an offset of 2 cells for every row/column)
    adjusted_row = row_index - 2 * max(row_index // 15 - 1, 0)
    adjusted_column = column_index - 2 * max(column_index // 15 - 1, 0)

    # Check if the cell is white
    is_white_row = adjusted_row % 15 in {0, 1} and row_index not in {0, 1}
    is_white_column = adjusted_column % 15 in {0, 1} and column_index not in {0, 1}

    # Return True if either the row or column satisfies the condition
    return is_white_row or is_white_column

# MAKES GAME GRID
def make_grid(NUMB_X_CELLS, NUMB_Y_CELLS):
    grid = np.zeros((NUMB_X_CELLS, NUMB_Y_CELLS), dtype=int)

    for idx in range(15, NUMB_X_CELLS, 15):
        idx_adj = idx + 2*(idx//15-1)
        if idx_adj >= NUMB_X_CELLS: continue
        grid[:, idx_adj] = 2
        grid[:, idx_adj+1] = 2
        grid[idx_adj, :] = 2
        grid[idx_adj+1, :] = 2

    

    return grid


grid = make_grid2(NUMB_X_CELLS, NUMB_Y_CELLS)
grid[NUMB_Y_CELLS-1, NUMB_X_CELLS-1] = 1

# Initialize pg
pg.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [NUMB_X_CELLS*WIDTH + MARGIN*NUMB_X_CELLS, NUMB_Y_CELLS*HEIGHT + MARGIN*NUMB_Y_CELLS]
screen = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE) # surface
 
# Set title of screen
pg.display.set_caption("simple traffic simulation")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pg.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pg.event.get():  # User did something
        if event.type == pg.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
            
        elif event.type == pg.MOUSEBUTTONDOWN: # clicked cells turn green
            # User clicks the mouse. Get the position
            pos = pg.mouse.get_pos()
            # gets discrete coordinate of mouse click pos
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one

            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)
 
    # Set the screen background
    screen.fill(GREY)
 
    # Draw the grid
    for row in range(NUMB_X_CELLS):
        for column in range(NUMB_Y_CELLS):

            colour = GREY

            #( (row-2*(row//15-1))%15 in {0, 1} or (column-2*(column//15-1))%15 in {0,1} )
            if grid[row][column] == 2:
                colour = WHITE

            if grid[row][column] == 1:
                colour = GREEN

            pg.draw.rect(screen,
                                colour,
                                [(MARGIN + WIDTH) * column + MARGIN, # left
                                (MARGIN + HEIGHT) * row + MARGIN, # top
                                WIDTH, # width
                                HEIGHT], # height    

                            ) 

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pg.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pg.quit()





