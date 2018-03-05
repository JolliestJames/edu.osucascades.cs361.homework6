#!/usr/bin/env python
import socket
import threading
import sys

accounts = {}

if len(sys.argv) < 2:
	print "usage: ./server.py port"
else: 
	port = sys.argv[1]
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.bind(('localhost', int(port)))
	socket.listen(5)
	
	while True:
		# accept connections from outside
		(clientsocket, address) = socket.accept()
		# now do something with the clientsocket
		# in this case, we'll pretend this is a threaded server
		print clientsocket 
		print address
		# ct = client_thread(clientsocket)
		# ct.run()