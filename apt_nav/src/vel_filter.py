#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class velFilter:
	def __init__(self):
		rospy.init_node('vel_filter')
		print "Node 'vel_filter' has initialized."

		rospy.Subscriber('/cmd_vel', Twist, self.vel_filters)

		self.pub_filtered_vel = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=1)

		self.filtered_vel = Twist()
		self.filtered_vel.linear.x = 0
		self.filtered_vel.linear.y = 0
		self.filtered_vel.linear.z = 0
		self.filtered_vel.angular.x = 0
		self.filtered_vel.angular.y = 0
		self.filtered_vel.angular.z = 0

	def vel_filters(self, msg):
		self.filtered_vel.linear.x = msg.linear.x
		self.filtered_vel.angular.z = msg.angular.z
		self.pub_filtered_vel.publish(self.filtered_vel)

if __name__ == '__main__':
	velFilter()
	rospy.spin()