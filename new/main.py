import pygame as pg
import numpy as np
import numpy.typing as npt
from Agent import Agent
from Grid import Grid
import time

GREY = (128, 128, 128)
WHITE = (255, 255, 255)

GREEN = (153, 255, 0)
RED =  (255, 0, 0)
ORANGE = (255,127,80)
BLUE = (30,144,255)

TEMP_AGENT_COLOUR = (242, 0, 255)

def env_loop(grid: Grid, agents: list[Agent], visualise = True, t=0, t_max=20000) -> None:
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
        while t != t_max: # todo will be eventually based on t = k where t is timesteps and k is user defined
            
            # HANDLE EVENTS
            for event in pg.event.get():
                # MOVE AGENTS
                if event.type == move_event:
                    update_ph_list = []
                    agents = [agent for agent in agents if agent.move()] # removes ones that have reached their destination # todo reinstate movement
                    # calculate pheromone increase
                    for agent in agents:
                        update_ph_list.extend(agent.spread_pheromone())
                    # apply pheromone changes
                    for agent, update_val in update_ph_list:
                        agent.pheromone += update_val
                    # add more agents
                    agents.extend(grid.generate_agents())
                    print(t)
                    t += 1
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
                colour = TEMP_AGENT_COLOUR
                match agent.pheromone:
                    case 0:
                        colour = TEMP_AGENT_COLOUR
                    case _:
                        colour =  BLUE
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
                            colour, # (agent.pheromone*2, 100, 100)
                            [(grid.MARGIN + grid.CELL_SIZE) * col + grid.MARGIN, # top y coord 
                             (grid.MARGIN + grid.CELL_SIZE) * row + grid.MARGIN, # top x left
                             grid.CELL_SIZE,   # width of rect
                             grid.CELL_SIZE])  # height of rect
                
            clock.tick(120) # fps
            pg.display.flip() # draws new frame
        pg.quit()
    else:
        while t != t_max:
            update_ph_list = []
            agents = [agent for agent in agents if agent.move()] # removes ones that have reached their destination # todo reinstate movement
            # calculate pheromone increase
            for agent in agents:
                update_ph_list.extend(agent.spread_pheromone())
            # apply pheromone changes
            for agent, update_val in update_ph_list:
                agent.pheromone += update_val
            # add more agents
            agents.extend(grid.generate_agents())
            print(t)
            t += 1


grid = Grid(num_roads_on_axis = 5)
agent = grid.generate_agents(guarantee=2,)

# for stationary testing, code doesn't work if you randomy appear in middle of grid
# grid = Grid(num_roads_on_axis = 3)
# agent = [Agent(grid=grid, src=(0, 16, "n"), ID=1), Agent(grid=grid, src=(15, 16, "n"), ID=2), Agent(grid=grid, src=(15, 31, "n"), ID=3)] # down right (3->2->1) should detect 2 and 1
# agent = [Agent(grid=grid, src=(0, 16, "n"), ID=1), Agent(grid=grid, src=(15, 16, "n"), ID=2), Agent(grid=grid, src=(15, 10, "n"), ID=3)] # down left  (3<-2->1) should detect 3 and 1
# agent = [Agent(grid=grid, src=(0, 16, "n"), ID=1), Agent(grid=grid, src=(16, 16, "n"), ID=2), Agent(grid=grid, src=(16, 10, "n"), ID=3)] # down left
# agent = [Agent(grid=grid, src=(0, 16, "n"), ID=1), Agent(grid=grid, src=(15, 16, "n"), ID=2), Agent(grid=grid, src=(30, 16, "n"), ID=3)] # straight line down
# agent = [Agent(grid=grid, src=(0, 16, "n"), ID=1), Agent(grid=grid, src=(10, 16, "n"), ID=2)]

# for pheromone choice testing
# grid = Grid(num_roads_on_axis=2)
# agent = [Agent(grid=grid, src=(0, 16, "n"), ID=1), Agent(grid=grid, src=(15, 30, "n"), ID="tracker")] # n -> s 1 block to the first right
# agent = [Agent(grid=grid, src=(0, 16, "n"), ID=1), Agent(grid=grid, src=(30, 16, "n"), ID="tracker")] # n -> s 1 block in the downwards direction
start_time = time.time()
env_loop(grid=grid, agents=agent, visualise=False)
print(time.time() - start_time)#
# density 2 = roughly 3 mins and 11 seconds