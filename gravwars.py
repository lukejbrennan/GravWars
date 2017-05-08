import random
import Planet
import sys
import pygame

class GameSpace(object):
	def __init__(self):
		MIN_PLANETS = 1
		MAX_PLANETS = 7
		pygame.init()
		self.size = self.width, self.height = 640, 420
		self.screen = pygame.display.set_mode(self.size)
		num_planets = random.randint(MIN_PLANETS, MAX_PLANETS)
		self.planets = []
		for planet in range(num_planets):
			self.planets.append(Planet.Planet(self))
		self.missle = None
		#self.ship1 = 
		#self.ship2 = 
		self.black = 0, 0, 0
	
	def main(self):
		self.clock = pygame.time.Clock()
		while 1:
			self.clock.tick(60) # 60x per second
			#Handle events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			self.screen.fill(self.black)
			
			#Do tick for all planet objects
			for planet in self.planets:	
				planet.tick()

			# Step 7 #
			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()

