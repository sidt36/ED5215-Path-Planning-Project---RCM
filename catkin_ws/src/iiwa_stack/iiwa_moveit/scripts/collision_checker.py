import numpy as np 
from FK import tf_total
import math

import numpy as np
def collision(config,RCM_Coordinates,RCM_Orientation,RCM_Radius,Safety_Radius):
    # Pass in as a list.
    x1, x2, x3, x4, x5, x6, x7 = config.tolist()
    Needle_Base_Position,_ = tf_total(x1,x2,x3,x4,x5,x6,x7,location='needle_base')
    Needle_Tip_Position,_ = tf_total(x1,x2,x3,x4,x5,x6,x7,location='needle_tip')
    Flag = True
    
    if Safety_Radius_Check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,Safety_Radius):
        #print('S_R_C', Safety_Radius_Check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,Safety_Radius))
        if orientation_check(Needle_Base_Position,Needle_Tip_Position,RCM_Orientation):
            #print('O_C', orientation_check(Needle_Base_Position,Needle_Tip_Position,RCM_Orientation))
            if constraint_check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,RCM_Radius):
                #print('C_C', constraint_check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,RCM_Radius))             
                Flag = False
    return Flag

def Safety_Radius_Check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,Safety_Radius):
    flag = False
    return True
    if(np.linalg.norm(Needle_Base_Position-RCM_Coordinates)>Safety_Radius):
        flag = True
        if(np.linalg.norm(Needle_Tip_Position-RCM_Coordinates)<=Safety_Radius):
            flag = True
            
    return flag        

def orientation_check(Needle_Base_Position,Needle_Tip_Position,RCM_Orientation):
    flag = False
    return True
    if(np.dot(Needle_Tip_Position-Needle_Base_Position,RCM_Orientation)>0):
        flag = True
    return flag  

def constraint_check(Needle_Base_Position,Needle_Tip_Position,RCM_Coordinates,RCM_Radius):
    x0  = Needle_Base_Position
    xf  = Needle_Tip_Position
    N = 1000
    epsilon = 1
    # Alternatively
    # epsilon = np.dot(Needle_Tip_Position-Needle_Base_Position,RCM_Orientation)/(np.linalg.norm(Needle_Base_Position-Needle_Base_Position)*np.linalg.norm(RCM_Orientation))
    way_pt_gen = np.linspace(0, 1, N, endpoint=False)
    flag = False
    for i in way_pt_gen:
        x = x0 + (xf-x0)*i
        if(np.linalg.norm(x - RCM_Coordinates)<= RCM_Radius*epsilon):
            return True
    return flag        


if __name__=="__main__":
    RCM_Coordinates = np.array([0.8,0.4,0.3])
    RCM_Orientation= np.array([-1,-1,1])
    RCM_Radius = 0.015
    Safety_Radius = 0.2

    configs = (-180 + 360*np.random.rand(100000,7))*np.pi/180
    for j in range(configs.shape[0]):
         config = configs[j,:] 
         if(not collision(config,RCM_Coordinates,RCM_Orientation,RCM_Radius,Safety_Radius)):
            print(config*180/np.pi)






  


