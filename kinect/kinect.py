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

class Game():
	def __init__(self):
		pygame.init()   # Initialize Pygame

		# Set the width and height of the screen [width, height]
		self._infoObject = pygame.display.Info()
		self._screen = pygame.display.set_mode(
			(self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), pygame.RESIZABLE, 32)

		pygame.display.set_caption("Kinect Game")  # Set the title of the window

		# Used to manage how fast the screen updates
		self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
		self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
		# self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

		# Create a Kinect Data object to get position information
		self.kinect_data = KinectData(self._kinect)

	def game_loop(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				# Other events as needed
			self.update()

	def update(self):

		hand_data = self.kinect_data.get_hand_data()

		if hand_data is not None:
			x_pos, y_pos, hand = hand_data

			x_pos *= self._screen.get_width() 
			y_pos *= self._screen.get_height()

			if hand is "open":
				color = (0, 0, 255)
			else:
				color = (255, 0, 0)

			self._screen.fill((255, 255, 255))
			pygame.draw.circle(self._screen, color, (int(x_pos), int(y_pos)), 10, 0)
			pygame.display.flip()

class KinectData():

	def __init__(self, kinect):

		self._kinect = kinect  # Kinect Runtime Object
		self._bodies = None  # Stores skeleton position data

	def get_hand_data(self):
		""" Retrives the positional data of the players right hand """
		if self._kinect.has_new_body_frame():  # Check if there is a new body frame
			self._bodies = self._kinect.get_last_body_frame()

		if self._bodies is not None:  # If there is a body in the frame
			for i in range(0, self._kinect.max_body_count):
				body = self._bodies.bodies[i]
				if not body.is_tracked: 
					continue

				joint_points = self._kinect.body_joints_to_color_space(body.joints)

				x_position = joint_points[11].x / self._kinect.color_frame_desc.Width
				y_position = joint_points[11].y / self._kinect.color_frame_desc.Height

				hand_states = {
					0 : "unkown",
					1 : "not tracked",
					2 : "open",
					3 : "closed",
					4 : "lasso"
				}

				return [x_position, y_position, hand_states[body.hand_right_state]]

	
__main__ = "Kinect Tracking"

game = Game()
game.game_loop()
