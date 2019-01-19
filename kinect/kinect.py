from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys

if sys.hexversion >= 0x03000000:
	import _thread as thread
else:
	import thread

class runtime(object):
	def __init__(self):
		# Kinect runtime object, we want only color and body frames 
		self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)

		# here we will store skeleton data 
		self._bodies = None

	def run(self):
		while(True):
			# -------- Main Program Loop -----------

			# --- Cool! We have a body frame, so can get skeletons
			if self._kinect.has_new_body_frame(): 
				self._bodies = self._kinect.get_last_body_frame()

			# --- draw skeletons to _frame_surface
			if self._bodies is not None: 
				for i in range(0, self._kinect.max_body_count):
					body = self._bodies.bodies[i]
					if not body.is_tracked: 
						continue 

					joints = body.joints 
					joint_points = self._kinect.body_joints_to_color_space(joints)

					print("x = ", joint_points[11].x) #get x
					print("y = ", joint_points[11].y) #get y
					
					RightHandState = body.HandRightState() #get hand state
					print(RightHandState);
	
__main__ = "Kinect Trackinig"
game = runtime();
game.run();
