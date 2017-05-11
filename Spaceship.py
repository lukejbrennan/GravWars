import sys, pygame, math
import Spaceship

class Spaceship(pygame.sprite.Sprite):
	def __init__(self, gs, angle, xper, yper, activeMover, activeCollider):
		self.gs = gs
		self.activeM = activeMover # 1 if the angle can be changed by player, 0 otherwise
		self.activeC = activeCollider
		self.angle = angle 
		self.health = 10
		self.expCount = 0
		self.image = pygame.image.load("spaceship.png").convert()
		
#		self.OG_image = pygame.image.load("spaceship.png").convert()
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.image = pygame.transform.scale(self.image, (80, 80))
		self.OG_image = self.image
		self.rect = self.image.get_rect().move(xper*self.gs.width, yper*self.gs.height)
		#Get rectangle and set placement
#		self.rect = self.OG_image.get_rect().move(xper*self.gs.width, yper*self.gs.height)

	def tick(self):
		if(self.activeM):
			(mouseX, mouseY) = pygame.mouse.get_pos()
			# Calculate new anglei
			self.angle = 180 - math.atan2(mouseY-self.rect.centery, mouseX-self.rect.centerx)*180/math.pi
		else: 
			self.angle = 0
		self.image = pygame.transform.rotate(self.OG_image, self.angle)
		self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
		self.gs.screen.blit(self.image, self.rect)
		
		###########Check for Collision#######
#		if(self.activeC):
		#rectIndex0 = self.rect.collidelist(laser.rectList)
#			if self.rect.colliderect(missile.rect): 
#				self.health -= 1
#                               if self.gs.is_your_turn:
#                                   self.conn_ref.transport.write('spaceship_collision')
#			if self.health <= 0 and self.expCount <= 16:
#				if self.expCount < 10:
#					self.image = pygame.image.load("/home/scratch/paradigms/deathstar/explosion/frames00"+str(self.expCount)+"a.png")
#					self.expCount +=1
#				else:
#					self.image = pygame.image.load("/home/scratch/paradigms/deathstar/explosion/frames0"+str(self.expCount)+"a.png")
#					self.expCount +=1
			
