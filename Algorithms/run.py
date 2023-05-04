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
    MAP = 1

    # Obstacles: 200, dims: 30
    # Hard: 0, 3, 6, 7
    # Medium: 1
    # Easy: 2
    SEED = 1
    
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
    elif ALGO == 'RRT_2':
        algo = RRT_2(START, GOAL, GOALRAD, MAPDIMS, obstacles)
    elif ALGO == 'RRTC':
        algo = RRTC(START, GOAL, GOALRAD, MAPDIMS, obstacles)

    # t1=time.time()
    while ITER < 500:
        ITER += 1
        print(f'Searching for Goal, {ITER}')

        if ALGO != 'RRTC':
            X, Y, P = algo.visualize_step()
        else:
            start_tree, goal_tree = algo.visualize_step()
            X1, Y1, P1 = start_tree['xs'], start_tree['ys'], start_tree['parents']
            X2, Y2, P2 = goal_tree['xs'], goal_tree['ys'], goal_tree['parents']
        if ITER % 10 == 0:
            if ALGO != 'RRTC':
                map_.reset_draw_everything(X, Y, P)
            else:
                map_.reset_draw_everything(X1, Y1, P1)
                map_.draw_everything(X2, Y2, P2)
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
    if ALGO != 'RRTC':
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