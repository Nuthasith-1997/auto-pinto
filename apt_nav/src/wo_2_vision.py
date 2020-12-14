#!/usr/bin/env python

import rospy

from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class wheelOdom2Vision:
	def __init__(self):
		rospy.init_node('wo_2_vision')
		print "Node 'wo_2_vision' has initialized."

		rospy.Subscriber('/mavros/wheel_odometry/odom', Odometry, self.wo_cb)

		self.counter = 0

		self.pub_vision = rospy.Publisher('/mavros/vision_pose/pose_cov', PoseWithCovarianceStamped, queue_size=1)
		self.vision = PoseWithCovarianceStamped()

		self.vision.header.seq = self.counter
		self.vision.header.stamp = rospy.Time.now()
		self.vision.header.frame_id = 'odom'
		self.vision.pose.pose.position.x = 0
		self.vision.pose.pose.position.y = 0
		self.vision.pose.pose.position.z = 0
		self.vision.pose.pose.orientation.x = 0
		self.vision.pose.pose.orientation.y = 0
		self.vision.pose.pose.orientation.z = 0
		self.vision.pose.pose.orientation.w = 1

		# Initial odom offset compensation.
		self.check = True

		self.px = 0
		self.py = 0

		self.roll = 0
		self.pitch = 0
		self.yaw = 0

	def wo_cb(self, msg):
		if self.check:
			self.px = msg.pose.pose.position.x
			self.py = msg.pose.pose.position.y

			orientation_q = msg.pose.pose.orientation
			orientation_list_q = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]

			(self.roll, self.pitch, self.yaw) = euler_from_quaternion(orientation_list_q)

			self.check = False

		self.vision.header.seq = self.counter
		self.vision.header.stamp = rospy.Time.now()

		self.vision.pose.pose.position.x = msg.pose.pose.position.x - self.px
		self.vision.pose.pose.position.y = msg.pose.pose.position.y - self.py
		self.vision.pose.pose.position.z = 0

		orientation_q_2 = msg.pose.pose.orientation
		orientation_list_q_2 = [orientation_q_2.x, orientation_q_2.y, orientation_q_2.z, orientation_q_2.w]
		euler = euler_from_quaternion(orientation_list_q_2)

		roll_pub = euler[0] - self.roll
		pitch_pub = euler[1] - self.pitch
		yaw_pub = euler[2] - self.yaw

		quat = quaternion_from_euler(roll_pub, pitch_pub, yaw_pub)
		self.vision.pose.pose.orientation.x = quat[0]
		self.vision.pose.pose.orientation.y = quat[1]
		self.vision.pose.pose.orientation.z = quat[2]
		self.vision.pose.pose.orientation.w = quat[3]
		#self.vision.pose.pose = msg.pose.pose

		self.vision.pose.covariance = msg.pose.covariance

		self.pub_vision.publish(self.vision)
		self.counter += 1

if __name__ == '__main__':
	wheelOdom2Vision()
	rospy.spin()