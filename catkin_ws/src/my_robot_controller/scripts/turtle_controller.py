#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

def pose_callback(msg: Pose):
    
    cmd = Twist()
    cmd.linear.x = 5
    cmd.angular.z = 0
    pub.publish(cmd)

if __name__=='__main__':
    rospy.init_node("Turtle_Controller")
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)
    sub = rospy.Subscriber("/turtle1/pose",Pose, callback = pose_callback)
    rospy.loginfo("Node has been started")
    rospy.spin()

