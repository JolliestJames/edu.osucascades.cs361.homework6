#!/usr/bin/env python
import socket
import threading
import sys

if len(sys.argv) < 3:
	print "usage: ./client.py port input_file"
else: 
	port = sys.argv[1]
	inputFile = sys.argv[2]
	
	try:
		with open(inputFile) as file:
			content = file.readlines()
			content = [x.strip() for x in content]
			
		#Create socket and connect to server
		socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.connect(('127.0.0.1', int(port)))
		
		#Send data to server
		for line in content:
			socket.send(line+'\n')
		
		#Receive terminating messaage from server
		st = socket.recv(100)
		# print st
		
		#Close socket
		socket.close()
		exit(0)
	except Exception as e:
		print e
		exit(1)