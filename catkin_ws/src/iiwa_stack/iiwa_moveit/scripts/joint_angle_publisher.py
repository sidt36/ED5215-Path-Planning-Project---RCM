import rospy 
from sensor_msgs.msg import String
import numpy as np 

goal = '0 0 0 0 0 0 0'
message = String()
message.data = goal

rospy.init_node('goal_angle_publisher',anonymous=True)
pub = rospy.Publisher('/command/JointPosition', String, queue_size=1)

pub.publish(message)



