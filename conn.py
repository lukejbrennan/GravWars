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
        self.gs.getConnRef(self)
    
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
			while data[0] != '':
                                print data
                                print data[0].strip()
				if data[0].strip() == 'new_planet':
					color = data[1].strip()
					color = color.split('_')
					color = [int(c) for c in color]
					radius = int(data[2].strip())
					mass = int(data[3].strip())
					x = int(data[4].strip())
					y = int(data[5].strip())
					data = data[6:]
					self.gs.planets.append(Planet.Planet(self.gs, False, color=color, radius=radius, mass=mass, x=x, y=y))

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
            self.gs.getConnRef(self)

    def connectionMade(self):
		print 'Successful contact for command connection from work.py'
		self.gs.getConnRef(self)
		self.gs.setPlanets()
		self.gs.connection_made = True

    def dataReceived(self, data):
        print data
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

