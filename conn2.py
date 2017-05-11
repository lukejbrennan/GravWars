# Work client to connect to home.py proxy server

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.python import log
import connections
COMMAND_PORT = 40037
DATA_PORT = 42037

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
