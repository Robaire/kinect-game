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

from random import uniform
from math import sin, cos

class Game():
	def __init__(self, width, height, title):

		# Window Height and Width
		self.width = width
		self.height = height

		pygame.init()   # Initialize Pygame
		pygame.font.init()
		self._screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE|pygame.FULLSCREEN) # Create display and set dimensions
		pygame.display.set_caption(title)  # Set the title of the window

        # Kinect runtime object
		self.kinect_runtime = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

		# Hand Object
		self.hand = Hand(self.kinect_runtime)
		self.hand.set_height(200)

		# Building Object
		self.building = Building()
		self.building.set_height(200)

		# Life Counter
		self.lives = Lives(3, "comicsansms")

		# Score Counter
		self.score = Score("comicsansms")

		# Test Projective
		self.projectile = Projectile("comicsansms", "AK is outdated!", "foisie", 100)

	def game_loop(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					sys.exit()
					
				# Other events as needed
			self.update()

	def update(self):

		## Make the background white
		self._screen.fill((255, 255, 0)) # Sets the background color

		## Draw the Building
		self._screen.blit(self.building.get_image(), (int(self.width / 2 - self.building.width / 2), int(self.height - self.building.height)))

		## Draw the Lives Display
		self._screen.blit(self.lives.get_image(), (0, 0))

		## Draw the Score Display
		self._screen.blit(self.score.get_image(), (int(self.width - self.score.width), 0))

		## Draw the Hand
		hand_state = self.hand.get_state() # Gets the state of the hand

		if hand_state is not None:  # If no one is in the view of the kinect hand_state is None
			x_pos, y_pos, hand = hand_state

			if x_pos is not float("inf") and y_pos is not float("inf"):  # If you are too close to the kinect the positions go to infinity

				x_pos *= self._screen.get_width()
				y_pos *= self._screen.get_height()

				if hand is "closed":	
			
					self._screen.blit(
						self.hand.get_image(), 
						(int(x_pos - self.hand.width / 2), int(y_pos - self.hand.height / 2))
					)

				else: 
					pygame.draw.circle(self._screen, (0, 0, 0), (int(x_pos), int(y_pos)), 10, 0)

		## Draw the Projectiles
		self._screen.blit(self.projectile.get_image(), (int(self.width / 2 + self.projectile.x_pos), int(self.height / 2 + self.projectile.y_pos)))

		## Update the Display
		pygame.display.flip()

class Hand():

	def __init__(self, kinect):

		self._kinect = kinect  # Kinect Runtime Object
		self._bodies = None  # Stores skeleton position data

		self.image = pygame.image.load("../images/laurie.png").convert_alpha()  # Load the image of Laurie's face
		self.height = self.image.get_height()
		self.width = self.image.get_width()

	def set_height(self, height):
		self.height = height
		self.width = int(self.image.get_width() / self.image.get_height() * height)

	def get_image(self):
		return pygame.transform.scale(self.image, (self.height, self.width))
	
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
		self.name = "foisie"

		self.image = pygame.image.load("../images/foisie.jpg").convert()
		self.height = self.image.get_height()
		self.width = self.image.get_width()

	def set_height(self, height):
		self.height = height
		self.width = int(self.image.get_width() / self.image.get_height() * height)

	def get_image(self):
		return pygame.transform.scale(self.image, (self.width, self.height))

class Lives():
	def __init__(self, lives, font):

		pygame.font.init()
		font_path = pygame.font.match_font(font, False, False)
		self.font = pygame.font.Font(font_path, 100)

		self.lives = lives

		self.width = 0
		self.height = 0

	def get_image(self):

		display = " Lives: " + str(self.lives)

		self.width, self.height = self.font.size(display)
		return self.font.render(display, True, (0, 0, 0), None)

class Score():
	def __init__(self, font):

		pygame.font.init()
		font_path = pygame.font.match_font(font, False, False)
		self.font = pygame.font.Font(font_path, 100)

		self.score = 0

		self.width = 0
		self.height = 0

	def get_image(self):

		display = "Score: " + str(self.score) + " "

		self.width, self.height = self.font.size(display)
		return self.font.render(display, True, (0,0,0), None)

class Projectile():
	def __init__(self, font, text, group, velocity):

		theta = uniform(0, 6.28)
		radius = 1000

		self.x_pos = radius * cos(theta)
		self.y_pos = -1 * abs(radius * sin(theta))

		pygame.font.init()
		font_path = pygame.font.match_font(font, False, False)
		self.font = pygame.font.Font(font_path, 50)

		self.text = text
		self.group = group
		self.velocity = velocity

	def get_image(self):
		
		self.width, self.height = self.font.size(self.text)
		return self.font.render(self.text, True, (0,0,0), None)

__main__ = "Kinect Tracking"

game = Game(1920, 1080, "Dumb Kinect Game")
game.game_loop()
