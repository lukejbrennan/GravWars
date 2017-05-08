import sys
import pygame
import random

class Planet(pygame.sprite.Sprite):
	def __init__(self, gs):
		MIN_RADIUS = gs.height * .05
		MAX_RADIUS = gs.height * .2 
		MIN_MASS = 100
		MAX_MASS = 1000
		self.gs = gs
		self.color = self.randColor()
		self.radius = random.randint(MIN_RADIUS, MAX_RADIUS)
		self.mass = random.randint(MIN_MASS, MAX_MASS)
		self.placePlanet()		

	def placePlanet(self):
		MIN_X = self.gs.width * .15
		MAX_X = self.gs.width * .85
		MIN_Y = self.gs.height * .15
		MAX_Y = self.gs.height * .85

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
			if num_placement_attempts > 100:
				raise RuntimeError('Unable to place planet after looking at 100 points on the screen')

	def tick(self):
		pygame.draw.circle(self.gs.screen, self.color, (self.x, self.y), self.radius)
		#Check for a missle collision with planet
		if self.gs.missle:
			if self.rect.colliderect(self.gs.missle.rect):
				self.gs.missle.rect = None
			

	def randColor(self):
		rgb = []
		for _ in range(3):
			rgb.append(random.randint(0, 255))
		return rgb
		
