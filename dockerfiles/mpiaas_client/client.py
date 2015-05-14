#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import argparse
import socket


PORT = 8000
SERVER_IP = 'localhost'
LOCAL_IP = socket.gethostbyname(socket.gethostname())


class EchoClient(LineReceiver):
    global PORT
    global SERVER_IP
    global LOCAL_IP

    parser = argparse.ArgumentParser(description='Run some funy tests !!')
    
    parser.add_argument('--localip', action="store", dest="localip",\
            help="Local client IP addres")
    parser.add_argument('--serverip', action="store", dest="serverip",\
            help="IP addres of server")
    parser.add_argument('--port', action="store", dest="port",\
            help="Connection port")

    args = parser.parse_args()
    
    if args.port:
        PORT = int(args.port)
    if args.serverip:
        SERVER_IP = args.serverip
    if args.localip:
        LOCAL_IP = args.localip


    end = "Bye-bye!"

    def connectionMade(self):
        self.sendLine("Hello, world!")
        self.sendLine("PORT: " + str(PORT))
        self.sendLine("SERVER_IP: " + str(SERVER_IP))
        self.sendLine("LOCAL_IP: " + str(LOCAL_IP))
        self.sendLine(self.end)


    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)



def main(reactor):

    factory = EchoClientFactory()
    reactor.connectTCP(SERVER_IP, PORT, factory)
    return factory.done


if __name__ == '__main__':
	task.react(main)
