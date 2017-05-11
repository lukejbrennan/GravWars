# Home server to get connections from client and and work

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
import time
import GameSpace
import conn
import sys
PORT = 40011

if __name__ == "__main__":
    if len(sys.argv) != 2:
            print('Usage: python ' + sys.argv[0] + ' -p1 | -p2')
            exit(0)        
    gs = GameSpace.GameSpace()
    if sys.argv[1] == '-p1':
		print 'listening for a command connection on port 40011'
		reactor.listenTCP(PORT, conn.p1ConnectionFactory(gs))
		#print("After listen")
		#reactor.run()
		#print("after reactor")
		gs.main('p1')
    elif sys.argv[1] == '-p2':
		reactor.connectTCP("ash.campus.nd.edu", PORT, conn.p2ConnectionFactory(gs))
		#print("After connect")
		#reactor.run()
		#print("after reactor")
		gs.main('p2')
    else:
		print('Usage: python ' + sys.argv[0] + ' -p1 | -p2')
		exit(0)

