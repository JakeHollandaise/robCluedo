#!/usr/bin/env python
from __future__ import division
import cv2
import numpy as np
import rospy
import sys
import tensorflow as tf

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

class CleudoCharacter:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn
        self.convScore = 0
        self.templateScore = 0

    def getScore(self):
        return self.templateScore

    def setScore(self, score):
        self.templateScore = score

class CluedoClassifier():

    def __init__(self):
        # Initialise a publisher to publish messages to the robot base
        # We covered which topic receives messages that move the robot in the 2nd Lab Session
        self.clu_list = createCharacterList()

        #Vars for image detection - courtesy of Andy Bullpit (School of Computing)
        self.input_height = 224
        self.input_width = 224
        self.input_mean = 0
        self.input_std = 255
        self.input_layer = "Placeholder"
        self.output_layer = "final_result"

    def analyseImg(self, img):
        cv_image = img
        clu_list = self.clu_list
        bestCharacter = CleudoCharacter(None, None)
        
        conv = np.float32(cv_image)
        img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        img2 = img.copy()
        for clu in clu_list:
            template = cv2.imread(clu.fn,0)
            template = cv2.resize(template, None, fx = 0.3, fy = 0.3, interpolation = cv2.INTER_CUBIC)
            w, h = template.shape[::-1]

            meth = 'cv2.TM_CCOEFF_NORMED'

            img = img2.copy()
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            clu.setScore(max_val)
            if clu.getScore() > bestCharacter.getScore() and clu.getScore() > 0.5:
                bestCharacter = clu

        return bestCharacter
        
        # print (bestCharacter.name, bestCharacter.getScore())
        # cv2.waitKey(3)

def createCharacterList():
    clu_list = []
    clu_list.append(CleudoCharacter("Mustard", "templates/mustard.png"))
    clu_list.append(CleudoCharacter("Peacock", "templates/peacock.png"))
    clu_list.append(CleudoCharacter("Scarlet", "templates/scarlet.png"))
    clu_list.append(CleudoCharacter("Plum", "templates/plum.png"))
    clu_list.append(CleudoCharacter("Wrench", "templates/wrench.png"))
    clu_list.append(CleudoCharacter("Rope", "templates/rope.png"))
    clu_list.append(CleudoCharacter("Revolver", "templates/scarlet.png"))

    return clu_list

