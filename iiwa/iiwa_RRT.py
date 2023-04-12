import random
import numpy as np 

class RRT:
    def __init__(self, start, goal, goalrad, mapdims, obstacles):
        self.ALPHA = 0.5
        self.GOALRAD = goalrad
        self.BIAS = 0.2
        self.DIST = 30

        self.start = start
        self.goal = goal
        self.goal_flag = False
        # self.maph, self.mapw = mapdims
        # low and high range:
        self.rangel, self.rangeh = -np.pi, np.pi 
        self.x1 = [self.start[0]]
        self.x2 = [self.start[1]]
        self.x3 = [self.start[2]]
        self.x4 = [self.start[3]]
        self.x5 = [self.start[4]]
        self.x6 = [self.start[5]]
        self.x7 = [self.start[6]]
        self.parents = [0]
        # self.obstacles = obstacles
        self.path = []
        self.goalidx = None

    def dist_squared_all(self, p):
        x1, x2, x3, x4, x5, x6, x7 = p
        d = (np.array(self.x1)-x1)**2 + (np.array(self.x2)-x2)**2 + (np.array(self.x3)-x3)**2 + (np.array(self.x4)-x4)**2 + (np.array(self.x5)-x5)**2 + (np.array(self.x6)-x6)**2 + (np.array(self.x7)-x7)**2
        return d
    
    def dist_squared(self, p1, p2):
        # Can be used for cartesian as well as 7 dof coords
        return np.sum((p2-p1)**2)
    
    def nearest(self, p):
        d = self.dist_squared_all(p)
        idxnear = np.argmin(d)
        x1near = self.x1[idxnear]
        x2near = self.x2[idxnear]
        x3near = self.x3[idxnear]
        x4near = self.x4[idxnear]
        x5near = self.x5[idxnear]
        x6near = self.x6[idxnear]
        x7near = self.x7[idxnear]
        return np.array([x1near, x2near, x3near, x4near, x5near, x6near, x7near]), idxnear

    def sample_envir(self):
        # # If IK available:
        # if self.BIAS > random.uniform(0, 1):
        #     # Return IK of goal
        #     pass
        # else:
        #     x1 = int(random.uniform(self.rangel, self.rangeh))
        #     x2 = int(random.uniform(self.rangel, self.rangeh))
        #     x3 = int(random.uniform(self.rangel, self.rangeh))
        #     x4 = int(random.uniform(self.rangel, self.rangeh))
        #     x5 = int(random.uniform(self.rangel, self.rangeh))
        #     x6 = int(random.uniform(self.rangel, self.rangeh))
        #     x7 = int(random.uniform(self.rangel, self.rangeh))
        #     return np.array([x1, x2, x3, x4, x5, x6, x7])
        x1 = int(random.uniform(self.rangel, self.rangeh))
        x2 = int(random.uniform(self.rangel, self.rangeh))
        x3 = int(random.uniform(self.rangel, self.rangeh))
        x4 = int(random.uniform(self.rangel, self.rangeh))
        x5 = int(random.uniform(self.rangel, self.rangeh))
        x6 = int(random.uniform(self.rangel, self.rangeh))
        x7 = int(random.uniform(self.rangel, self.rangeh))
        return np.array([x1, x2, x3, x4, x5, x6, x7])
        
    def lin_interpol(self, p1, p2, alpha):
        p3 = p1 + alpha * (p2-p1)
        return p3

    def collision_checker(self):
        # Add collision checker
        # Return True if collision else False
        return False

    def collision(self, p1, p2):
        # collision checker
        ps = []
        for alpha in np.linspace(0, 1, 101):
            pnew= self.lin_interpol(p1, p2, alpha)
            ps.append(pnew)
        
        for p in ps:
            if self.collision_checker(p):
                return True
        return False

    def cut_dist(self, p1, p2):
        d = self.dist_squared(p1, p2)
        if d > self.DIST ** 2:
            pnew = p1 + self.DIST * (p2-p1) / np.sqrt(d)
        else:
            pnew = p2
        return pnew

    def FK(self, p):
        # Implement FK, takes x1-x7 and returns cartesian coords
        pass

    def is_goal(self, p):
        x, y, z = self.FK(p)
        d = self.dist_squared(np.array(x, y, z), np.array(self.goal))
        return d <= self.GOALRAD ** 2

    def add_node(self):
        xsample = self.sample_envir()
        xnear, pnear = self.nearest(xsample)
        xint = self.lin_interpol(xnear, xsample, self.ALPHA)
        xint = self.cut_dist(xnear, xint)
        if not self.collision(xnear, xint):
            self.x1.append(xint[0])
            self.x2.append(xint[1])
            self.x3.append(xint[2])
            self.x4.append(xint[3])
            self.x5.append(xint[4])
            self.x6.append(xint[5])
            self.x7.append(xint[6])
            self.parents.append(pnear)
            if self.is_goal(xint) and not self.goal_flag:
                self.goal_flag = True
                self.goalidx = len(self.x1) - 1
            return True
        return False
    
    def step(self):
        flag = False
        while not flag:
            flag = self.add_node()
    
    # def visualize_step(self):
    #     self.step()
    #     return self.x1, self.x2, self.x3, self.x4, self.x5, self.x6, self.x7, self.parents

    def get_path(self):
        path = [(self.x1[self.goalidx], self.x2[self.goalidx], self.x3[self.goalidx], self.x4[self.goalidx], self.x5[self.goalidx], self.x6[self.goalidx], self.x7[self.goalidx])]
        p = self.parents[self.goalidx]
        while p != 0:
            path.append((self.x1[p], self.x2[p], self.x3[p], self.x4[p], self.x5[p], self.x6[p], self.x7[p]))
            p = self.parents[p]
        path.reverse()
        return path

    def get_cost(self, n):
        c = 0
        x = np.array((self.x1[n], self.x2[n], self.x3[n], self.x4[n], self.x5[n], self.x6[n], self.x7[n]))
        p = self.parents[n]
        while p != 0:
            c += np.sqrt(self.dist_squared(x, np.array((self.x1[p], self.x2[p], self.x3[p], self.x4[p], self.x5[p], self.x6[p], self.x7[p]))))
            x = np.array((self.x1[p], self.x2[p], self.x3[p], self.x4[p], self.x5[p], self.x6[p], self.x7[p]))
            p = self.parents[p]
        return c

    def get_goal_cost(self):
        return self.get_cost(self.goalidx)

    def run_algo(self, max_iter):
        for iter in range(1,1 + max_iter):
            self.step()
            if self.goal_flag:
                break
        path = self.get_path()
        return path