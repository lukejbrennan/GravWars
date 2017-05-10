import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

class TextBox():
#	def __init__(self, message1, message2):
#		self.message1 = message1
#		self.message2 = message2
	def get_key():
		while 1:
			event = pygame.event.poll()
			if event.type == KEYDOWN:
				return event.key
			else:
				pass

	def display_box(screen, message1, message2):
		"Print a message in a box in the middle of the screen"
		fontobject1 = pygame.font.Font(None,18)
		fontobject2 = pygame.font.Font(None,18)
	#	pygame.draw.rect(screen, (0,0,0),
	#			((screen.get_width() / 2) - 100,
	#			 (screen.get_height() / 2) - 10,
	#			 200,20), 0)
	#	pygame.draw.rect(screen, (255,255,255),
	#			((screen.get_width() / 2) - 102,
	#			 (screen.get_height() / 2) - 12,
	#			 204,24), 1)
		if len(message1) != 0:
			screen.blit(fontobject1.render(message1, 1, (255,255,255)), (0,0)) 
			print message1
		if len(message2) != 0:
			screen.blit(fontobject2.render(message2, 1, (255,255,255)), (0,20)) 
	#		print message2
		
		pygame.display.flip()
	def ask(screen, q1, q2):
		"ask(screen, question) -> answer"
		pygame.font.init()
		out1 = []
		out2 = []
		display_box(screen, q1 + ": " + string.join(out1,""), q2+": "+string.join(out2,""))
		while 1:
			inkey = get_key()
			if inkey == K_BACKSPACE:
				out1 = out1[0:-1]
			elif inkey == K_RETURN:
				while 1:
					inkey = get_key()
					if inkey == K_BACKSPACE:
						out2 = out2[0:-1]
					elif inkey == K_RETURN:
						break
					elif inkey == K_MINUS:
						out2.append("_")
					elif inkey <= 127:
						out2.append(chr(inkey))
					display_box(screen,q1+": " + string.join(out1,""), q2+": "+string.join(out2,""))
				break
			elif inkey == K_MINUS:
				out1.append("_")
			elif inkey <= 127:
				out1.append(chr(inkey))
			display_box(screen,q1+": " + string.join(out1,""), q2+": "+string.join(out2,""))
		return [ string.join(out1,""), string.join(out2, "")]

#def main():
#	screen = pygame.display.set_mode((320,240))
#	retList = ask(screen, "Angle", "Velocity")
#	for item in retList:
#		print item+ " was returned"
#
#if __name__ == '__main__': main()
