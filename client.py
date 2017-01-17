#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET indicates that we want an IPV4 socket
# socket.SOCK_STREAM indicates that we want a TCP socket

clientSocket.connect(("www.google.com",80)) # 80 is the portal number
# note that there is no http://
# we have a tuple is because in C, it ask for a struct as param

request = "GET / HTTP/1.0\r\n\r\n"

clientSocket.sendall(request)

response = bytearray()
while True:
    part = clientSocket.recv(1024)
    if (part):
        response.extend(part)
    else:
        break

print response
