#!/usr/bin/env python
import socket
import threading
import signal
import sys

accounts = {}
threads = []

def signal_handler(signal, frame):
	print "\nJoining threads... "
	#Join every thread in list
	for thread in threads:
		thread.join()
	print "Writing data to log.txt"
	writeToFile()
	exit(0)
	
def writeToFile():
	#Open file to write
	file = open("log.txt", "w+")
	names = accounts.keys()
	names.sort()
	#Write each account name and balance to file
	for name in names:
		file.write(name + " $" + str(accounts[name]) + "\n")
	file.close()
	
def adjustAccounts(data):
	#Operate on each transaction
	for line in data:
		line = line.split(' ')
		#Add to balance
		if line[1] == "credit":
			if line[0] in accounts.keys():
				accounts[line[0]] += int(line[2][1:len(line[2])])
			else:
				accounts[line[0]] = int(line[2][1:len(line[2])])
		#Subtract from balance
		elif line[1] == "debit":
			if line[0] in accounts.keys():
				accounts[line[0]] -= int(line[2][1:len(line[2])])
			else:
				accounts[line[0]] = -int(line[2][1:len(line[2])])
	
def handleSocket(socket):
	#Receive data
	data = socket.recv(4096)
	#Split data up by entries to work on
	data = data.split('\n')
	#Remove last line
	data = data[:len(data)-1]
	#Operate transactions
	adjustAccounts(data)		
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
		#Create socket
		socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#Bind socket to local host on port provided by user
		socket.bind(('127.0.0.1', int(port)))
		#Handle up to 5 clients at a time
		socket.listen(50)
	
		while True:
			#Accept client connection
			(client_socket, address) = socket.accept()
			#Create thread and add to list
			t = threading.Thread(target = handleSocket, args=(client_socket,))
			threads.append(t)
			#Begin thread for handling transactions
			t.start()

	#Error handling
	except Exception as e:
		print e
		exit(1)