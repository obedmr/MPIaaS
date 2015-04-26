#!/usr/bin/env python
import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

TCP_IP = str(sys.argv[1])

print TCP_IP

 
s = socket.socket(socket.AF_INET,
socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
print "received data:", data
