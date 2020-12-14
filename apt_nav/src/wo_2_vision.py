#!/usr/bin/env python

import rospy

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class wheelOdom2Vision:
	def __init__(self):
		rospy.init_node('wo_2_vision')
		print "Node 'wo_2_vision' has initialized."

		rospy.Subscriber('/mavros/wheel_odometry/odom', Odometry, self.wo_cb)

		self.counter = 0

		self.pub_vision = rospy.Publisher('/mavros/vision_pose/pose', PoseStamped, queue_size=1)
		self.vision = PoseStamped()

		self.vision.header.seq = self.counter
		self.vision.header.stamp = rospy.Time.now()
		self.vision.header.frame_id = 'odom'
		self.vision.pose.position.x = 0
		self.vision.pose.position.y = 0
		self.vision.pose.position.z = 0
		self.vision.pose.orientation.x = 0
		self.vision.pose.orientation.y = 0
		self.vision.pose.orientation.z = 0
		self.vision.pose.orientation.w = 1

	def wo_cb(self, msg):
		self.vision.header.seq = self.counter
		self.vision.header.stamp = rospy.Time.now()

		#self.vision.pose.position.x = msg.pose.pose.position.x
		#self.vision.pose.position.y = msg.pose.pose.position.y
		#self.vision.pose.position.z = 0

		#self.vision.pose.orientation.x = msg.pose.pose.orientation.x
		#self.vision.pose.orientation.y = msg.pose.pose.orientation.y
		#self.vision.pose.orientation.z = msg.pose.pose.orientation.z
		#self.vision.pose.orientation.w = msg.pose.pose.orientation.w
		self.vision.pose = msg.pose.pose

		#self.vision.pose.covariance = msg.pose.covariance

		self.pub_vision.publish(self.vision)
		self.counter += 1

if __name__ == '__main__':
	wheelOdom2Vision()
	rospy.spin()
