#!/usr/bin/env python
import socket
import threading
import signal
import sys

def signal_handler(signal, frame):
	print "\nJoining threads"
	for thread in threads:
		thread.join()
	#write sorted data to log.txt
	exit(0)
	

def handle_socket(socket):
	st = socket.recv(1024)
	print st
	socket.send('OK\n')
	socket.close()
	
accounts = {}
threads = []

#Initialize listener for signal interrupt
signal.signal(signal.SIGINT, signal_handler)

if len(sys.argv) < 2:
	print "usage: ./server.py port"
else: 
	try:
		port = sys.argv[1]
		socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.bind(('127.0.0.1', int(port)))
		socket.listen(5)
	
		while True:
			#Accept client connection
			(client_socket, address) = socket.accept()
			t = threading.Thread(target = handle_socket, args=(client_socket,))
			threads.append(t)
			t.start()
			
			
	except  Exception as e:
		print e
		exit(1)
		