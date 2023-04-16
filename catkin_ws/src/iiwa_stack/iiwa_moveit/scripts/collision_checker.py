import numpy as np 
from fk import tf_total
import math

import numpy as np
def collision(config,RCM_Coordinates,RCM_Orientation,RCM_Radius,Safety_Radius):
    # Pass in as a list.
    x1, x2, x3, x4, x5, x6, x7 = config
    Needle_Base_Position = tf_total(x1,x2,x3,x4,x5,x6,x7,location='needle_base')
    Needle_Tip_Position = tf_total(x1,x2,x3,x4,x5,x6,x7,location='needle_tip')
    Flag = False
    if Safety_Radius_Check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,Safety_Radius):
        if orientation_check(Needle_Base_Position,Needle_Tip_Position,RCM_Orientation):
            if constraint_check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,RCM_Radius):
                Flag = True
    return Flag

def Safety_Radius_Check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,Safety_Radius):
    flag = False

    if(np.linalg.norm(Needle_Base_Position-RCM_Coordinates)>Safety_Radius):
        if(np.linalg.norm(Needle_Tip_Position-RCM_Coordinates)<=Safety_Radius):
            flag = True

    return flag        

def orientation_check(Needle_Base_Position,Needle_Tip_Position,RCM_Orientation):
    flag = False

    if(np.dot(Needle_Tip_Position-Needle_Base_Position,RCM_Orientation)>0):
        flag = True
        
    return flag  

def constraint_check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,RCM_Radius):
    x0  = Needle_Base_Position
    xf  = Needle_Tip_Position
    N = 50
    epsilon = 0.7
    # Alternatively
    # epsilon = np.dot(Needle_Tip_Position-Needle_Base_Position,RCM_Orientation)/(np.linalg.norm(Needle_Base_Position-Needle_Base_Position)*np.linalg.norm(RCM_Orientation))
    way_pt_gen = np.linspace(0, 1, N, endpoint=False)

    flag = False

    for i in way_pt_gen:
        x = x0 + xf*i
        if(np.linalg.norm(x - RCM_Coordinates)<= RCM_Radius*epsilon):
            flag = True

    return flag        





  


