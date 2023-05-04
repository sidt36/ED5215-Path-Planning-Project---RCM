import pygame
import time 
import numpy as np
from environment import envir
from RRT import RRT
from RRT_star import RRT_star
from Informed_RRT_star import IRRT_star
from RRT_variation import RRT_2
from RRT_Connect import RRTC
import imageio

def main():
    # ALGO = 'RRT'
    # ALGO = 'RRT_star'
    # ALGO = 'IRRT_star'
    # ALGO = 'RRT_2'
    ALGO = 'RRTC'

    MAPDIMS = (500, 1000)
    START = (100, 250)
    GOAL = (900, 250)
    OBSDIM = 30
    OBSNUM = 200
    GOALRAD = 30
    MAP = 4

    # Obstacles: 200, dims: 30
    # Hard: 0, 3, 6, 7
    # Medium: 1
    # Easy: 2
    SEED = 1
    

    pygame.init()
    map_ = envir(START, GOAL, GOALRAD, MAPDIMS, ALGO, OBSDIM, OBSNUM, MAP)
    obstacles = map_.makeobs(SEED)
    # map_.drawMap(obstacles)

    times = []

    for i in range(100):
        print(i)

        if ALGO == 'RRT':
            algo = RRT(START, GOAL, GOALRAD, MAPDIMS, obstacles)
        elif ALGO == 'RRT_star':
            algo = RRT_star(START, GOAL, GOALRAD, MAPDIMS, obstacles)
        elif ALGO == 'IRRT_star':
            algo = IRRT_star(START, GOAL, GOALRAD, MAPDIMS, obstacles)
        elif ALGO == 'RRT_2':
            algo = RRT_2(START, GOAL, GOALRAD, MAPDIMS, obstacles)
        elif ALGO == 'RRTC':
            algo = RRTC(START, GOAL, GOALRAD, MAPDIMS, obstacles)

        t1 = time.time()
        ITER = 0
        while ITER < 2000:
            ITER += 1
            _ = algo.visualize_step()
            if algo.goal_flag:
                t2 = time.time()
                times.append(t2-t1)
                break
    print(np.mean(times))
    pygame.quit()



if __name__ == '__main__':
    main()