#!/usr/bin/python
import rospy
from std_msgs.msg import Float64
import math

def talker():
    pub1= rospy.Publisher('/rrbot/joint1_position_controller/command',
                          Float64, queue_size=10)
    pub2 = rospy.Publisher('/rrbot/joint2_position_controller/command',
                          Float64, queue_size=10)
    rospy.init_node('rrbot_talker', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    i = 1
    while not rospy.is_shutdown():
        position1 = math.sin(i)
        position2 = math.cos(i)
        rospy.loginfo(position1)
        pub1.publish(position1)
        rospy.loginfo(position2)
        pub2.publish(position2)
        rate.sleep()
        i+= 0.1
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
