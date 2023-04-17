import random
import numpy as np 

class RRTC:
    def __init__(self, start, goal, goalrad, mapdims, obstacles):
        self.ALPHA = 0.5
        self.GOALRAD = goalrad
        self.BIAS = 0.2
        self.DIST = 30

        self.start = start
        self.goal = goal
        self.goal_flag = False
        self.maph, self.mapw = mapdims
        self.xs = [self.start[0]]
        self.ys = [self.start[1]]
        self.parents = [0]
        self.obstacles = obstacles
        self.path = []
        self.goalidx = 0

    def dist_squared_all(self, x, y):
        d = (np.array(self.xs)-x)**2 + (np.array(self.ys)-y)**2
        return d
    
    def dist_squared(self, x1, y1, x2, y2):
        return (x2-x1)**2 + (y2-y1)**2
    
    def nearest(self, x, y):
        d = self.dist_squared_all(x, y)
        idxnear = np.argmin(d)
        xnear = self.xs[idxnear]
        ynear = self.ys[idxnear]
        return xnear, ynear, idxnear

    def sample_envir(self):
        if self.BIAS > random.uniform(0, 1):
            return self.goal[0], self.goal[1]
        else:
            x = int(random.uniform(0, self.mapw))
            y = int(random.uniform(0, self.maph))
            return x, y
    
    def lin_interpol(self, x1, y1, x2, y2, alpha):
        xint = x1 + alpha * (x2-x1)
        yint = y1 + alpha * (y2-y1)
        return xint, yint

    def collision(self, x1, y1, x2, y2):
        xs = []
        ys = []
        for alpha in np.linspace(0, 1, 101):
            xnew, ynew = self.lin_interpol(x1, y1, x2, y2, alpha)
            xs.append(xnew)
            ys.append(ynew)
        for obs in self.obstacles.copy():
            for x, y in zip(xs, ys):
                if obs.collidepoint(x, y):
                    return True
        return False

    def cut_dist(self, x1, y1, x2, y2):
        d = self.dist_squared(x1, y1, x2, y2)
        if d > self.DIST ** 2:
            xnew = x1 + self.DIST * (x2-x1) / np.sqrt(d)
            ynew = y1 + self.DIST * (y2-y1) / np.sqrt(d)
        else:
            xnew = x2
            ynew = y2
        return xnew, ynew

    def add_node(self):
        xsample, ysample = self.sample_envir()
        xnear, ynear, pnear = self.nearest(xsample, ysample)
        xint, yint = self.lin_interpol(xnear, ynear, xsample, ysample, self.ALPHA)
        xint, yint = self.cut_dist(xnear, ynear, xint, yint)
        if not self.collision(xnear, ynear, xint, yint):
            self.xs.append(xint)
            self.ys.append(yint)
            self.parents.append(pnear)
            if self.is_goal(xint, yint) and not self.goal_flag:
                self.goal_flag = True
                self.goalidx = len(self.xs) - 1
            return True
        return False
    
    def is_goal(self, x, y):
        d = self.dist_squared(x, y, self.goal[0], self.goal[1])
        return d <= self.GOALRAD ** 2
    
    def step(self):
        flag = False
        while not flag:
            flag = self.add_node()
    
    def visualize_step(self):
        self.step()
        return self.xs, self.ys, self.parents

    def get_path(self):
        path = [(self.xs[self.goalidx], self.ys[self.goalidx])]
        p = self.parents[self.goalidx]
        while p != 0:
            path.append((self.xs[p], self.ys[p]))
            p = self.parents[p]
        path.reverse()
        return path

    def get_cost(self, n):
        c = 0
        x = self.xs[n]
        y = self.ys[n]
        p = self.parents[n]
        while p != 0:
            c += np.sqrt(self.dist_squared(x, y, self.xs[p], self.ys[p]))
            x = self.xs[p]
            y = self.ys[p]
            p = self.parents[p]
        return c

    def get_goal_cost(self):
        return self.get_cost(self.goalidx)

    def run_algo(self):
        while not self.goal_flag:
            self.step
        path = self.get_path()
        return path