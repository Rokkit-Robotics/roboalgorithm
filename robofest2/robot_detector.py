#!/usr/bin/env python

import zmq
from struct import unpack
from sys import argv
import sys
from time import sleep

server = "tcp://localhost:4444"

if (len(argv) > 3):
    #server = argv[2]
    pass

context = zmq.Context(1)
sub = context.socket(zmq.SUB)

sub.setsockopt(zmq.SUBSCRIBE, "")
sub.setsockopt(zmq.CONFLATE, 1)

sub.connect(server)
print "Connected to detector %s" % (server)


def read_from_socket():
	print "in socket"
	#a = raw_input()
	#sleep(1)
	data = sub.recv()
	data = unpack("<iiiii", data)

	print data
	return data

"""while True:
	read_from_socket()
	sleep(1)"""