#!/usr/bin/python
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import time
import connections
COMMAND_PORT = 40011
DATA_PORT = 42011
CLIENT_PORT = 43011

###########################################
# P1 Server Connection
###########################################

class P1Connection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connnectionMade(self):
        print "conn made"
        gs.getConnRef(self)
        gs.main('p1')

    def dataReceived(self, data):
        if data == 'spaceship_collision':
            #end game
            return
        elif data == 'planet_collision':
            self.gs.is_your_turn = not self.gs.is_you_turn
        else:
            print "Error: Unknown data"

class p1Factory(Factory):
    def __init__(self, gs):
		self.myconn = P1Connection(gs)
		print "connection factory initialized"

    def buildProtocol(self, addr):
        return self.myconn

#Listen for command connection
print 'listening for a command connection on port 40011'
reactor.listenTCP(40011, p1Factory(2))
reactor.run()
