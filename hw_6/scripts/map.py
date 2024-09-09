#!/usr/bin/env python3

import os
import rospy
import cv2
from cv_bridge import CvBridge

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range

import math
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians, pi
from collections import deque

from sources import lidar_to_grid_map as lg

class Map():

    def __init__(self):
        rospy.loginfo("[Map] loading")

        self.sonar_subscriber = rospy.Subscriber("/range/front", Range, callback=self.sonar_front_callback)
        self.sonar_subscriber = rospy.Subscriber("/range/right", Range, callback=self.sonar_right_callback)
        self.sonar_subscriber = rospy.Subscriber("/range/rear", Range, callback=self.sonar_rear_callback)
        self.sonar_subscriber = rospy.Subscriber("/range/left", Range, callback=self.sonar_left_callback)

        self.movement_subscriber = rospy.Subscriber("/cmd_vel", Twist, callback=self.movement_callback)

        self.movement_data = Twist()
        self.sonar_data = [0, 0, 0, 0]
        self.sonar_angles = np.array([0, pi/2, pi, 3*pi/2])
        self.ox = np.zeros(4)
        self.oy = np.zeros(4)

    def sonar_front_callback(self, msg):
        self.sonar_data[0] = msg.range
    def sonar_right_callback(self, msg):
        self.sonar_data[1] = msg.range
    def sonar_rear_callback(self, msg):
        self.sonar_data[2] = msg.range
    def sonar_left_callback(self, msg):
        self.sonar_data[3] = msg.range

    def movement_callback(self, msg):
        self.movement_data = msg

    def update_map(self):
        self.ox = np.sin(self.sonar_angles) * self.sonar_data
        self.oy = np.cos(self.sonar_angles) * self.sonar_data

    def spin(self):
        rate = rospy.Rate(30)

        # plt.figure(figsize=(5, 5))       
        while not rospy.is_shutdown():
            # plt.plot([self.oy, np.zeros(np.size(self.oy))], [self.ox, np.zeros(np.size(self.oy))], "ro-")
            # plt.grid(True)
            # plt.axis("equal")
            # plt.draw()
            # plt.pause(0.5)

            # rate.sleep()
        
    ### ### ### ### ###

        # xyreso = 0.02  # x-y grid resolution
        # yawreso = math.radians(3.1)  # yaw angle resolution [rad]

        # while not rospy.is_shutdown():
        #     pmap, minx, maxx, miny, maxy, xyreso = lg.generate_ray_casting_grid_map(self.ox, self.oy, xyreso, False)
        #     xyres = np.array(pmap).shape
        #     plt.figure(figsize=(20,8))
        #     plt.subplot(122)
        #     plt.imshow(pmap, cmap = "PiYG_r")
        #     plt.clim(-0.4, 1.4)
        #     plt.gca().set_xticks(np.arange(-.5, xyres[1], 1), minor = True)
        #     plt.gca().set_yticks(np.arange(-.5, xyres[0], 1), minor = True)
        #     plt.grid(True, which="minor", color="w", linewidth = .6, alpha = 0.5)
        #     plt.colorbar()
        #     plt.draw()
        #     plt.pause(0.00000000001

        #     rate.sleep()



def main(args=None):
    rospy.init_node("map_node")

    map = Map()
    # plt.ion()
    # plt.show()
    map.spin()



if __name__ == "__main__":
    main()