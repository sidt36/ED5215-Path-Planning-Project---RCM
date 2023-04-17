#!/usr/bin/env python3

from __future__ import print_function
from six.moves import input

from fk import tf_total
from  Informed_RRT_Star_No_Constraint_working import Informed_RRT_star

import time
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

import RRT_Star_No_Constraint_7Dgoal
import numpy as np

if __name__=="__main__":
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("move_group_python_interface_tutorial", anonymous=True)

    
    pub = rospy.Publisher('/command/JointPosition', String, queue_size=1)

    # We can get the name of the reference frame for this robot:
    # planning_frame = move_group.get_planning_frame()
    # print("============ Planning frame: %s" % planning_frame)

    # # We can also print the name of the end-effector link for this group:
    # eef_link = move_group.get_end_effector_link()
    # print("============ End effector link: %s" % eef_link)

    # # We can get a list of all the groups in the robot:
    # group_names = robot.get_group_names()
    # print("============ Available Planning Groups:", robot.get_group_names())

    # # Sometimes for debugging it is useful to print the entire state of the
    # # robot:
    # print("============ Printing robot state")
    # print(robot.get_current_state())
    # print("")

    joint_goal = [0 for i in range(7)]
 
    start = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    joint_goal[0] = start[0]
    joint_goal[1] = start[1]
    joint_goal[2] = start[2]
    joint_goal[3] = start[3]
    joint_goal[4] = start[4]
    joint_goal[5] = start[5]
    joint_goal[6] = start[6]

    goalrad = 0.05
    goal = np.array([0.1,0.1,0.1,0.1,0.1,0.1,0.1])
    #goal = [0.1,0.1,0.1]
    print(goal)
    RRT_Instance = Informed_RRT_star(start, goal, goalrad)
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
        time.sleep(0.2)
        




