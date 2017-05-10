import sys
import pygame
import random
import math

class Missle(pygame.sprite.Sprite):
	def __init__(self, gs, angle, rect):
                self.gs = gs
		self.mass = 20
                self.Vx = 100 * math.cos(angle)
                self.Vy = 100 * math.sin(angle)
		print('vx is ' + str(self.Vx) + ' and vy is ' + str(self.Vy))
                self.angle = angle 
		self.image = pygame.image.load("/home/brent/GravWars/missile.png").convert()
		self.image = pygame.transform.rotate(self.image, -90)
		self.image = pygame.transform.scale(self.image, (100, 100))
		self.OG_image = self.image
                self.rect = self.image.get_rect(center=(rect.centerx, rect.centery))

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
            dx = math.ceil(self.Vx * dt + .5 * ax * dt**2)
            dy = math.ceil(self.Vy * dt + .5 * ay * dt**2)
            self.Vx = self.Vx + ax * dt
            self.Vy = self.Vy + ay * dt
            self.angle = math.atan2(self.Vy, self.Vx)
	    
            # Now move the missile
	    self.image = pygame.transform.rotate(self.OG_image, -1 * self.angle * 180 / math.pi)
	    self.rect = self.rect.move(dx, dy)
	    self.gs.screen.blit(self.image, self.rect)
					
