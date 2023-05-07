#!/usr/bin/env python3
from FK import tf_total
from RRT_7D import RRT 
from RRT_Star_7D import RRT_star
from IRRT_Star_7D import Informed_RRT_star
import time
import sys
import rospy
import moveit_commander

from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

import numpy as np

if __name__=="__main__":
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("move_group_python_interface_tutorial", anonymous=True)
    pub = rospy.Publisher('/command/JointPosition', String, queue_size=1)

    joint_goal = [0 for i in range(7)]
    #start = [0.5,0.5,-0.5,0.5,0.5,-0.5,0.5]
    #start = [0.1,-0.3,-0.9,0.6,-0.5,0.2,0.7]

    #start = [14,93,14,49,-10,74,11]
    start = [44,23,15,-44,-37,80,0]

    start = [i*np.pi/180 for i in start]

    joint_goal[0] = start[0]
    joint_goal[1] = start[1]
    joint_goal[2] = start[2]
    joint_goal[3] = start[3]
    joint_goal[4] = start[4]
    joint_goal[5] = start[5]
    joint_goal[6] = start[6]
    

    goalrad = 0.004
    #goal = np.array([-7,69,15,7,23,79,-3.00])*np.pi/180
    goal = np.array([26 ,27,22,-51,-23 ,62,-41])*np.pi/180

    #goal = [0.5,0.5,-0.5,0.5,0.5,-0.5,0.5]
    #goal = [0.1,-0.3,-0.9,0.6,-0.5,0.2,0.7]

    print(goal)
    RRT_Instance = RRT(start, goal, goalrad)
    #RRT_Instance = RRT_star(start, goal, goalrad)
    #RRT_Instance = Informed_RRT_star(start, goal, goalrad)
    Path = RRT_Instance.run_algo(500)
    print(tf_total(Path[-1][0],Path[-1][1],Path[-1][2],Path[-1][3],Path[-1][4],Path[-1][5],Path[-1][6]))
    

    for config in Path:
        joint_goal[0] = config[0]
        joint_goal[1] = config[1]
        joint_goal[2] = config[2]
        joint_goal[3] = config[3]
        joint_goal[4] = config[4]
        joint_goal[5] = config[5]
        joint_goal[6] = config[6]

        s = ""
        for i in joint_goal:
            s += str(i * 180 / np.pi)
            s += " " 
        pub.publish(s)
        print(s)
        time.sleep(0.1)