#!/usr/bin/env python

import serial as s
import struct
from sys import argv

serial = s.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1.0)

#serial.open()
print "Connected to serial on port"

def chassis_enable():
	data = struct.pack("<BBB", 2, 1, 1)
	serial.write("@")
	serial.write(data)

def chassis_disable():
	data = struct.pack("<BBB", 2, 1, 0)
	serial.write("@")
	serial.write(data)

def move_forward(speed, len):
	data = struct.pack("<BBBhh", 0x06, 0x02, 0x01, speed, len)

	serial.write("@")
	serial.write(data)

def move_rotate(speed, len):
	data = struct.pack("<BBBhh", 0x06, 0x02, 0x02, speed, len)

	serial.write("@")
	serial.write(data)

def move_isBusy():
	serial.flushInput() # just clean the buffer
	data = struct.pack("<BBB", 0x02, 0x02, 0x00)

	serial.write("@")
	serial.write(data)

	reply = serial.read(2)
	dummy = 0
	(reply, dummy) = struct.unpack("BB", reply)

	#print "%x" % (reply)
	return reply

def move_wait():
	while (move_isBusy() > 0):
		pass


#chassis_enable()
#move_forward(1024, 500)

