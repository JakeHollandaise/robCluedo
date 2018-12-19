#!/usr/bin/env python

import rospy
import sys
import cv2
import os
import tf
import random
import math

from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from ar_track_alvar_msgs.msg import AlvarMarkers
from kobuki_msgs.msg import BumperEvent
from cv_bridge import CvBridge, CvBridgeError

from std_msgs.msg import String, Bool
from modules import robotStatus
from modules import Tracker
from modules import CluedoClassifier
from modules import follow_wall

class robCluedo:
    def __init__(self, pub, rate):
        self.image_sub = rospy.Subscriber('CluARFound', Bool, self.callback)
        self.image_feed = rospy.Subscriber('/camera/rgb/image_raw/', Image, self.setRawImage)
        self.bridge = CvBridge()

        self.rawImage = None
        self.murderer = None
        self.murderWeapon = None
        print("Up and Running")

    def callback(self, data):
        print(data.data)

    def ImageResult(self, data):
        print(data.data)

    def setRawImage(self, data):
        # print("Got Image!")
        self.rawImage = self.bridge.imgmsg_to_cv2(data, "bgr8")
        # print(data)

    def getRawImage(self):
        return self.rawImage

def publisher(name, type):
	pub = rospy.Publisher(name, type, queue_size=10)
	rate = rospy.Rate(10) #10hz

	return pub, rate

def main():
    rospy.init_node('cluedo_main', anonymous=True)
    pub, rate = publisher("CluedoMain", Bool)
    cI = robCluedo(pub, rate)
    running = True

    try:
        robotRunning = robotStatus.RobotStatus()
        # robotRunning.goToMiddle()
        while running:
            if robotRunning.tracker.postercounter == 2:
                print(' poster counter 2. Done!')
                for i in range(0,2):
                    gotToDest = robotRunning.tracker.position(i)
                    if goToDest:
                        print('000000')
                        data = robotRunning.cluedoClassifier.analyseImg(cI.getRawImage())
                        print(data)
                        print('finished image analysis')
                        ########## Jake #########
                        #### infront of the poster mate insert your code here
                        ########## Jake #########
                        ###write file
                        ##end program
                        running = False
            if robotRunning.tracker.postercounter == 1:
                print('before moving to position')
                goToDest = robotRunning.tracker.position(0)
                if goToDest:
                    # data = robotRunning.cluedoClassifier.analyseImg(cI.getRawImage())
                    # print(data)
                    print('scanning image exciting...')
                    # cluedoClassifier.main()
                    ##### Jake ######
                    #### check images if found
                print('go to entrance')
                robotRunning.goToEntrance()
                # while robotRunning.tracker.postercounter < 2:
                #     print('poster counter < 2')
                followWall = follow_wall.FollowWall()
                if (robotRunning.tracker.postercounter == 2):
                    goToDest = robotRunning.tracker.position(1)
                    if goToDest:
                    #### Vision analysis here
                        print('scanning image 2...')
                running = True
            else:
                robotRunning.goToEntrance()
                # while robotRunning.tracker.postercounter < 2:
                #     print('poster counter < 2')
                followWall = follow_wall.FollowWall()
                if robotRunning.tracker.postercounter == 1:
                    robotRunning.stopMovement()
                    goToDest = robotRunning.tracker.position(0)
                    if goToDest:
                        print('scanning image exciting...')
                elif robotRunning.tracker.postercounter == 2:
                    print('poster counter = 2')
                    robotRunning.stopMovement()
                    goToDest = robotRunning.tracker.position(1)
                    if goToDest:
                        print('scanning image exciting...')
                    ##### Jake ######
                    #### check images if found
                    ### running = False
                running = True
            rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()