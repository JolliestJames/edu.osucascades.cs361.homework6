#!/usr/bin/env python
import socket
import threading
import sys

if len(sys.argv) < 3:
	print "usage: ./client.py port input_file"
else: 
	port = sys.argv[1]
	inputFile = sys.argv[2]
	# print inputFile	