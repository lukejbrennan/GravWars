# Home server to get connections from client and and work

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
import time
import connections
COMMAND_PORT = 40037
DATA_PORT = 42037
CLIENT_PORT = 43037

#Listen for command connection
print 'listening for a command connection on port 40037'
reactor.listenTCP(COMMAND_PORT, connections.p2Factory(2))
reactor.run()
