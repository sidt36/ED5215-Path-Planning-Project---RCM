import random
import numpy as np 

class RRTC:
    def __init__(self, start, goal, goalrad, mapdims, obstacles):
        self.GOALRAD = goalrad
        self.BIAS = 0.2
        self.DIST = 30

        self.start = start
        self.goal = goal
        self.goal_flag = False
        self.maph, self.mapw = mapdims
        self.start_tree = {'xs':[self.start[0]],
                           'ys':[self.start[1]],
                           'parents': [0]}
        self.goal_tree = {'xs':[self.goal[0]],
                          'ys':[self.goal[1]],
                          'parents': [0]}
        self.obstacles = obstacles
        self.path = []

    def dist_squared_all(self, x, y, tree):
        d = (np.array(tree['xs'])-x)**2 + (np.array(tree['ys'])-y)**2
        return d
    
    def dist_squared(self, x1, y1, x2, y2):
        return (x2-x1)**2 + (y2-y1)**2
    
    def nearest(self, x, y, tree):
        d = self.dist_squared_all(x, y, tree)
        idxnear = np.argmin(d)
        xnear = tree['xs'][idxnear]
        ynear = tree['ys'][idxnear]
        return xnear, ynear, idxnear

    def sample_env(self, tree):
        if self.BIAS > random.uniform(0, 1):
            idx = np.random.choice(len(tree['xs']))
            x = tree['xs'][idx]
            y = tree['ys'][idx]
        else:
            x = int(random.uniform(0, self.mapw))
            y = int(random.uniform(0, self.maph))
            idx = None
        return x, y, idx
    
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
        flag = False
        # Adding node to start tree
        xsample, ysample, idx = self.sample_env(self.goal_tree)
        xnear, ynear, pnear = self.nearest(xsample, ysample, self.start_tree)
        xint, yint = self.cut_dist(xnear, ynear, xsample, ysample)
        if not self.collision(xnear, ynear, xint, yint):
            self.start_tree['xs'].append(xint)
            self.start_tree['ys'].append(yint)
            self.start_tree['parents'].append(pnear)
            flag = True
            if (xint in self.goal_tree['xs']) and (yint in self.goal_tree['ys']) and (idx is not None):
                self.goal_flag = True
                self.goal_tree_idx = idx
                self.start_tree_idx = len(self.start_tree['xs']) - 1
                return True
        
        # Adding node to goal tree
        xsample, ysample, flag = self.sample_env(self.start_tree)
        xnear, ynear, pnear = self.nearest(xsample, ysample, self.goal_tree)
        xint, yint = self.cut_dist(xnear, ynear, xsample, ysample)
        if not self.collision(xnear, ynear, xint, yint):
            self.goal_tree['xs'].append(xint)
            self.goal_tree['ys'].append(yint)
            self.goal_tree['parents'].append(pnear)
            flag = True
            if (xint in self.start_tree['xs']) and (yint in self.start_tree['ys']) and (idx is not None):
                self.goal_flag = True
                self.goal_tree_idx = len(self.goal_tree['xs']) - 1
                self.start_tree_idx = idx
                return True
        return flag
    
    def step(self):
        flag = False
        while not flag:
            flag = self.add_node()
    
    def visualize_step(self):
        self.step()
        return self.start_tree, self.goal_tree

    def get_path(self):
        if len(self.path) > 1:
            return self.path
        path1 = [(self.start_tree['xs'][self.start_tree_idx], self.start_tree['ys'][self.start_tree_idx])]
        p = self.start_tree['parents'][self.start_tree_idx]
        while p != 0:
            path1.append((self.start_tree['xs'][p], self.start_tree['ys'][p]))
            p = self.start_tree['parents'][p]
        path1.reverse()

        path2 = [(self.goal_tree['xs'][self.goal_tree_idx], self.goal_tree['ys'][self.goal_tree_idx])]
        p = self.goal_tree['parents'][self.goal_tree_idx]
        while p != 0:
            path2.append((self.goal_tree['xs'][p], self.goal_tree['ys'][p]))
            p = self.goal_tree['parents'][p]
        self.path = path1 + path2
        return self.path

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
        print('CODE EXECUTED')
        return path
    