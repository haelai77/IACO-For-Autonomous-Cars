import pygame
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
NUMB_X_CELLS = 100
NUMB_Y_CELLS = 100
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
grid = [] # stores colour states
for row in range(NUMB_X_CELLS):
    grid.append([])
    for column in range(NUMB_Y_CELLS):
        if isroad(row, column):
            grid[row].append(2)
        else:
            grid[row].append(0)  # Append a cell
 
grid[NUMB_X_CELLS-1][ NUMB_Y_CELLS-1] = 1

# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [NUMB_X_CELLS*WIDTH + MARGIN*NUMB_X_CELLS, NUMB_Y_CELLS*HEIGHT + MARGIN*NUMB_Y_CELLS]
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE) # surface
 
# Set title of screen
pygame.display.set_caption("simple traffic simulation")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN: # clicked cells turn green
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
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

            pygame.draw.rect(screen,
                                colour,
                                [(MARGIN + WIDTH) * column + MARGIN, # left
                                (MARGIN + HEIGHT) * row + MARGIN, # top
                                WIDTH, # width
                                HEIGHT], # height    

                            ) 

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()





