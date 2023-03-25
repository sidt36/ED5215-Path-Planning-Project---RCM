import numpy as np 
import random

class RRTGraph:
    def __init__(self, start, goal, goal_dmax, step_size):
        self.start = start
        self.goal = goal
        self.goalFlag = False
        self.x = [self.start[0]]
        self.y = [self.start[1]]
        self.parent = [0]
        self.goalstate = None
        self.path = []
        self.goal_dmax = goal_dmax
        self.step_size = step_size

    def add_node(self, x, y, idx):
        self.x.append(x)
        self.y.append(y)
        self.parent.append(idx)
        
    def distance_from_nodes(self, x, y):
        xnp = np.array(self.x)
        ynp = np.array(self.y)
        return (x-xnp)**2 + (y-ynp)**2

    def nearest_node(self, x, y):
        dists = self.distance_from_nodes(x, y)
        nearest = np.argmin(dists)
        return self.x[nearest], self.y[nearest], nearest

    def sample_envir(self):
        # add bias
        x = int(random.uniform(0, 360))
        y = int(random.uniform(0, 360))
        return x, y
    
    def step(self, x1, y1, x2, y2, step_size):
        xstep = x1 + step_size * (x2 - x1)
        ystep = y1 + step_size * (y2 - y1)
        return xstep, ystep


    def collision_check(self, x1, y1, x2, y2):
        # collision check along path from node 1 to node 2
        # use step size
        pass

    def isGoalState(self, x, y):
        dist = (x-self.goal[0])**2 + (y-self.goal[1])**2
        return dist <= self.goal_dmax

    def getPath(self):
        # get path
        pass

    def rrt(self):
        while not self.goalFlag:
            step_size = self.step_size
            xsample, ysample = self.sample_envir()
            nnx, nny, idx = self.nearest_node(xsample, ysample)
            xnew, ynew = self.step(nnx, nny, xsample, ysample, step_size)
            if self.collision_check(nnx, nny, xnew, ynew):
                # reduce step size and try again?
                continue
            if self.isGoalState(xnew, ynew):
                self.goalstate = (xnew, ynew)
                self.goalFlag = True
            self.add_node(xnew, ynew, idx)
        self.path = self.getPath()
        return self.path


