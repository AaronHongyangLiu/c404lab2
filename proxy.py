#!/usr/bin/env python


# from github: https://github.com/joshua2ua
import socket
import os, sys, select
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(("0.0.0.0", 8000)) # only root user can use port less than 1024, e.g. use 8000 on lab machine
serverSocket.listen(5) #OS only accept 5 incoming connections in the queue

while True:
    (incomingSocket, address) = serverSocket.accept()
    print "We got a connection from %s"%(str(address))
    if os.fork() != 0:
        continue
	
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.AF_INET indicates that we want an IPV4 socket
    # socket.SOCK_STREAM indicates that we want a TCP socket

    clientSocket.connect(("www.google.com", 80))  # 80 is the portal number
	
    incomingSocket.setblocking(0)
    clientSocket.setblocking(0)

    while True:
        request = bytearray()
        while True:
            try:
                part = incomingSocket.recv(1024)
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    part = None
                else:
                    raise

            if (part):
                clientSocket.sendall(part)
                request.extend(part)
            elif part is None:
                break
            else:
                exit(0)
                
        if len(request)>0:
            print request

        response = bytearray()
        while True:
            try:
                part = clientSocket.recv(1024)
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    part = None
                else:
                    raise

            if (part):
                incomingSocket.sendall(part)
                response.extend(part)
            elif part is None:
                break
            else:
                exit(0)
        if len(response)>0:
            print response
        select.select(
            [incomingSocket, clientSocket], #read
            [],                             #write
            [incomingSocket, clientSocket], #exceptions
            1.0                             #timeout
        )
