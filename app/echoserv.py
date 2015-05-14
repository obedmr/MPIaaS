#!/usr/bin/env python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import twisted.internet.error
import sys

PORT=8000

class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        print data
        self.transport.write(data)

def main():

    try:
        f = Factory()
        f.protocol = Echo
        reactor.listenTCP(PORT, f)
        reactor.run()
    except twisted.internet.error.CannotListenError, ex:
        print "Port is %d busy: %s" % (PORT, ex)
        print "Run ./mpiaas_runner.py --killserver"
        sys.exit(1)

if __name__ == '__main__':
    main()
