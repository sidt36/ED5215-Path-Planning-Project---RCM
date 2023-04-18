# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:45:46 2023

@author: Tejas Rao
"""

#!/usr/bin/env python3
from __future__ import print_function
# from six.moves import input

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

import random
import numpy as np 
from FK import tf_total
from collision_checker import collision
class RRT_star:
    def __init__(self, start, goal, goalrad):
        self.ALPHA = 0.05
        self.GOALRAD = goalrad
        self.BIAS = 0.3
        self.DIST = 0.1
        self.NEIGH = 1
        self.start = start
        self.goal = goal
        self.goal_flag = False
        self.rangel, self.rangeh = -np.pi, np.pi 
        self.x1 = [self.start[0]]
        self.x2 = [self.start[1]]
        self.x3 = [self.start[2]]
        self.x4 = [self.start[3]]
        self.x5 = [self.start[4]]
        self.x6 = [self.start[5]]
        self.x7 = [self.start[6]]
        self.parents = [0]
        self.path = []
        self.goalidx = None
        self.goal_idxs = []

    def dist_squared_all(self, p):
        x1, x2, x3, x4, x5, x6, x7 = p
        d = (np.array(self.x1)-x1)**2 + (np.array(self.x2)-x2)**2 + (np.array(self.x3)-x3)**2 + (np.array(self.x4)-x4)**2 + (np.array(self.x5)-x5)**2 + (np.array(self.x6)-x6)**2 + (np.array(self.x7)-x7)**2
        return d
    
    def dist_squared(self, p1, p2):
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
        if self.BIAS > random.uniform(0, 1):
            return self.goal
        else:
            x1 = random.uniform(self.rangel, self.rangeh)
            x2 = random.uniform(self.rangel, self.rangeh)
            x3 = random.uniform(self.rangel, self.rangeh)
            x4 = random.uniform(self.rangel, self.rangeh)
            x5 = random.uniform(self.rangel, self.rangeh)
            x6 = random.uniform(self.rangel, self.rangeh)
            x7 = random.uniform(self.rangel, self.rangeh)
            return np.array([x1, x2, x3, x4, x5, x6, x7])
    
    def lin_interpol(self, p1, p2, alpha):
        p3 = p1 + alpha * (p2-p1)
        return p3

    def collision(self, p1, p2):
        # collision checker
        self.RCM_Coordinates = np.array([1.050300 ,0.150100 ,0.37])
        self.RCM_Orientation= np.array([-1,-1,1])
        self.RCM_Radius = 1
        self.Safety_Radius = 0.2
        ps = []
        for alpha in np.linspace(0, 1, 101):
            pnew= self.lin_interpol(p1, p2, alpha)
            ps.append(pnew)
        
        for p in ps:
            #return(collision(p,self.RCM_Coordinates,self.RCM_Orientation,self.RCM_Radius,self.Safety_Radius))
            pass
        return False

    def cut_dist(self, p1, p2):
        d = self.dist_squared(p1, p2)
        if d > self.DIST ** 2:
            pnew = p1 + self.DIST * (p2-p1) / np.sqrt(d)
        else:
            pnew = p2
        return pnew

    def FK(self, p):
        x1, x2, x3, x4, x5, x6, x7 = p
        EE_position,_ = tf_total(x1,x2,x3,x4,x5,x6,x7)
        return EE_position

    def is_goal(self, p):
        d = self.dist_squared(np.array(p), self.goal)
        return d <= self.GOALRAD ** 2
    
    def update_tree(self, k):
        p = np.array([self.x1[k], self.x2[k], self.x3[k], self.x4[k], self.x5[k], self.x6[k], self.x7[k]])
        d = self.dist_squared_all(p)
        idxs = list(np.where(d <= self.NEIGH**2)[0])
        cmin = self.get_cost(k)
        idxmin = self.parents[k]
        for i in idxs:
            if i == k:
                continue
            pi =  np.array([self.x1[i], self.x2[i], self.x3[i], self.x4[i], self.x5[i], self.x6[i], self.x7[i]])
            c = self.get_cost(i) + np.sqrt(self.dist_squared(p, pi))
            if  c < cmin:
                if not self.collision(p,pi):
                    cmin = c
                    idxmin = i
        self.parents[k] = idxmin

        for i in idxs:
            if i == k or i == 0:
                continue
            pi =  [self.x1[i], self.x2[i], self.x3[i], self.x4[i], self.x5[i], self.x6[i], self.x7[i]]
            if self.get_cost(k) + np.sqrt(self.dist_squared(p,pi)) < self.get_cost(i):
                if not self.collision(p,pi):
                    self.parents[i] = k
                    
    def add_node(self):
        xsample = self.sample_envir()
        xnear, pnear = self.nearest(xsample)
        xint = self.lin_interpol(xnear, xsample, self.ALPHA)
        xint = self.cut_dist(xnear, xint)
        self.update_tree(len(self.x1)-1)
        if not self.collision(xnear, xint):
            self.x1.append(xint[0])
            self.x2.append(xint[1])
            self.x3.append(xint[2])
            self.x4.append(xint[3])
            self.x5.append(xint[4])
            self.x6.append(xint[5])
            self.x7.append(xint[6])
            self.parents.append(pnear)
            if self.is_goal(xint):
                self.goal_flag = True
                print('Flag Changed')
                self.goalidx = len(self.x1) - 1
                self.goal_idxs.append(self.goalidx)
            return True
        return False
    
    def step(self):
        flag = False
        while not flag:
            flag = self.add_node()

    def get_path(self):
        self.goalidx = self.get_min_goal_idx()
        path = [(self.x1[self.goalidx], self.x2[self.goalidx], self.x3[self.goalidx], self.x4[self.goalidx], self.x5[self.goalidx], self.x6[self.goalidx], self.x7[self.goalidx])]
        p = self.parents[self.goalidx]
        while p != 0:
            path.append((self.x1[p], self.x2[p], self.x3[p], self.x4[p], self.x5[p], self.x6[p], self.x7[p]))
            p = self.parents[p]
        path.reverse()
        return path
    
    def get_point_from_idx(self, i):
        return np.array([self.x1[i], self.x2[i], self.x3[i], self.x4[i], self.x5[i], self.x6[i], self.x7[i]])

    def get_min_goal_idx(self):
        cmin = np.inf
        idxmin = 0
        for i in self.goal_idxs:
            pi = self.get_point_from_idx(i)
            c = self.dist_squared(pi, self.goal)
            if c <= cmin:
                cmin = c
                idxmin = i
        return idxmin

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
        iter = 0
        while iter < max_iter:
            iter += 1
            self.step()

            cmin = np.inf
            idxmin = 0
            for i in range(len(self.x1)):
                c = self.dist_squared(np.array([self.x1[i], self.x2[i], self.x3[i], self.x4[i], self.x5[i], self.x6[i], self.x7[i]]), np.array(self.goal))
                if c < cmin:
                    cmin = c
                    idxmin = i
            print(iter, np.sqrt(cmin))
        path = self.get_path()
        return path
    

if __name__ == "__main__":

    start = np.array([0.80423491,  1.90611439, -2.15948642 ,-0.78850263 ,-2.67168602 ,-1.2173844, 3.02918738])
    goal = np.array([ 0.94502209 , 1.23225196 , 1.76922747 , 1.87633753 ,-0.53324368 , 1.20997036, -1.49405437])
    goalrad = 1

    RRT_Instance = RRT_star(start, np.array(goal), goalrad)
    Path = RRT_Instance.run_algo(1000)
    print(tf_total(Path[-1][0],Path[-1][1],Path[-1][2],Path[-1][3],Path[-1][4],Path[-1][5],Path[-1][6]))
    print(Path)   
