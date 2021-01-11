#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class joyStick:
	def __init__(self):
		rospy.init_node('joy_2_vel')
		print "Node 'joy_2_vel' has initialized."

		rospy.Subscriber('/joy', Joy, self.joyCb)
		self.pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

		self.vel = Twist()
		self.vel.linear.x = 0.0
		self.vel.linear.y = 0.0
		self.vel.linear.z = 0.0

		self.vel.angular.x = 0.0
		self.vel.angular.y = 0.0
		self.vel.angular.z = 0.0

		self.check = False

	def joyCb(self, msg):
		if msg.buttons[4] == 1:
			self.check = True

		else: self.check = False

		self.vel.linear.x = msg.axes[1] * 0.40
		self.vel.angular.z = msg.axes[2] * 0.50

	def pubVelocities(self):
		if not self.check:
			self.vel.linear.x = 0.0
			self.vel.linear.y = 0.0
			self.vel.linear.z = 0.0

			self.vel.angular.x = 0.0
			self.vel.angular.y = 0.0
			self.vel.angular.z = 0.0

		self.pub_vel.publish(self.vel)

if __name__ == '__main__':
	js = joyStick()
	rate = rospy.Rate(30)

	while not rospy.is_shutdown():
		js.pubVelocities()
		rate.sleep()
