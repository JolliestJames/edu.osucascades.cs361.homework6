#!/usr/bin/env python
import socket
import threading
import signal
import sys

#Initialize global variables
accounts = {}
threads = []
lock = threading.Lock()

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
	
def adjustAccounts(transactions):
	#Operate on each transaction
	for t in transactions:
		t = t.split(' ')
		#Acquire lock on accounts for performing operations
		lock.acquire()
		try:
			if t[1] == "credit":
				#Add to balance
				if t[0] in accounts.keys():
						accounts[t[0]] += int(t[2][1:len(t[2])])
				else:
					accounts[t[0]] = int(t[2][1:len(t[2])])
			elif t[1] == "debit":
				#Subtract from balance
				if t[0] in accounts.keys():
					accounts[t[0]] -= int(t[2][1:len(t[2])])
				else:
					accounts[t[0]] = -int(t[2][1:len(t[t2])])
		finally:
			#Let go of lock so other threads can operate
			lock.release()
	
def handleSocket(socket):

	#Initialize list for storing transactions to adjust accounts
	transactions = []
	
	#Store each transaction in a string
	transaction = ''
	
	while True:
		#Receive transactions until the client sends one of length zero
		transaction = socket.recv(1024)
		if len(transaction) is 0:
			#Let client know it can exit its send loop
			socket.send('OK')
			break
		else:
			#Add transaction to list 
			transactions.append(transaction)
			#Let client know it can send another transaction
			socket.send('OK')

	adjustAccounts(transactions)
	socket.close()
	
#Initialize listener for signal interrupt
signal.signal(signal.SIGINT, signal_handler)

if len(sys.argv) < 2:
	print "usage: ./server.py port"
else: 
	try:
		#Set port
		port = sys.argv[1]
		#Create socket
		socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#Bind socket to local host on port provided by user
		socket.bind(('127.0.0.1', int(port)))
		#Handle up to 1000 clients at a time
		socket.listen(1000)
	
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