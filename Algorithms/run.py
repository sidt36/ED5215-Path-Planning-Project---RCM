import pygame
import time 
import numpy as np
from environment import envir
from RRT import RRT
from RRT_star import RRT_star
from Informed_RRT_star import IRRT_star
import imageio

def main():
    # ALGO = 'RRT'
    # ALGO = 'RRT_star'
    ALGO = 'IRRT_star'

    MAPDIMS = (500, 1000)
    START = (100, 250)
    GOAL = (900, 250)
    OBSDIM = 30
    OBSNUM = 200
    GOALRAD = 30
    MAP = 0

    # Obstacles: 200, dims: 30
    # Hard: 0, 3, 6, 7
    # Medium: 1
    # Easy: 2
    SEED = 6
    
    frames = []
    path = 'D:\IITM Academic Stuff\Sem 8 Books\ED5215\Project\ED5215-Path-Planning-Project---RCM\Algorithms\Result_GIFs'
    gif_name = path + '\Map' + str(MAP) + '_' + ALGO + '.gif'
    print(gif_name)

    pygame.init()
    map_ = envir(START, GOAL, GOALRAD, MAPDIMS, ALGO, OBSDIM, OBSNUM, MAP)
    obstacles = map_.makeobs(SEED)
    map_.drawMap(obstacles)
    ITER = -1

    if ALGO == 'RRT':
        algo = RRT(START, GOAL, GOALRAD, MAPDIMS, obstacles)
    elif ALGO == 'RRT_star':
        algo = RRT_star(START, GOAL, GOALRAD, MAPDIMS, obstacles)
    elif ALGO == 'IRRT_star':
        algo = IRRT_star(START, GOAL, GOALRAD, MAPDIMS, obstacles)

    # t1=time.time()
    while ITER < 3000:
        ITER += 1
        print(f'Searching for Goal, {ITER}')

        X, Y, P = algo.visualize_step()

        if ITER % 100 == 0:
            map_.reset_draw_everything(X, Y, P)
            if algo.goal_flag:
                map_.drawPath(algo.get_path())
                if ALGO == 'IRRT_star':
                    map_.draw_ellipse(algo.ellipse) 
            pygame.display.update()
            # time.sleep(0.5)

            frame = pygame.surfarray.array3d(pygame.display.get_surface())
            frame = np.flip(frame, 0)
            frame = np.rot90(frame, k=3)
            frames.append(frame)

    print('Goal Found')
    print(f'Cost to Goal: {algo.get_goal_cost()}')
    # map_.drawPath(algo.get_path())
    # pygame.display.update()
    pygame.event.clear()

    # imageio.mimsave(gif_name, frames, fps=5)
    
    # pygame.event.wait(5000)
    pygame.quit()



if __name__ == '__main__':
    # result=False
    # while not result:
    #     try:
    #         main()
    #         result=True
    #     except:
    #         result=False
    main()