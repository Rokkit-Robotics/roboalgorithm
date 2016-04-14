import robot_serial
from time import time

_start_time = None

def init():
	global _start_time
	_start_time = time()
	print "chassis init"
	robot_serial.chassis_enable()

def deinit():
	print "chassis deinit"
	robot_serial.chassis_disable()

def is_busy():
	global _start_time
	if time() - _start_time > 174:
		print "time over"
		deinit()
	return robot_serial.move_isBusy()


def turn(speed, angle):
	print "chassis turn: speed: %d angle: %d" % (speed, angle)
	robot_serial.move_rotate(speed, angle)

def move(speed, dest):
	print "chassis move: speed: %d dest: %d" % (speed, dest)
	robot_serial.move_forward(speed, dest)