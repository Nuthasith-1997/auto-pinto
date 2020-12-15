#!/usr/bin/env python

import rospy
import tf2_ros

from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry

class odomFilters:
	def __init__(self):
		rospy.init_node('odom_filters')
		print "Node 'odom_filters' has initialized."

		rospy.Subscriber('/mavros/local_position/odom', Odometry, self.filter_z)

		self.counter = 0

		self.pub_odom = rospy.Publisher('/odom', Odometry, queue_size=1)
		self.odom_topic = Odometry()

		self.odom_topic.header.seq = self.counter
		self.odom_topic.header.stamp = rospy.Time.now()
		self.odom_topic.header.frame_id = 'odom'
		self.odom_topic.child_frame_id = 'base_footprint'
		self.odom_topic.pose.pose.position.x = 0
		self.odom_topic.pose.pose.position.y = 0
		self.odom_topic.pose.pose.position.z = 0
		self.odom_topic.pose.pose.orientation.x = 0
		self.odom_topic.pose.pose.orientation.y = 0
		self.odom_topic.pose.pose.orientation.z = 0
		self.odom_topic.pose.pose.orientation.w = 1
		self.odom_topic.twist.twist.linear.x = 0
		self.odom_topic.twist.twist.linear.y = 0
		self.odom_topic.twist.twist.linear.z = 0
		self.odom_topic.twist.twist.angular.x = 0
		self.odom_topic.twist.twist.angular.y = 0
		self.odom_topic.twist.twist.angular.z = 0

		
		self.tf_bc = tf2_ros.TransformBroadcaster()
		self.tf = TransformStamped()

		self.tf.header.seq = self.counter
		self.tf.header.stamp = rospy.Time.now()
		self.tf.header.frame_id = 'odom'
		self.tf.child_frame_id = 'base_footprint'
		self.tf.transform.translation.x = 0
		self.tf.transform.translation.y = 0
		self.tf.transform.translation.z = 0
		self.tf.transform.rotation.x = 0
		self.tf.transform.rotation.y = 0
		self.tf.transform.rotation.z = 0
		self.tf.transform.rotation.w = 1

	def filter_z(self, msg):
		self.odom_topic.header.seq = self.counter
		self.odom_topic.header.stamp = rospy.Time.now()
		self.odom_topic.pose.pose.position.x = msg.pose.pose.position.x
		self.odom_topic.pose.pose.position.y = msg.pose.pose.position.y
		self.odom_topic.pose.pose.position.z = 0
		self.odom_topic.pose.pose.orientation = msg.pose.pose.orientation
		#self.odom_topic.pose.pose.orientation.x = msg.pose.pose.orientation.x
		#self.odom_topic.pose.pose.orientation.y = msg.pose.pose.orientation.y
		#self.odom_topic.pose.pose.orientation.z = msg.pose.pose.orientation.z
		#self.odom_topic.pose.pose.orientation.w = msg.pose.pose.orientation.w
		self.odom_topic.twist.twist.linear.x = msg.twist.twist.linear.x
		self.odom_topic.twist.twist.linear.y = msg.twist.twist.linear.y
		self.odom_topic.twist.twist.linear.z = 0
		self.odom_topic.twist.twist.angular = msg.twist.twist.angular
		#self.odom_topic.twist.twist.angular.x = 0
		#self.odom_topic.twist.twist.angular.y = 0
		#self.odom_topic.twist.twist.angular.z = msg.twist.twist.angular.z
		self.odom_topic.pose.covariance = msg.pose.covariance
		self.odom_topic.twist.covariance = msg.twist.covariance

		self.tf.header.stamp = rospy.Time.now()
		self.tf.header.seq = self.counter
		self.tf.transform.translation.x = msg.pose.pose.position.x
		self.tf.transform.translation.y = msg.pose.pose.position.y
		self.tf.transform.translation.z = 0
		self.tf.transform.rotation.x = msg.pose.pose.orientation.x
		self.tf.transform.rotation.y = msg.pose.pose.orientation.y
		self.tf.transform.rotation.z = msg.pose.pose.orientation.z
		self.tf.transform.rotation.w = msg.pose.pose.orientation.w

		self.pub_odom.publish(self.odom_topic)
		self.tf_bc.sendTransform(self.tf)
		self.counter += 1

if __name__ == '__main__':
	odomFilters()
	rospy.spin()