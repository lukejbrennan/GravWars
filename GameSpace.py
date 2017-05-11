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
from twisted.internet.task import LoopingCall


class GameSpace(object):
	def __init__(self):
            MIN_PLANETS = 2
            MAX_PLANETS = 4
            pygame.init()
            self.disable = False
            self.angle = 0
            self.velocity = 100
            self.size = self.width, self.height = 840, 620
            self.screen = pygame.display.set_mode(self.size)
            self.num_planets = random.randint(MIN_PLANETS, MAX_PLANETS)
            self.planets = []
            self.missile = None
            self.p1 = Spaceship.Spaceship(self, 90, .0, .5, 180, False, False)
            self.p2 = Spaceship.Spaceship(self, 90, .88, .5, 0, False, False)
            self.black = 0,0,0
            self.is_your_turn = None
            self.conn_ref = None
            self.connection_made = False
            self.planets_set = False 
            self.player = 'p0'

        def getConnRef(self, conn_ref):
		self.conn_ref = conn_ref
	
	def sendPlanet(self, planet):
                #Send data for a planet
		data = 'new_planet\n'
		data = data + str(planet.color[0]) + '_'
		data = data + str(planet.color[1]) + '_'
		data = data + str(planet.color[2]) + '\n'
		data = data + str(planet.radius) + '\n'
		data = data + str(planet.mass) + '\n'
		data = data + str(planet.x) + '\n'
		data = data + str(planet.y) + '\n'
		self.conn_ref.transport.write(data)
	
	def setTurnPermissions(self):
		#Do all checks on whose turn it is
		if self.is_your_turn:
			if self.player == 'p2':
				self.p1.activeM = False
				self.p1.activeC = True
				self.p2.activeC = False
                                self.p2.activeM = True
			elif self.player == 'p1':
				self.p2.activeM = False
				self.p2.activeC = True
                                self.p1.activeC = False
                                self.p1.activeM = True
		else:
			if self.player == 'p2':
				self.p1.activeM = False
				self.p1.activeC = False
				self.p2.activeC = True
                                self.p2.activeM = False
			elif self.player == 'p1':
				self.p2.activeM = False
				self.p2.activeC = False
				self.p1.activeC = True
                                self.p1.activeM = False

	def fireMissile(self):
		(mouseX, mouseY) = pygame.mouse.get_pos()
		ship_x = None
		ship_y = None
		if self.player == 'p1':
			ship_x = self.p1.rect.centerx
			ship_y = self.p1.rect.centery
			angle = math.atan2(mouseY-ship_y, mouseX - ship_x)
			self.missile = Missile.Missle(self, angle, self.p1.rect.centerx, self.p1.rect.centery, True)
		elif self.player == 'p2':
			ship_x = self.p2.rect.centerx
			ship_y = self.p2.rect.centery
			angle = math.atan2(mouseY-ship_y, mouseX - ship_x)
			self.missile = Missile.Missle(self, angle, self.p2.rect.centerx, self.p2.rect.centery, True)

	def setPlanets(self):
                #Put the planets on the map
		if self.player == 'p1':
		    for planet in range(self.num_planets):
			self.planets.append(Planet.Planet(self, True))
			self.sendPlanet(self.planets[planet])
		elif self.player == 'p2':
                        return
		else:
			print('Error: unknown self.player name')
	
	def main(self, player):
                #Run two main event loops
		self.player = player
                if player == 'p1':
                    self.is_your_turn = True
                else:
                    self.is_your_turn = False
		lc = LoopingCall(self.eventLoop)
		lc.start(0.1)
		reactor.run()
	
	def eventLoop(self):
                try:
                    #Handle Events
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                    reactor.stop()
                                    sys.exit(0)
                            if event.type == pygame.MOUSEBUTTONUP:
                                    if self.is_your_turn and not self.disable:
                                            self.fireMissile()
                    
                    self.screen.fill(self.black)
                    self.setTurnPermissions()
                    
                    #Do ticks for all sprite objects
                    for planet in self.planets:	
                            planet.tick()

                    if not self.disable:
                        self.p1.tick()
                        self.p2.tick()

                    if self.missile:
                            self.missile.tick()
                    
                    #Check if missile has gone off the page
                    if self.missile:
                            if self.missile.true_x < 0 or self.missile.true_x > self.width or self.missile.true_y < 0 or self.missile.true_y > self.height:
                                    self.missile = None
                                    self.is_your_turn = not self.is_your_turn
                                            
                    pygame.display.flip()
                except Exception as e:
                    print e
