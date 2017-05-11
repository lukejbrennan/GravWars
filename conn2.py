#!/usr/bin/python
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.python import log
import connections
COMMAND_PORT = 40011
DATA_PORT = 42011

###########################################
# P2 Client Connection
###########################################

class P2Connection(Protocol):
    def __init__(self, gs):
		self.gs = gs
		print "connection initialized"

    def connnectionMade(self):
        print "conn_made"
        gs.getConnRef(self)
        gs.main('p2')

    def dataReceived(self, data):
        if data == 'spaceship_collision':
            #end game
            return
        elif data == 'planet_collision':
            self.gs.is_your_turn = not self.gs.is_you_turn
        else:
            data = data.split('\n')
            self.gs.planets.append(pickle.loads(data[1]))

class p2Factory(ClientFactory):
    def __init__(self, gs):
		self.myconn = P2Connection(gs)
		print "factory initialized"
    def buildProtocol(self, addr):
        return self.myconn

###########################################
# P2 Client Connection
###########################################

class P2Connection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connnectionMade(self):
        print('conn_made')
        gs.getConnRef(self)
        gs.main('p2')

    def dataReceived(self, data):
        if data == 'spaceship_collision':
            #end game
            return
        elif data == 'planet_collision':
            self.gs.is_your_turn = not self.gs.is_you_turn
        else:
            data = data.split('\n')
            self.gs.planets.append(pickle.loads(data[1]))

class p2Factory(ClientFactory):
    def __init__(self, gs):
        self.myconn = P2Connection(gs)

    def buildProtocol(self, addr):
        return self.myconn



if __name__ == '__main__':
    reactor.connectTCP("ash.campus.nd.edu", COMMAND_PORT, p2Factory(2))
    reactor.run()
>>>>>>> e2f46ed6c77b324ce5fcefa6901538b6478ea226
