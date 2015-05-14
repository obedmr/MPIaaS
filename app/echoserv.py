#!/usr/bin/env python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import twisted.internet.error
import sys

import ConfigParser
CONFIG_CONF = "setup.conf"

PORT=8000

class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        lines = data.split('\n') 
        for line in lines:
            if "PORT:" in line:
                print line
                port = line.split(":")[1].strip()
            if "SERVER_IP:" in line:
                print line
                server_ip = line.split(":")[1].strip()
            if "LOCAL_IP:" in line:
                print line
                client_ip = line.split(":")[1].strip()

        parser = ConfigParser.SafeConfigParser()
        section = 'CLIENTS_' + client_ip
        parser.add_section(section)
        parser.set(section, 'ip',str(client_ip))
        parser.set(section, 'port',str(port))

        parser.write(sys.stdout)
        file_conf = open(CONFIG_CONF,'a')
        parser.write(file_conf)
        file_conf.close()

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
