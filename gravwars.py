import random
import Planet
import Missile
import Spaceship
import sys
import pygame
import math
import pickle
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class GameSpace(object):
	def __init__(self):
		MIN_PLANETS = 1  
		MAX_PLANETS = 1
		pygame.init()
		self.angle = 0
		self.velocity = 100
		self.size = self.width, self.height = 840, 620 # 320, 320
		self.screen = pygame.display.set_mode(self.size)
		num_planets = random.randint(MIN_PLANETS, MAX_PLANETS)
		self.planets = []
		self.missile = None
		#### (self, rot, xpos, ypos, activeMover, activeCollider
		self.p1 = Spaceship.Spaceship(self, 90, .0, .5, True, True)
		self.p2 = Spaceship.Spaceship(self, 90, .88, .5, True, True)
		self.black = 0,0,0
                self.is_your_turn = None
                self.conn_ref = None
        
        def getConnRef(conn_ref):
            self.conn_ref = conn_ref

	def main(self, player):
		self.clock = pygame.time.Clock()
                if player == 'p1':
                    self.is_your_turn = True
        	    for planet in range(num_planets):
			self.planets.append(Planet.Planet(self, True))
                        self.conn_ref.transport.write('planet\n' + pickle.dumps(planets[planet]))

                elif player == 'p2':
                    self.is_your_turn = False
                else:
                    print('Error: unknown player name')

		while 1:
			self.clock.tick(60) # 60x per second
			#Handle events
			for event in pygame.event.get():
			        if event.type == pygame.QUIT:
				    sys.exit()
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
                                p1.activeM = True
                                p1.activeC = False
                                p2.activeM = False
                                p2.activeC = True
                            elif player == 'p2':
                                p2.activeM = True
                                p2.activeC = False
                                p1.activeM = False
                                p1.activeC = True

			#Do ticks for all sprite objects
			for planet in self.planets:	
				planet.tick()
				self.p1.tick()
				if self.missile:
					self.missile.tick()
				self.p2.tick()
				
				#Check if missile has gone off the page
				if self.missile:
					if self.missile.true_x < 0 or self.missile.true_x > self.width or self.missile.true_y < 0 or self.missile.true_y > self.height:
						self.missile = None

                        
			pygame.display.flip()

if __name__ == '__main__':
    PORT = 40037
    if len(sys.argv) != 2:
            print('Usage: python ' + sys.argv[0] + ' -p1 | -p2')
            exit(0)        
    gs = GameSpace()
    if sys.argv[1] == '-p1':
        reactor.listenTCP(PORT, connections.p1Factory(gs))
        reactor.run()
    elif sys.argv[1] == '-p2':
        reactor.connectTCP("ash.campus.nd.edu", PORT, connections.p2Factory(gs))
        reactor.run()
    else:
        print('Usage: python ' + sys.argv[0] + ' -p1 | -p2')
        exit(0)

