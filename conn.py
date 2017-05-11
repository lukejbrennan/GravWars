from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import time

###################################
# p2 client Connection
###################################

class p2Connection(Protocol):
    def __init__(self, gs):
            self.gs = gs

    def connectionMade(self):
        print 'Successful contact for command connection from work.py'
        self.gs.getConnRef(self)
        self.gs.main('p1')

    def dataReceived(self, data):
        if data == 'spaceship_collision':
            #end game
            return
        elif data == 'planet_collision':
            self.gs.is_your_turn = not self.gs.is_you_turn
        else:
            print('Error: Unknown data')



class p2ConnectionFactory(ClientFactory):
    def __init__(self, gs):
        self.myconn = p1Connection(gs)

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
        self.gs.main('p1')


    def dataReceived(self, data):
        if data == 'spaceship_collision':
            #end game
            return
        elif data == 'planet_collision':
            self.gs.is_your_turn = not self.gs.is_you_turn
        else:
            print('Error: Unknown data')

class p1ConnectionFactory(Factory):
    def __init__(self, gs):
        self.myconn = p1Connection(gs)

    def buildProtocol(self, addr):
        return self.myconn

