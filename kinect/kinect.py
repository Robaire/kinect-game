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
		self._screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE) # Create display and set dimensions
		pygame.display.set_caption("Kinect Game")  # Set the title of the window

        # Kinect runtime object
		self.kinect_runtime = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

		# Hand Object
		self.hand = Hand(self.kinect_runtime)

		# Building
		self.building = Building()

	def game_loop(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				# Other events as needed
			self.update()

	def update(self):

		self._screen.fill((255, 255, 255)) # Sets the background color
		self._screen.blit(self.building.get_image(200), (1080, 1920 / 2))

		hand_state = self.hand.get_state() # Gets the state of the hand

		if hand_state is not None:  # If no one is the in the view of the kinect hand_state is None
			x_pos, y_pos, hand = hand_state

			if x_pos is not float("inf") and y_pos is not float("inf"):  # If you are too close to the kinect the positions go to infinity

				x_pos *= self._screen.get_width() 
				y_pos *= self._screen.get_height()

				if hand is "closed":	
			
					size = 200
					self._screen.blit(
						self.hand.get_image(size), 
						(int(x_pos - size / 2), int(y_pos - size / 2))
					)

				else: 
					pygame.draw.circle(self._screen, (0, 0, 0), (int(x_pos), int(y_pos)), 10, 0)

		pygame.display.flip()

class Hand():

	def __init__(self, kinect):

		self._kinect = kinect  # Kinect Runtime Object
		self._bodies = None  # Stores skeleton position data

		self.image = pygame.image.load("../images/laurie.png").convert_alpha  # Load the image of Laurie's face
	
	def get_image(self, size):
		return pygame.transform.scale(self.image, (size, size))

	def get_state(self):
		""" Retrives the positional data of the players hand """
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

class Building():

	def __init__(self):
		self.image = pygame.image.load("../images/foise.jpg").convert()
		self.name = "foise"
		self.lives = 3
		self.score = 0

	def get_image(self, height):
		return pygame.transform.scale(self.image, (height, self.image.get_width() / self.image.get_height() * height) )

__main__ = "Kinect Tracking"

game = Game()
game.game_loop()
