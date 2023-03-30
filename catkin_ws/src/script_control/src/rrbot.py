   1 #!/usr/bin/env python3

   3 import rospy
   4 from std_msgs.msg import Float64
   5 
   6 def talker():
   7     pub = rospy.Publisher('/rrbot/joint1_position_controller/command', Float64, queue_size=10)
   8     rospy.init_node('rrbot_talker', anonymous=True)
   9     rate = rospy.Rate(10) # 10hz
  10     while not rospy.is_shutdown():
  11         position = 0.0
  12         rospy.loginfo(position)
  13         pub.publish(position)
  14         rate.sleep()
  15 
  16 if __name__ == '__main__':
  17     try:
  18         talker()
  19     except rospy.ROSInterruptException:
  20         pass
