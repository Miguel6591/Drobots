#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots
import math
import random

class RobotControllerDetectorI(drobots.ControllerDetector):
	def __init__(self):
		self.enemies = -1
		self.pos = None

        
	def alert(self, pos, enemies, current = None):
        print("Alert: {} robots detected at {},{}".format(enemies, pos.x, pos.y)) 
        self.enemies = enemies
        self.pos = pos  

    def getEnemigo(self, current = None):
        if(self.enemies > 0):
            return self.pos
        
    def robotDestroyed(self, current = None):
		print("Robot Destruido")