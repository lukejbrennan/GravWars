import random
import Planet
import Missile
import Spaceship
import sys
import pygame
import math
import conn
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor


class GameSpace(object):
	def __init__(self):
            MIN_PLANETS = 2
            MAX_PLANETS = 6
            pygame.init()
            self.angle = 0
            self.velocity = 100
            self.size = self.width, self.height = 840, 620
            self.screen = pygame.display.set_mode(self.size)
            self.num_planets = random.randint(MIN_PLANETS, MAX_PLANETS)
            self.planets = []
            self.missile = None
            self.p1 = Spaceship.Spaceship(self, 90, .0, .5, True, True)
            self.p2 = Spaceship.Spaceship(self, 90, .88, .5, True, True)
            self.black = 0,0,0
            self.is_your_turn = None
            self.conn_ref = None
        
        def getConnRef(self, conn_ref):
            self.conn_ref = conn_ref
        
        def sendPlanet(self, planet):
            data = 'new_planet\n'
            data = data + str(planet.color[0]) + '_'
            data = data + str(planet.color[1]) + '_'
            data = data + str(planet.color[2]) + '\n'
            data = data + str(planet.radius) + '\n'
            data = data + str(planet.mass) + '\n'
            data = data + str(planet.x) + '\n'
            data = data + str(planet.y)
            self.conn_ref.transport.write(data)

	def main(self, player):
		self.clock = pygame.time.Clock()
                if player == 'p1':
                    self.is_your_turn = True
        	    for planet in range(self.num_planets):
			self.planets.append(Planet.Planet(self, True))
                        self.sendPlanet(self.planets[planet])

                elif player == 'p2':
                    self.is_your_turn = False
                else:
                    print('Error: unknown player name')

		while 1:
			self.clock.tick(60) # 60x per second
			#Handle events
			for event in pygame.event.get():
			        if event.type == pygame.QUIT:
				    sys.exit(0)
                                if event.type == pygame.MOUSEBUTTONUP:
                                    if not self.is_your_turn:
                                        (mouseX, mouseY) = pygame.mouse.get_pos()
                                        ship_x = None
                                        ship_y = None
                                        if player == 'p1':
                                            ship_x = self.p1.rect.centerx
                                            ship_y = self.p1.rect.centery
                                            angle = math.atan2(mouseY-ship_y, mouseX - ship_x)
                                            self.missile = Missile.Missle(self, angle, self.p1.rect)
                                        elif player == 'p2':
                                            ship_x = self.p2.rect.centerx
                                            ship_y = self.p2.rect.centery
                                            angle = math.atan2(mouseY-ship_y, mouseX - ship_x)
                                            self.missile = Missile.Missle(self, angle, self.p2.rect)
			self.screen.fill(self.black)
		
                        #Do all checks on whose turn it is
                        if self.is_your_turn:
                            if player == 'p1':
                                self.p1.activeM = True
                                self.p1.activeC = False
                                self.p2.activeM = False
                                self.p2.activeC = True
                            elif player == 'p2':
                                self.p2.activeM = True
                                self.p2.activeC = False
                                self.p1.activeM = False
                                self.p1.activeC = True

			#Do ticks for all sprite objects
			for planet in self.planets:	
			    planet.tick()

                        self.p1.tick()
                        self.p2.tick()

                        if self.missile:
                            self.missile.tick()
                        
			pygame.display.flip()
