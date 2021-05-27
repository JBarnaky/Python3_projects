#!/bin.python3

import sys
import socket
from datetime import datetime

if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1])
else:
	print("Not enough arguments")
	print("Syntax: python3 pscanner.py <ip>")
	sys.exit()

print("-" * 50)
print("Scanning target" + target)
print("Time started" + str(datetime.now()))
print("-" * 50)

try:
	for port in range(50,85):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		result = s.connect_ex((target, port))
		print("Scanning port {}".format(port))
		if result == 0:
			print("Port {} is open".format(port))