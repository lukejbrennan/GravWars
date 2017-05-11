from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import pickle


###########################################
# P1 Server Connection
###########################################

class P1Connection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connnectionMade(self):
        print('conn made')
        gs.getConnRef(self)
        gs.main('p1')

    def dataReceived(self, data):
        if data == 'spaceship_collision':
            #end game
            return
        elif data == 'planet_collision':
            self.gs.is_your_turn = not self.gs.is_you_turn
        else:
            print('Error: Unknown data')

class p1Factory(Factory):
    def __init__(self, gs):
        self.myconn = P1Connection(gs)

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


