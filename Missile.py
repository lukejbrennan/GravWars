import sys
import pygame
import random
import math

class Missle(pygame.sprite.Sprite):
	def __init__(self, gs, angle, x, y, sendData):
		self.gs = gs
		self.mass = 20
		self.Vx = 300 * math.cos(angle)
		self.Vy = 300 * math.sin(angle)
		self.angle = angle 
		self.image = pygame.image.load("/home/brent/GravWars/missile.png").convert()
		self.image = pygame.transform.scale(self.image, (31, 13))
		self.OG_image = self.image
		self.rect = self.image.get_rect(center=(x, y))
		self.true_x = self.rect.centerx
		self.true_y = self.rect.centery
                if sendData:
                    self.sendFiringData()

        def sendFiringData(self):
            data = 'firing\n'
            data = data + str(self.Vx) + '\n' + str(self.Vy) + '\n'
            data = data + str(self.angle) + '\n'
            data = data + str(self.rect.centerx) + '\n' + str(self.rect.centery) + '\n'
            self.gs.conn_ref.transport.write(data)

	def tick(self):
	   	G = 1e4
	  	dt = float(1)/float(60)
		x_components = []
		y_components = []
		curr_x = self.rect.centerx
		curr_y = self.rect.centery
		for planet in self.gs.planets:
                    #Force on missile from planet
                    planet_x = planet.rect.centerx
                    planet_y = planet.rect.centery
                    r = math.sqrt((planet_x - curr_x)**2 + (planet_y - curr_y)**2)
                    F = float(G) * float(self.mass) * float(planet.mass) / float(r)**2

                    #Calculate angle between planet and missile and decompose force vector
                    angle = math.atan2(planet_y - curr_y, planet_x - curr_x)
                    x_components.append(math.cos(angle) * F)
                    y_components.append(math.sin(angle) * F)

                # Sum components and calculate a new force vector and accelerations
		Fx_tot = sum(x_components)
		Fy_tot = sum(y_components)
		ax = float(Fx_tot) / float(self.mass)
		ay = float(Fy_tot) / float(self.mass)
		dx = self.Vx * dt + .5 * ax * dt**2
		dy = self.Vy * dt + .5 * ay * dt**2
		self.Vx = self.Vx + ax * dt
		self.Vy = self.Vy + ay * dt
		self.angle = math.atan2(self.Vy, self.Vx)

		# Now move the missile
		self.true_x += dx
		self.true_y += dy
		self.image = pygame.transform.rotate(self.OG_image, -1 * self.angle * 180 / math.pi)
		self.rect.centerx = self.true_x
		self.rect.centery = self.true_y
		self.gs.screen.blit(self.image, self.rect)
					
