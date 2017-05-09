import sys
import pygame
import random
import math

class Missle(pygame.sprite.Sprite):
	def __init__(self, gs, angle, rect):
                self.gs = gs
		self.mass = 20
		self.angle = angle 
		self.image = pygame.image.load("Missle.png").convert()
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.image = pygame.transform.scale(self.image, (100, 100))
		self.OG_image = self.image
                self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

	def tick(self):
            G = 6.67e-11
            step_size = .05
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
	        angle = 180 - math.atan2(planet_y - curr_y, planet_x - curr_x) * 180 / math.pi
                x_components.append(math.sin(angle) * F)
                y_components.append(math.cos(angle) * F)

            # Sum components and calculate a new vector and angle
            Fx_tot = sum(x_components)
            Fy_tot = sum(y_components)
            self.angle = 180 - math.atan2(Fy_tot, Fx_tot)

	    # Now move the missile
	    self.image = pygame.transform.rotate(self.OG_image, self.angle)
	    self.rect = self.image.get_rect().move(Fx_tot * step_size, Fy_tot * step_size)
	    self.gs.screen.blit(self.image, self.rect)
					
