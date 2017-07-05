""" Demo of a simple TCP server
    Use the included manifest.yaml to deploy to 
    Cloud Foundry and show off the tcp router.
"""

import os
from twisted.internet import protocol, reactor
from twisted.protocols import basic


class FingerProtocol(basic.LineReceiver):
    """Basic finger protocol implementation,
        returns a single line of user detail."""

    def lineReceived(self, line):
        self.transport.write("%s\n" % (self.factory.getUser(line)))
        self.transport.loseConnection()


class FingerFactory(protocol.ServerFactory):
    """Twisted factory for simple finger server.
    Accepts a set of users and descriptions in constructor."""

    protocol = FingerProtocol

    def __init__(self, **kwargs):
        self.users = kwargs

    def getUser(self, user):
        return self.users.get(user, "no such user")

PORT = int(os.environ.get('PORT', 8080))
print("I found a PORT and it is %s" % PORT)
reactor.listenTCP(PORT, FingerFactory(josh="awesome guy"))
reactor.run()
