#!/usr/bin/env python

import rospy

from geometry_msgs.msg import TwistWithCovariance, PoseStamped
from nav_msgs.msg import Odometry

class wheelOdom2Vision:
	def __init__(self):
		rospy.Subscriber('/mavros', Odometry, self.wo_cb)
		#rospy.Subscriber('/mavros', TwistWithCovariance, self.wo_cb)

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

	def pub(self):
		self.pub_vision.publish(self.vision)
		self.counter += 1

if __name__ == '__main__':
	rospy.init_node('wo_2_vision')
	print "Node 'wo_2_vision' has initialized."
