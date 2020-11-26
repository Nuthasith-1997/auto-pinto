#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

class rf2vision:
    def __init__(self):
        rospy.init_node('rf_2_vision')
        print "Node 'rf_2_vision' has initialized."

        self.counter = 0

        rospy.Subscriber('/odom_rf2o', Odometry, self.rf2o_cb)
        #self.pub_vision = rospy.Publisher('/rf2o_vision', PoseStamped, queue_size=1)
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

    def rf2o_cb(self, msg):
        ## Create a vision_pose msg ##
        self.vision.header.seq = self.counter
        self.vision.header.stamp = rospy.Time.now()
        self.vision.header.frame_id = 'odom'

        self.vision.pose.position.x = msg.pose.pose.position.x
        self.vision.pose.position.y = msg.pose.pose.position.y
        self.vision.pose.position.z = msg.pose.pose.position.z
        self.vision.pose.orientation.x = msg.pose.pose.orientation.x
        self.vision.pose.orientation.y = msg.pose.pose.orientation.y
        self.vision.pose.orientation.z = msg.pose.pose.orientation.z
        self.vision.pose.orientation.w = msg.pose.pose.orientation.w

    def pub(self):
        self.pub_vision.publish(self.vision)
        self.counter += 1

if __name__ == '__main__':
    rf = rf2vision()
    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        rf.pub()
        rate.sleep()