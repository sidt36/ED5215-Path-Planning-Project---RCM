import pygame
import random
import numpy as np

class envir:
    def __init__(self, start, goal, goalrad, mapdims, obsdim=0, obsnum=0, MAP=0):
        self.start = start
        self.goal = goal
        self.mapdims = mapdims
        self.maph, self.mapw = mapdims
        self.goalrad = goalrad
        self.MAP = MAP
        
        self.map_window_name = 'Test'
        pygame.display.set_caption(self.map_window_name)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.fill((255, 255, 255))
        self.nodeRad = 2
        self.nodeThickness = 0
        self.edgeThickness = 1

        self.obstacles = []
        self.obsDim = obsdim
        self.obsNum = obsnum

        # Colors
        self.grey = (70, 70, 70)
        self.Blue = (0, 0, 255)
        self.Green = (0, 255, 0)
        self.Red = (255, 0, 0)
        self.white = (255, 255, 255)
    
    def draw_all_nodes(self, xs, ys):
        for x, y in zip(xs,ys):
            self.drawNode(x, y)
    
    def draw_all_edges(self, xs, ys, ps):
        for i in range(1, len(xs)):
            self.drawEdge(xs[i], ys[i], xs[ps[i]], ys[ps[i]])

    def reset_draw_everything(self, x, y, p):
        self.map.fill((255, 255, 255))
        self.drawMap(self.obstacles)
        self.draw_all_nodes(x, y)
        self.draw_all_edges(x, y, p)

    def makeRandomRect(self):
        uppercornerx = int(np.random.uniform(0, self.mapw - self.obsDim))
        uppercornery = int(np.random.uniform(0, self.maph - self.obsDim))
        return (uppercornerx, uppercornery)
    
    def makeobs(self, seed=0):
        obs = []
        if self.MAP == 0:
            np.random.seed(seed)
            for i in range(0, self.obsNum):
                rectang = None
                startgoalcol = True
                while startgoalcol:
                    upper = self.makeRandomRect()
                    rectang = pygame.Rect(upper, (self.obsDim, self.obsDim))
                    if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                        startgoalcol = True
                    else:
                        startgoalcol = False
                obs.append(rectang)

        elif self.MAP == 1:
            rects = {'rect1': ((500, 0), (30, 146)),
                     'rect2': ((500, 154), (30, 346))}
            for rect in rects.keys():
                print(rects[rect][0])
                obs.append(pygame.Rect(rects[rect][0], rects[rect][1]))
        
        elif self.MAP == 2:
            rects = {'rect1': ((500, 100), (30, 46)),
                     'rect2': ((500, 154), (30, 246))}
            for rect in rects.keys():
                print(rects[rect][0])
                obs.append(pygame.Rect(rects[rect][0], rects[rect][1]))

        elif self.MAP == 3:
            rects = {'rect1': ((500, 0), (30, 346)),
                     'rect2': ((500, 354), (30, 146)),
                     'rect3': ((400, 0), (30, 146)),
                     'rect4': ((400, 154), (30, 346)),
                     'rect5': ((600, 0), (30, 146)),
                     'rect6': ((600, 154), (30, 346))}
            for rect in rects.keys():
                print(rects[rect][0])
                obs.append(pygame.Rect(rects[rect][0], rects[rect][1]))
        
        elif self.MAP == 4:
            rects = {'rect1': ((500, 50), (30, 146)),
                     'rect2': ((500, 204), (30, 196)),
                     'rect3': ((400, 100), (30, 46)),
                     'rect4': ((400, 154), (30, 246)),
                     'rect5': ((600, 100), (30, 46)),
                     'rect6': ((600, 154), (30, 246))}
            for rect in rects.keys():
                print(rects[rect][0])
                obs.append(pygame.Rect(rects[rect][0], rects[rect][1]))

        self.obstacles = obs.copy()
        return obs
    
    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, self.Green, self.start, self.nodeRad + 5, 0)
        pygame.draw.circle(self.map, self.Green, self.goal, self.goalrad, 1)
        self.drawObs(obstacles)

    def drawPath(self, path):
        pygame.draw.circle(self.map, self.Green, path[0], 3, 0)
        for i in range(1, len(path)):
            pygame.draw.circle(self.map, self.Green, path[i], 3, 0)
            pygame.draw.line(self.map, self.Green, path[i], path[i-1], self.edgeThickness)
    
    def drawObs(self, obstacles):
        obstaclesList = obstacles.copy()
        while (len(obstaclesList) > 0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)
    
    def drawNode(self, x, y):
        pygame.draw.circle(self.map, self.grey, (x, y), self.nodeRad*2, 0)

    def drawEdge(self, x1, y1, x2, y2):
        pygame.draw.line(self.map, self.Blue, (x1, y1), (x2, y2), self.edgeThickness)

    def draw_ellipse(self, ellipse):
        a = ellipse['a']
        b = ellipse['b']
        centre = ellipse['centre']
        alpha = ellipse['alpha']
        pointsx = []
        pointsy = []
        for theta in np.linspace(0, 2*np.pi, 200):
            X = a * np.cos(theta)
            Y = b * np.sin(theta)
            x = centre[0] + np.cos(alpha) * Y + np.sin(alpha) * X
            y = centre[1] - np.sin(alpha) * Y + np.cos(alpha) * X
            pointsx.append(x)
            pointsy.append(y)
        for i in range(1, len(pointsx)):
            pygame.draw.line(self.map, self.Red, (pointsx[i], pointsy[i]), (pointsx[i-1], pointsy[i-1]), self.edgeThickness)