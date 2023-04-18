#!/usr/bin/env python3
import roslib
import rospy
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('tf_listener')

    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():

        try:
            Pose, Orientation = (listener.lookupTransform("iiwa_link_0", "iiwa_link_7", rospy.Time(0)))
            rospy.loginfo("Pose")
            rospy.loginfo(Pose)
            rospy.loginfo("Orientation")
            rospy.loginfo(Orientation)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()