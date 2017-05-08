import sys, pygame, math
import Spaceship

class Spaceship(pygame.sprite.Sprite):
	def __init__(self, gs, angle, xper, yper):
		self.gs = gs
		self.angle = angle 
		self.health = 10
		self.image = pygame.image.load("spaceship.png").convert()
		
#		self.OG_image = pygame.image.load("spaceship.png").convert()
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.image = pygame.transform.scale(self.image, (100, 100))
		self.OG_image = self.image
		self.rect = self.image.get_rect().move(xper*self.gs.width, yper*self.gs.height)
		#Get rectangle and set placement
#		self.rect = self.OG_image.get_rect().move(xper*self.gs.width, yper*self.gs.height)

	def tick(self):
		(mouseX, mouseY) = pygame.mouse.get_pos()
		# Calculate new anglei
		self.angle = 180 - math.atan2(mouseY-self.rect.centery, mouseX-self.rect.centerx)*180/math.pi

		self.image = pygame.transform.rotate(self.OG_image, self.angle)
		self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
		self.gs.screen.blit(self.image, self.rect)
			
