import MapBot from main.py
import sys
from time import sleep

# class route:
SPEED = 1024
ANGLE_LEFT = -90
ANGLE_RIGHT = 90
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
SEMAFORE = 4

TILE_SIZE = 1000

def tiles(amount):
	return amount * TILE_SIZE

#crutch №1
def move_1_tile():
	chassis.move(SPEED, TILE_SIZE)

def move(distance):
	chassis.move(SPEED, distance * TILE_SIZE)

#use for road points in algorithm, this function moves robot -1 tile from the set distance
def make_a_move(x_dif, y_dif, cur_dir):
	#case : LEFT
	if x_dif < 0:
		if cur_dir == RIGHT:
			chassis.turn(SPEED, REVERSE)
		elif cur_dir == UP:
			chassis.turn(SPEED, ANGLE_LEFT)
		elif cur_dir == DOWN:
			chassis.turn(SPEED, ANGLE_RIGHT)
		return LEFT
	#case: RIGHT
	elif x_dif > 0:
		if cur_dir == LEFT:
			chassis.turn(SPEED, REVERSE)
		elif cur_dir == UP:
			chassis.turn(SPEED, ANGLE_RIGHT)
		elif cur_dir == DOWN:
			chassis.turn(SPEED, ANGLE_LEFT)
		return RIGHT
	#case: UP
	if y_dif < 0:
		if cur_dir == LEFT:
			chassis.turn(SPEED, ANGLE_RIGHT)
		elif cur_dir == RIGHT:
			chassis.turn(SPEED, ANGLE_LEFT)
		elif cur_dir == DOWN:
			chassis.turn(SPEED, REVERSE)
		return UP
	#case: DOWN
	if y_dif > 0:
		if cur_dir == LEFT:
			chassis.turn(SPEED, ANGLE_LEFT)
		elif cur_dir == RIGHT:
			chassis.turn(SPEED, ANGLE_RIGHT)
		elif cur_dir == UP:
			chassis.turn(SPEED, REVERSE)
		return DOWN

	while chassis.is_busy():
		pass

#is it guaranteed that list_of_res contains all restrictions by the time of its invokation
def check_restrictions(map, cur, prev, direction):
	list_of_res = read_from_socket()

	idx = 0

	for i, x in enumerate(list_of_res):
		if x == 1:
			type_of_res = i

		if type_of_res == STOP:
			list_of_p = map._find_nearest_points(cur)

			if direction == LEFT:
				while !(list_of_p[idx].x - cur.x < 0):
					idx = idx + 1

			elif direction == RIGHT:
				while !(list_of_p[idx].x - cur.x > 0):
					idx = idx + 1

			elif direction == UP:
				while !(list_of_p[idx].y - cur.y < 0):
					idx = idx + 1

			elif direction == DOWN:
				while !(list_of_p[idx].y - cur.y > 0):
					idx = idx + 1
			map.remove_way(cur, prev, list_of_p[idx])

		elif type_of_res == RIGHT_ONLY:
			list_of_p = map._find_nearest_points(cur)

			if direction == LEFT:
				while idx < len(list_of_p) && list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

			elif direction == RIGHT:
				while idx < len(list_of_p) && list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

			elif direction == UP:
				while idx < len(list_of_p) && list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

			elif direction == DOWN:
				while idx < len(list_of_p) && list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

		elif type_of_res == LEFT_ONLY:
			list_of_p = map._find_nearest_points(cur)

			if direction == LEFT:
				while idx < len(list_of_p) && list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

			elif direction == RIGHT:
				while idx < len(list_of_p) && list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

			elif direction == UP:
				while idx < len(list_of_p) && list_of_p[idx].x <= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y >= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

			elif direction == DOWN:
				while idx < len(list_of_p) && list_of_p[idx].x >= cur.x:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])
				idx = 0
				while idx < len(list_of_p) && list_of_p[idx].y <= cur.y:
					idx = idx + 1
				if(idx != len(list_of_p)):
					map.remove_way(cur, prev, list_of_p[idx])

		elif type_of_res == STRAIGHT_ONLY:
			list_of_p = map._find_nearest_points(cur)

			if direction == LEFT:
				while idx < len(list_of_p):
					if(list_of_p[idx].y == cur.y):
						map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1

			elif direction == RIGHT:
				while idx < len(list_of_p):
					if(list_of_p[idx].y == cur.y):
						map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1

			elif direction == UP:
				while idx < len(list_of_p):
					if(list_of_p[idx].x == cur.x):
						map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1

			elif direction == DOWN:
				while idx < len(list_of_p):
					if(list_of_p[idx].x == cur.x):
						map.remove_way(cur, prev, list_of_p[idx])
					idx = idx + 1

		elif type_of_res == SEMAFORE_RED:
			while(list_of_res[4] == 1):
				list_of_res = read_from_socket()
				sleep(0.01)


def route(map, direction):
	start = map.get_start_point()
	finish = map.get_finish_point()
	cur_way = map.get_way(start, finish)
	direction = make_a_move(cur_way[1].x - cur_way[0].x, cur_way[1].y - cur_way[0].y, direction)
	idx = 1
	check_restrictions(map, cur_way[1], cur_way[0], cur_dir)
	cur_way = map.get_way(cur_way[1])
	#check the comparison if it works as intended
	while cur_way[idx] != finish:
		restriction = is_restricted()
		if restriction:
			if restriction == STOP


map_file = open(sys.argv[1], 'r')

my_map = mapBot(map_file)
directions = []
cur_dir = None
if x1 - x3 > 0:
	cur_dir = DOWN
elif x1 - x3 < 0:
	cur_dir = UP

if y1 - y3 > 0:
	cur_dir = RIGHT
elif y1 - y3 < 0:
	cur_dir = LEFT

turns = []

dot_list = my_map.get_way(sys.argv[1], sys.argv[2], sys.argv[3])
for i in range(len(dot_list) - 1):
	# assume that coordinate system is directed south-east
	if dot_list[i+1].x - dot_list[i].x > 0:
		directions.append(DOWN)
	elif dot_list[i+1].x - dot_list[i].x < 0:
		directions.append(UP)

	if dot_list[i+1].y - dot_list[i].y > 0:
		directions.append(RIGHT)
	elif dot_list[i+1].y - dot_list[i].y < 0:
		directions.append(LEFT)


