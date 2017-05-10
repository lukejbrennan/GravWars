import random
import Planet
import Missile
import Spaceship
import sys
import pygame

class GameSpace(object):
	def __init__(self):
		MIN_PLANETS = 1
		MAX_PLANETS = 7
		pygame.init()
		self.size = self.width, self.height = 840, 620
		self.screen = pygame.display.set_mode(self.size)
		num_planets = random.randint(MIN_PLANETS, MAX_PLANETS)
		self.planets = []
		for planet in range(num_planets):
			self.planets.append(Planet.Planet(self))
		self.missile = None
		self.player_ship = Spaceship.Spaceship(self, 90, .0, .5)
		self.opponent_ship = Spaceship.Spaceship(self, 90, .88, .5)
		self.black = 0, 0, 0
	
	def main(self):
		self.clock = pygame.time.Clock()
		while 1:
			self.clock.tick(60) # 60x per second
			#Handle events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
                                if event.type == pygame.MOUSEBUTTONUP:
                                    self.missile = Missile.Missle(self, 0, self.ship1.rect)

			self.screen.fill(self.black)
			
			#Do ticks for all sprite objects
			for planet in self.planets:	
			    planet.tick()

                        if self.missile:
                            self.missile.tick()
                        else:
                            self.player_ship.tick()
                            self.opponent_ship.tick()

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()

