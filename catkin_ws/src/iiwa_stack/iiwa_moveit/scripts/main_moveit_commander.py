#!/usr/bin/env python3
from six.moves import input

from FK import tf_total
from RRT_7D import RRT

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

if __name__=="__main__":
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("move_group_python_interface_tutorial", anonymous=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()

    group_name = "manipulator"
    move_group = moveit_commander.MoveGroupCommander(group_name,ns='/iiwa')

    display_trajectory_publisher = rospy.Publisher(
    "/move_group/display_planned_path",
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20,)

    joint_goal = move_group.get_current_joint_values()

    start = [0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    joint_goal[0] = start[0]
    joint_goal[1] = start[1]
    joint_goal[2] = start[2]
    joint_goal[3] = start[3]
    joint_goal[4] = start[4]
    joint_goal[5] = start[5]
    joint_goal[6] = start[6]

    move_group.go(joint_goal, wait=True)
    move_group.stop()

    goalrad = 0.5
    goal,_ = tf_total(0.9,0.9,0.9,0.9,0.9,0.9,0.9)
    #goal = [0.1,0.1,0.1]
    print(goal)
    RRT_Instance = RRT(start, goal, goalrad)
    Path = RRT_Instance.run_algo(3000)
    print(tf_total(Path[-1][0],Path[-1][1],Path[-1][2],Path[-1][3],Path[-1][4],Path[-1][5],Path[-1][6]))

    for config in Path:
        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = config[0]
        joint_goal[1] = config[1]
        joint_goal[2] = config[2]
        joint_goal[3] = config[3]
        joint_goal[4] = config[4]
        joint_goal[5] = config[5]
        joint_goal[6] = config[6]

        move_group.go(joint_goal, wait=True)

    move_group.stop()    