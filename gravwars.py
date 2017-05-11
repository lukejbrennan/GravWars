# Home server to get connections from client and and work

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
import time
import GameSpace
import conn
import sys
PORT = 40037

if __name__ == "__main__":
    if len(sys.argv) != 2:
            print('Usage: python ' + sys.argv[0] + ' -p1 | -p2')
            exit(0)        
    gs = GameSpace.GameSpace()
    if sys.argv[1] == '-p1':
        print 'listening for a command connection on port 40037'
        reactor.listenTCP(PORT, conn.p1ConnectionFactory(gs))
        reactor.run()
    elif sys.argv[1] == '-p2':
        reactor.connectTCP("localhost", PORT, conn.p2ConnectionFactory(gs))
        reactor.run()
    else:
        print('Usage: python ' + sys.argv[0] + ' -p1 | -p2')
        exit(0)


