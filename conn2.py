# Work client to connect to home.py proxy server

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.python import log
import connections
COMMAND_PORT = 40037
DATA_PORT = 42037

if __name__ == '__main__':
    reactor.connectTCP("ash.campus.nd.edu", COMMAND_PORT, connections.p2Factory(2))
    reactor.run()
