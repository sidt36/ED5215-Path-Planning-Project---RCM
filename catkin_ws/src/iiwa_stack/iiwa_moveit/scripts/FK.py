#!/usr/bin/env python3
# Reference: https://github.com/yongan007/inverse_foward_kinematics_Kuka_iiwa/blob/master/FKinematics.m
import numpy as np
import math

def tf(t,d,a,al):
    T=np.array([[math.cos(t),-math.sin(t)*math.cos(al*3.14/180),math.sin(t)*math.sin(al*3.14/180),a*math.cos(t)],
                        [math.sin(t),math.cos(t)*math.cos(al*3.14/180),-math.cos(t)*math.sin(al*3.14/180),a*math.sin(t)],
                        [0,math.sin(al*3.14/180),math.cos(al*3.14/180),d],
                        [0,0,0,1]])
    return T

def tf_total(x1,x2,x3,x4,x5,x6,x7,location='needle_tip'):
    #Verfied the DH Parameters to be Accurate
    d1 = 0.34
    d3 = 0.4
    d5 = 0.4
    d7 = 0.645

    if(location == 'needle_base'):
        d7 = 0.126
    if(location == 'needle_tip'):
        d7 = 0.645

    TF1 = tf(x1,d1,0,-90)
    TF2 = tf(x2,0,0,90)
    TF3 = tf(x3,d3,0,90)
    TF4 = tf(x4,0,0,-90)
    TF5 = tf(x5,d5,0,-90)
    TF6 = tf(x6,0,0,90)
    TF7 = tf(x7,d7,0,0)
    
    TF = TF1.dot(TF2).dot(TF3).dot(TF4).dot(TF5).dot(TF6).dot(TF7)
    
    EE_Position = TF[0:3,3]
    EE_Orientation = TF[0:3,0:3]

    return(EE_Position,EE_Orientation)


if __name__ == "__main__":
    start = [34.549541573151316, 25.033332285942997, 17.853776133305487, -47.38517110902736,-29.875131140872302, 70.1306076478629, -19.783874754727584 ]
    start = [i*np.pi/180 for i in start]
    goal = np.array([44,23,15,-44,-37,80,0])*np.pi/180
    print(goal)
    print(tf_total(start[0],start[1],start[2],start[3],start[4],start[5],start[6]))
    print(tf_total(goal[0],goal[1],goal[2],goal[3],goal[4],goal[5],goal[6]))





    