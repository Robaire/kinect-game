from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from random import randint
from math import sin, cos

class KinectApp(App):
    def build(self):
        game = KinectGame()  # Initialize Game Instance
        game.spawn_hand()  # Spawns the hand
        game.spawn_target()  # Spawns the target
        Clock.schedule_interval(game.update, 1.0/60.0)  # Game Clock

        return game

class KinectGame(Widget):

    target = ObjectProperty(None)
    hand = ObjectProperty(None)

    foise_score = NumericProperty(0)
    ak_score = NumericProperty(0)

    def update(self, dt):
        """ Main Game Logic """
        # Move the target one time step
        self.target.move()

        # Check if the hand as collided with the target
        self.hand.hit_target(self.target)

        # Check if the target has hit any of the walls
        if(self.target.y < 0) or (self.target.top > self.height):
            self.target.velocity_y *= -1

        if(self.target.x < 0) or (self.target.right > self.width):
            self.target.velocity_x *= -1

    def spawn_target(self):
        """ Spawns a Target and gives it a velocity """

        theta = randint(0,360)  # Angular Offset
        radius = self.width # Sets the radius of the spawn circle

        self.target.position_x = (radius * cos(theta))  # Set X Coordinate
        self.target.position_y = (radius * sin(theta))  # Set Y Coordinate

        #self.target.center_x = 50 + (radius * cos(theta))  # Set X Coordinate
        #self.target.center_y = 50 + (radius * sin(theta))  # Set Y Coordinate

        self.target.velocity_x = 0
        self.target.velocity_y = 0

    def spawn_hand(self):
        """ Spawns the Hand """
        self.hand.center = self.center

    def on_touch_move(self, touch):
        """ Sets the position of the hand on touch events """
        self.hand.pos = touch.pos

class Target(Widget):
    """ Target the player must hit """

    position_x = NumericProperty(0)
    position_y = NumericProperty(0)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    def move(self):
        """ Adjusts its position according to the velocity """
        self.pos = Vector(self.velocity_x, self.velocity_y) + self.pos

class Hand(Widget):
    score = NumericProperty(0)

    def hit_target(self, target):
        if self.collide_widget(target):
            self.score += 1


if __name__ == '__main__':
    KinectApp().run()