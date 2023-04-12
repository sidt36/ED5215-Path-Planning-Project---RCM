import random
import numpy as np 

class IRRT_star:
    def __init__(self, start, goal, goalrad, mapdims, obstacles):
        self.ALPHA = 0.5
        self.GOALRAD = goalrad
        self.BIAS = 0.2
        self.DIST = 30
        self.NEIGH = 50

        self.start = start
        self.goal = goal
        self.goal_flag = False
        self.goal_idxs = []
        self.maph, self.mapw = mapdims
        self.xs = [self.start[0]]
        self.ys = [self.start[1]]
        self.parents = [0]
        self.obstacles = obstacles
        self.goal_state = None
        self.path = []
        self.goalidx = None
        self.costs = {}

    def add_node(self, x_, y_, p_):
        self.xs.append(x_)
        self.ys.append(y_)
        self.parents.append(p_)
    
    def num_nodes(self):
        return len(self.x)
    
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
        if not self.goal_flag:
            if self.BIAS > random.uniform(0, 1) and not self.goal_flag:
                return self.goal[0], self.goal[1]
            else:
                x = int(random.uniform(0, self.mapw))
                y = int(random.uniform(0, self.maph))
                return x, y
        else:
            if self.BIAS/3 > random.uniform(0, 1) and not self.goal_flag:
                return self.goal[0], self.goal[1]
            else: 
                a = self.ellipse['a']
                b = self.ellipse['b']
                centre = self.ellipse['centre']
                alpha = self.ellipse['alpha']
                theta = random.uniform(0, 2 * np.pi)
                d = random.triangular(0, 1, 1)
                X = d * a * np.cos(theta)
                Y = d * b * np.sin(theta)
                x = centre[0] + np.cos(alpha) * Y + np.sin(alpha) * X
                y = centre[1] - np.sin(alpha) * Y + np.cos(alpha) * X
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
        for obs in self.obstacles:
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

    def update_tree(self, k):
        d = self.dist_squared_all(self.xs[k], self.ys[k])
        idxs = list(np.where(d <= self.NEIGH**2)[0])
        cmin = self.get_cost(k)
        idxmin = self.parents[k]
        for i in idxs:
            if i == k:
                continue
            c = self.get_cost(i) + np.sqrt(self.dist_squared(self.xs[k], self.ys[k], self.xs[i], self.ys[i]))
            if  c < cmin:
                if not self.collision(self.xs[k], self.ys[k], self.xs[i], self.ys[i]):
                    cmin = c
                    idxmin = i
        self.parents[k] = idxmin
        for i in idxs:
            if i == k or i == 0:
                continue
            if self.get_cost(k) + np.sqrt(self.dist_squared(self.xs[k], self.ys[k], self.xs[i], self.ys[i])) < self.get_cost(i):
                if not self.collision(self.xs[k], self.ys[k], self.xs[i], self.ys[i]):
                    self.parents[i] = k

    def add_node(self):
        xsample, ysample = self.sample_envir()
        xnear, ynear, pnear = self.nearest(xsample, ysample)
        xint, yint = self.lin_interpol(xnear, ynear, xsample, ysample, self.ALPHA)
        xint, yint = self.cut_dist(xnear, ynear, xint, yint)
        if not self.collision(xnear, ynear, xint, yint):
            self.xs.append(xint)
            self.ys.append(yint)
            self.parents.append(pnear)
            self.update_tree(len(self.xs)-1)
            if self.is_goal(xint, yint):
                self.goal_flag = True
                self.goalidx = len(self.xs) - 1
                self.goal_idxs.append(self.goalidx)
                goalx = self.xs[self.get_min_goal_idx()]
                goaly = self.ys[self.get_min_goal_idx()]
                alpha = np.arctan2(goalx - self.start[0], goaly - self.start[1])
                centre = ((self.start[0] + goalx)/2, (self.start[1] + goaly)/2)
                a = self.get_goal_cost()/2
                b = np.sqrt(a**2 - self.dist_squared(goalx, goaly, centre[0], centre[1]))
                self.ellipse = {'alpha': alpha, 'centre':centre, 'a':a, 'b':b}
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

    def get_min_goal_idx(self):
        cmin = np.inf
        idxmin = 0
        for i in self.goal_idxs:
            c = self.dist_squared(self.goal[0], self.goal[1], self.xs[i], self.ys[i])
            if c <= cmin:
                cmin = c
                idxmin = i
        return idxmin

    def get_path(self):
        idxmin = self.get_min_goal_idx()
        path = [(self.xs[idxmin], self.ys[idxmin])]
        p = self.parents[idxmin]
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
        while True:
            c = c + np.sqrt(self.dist_squared(x, y, self.xs[p], self.ys[p]))
            x = self.xs[p]
            y = self.ys[p]
            if p == 0:
                break
            p = self.parents[p]
        return c

    def get_goal_cost(self):
        return self.get_cost(self.get_min_goal_idx())

    def run_algo(self):
        while not self.goal_flag:
            self.step
        path = self.get_path()
        return path