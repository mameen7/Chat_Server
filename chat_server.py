# Chat Server

__author__ = 'Ahmad M Ameen <ahmadmameen7@gmail.com>'
__copyright__ = 'Copyright (c) 2018, algebra'
__version__ = "1.1"

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = 'REGISTER'
    def connectionMade(self):
        self.sendLine('What is your name?')
    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage("%s has left the channel" %(self.name))
    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)
    def handle_REGISTER(self, name):
        if name in self.factory.users:
            print 'Name taken, choose different name'
            return
        self.sendLine('Welcome, %s!' %(name,))
        self.broadcastMessage('<%s> has joined the channel' %(name))
        self.name = name
        self.factory.users[name] = self
        self.state = 'CHAT'
    def handle_CHAT(self, message):
        message = "<%s> %s" %(self.name, message)
        self.broadcastMessage(message)
    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            if protocol != self:  
                protocol.sendLine(message)

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}
    def buildProtocol(self, addr):
        return ChatProtocol(self)

reactor.listenTCP(8000, ChatFactory())
reactor.run()
