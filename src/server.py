import socket
import threading
import sys

accounts = {}

if len(sys.argv) < 2:
	print "usage: ./server.py port"
	
	