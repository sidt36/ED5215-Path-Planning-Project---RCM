import pygame
import time 
from environment import envir
from RRT import RRT
from RRT_star import RRT_star
from Informed_RRT_star import IRRT_star

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
    MAP = 4

    # Obstacles: 200, dims: 30
    # Hard: 0, 3, 6, 7
    # Medium: 1
    # Easy: 2
    SEED = 6
    
    pygame.init()
    map_ = envir(START, GOAL, GOALRAD, MAPDIMS, OBSDIM, OBSNUM, MAP)
    obstacles = map_.makeobs(SEED)
    map_.drawMap(obstacles)
    ITER = 0

    if ALGO == 'RRT':
        algo = RRT(START, GOAL, GOALRAD, MAPDIMS, obstacles)
    elif ALGO == 'RRT_star':
        algo = RRT_star(START, GOAL, GOALRAD, MAPDIMS, obstacles)
    elif ALGO == 'IRRT_star':
        algo = IRRT_star(START, GOAL, GOALRAD, MAPDIMS, obstacles)

    # t1=time.time()
    while ITER <= 5000:
        ITER += 1
        print(f'Searching for Goal, {ITER}')

        X, Y, P = algo.visualize_step()

        if ITER % 1 == 0:
            map_.reset_draw_everything(X, Y, P)
            if algo.goal_flag:
                map_.drawPath(algo.get_path())
                if ALGO == 'IRRT_star':
                    map_.draw_ellipse(algo.ellipse) 
            pygame.display.update()
            # time.sleep(0.5)

    print('Goal Found')
    print(f'Cost to Goal: {algo.get_goal_cost()}')
    # map_.drawPath(algo.get_path())
    # pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(15000)



if __name__ == '__main__':
    # result=False
    # while not result:
    #     try:
    #         main()
    #         result=True
    #     except:
    #         result=False
    main()