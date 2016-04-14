#!/usr/bin/python
# -*- coding: utf-8 -*-

import chassis
import road_graph
import sys
import RPi.GPIO as GPIO
from robot_detector import *
from time import sleep
from time import time

"""def read_from_socket():
	return [0, 0, 0, 0, 0]"""
# class route:
SPEED = 1250
ANGLE_LEFT = 88
ANGLE_RIGHT = -88
REVERSE = 180
CIRCLE = 360
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

#	def __init__(self)
STOP = 3
RIGHT_ONLY = 2
LEFT_ONLY = 0
STRAIGHT_ONLY = 1
SEMAFORE_RED = 4

TILE_SIZE = 1060

def tiles(amount):
	return amount * TILE_SIZE

#crutch 1
def move_1_tile():
	chassis.move(SPEED, TILE_SIZE)
	while chassis.is_busy():
		sleep(0.01)
		pass
	print ('move_1_tile')

def move_half_tile():
	chassis.move(SPEED, TILE_SIZE/2)
	while chassis.is_busy():
		sleep(0.01)
		pass
	print ('move_0.5_tile')


def move(distance):
	chassis.move(SPEED, distance * TILE_SIZE)
	while chassis.is_busy():
		sleep(0.01)
		pass
	print('move ', distance)

#use for road points in algorithm, this function moves robot -1 tile from the set distance
def turn(x_dif, y_dif, cur_dir):
	#case : LEFT
	if x_dif < 0:
		print ("AIM_DIR: left")
		if cur_dir == RIGHT:
			print ("TURN reverse")
			chassis.turn(SPEED, REVERSE)
		elif cur_dir == UP:
			print ("TURN left")
			chassis.turn(SPEED, ANGLE_LEFT)
		elif cur_dir == DOWN:
			print ("TURN right")
			chassis.turn(SPEED, ANGLE_RIGHT)
		while chassis.is_busy():
			sleep(0.01)

		return LEFT
	#case: RIGHT
	elif x_dif > 0:
		print ("AIM_DIR: right")
		if cur_dir == LEFT:
			print ("TURN reverse")
			chassis.turn(SPEED, REVERSE)
		elif cur_dir == UP:
			print ("TURN right")
			chassis.turn(SPEED, ANGLE_RIGHT)
		elif cur_dir == DOWN:
			print ("TURN left")
			chassis.turn(SPEED, ANGLE_LEFT)
		while chassis.is_busy():
			sleep(0.01)

		return RIGHT
	#case: UP
	if y_dif < 0:
		print ("AIM_DIR: up")
		if cur_dir == LEFT:
			print ("TURN right")
			chassis.turn(SPEED, ANGLE_RIGHT)
		elif cur_dir == RIGHT:
			print ("TURN left")
			chassis.turn(SPEED, ANGLE_LEFT)
		elif cur_dir == DOWN:
			print ("TURN reverse")
			chassis.turn(SPEED, REVERSE)
		while chassis.is_busy():
			sleep(0.01)

		return UP
	#case: DOWN
	if y_dif > 0:
		print ("AIM_DIR: down")
		if cur_dir == LEFT:
			print ("TURN left")
			chassis.turn(SPEED, ANGLE_LEFT)
		elif cur_dir == RIGHT:
			print ("TURN right")
			chassis.turn(SPEED, ANGLE_RIGHT)
		elif cur_dir == UP:
			print ("TURN reverse")
			chassis.turn(SPEED, REVERSE)
		while chassis.is_busy():
			sleep(0.01)

		return DOWN




#is it guaranteed that list_of_res contains all restrictions by the time of its invokation
def check_restrictions(my_map, cur, prev, direction, flag = None):
	list_of_res = read_from_socket()
	type_of_res = None
	idx = 0
	if_used = False

	for i, x in enumerate(list_of_res):
		idx = 0
		if x == 1:
			type_of_res = i
			if_used = True

		if type_of_res == STOP:
			print ("RESTRICTION: stop")
			list_of_p = my_map._find_nearest_points(cur)

			if direction == LEFT:
				print('LEFT')
				idx1 = 0
				while idx < len(list_of_p):
					if list_of_p[idx].x < cur.x:
						idx1 = idx
					idx = idx + 1

				idx = 0
				while idx < len(list_of_p):
					if idx != idx1:
						my_map.remove_way(cur, list_of_p[idx], list_of_p[idx1])
					idx = idx + 1

			elif direction == RIGHT:
				print('RIGHT')
				idx1 = 0
				while idx < len(list_of_p):
					if list_of_p[idx].x > cur.x:
						idx1 = idx
					idx = idx + 1

				idx = 0
				while idx < len(list_of_p):
					if idx != idx1:
						my_map.remove_way(cur, list_of_p[idx], list_of_p[idx1])
					idx = idx + 1

			elif direction == UP:
				print('UP')
				idx1 = 0
				while idx < len(list_of_p):
					if list_of_p[idx].y < cur.y:
						idx1 = idx
					idx = idx + 1

				idx = 0
				while idx < len(list_of_p):
					if idx != idx1:
						my_map.remove_way(cur, list_of_p[idx], list_of_p[idx1])
					idx = idx + 1

			elif direction == DOWN:
				print('DOWN')
				idx1 = 0
				while idx < len(list_of_p):
					if list_of_p[idx].y > cur.y:
						idx1 = idx
					idx = idx + 1

				idx = 0
				while idx < len(list_of_p):
					if idx != idx1:
						my_map.remove_way(cur, list_of_p[idx], list_of_p[idx1])
					idx = idx + 1

		elif type_of_res == RIGHT_ONLY and flag == None:
			print ("RESTRICTION: right_only")
			list_of_p = my_map._find_nearest_points(cur)

			if direction == LEFT:
				print('LEFT')
				while idx < len(list_of_p) and list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

			elif direction == RIGHT:
				print('RIGHT')
				while idx < len(list_of_p) and list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

			elif direction == UP:
				print('UP')
				while idx < len(list_of_p) and list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

			elif direction == DOWN:
				print('DOWN')
				while idx < len(list_of_p) and list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

		elif type_of_res == LEFT_ONLY  and flag == None:
			print ("RESTRICTION: left_only")
			list_of_p = my_map._find_nearest_points(cur)

			if direction == LEFT:
				print('LEFT')
				while idx < len(list_of_p) and list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

			elif direction == RIGHT:
				print('RIGHT')
				while idx < len(list_of_p) and list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

			elif direction == UP:
				print('UP')
				while idx < len(list_of_p) and list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):

					print(cur.x, cur.y, prev.x, prev.y, list_of_p[idx].x, list_of_p[idx].y)
					my_map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):

					print(cur.x, cur.y, prev.x, prev.y, list_of_p[idx].x, list_of_p[idx].y)
					my_map.remove_way(cur, prev, list_of_p[idx])

			elif direction == DOWN:
				print('DOWN')
				while idx < len(list_of_p) and list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) and list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					my_map.remove_way(cur, prev, list_of_p[idx])

		elif type_of_res == STRAIGHT_ONLY  and flag == None:
			print ("RESTRICTION: straight only")
			list_of_p = my_map._find_nearest_points(cur)

			if direction == LEFT:
				print('LEFT')
				while idx < len(list_of_p):
					if(list_of_p[idx].x == cur.x):
						my_map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1
				my_map.remove_way(cur, prev, prev)

			elif direction == RIGHT:
				print('RIGHT')
				while idx < len(list_of_p):
					if(list_of_p[idx].x == cur.x):
						my_map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1
				my_map.remove_way(cur, prev, prev)
			elif direction == UP:
				print('UP')
				while idx < len(list_of_p):
					if(list_of_p[idx].y == cur.y):
						my_map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1
				my_map.remove_way(cur, prev, prev)
			elif direction == DOWN:
				print('DOWN')
				while idx < len(list_of_p):
					if(list_of_p[idx].y == cur.y):
						my_map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1
				my_map.remove_way(cur, prev, prev)

		elif type_of_res == SEMAFORE_RED  and flag == None:
			#добавлено ограничение выхода по времени
			print ("RESTRICTION: semaphore")
			counter = 0
			while (list_of_res[4] == 1) and counter < 400:
				list_of_res = read_from_socket()
				sleep(0.1)
				counter = counter + 1

		type_of_res = -1

	if if_used == False:
		return 1

	return 0

def max(a1, a2):
	if a1 > a2:
		return a1
	else:
		return a2

def abs(a):
	if a < 0:
		return -a
	else:
		return a

def route(my_map, cur_dir):
	start = my_map.get_start_point()
	finish = my_map.get_finish_point()
	cur_way = my_map.get_way(start, finish)

	cur_dir = sys.argv[2] # <--- this is what a professionalism is

	if cur_dir == "LEFT":
		print "start: LEFT"
		cur_dir = LEFT
	elif cur_dir == "RIGHT":
		print "start: RIGHT"
		cur_dir = RIGHT
	elif cur_dir == "UP":
		print "start: UP"
		cur_dir = UP
	else:
		print "start: DOWN"
		cur_dir = DOWN


	cur_dir = turn(cur_way[1].x - cur_way[0].x, cur_way[1].y - cur_way[0].y, cur_dir)
	move(max(max(abs(cur_way[1].x - cur_way[0].x), abs(cur_way[1].y - cur_way[0].y)) - 1.5, 0))

	idx = 1
	prev_road_point = cur_way[0]
	while cur_way[idx] != finish:
		print "sleep 1 :"
		sleep(5)
		print "after sleep 1"


		if  not(check_restrictions(my_map, cur_way[idx], prev_road_point, cur_dir)):
			cur_way = my_map.get_way(cur_way[idx], finish, prev_road_point)
			idx = 0
		move_half_tile()
		move_1_tile()
		print (cur_way[idx].x, cur_way[idx].y)
		cur_dir = turn(cur_way[idx + 1].x - cur_way[idx].x, cur_way[idx + 1].y - cur_way[idx].y, cur_dir)

		counter_of_dirs = 0

		print "sleep 2:"
		sleep(5)
		print "after sleep 2"

		while not(check_restrictions(my_map, cur_way[idx], prev_road_point, cur_dir, 1)):

			cur_way = my_map.get_way(cur_way[idx], finish, prev_road_point)
			idx = 0
			new_dir = turn(cur_way[idx + 1].x - cur_way[idx].x, cur_way[idx + 1].y - cur_way[idx].y, cur_dir)
			if new_dir == cur_dir:
				counter_of_dirs = counter_of_dirs + 1

			if counter_of_dirs == 5:
				break
			cur_dir = new_dir

		move(max(max(abs(cur_way[idx + 1].x - cur_way[idx].x), abs(cur_way[idx + 1].y - cur_way[idx].y)) - 1.5, 0))
		prev_road_point = cur_way[idx]
		idx = idx + 1
	move_1_tile()

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "Waiting For Shmorgalka"
while GPIO.input(21) == 1:
	sleep(0.1)
print "Start"
sleep(5)
print "After 5..."
map_file = open(sys.argv[1], 'r')
chassis.init()
my_map = road_graph.mapBot(map_file)

route(my_map, RIGHT)