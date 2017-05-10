import random
import Planet
import Missile
import Spaceship
import sys
import pygame
import math
import TextBox

class GameSpace(object):
	def __init__(self):
		MIN_PLANETS = 0
		MAX_PLANETS = 0
		pygame.init()
		self.angle = 0
		self.velocity = 100
		self.size = self.width, self.height = 840, 620
		self.screen = pygame.display.set_mode(self.size)
		num_planets = random.randint(MIN_PLANETS, MAX_PLANETS)
		self.planets = []
		for planet in range(num_planets):
			self.planets.append(Planet.Planet(self))
		self.missile = None
		active = 1
		notActive = 0
		#### (self, rot, xpos, ypos, activeMover, activeCollider
		self.textbox = TextBox.TextBox(self)
		self.player_ship = Spaceship.Spaceship(self, 90, .0, .5, active, notActive)
		self.opponent_ship = Spaceship.Spaceship(self, 90, .88, .5, notActive, active)
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
                		    (mouseX, mouseY) = pygame.mouse.get_pos()
                                    ship_x = self.player_ship.rect.centerx
                                    ship_y = self.opponent_ship.rect.centery
	    		            angle = math.atan2(mouseY-ship_y, mouseX - ship_x)
                                    self.missile = Missile.Missle(self, angle, self.player_ship.rect)

			self.screen.fill(self.black)
			
			#Do ticks for all sprite objects
			for planet in self.planets:	
				planet.tick()
				if self.missile:
					self.missile.tick()
				self.player_ship.tick()
				self.opponent_ship.tick()
				self.textbox.tick()

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()

