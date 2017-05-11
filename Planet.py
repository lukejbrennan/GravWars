import sys
import pygame
import random
import pickle

class Planet(pygame.sprite.Sprite):
	def __init__(self, gs, place, color=None, radius=None, mass=None, x=None, y=None):
		MIN_RADIUS = int(gs.height * .05)
		MAX_RADIUS = int(gs.height * .12)
		MIN_MASS = 100
		MAX_MASS = 1000
		self.gs = gs
                if color:
                    self.color = color
                else:
		    self.color = self.randColor()
                if radius:
                    self.radius = radius
                else:
                    self.radius = random.randint(MIN_RADIUS, MAX_RADIUS)
                if mass:
                    self.mass = mass
                else:
		    self.mass = random.randint(MIN_MASS, MAX_MASS)
                if place:
		    self.placePlanetRandom()
                elif not x or not y:
                    print('Error: Place must be true or coordinates provided')
                else:
                    self.placePlanetGiven()

        def placePlanetGiven(self):
	    self.rect = pygame.draw.circle(self.gs.screen, self.color, (self.x, self.y), self.radius)

	def placePlanetRandom(self):
		MIN_X = int(self.gs.width * .23)
		MAX_X = int(self.gs.width * .78)
		MIN_Y = int(self.gs.height * .18)
		MAX_Y = int(self.gs.height * .82)

		num_placement_attempts = 0
		successful_placement = False
		while not successful_placement:
			#Find a random spot to put the planet
			self.x = random.randint(MIN_X, MAX_X)
			self.y = random.randint(MIN_Y, MAX_Y)
			self.rect = pygame.draw.circle(self.gs.screen, self.color, (self.x, self.y), self.radius)
			successful_placement = True

			#Make sure that planet doesn't intersect with other
			for planet in self.gs.planets:
				if self.rect.colliderect(planet.rect):
					successful_placement = False

			#Do some sanity checking to make sure we are sucessfully placing planets after a reasonable number of attempts
			num_placement_attempts += 1
			if num_placement_attempts > 200:
				raise RuntimeError('Unable to place planet after looking at 200 points on the screen')

	def tick(self):
		pygame.draw.circle(self.gs.screen, self.color, (self.x, self.y), self.radius)
		#Check for a missle collision with planet
		if self.gs.missile:
			if self.rect.colliderect(self.gs.missile.image.get_rect()):
				self.gs.missile.rect = None
                                if self.gs.is_your_turn:
                                    self.conn_ref.transport.write('planet_collision')		

	def randColor(self):
		rgb = []
		for _ in range(3):
			rgb.append(random.randint(0, 255))
		return rgb
		
