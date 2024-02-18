import pygame as pg
import numpy as np
import numpy.typing as npt
from Agent import Agent
from Grid import Grid

GREY = (128, 128, 128)
WHITE = (255, 255, 255)

GREEN = (153, 255, 0)
RED =  (255, 0, 0)

TEMP_AGENT_COLOUR = (242, 0, 255)


def env_loop(grid: Grid, agents: list[Agent], visualise = True) -> None:
    '''runs simulation'''
    if visualise:
        pg.init() # initialises imported pygame modules
        end = False
        screen = pg.display.set_mode(grid.WINDOW_SIZE, pg.RESIZABLE)
        pg.display.set_caption("simple traffic simulation") # set window title
        clock = pg.time.Clock() # Used to manage how fast the screen updates

        # updates agents on screen
        move_event = pg.USEREVENT
        pg.time.set_timer(move_event, 100)

        # -------- Main Game Loop ----------- #
        while not end: # todo will be eventually based on t = k where t is timesteps and k is user defined

            # HANDLE EVENTS
            for event in pg.event.get():
                # MOVE AGENTS
                if event.type == move_event:
                    for agent in agents:
                       agent.move()
                        
                # QUIT SCREEN
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                elif event.type == pg.QUIT:  # If user clicked close
                    end = True  

            screen.fill(GREY)
            
            # draw grid
            for row in range(grid.CELLS_IN_WIDTH):
                for col in range(grid.CELLS_IN_HEIGHT):

                    colour = GREY
                    if grid.grid[row][col] in {"n","s","e", "w", "ne", "se", "nw", "sw"}: colour = WHITE # junction

                    # draw cell
                    pg.draw.rect(screen,
                                 colour,
                                 [(grid.MARGIN + grid.CELL_SIZE) * col + grid.MARGIN, # top y coord 
                                  (grid.MARGIN + grid.CELL_SIZE) * row + grid.MARGIN, # top x left
                                  grid.CELL_SIZE,   # width of rect
                                  grid.CELL_SIZE])  # height of rect
            # draw agents
            for agent in agents:
                row, col = agent.grid_coord
                srow, scol = agent.src
                drow, dcol = agent.dst
                pg.draw.rect(screen,
                            GREEN,
                            [(grid.MARGIN + grid.CELL_SIZE) * scol + grid.MARGIN, # top y coord 
                             (grid.MARGIN + grid.CELL_SIZE) * srow + grid.MARGIN, # top x left
                             grid.CELL_SIZE,   # width of rect
                             grid.CELL_SIZE])  # height of rect
                pg.draw.rect(screen,
                            RED,
                            [(grid.MARGIN + grid.CELL_SIZE) * dcol + grid.MARGIN, # top y coord 
                             (grid.MARGIN + grid.CELL_SIZE) * drow + grid.MARGIN, # top x left
                             grid.CELL_SIZE,   # width of rect
                             grid.CELL_SIZE])  # height of rect
                pg.draw.rect(screen,
                            TEMP_AGENT_COLOUR,
                            [(grid.MARGIN + grid.CELL_SIZE) * col + grid.MARGIN, # top y coord 
                             (grid.MARGIN + grid.CELL_SIZE) * row + grid.MARGIN, # top x left
                             grid.CELL_SIZE,   # width of rect
                             grid.CELL_SIZE])  # height of rect
                
            clock.tick(60) # fps
            pg.display.flip() # draws new frame
        pg.quit()

grid = Grid()
agent = grid.generate_agents(guarantee=1)
# agent = [Agent(grid=grid, src=(50,99, "e"))]

env_loop(grid=grid, agents=agent)