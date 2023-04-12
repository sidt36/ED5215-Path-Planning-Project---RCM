#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
if __name__ == '__main__':
    rospy.init_node("Ddraw_circle")
    rospy.loginfo("Node has been Started")

    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)

    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        msg = Twist()
        msg.linear.x = 2.0
        msg.linear.y = 0
        msg.linear.z = 0
        msg.angular.x = 0 
        msg.angular.y = 0
        msg.angular.z = 1.0

        pub.publish(msg)
        rate.sleep()





