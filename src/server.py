#!/usr/bin/env python
import socket
import threading
import signal
import sys

accounts = {}
threads = []

def signal_handler(signal, frame):
	print "\nJoining threads... "
	for thread in threads:
		thread.join()
	#write sorted data to log.txt
	# print "Writing data to log.txt"
	writeToFile()
	exit(0)
	
def writeToFile():
	keylist = accounts.keys()
	keylist.sort()
	for name in accounts:
		print name + " " + str(accounts[name])
	
def adjust_accounts(data):
	for line in data:
		line = line.split(' ')
		#Operate on data
		if line[1] == "credit":
			if line[0] in accounts.keys():
				accounts[line[0]] += int(line[2][1:len(line[2])])
			else:
				accounts[line[0]] = int(line[2][1:len(line[2])])
		elif line[1] == "debit":
			if line[0] in accounts.keys():
				accounts[line[0]] -= int(line[2][1:len(line[2])])
			else:
				accounts[line[0]] = -int(line[2][1:len(line[2])])
	
def handle_socket(socket):
	#Receive data
	data = socket.recv(4096)
	#Split data up by entries to work on
	data = data.split('\n')
	#Remove last line
	data = data[:len(data)-1]
	adjust_accounts(data)		
	#Send response and close the socket
	socket.send('OK')
	socket.close()
	
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
		