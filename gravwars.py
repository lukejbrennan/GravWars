import sys, pygame, math
class DeathStar(pygame.sprite.Sprite):
	def __init__(self, gs):
		self.gs = gs
		self.image= pygame.image.load("spaceship.png").convert() 
		self.rect = self.image.get_rect() 
		self.OG_image=pygame.image.load("spaceship.png")
		self.angle =-80 
		self.image = pygame.transform.rotate(self.OG_image, self.angle)
	def tick(self):
		(mouseX, mouseY) = pygame.mouse.get_pos()
		# Calculate new anglei
		self.angle = 320-  math.atan2(mouseY-self.rect.centery, mouseX-self.rect.centerx)*180/math.pi

		self.image = pygame.transform.rotate(self.OG_image, self.angle)
		self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
		self.gs.screen.blit(self.image, self.rect)
			
	def move(self, event):
		if event.key == pygame.K_UP:
			self.rect.centery -=5
		elif event.key == pygame.K_DOWN:
			self.rect.centery +=5
		elif event.key == pygame.K_LEFT:
			self.rect.centerx -=5
		elif event.key == pygame.K_RIGHT:
			self.rect.centerx +=5

class Laser(pygame.sprite.Sprite):
	def __init__(self, gs):
		self.rectList = []
		self.gs = gs
		self.image = pygame.image.load("/home/scratch/paradigms/deathstar/laser.png")
		self.rect = self.image.get_rect()
		self.OG_image = pygame.image.load("/home/scratch/paradigms/deathstar/laser.png")
		self.vx = 5
		self.vy = 5
		self.count=0
	def tick(self, centerx, centery):
		for rt in self.rectList:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			angle = math.atan2(mouseY-centery, mouseX - centerx)
			#angle = math.degrees(angle)
			rt.centerx+= 20*self.vx
			rt.centery+= 20*self.vy
	def move(self, centerx, centery):
		rect = self.image.get_rect(center= (centerx, centery))
		self.rectList.append(rect)
		self.count = self.count + 1
		for rt in self.rectList:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			angle = math.atan2(mouseX-centerx, mouseY - centery)
			self.vx = math.sin(angle)
			self.vy = math.cos(angle)
			rt.centerx+= 0#self.vx 
			rt.centery+= 0 #self.vy

class Earth(pygame.sprite.Sprite):
	def __init__(self, gs):
		self.gs = gs
		self.image= pygame.image.load("/home/scratch/paradigms/deathstar/globe.png").convert()
		self.rect = self.image.get_rect().move(self.gs.width-250, self.gs.height-250)
		self.OG_image= pygame.image.load("/home/scratch/paradigms/deathstar/globe.png")
		self.health = 10
		self.expCount = 0
	def tick(self, laser):
		#Check for Collision
		rectIndex0 = self.rect.collidelist(laser.rectList)
		if rectIndex0 != -1:
			# pop off rectIndex0 from list
			laser.rectList.pop(0)
			self.health -= 1
		if self.health < 10:
			self.image = pygame.image.load("/home/scratch/paradigms/deathstar/globe_red100.png")
		if self.health <= 0 and self.expCount <= 16:
			if self.expCount < 10:
				self.image = pygame.image.load("/home/scratch/paradigms/deathstar/explosion/frames00"+str(self.expCount)+"a.png")
				self.expCount +=1
			else:
				self.image = pygame.image.load("/home/scratch/paradigms/deathstar/explosion/frames0"+str(self.expCount)+"a.png")
				self.expCount +=1
				
#	def move():
class GameSpace(object):
	def main(self):
		#Step 1#
		pygame.init()
		self.size = self.width, self.height = 640, 420
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)
		#Step 2#
		playerList = []		# initialize playerList
		displayList = []
		self.laserList = [] 		# List of lasers
		# Create objects
		self.player = DeathStar(self)
		self.laser = Laser(self)
		self.earth = Earth(self)
		# Set playerList
		playerList.append(self.player)
		# Set displayList
		displayList.append(self.earth)
		displayList.append(self.player)
		#displayList.append(self.laser)
		self.clock = pygame.time.Clock()

		while 1: #Step 3
			#Step 4#
			self.clock.tick(60) # 60x per second

			#Step 5#
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN: 		# if event
					self.player.move(event)	# call event handler

			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE]:
				laser = Laser(self)
				laser.move(self.player.rect.centerx, self.player.rect.centery)
				self.laserList.append(laser)
			# Step 6 #----> watch order of tics
			for p in playerList:
				p.tick()
			for ls in self.laserList:
				ls.tick(self.player.rect.centerx, self.player.rect.centery)
				self.earth.tick(ls)
			# Step 7 #
			self.screen.fill(self.black)
			#block transfer#
			if(self.earth.expCount <= 16):
				self.screen.blit(self.earth.image, self.earth.rect)
			#display laser
			for ls in self.laserList:
				for rt in ls.rectList:
					self.screen.blit(ls.image, rt)
			#for player in displayList:
			self.screen.blit(self.player.image, self.player.rect)#
			pygame.display.flip()
			

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()

