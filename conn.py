from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import time
import Planet

###################################
# p2 client Connection
###################################

class p2Connection(Protocol):
    def __init__(self, gs):
            self.gs = gs

    def connectionMade(self):
        print 'Successful contact for command connection from work.py'
        self.gs.getConnRef(self)
        self.gs.connection_made = True

    def dataReceived(self, data):
		print 'Receiving data'
		if data == 'spaceship_collision':
            #end game
			return
		elif data == 'planet_collision':
			self.gs.is_your_turn = not self.gs.is_your_turn
		else:
			print 'Receiving planets'
			data = data.split('\n')
			print data
			while data[0] != '':
				if data[0].strip() == 'new_planet':
					color = data[1].strip()
					color = color.split('_')
					color = [int(c) for c in color]
					radius = int(data[2].strip())
					mass = int(data[3].strip())
					x = int(data[4].strip())
					y = int(data[5].strip())
					data = data[5:]
					
					####
					self.gs.planets.append(Planet.Planet(self.gs, False, color=color, radius=radius, mass=mass, x=x, y=y))
			else:
				print('Error: Unknown data')




class p2ConnectionFactory(ClientFactory):
    def __init__(self, gs):
        self.myconn = p2Connection(gs)

    def buildProtocol(self, addr):
        return self.myconn


###################################
# p1 server Connection
###################################

class p1Connection(Protocol):
    def __init__(self, gs):
            self.gs = gs

    def connectionMade(self):
		print 'Successful contact for command connection from work.py'
		self.gs.getConnRef(self)
		self.gs.setPlanets()
		self.gs.connection_made = True


    def dataReceived(self, data):
        if data == 'spaceship_collision':
            #end game
            return
        elif data == 'planet_collision':
            self.gs.is_your_turn = not self.gs.is_your_turn
        else:
            print('Error: Unknown data')

class p1ConnectionFactory(Factory):
    def __init__(self, gs):
        self.myconn = p1Connection(gs)

    def buildProtocol(self, addr):
        return self.myconn

