import sys, pygame, math
import Spaceship

class Spaceship(pygame.sprite.Sprite):
	def __init__(self, gs, angle, xper, yper, inactive_angle, activeMover, activeCollider):
		self.gs = gs
		self.activeM = activeMover # 1 if the angle can be changed by player, 0 otherwise
		self.activeC = activeCollider
		self.angle = angle 
                self.inactive_angle = inactive_angle
		self.health = 1 
		self.expCount = 0
		self.image = pygame.image.load("spaceship.png").convert()
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.image = pygame.transform.scale(self.image, (80, 80))
		self.OG_image = self.image
		self.rect = self.image.get_rect().move(xper*self.gs.width, yper*self.gs.height)

	def tick(self):
		if(self.activeM):
			(mouseX, mouseY) = pygame.mouse.get_pos()
			self.angle = 180 - math.atan2(mouseY-self.rect.centery, mouseX-self.rect.centerx)*180/math.pi
		else: 
			self.angle = self.inactive_angle
		self.image = pygame.transform.rotate(self.OG_image, self.angle)
		self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
		
		#Check for Collision
		if(self.activeC):
			if self.gs.missile is not None and self.rect.colliderect(self.gs.missile.rect): 
				self.health -= 1
				self.gs.missile = None
			if self.health <= 0 and self.expCount <= 16:
				if self.expCount < 10:
					self.image = pygame.image.load("/home/brent/GravWars/frames00"+str(self.expCount)+"a.png")
					self.expCount +=1
				else:
					self.image = pygame.image.load("/home/brent/GravWars/frames0"+str(self.expCount)+"a.png")
					self.expCount +=1
		if self.expCount <= 16:
			self.gs.screen.blit(self.image, self.rect)
			
