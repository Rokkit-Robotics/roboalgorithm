#!/usr/bin/python
# -*- coding: utf-8 -*-

X_CROSSROAD = 1
T_CROSSROAD = 2
ROAD_CORNER = 3
END_ROAD = 4
START_POINT = 5
FINISH_POINT = 6
import sys
import networkx as nx

class mapBot:
	_robo_map = []
	_road_points = []
	def __init__(self, map_file):
		#складываем все в массив массивов
		for x in map_file.readlines():
			b = x.replace('\n', '')
			self._robo_map.append(list(b))

		print self._robo_map

	#Поиск X-перекрестков
	def _is_X_cross_road(self, coord):
		x_point = coord.x
		y_point = coord.y

		if self._robo_map[y_point][x_point] != ' ':
			return False
		if (self._robo_map[y_point][x_point - 1] == ' ') and \
		   (self._robo_map[y_point][x_point + 1] == ' ') and \
		   (self._robo_map[y_point - 1][x_point] == ' ') and \
		   (self._robo_map[y_point + 1][x_point] == ' '):

		   return True
		else:
			return False

	#Поиск T-перекрестков
	def _is_T_cross_road(self, coord):
		x_point = coord.x
		y_point = coord.y

		if self._robo_map[y_point][x_point] != ' ':
			return False

		counter = 0
		if self._robo_map[y_point][x_point - 1] == ' ':
			counter = counter + 1
		if self._robo_map[y_point][x_point + 1] == ' ':
			counter = counter + 1
		if self._robo_map[y_point - 1][x_point] == ' ':
			counter = counter + 1
		if self._robo_map[y_point + 1][x_point] == ' ':
			counter = counter + 1

		if counter == 3:
		   return True
		else:
			return False

	#поиск тупиков
	def _is_end_road(self, coord):
		x_point = coord.x
		y_point = coord.y

		if self._robo_map[y_point][x_point] != ' ':
			return False

		counter = 0
		if self._robo_map[y_point][x_point - 1] == ' ':
			counter = counter + 1
		if self._robo_map[y_point][x_point + 1] == ' ':
			counter = counter + 1
		if self._robo_map[y_point - 1][x_point] == ' ':
			counter = counter + 1
		if self._robo_map[y_point + 1][x_point] == ' ':
			counter = counter + 1

		if counter == 1:
		   return True
		else:
			return False

	#поиск углов (работает при условии, что не X или T - перекресток)
	def _is_corner(self, coord):
		x_point = coord.x
		y_point = coord.y

		if self._robo_map[y_point][x_point] != ' ':
			return False

		if self._robo_map[y_point][x_point - 1] == ' ' and \
		   self._robo_map[y_point][x_point + 1] == ' ':

		   return False

		if self._robo_map[y_point + 1][x_point] == ' ' and \
		   self._robo_map[y_point - 1][x_point] == ' ':

		   return False

		return True

	def _is_start(self, coord):
		x_point = coord.x
		y_point = coord.y

		if self._robo_map[y_point][x_point] == 's':
			self._robo_map[y_point][x_point] = ' '
			return True

		return False

	def _is_end(self, coord):
		x_point = coord.x
		y_point = coord.y

		if self._robo_map[y_point][x_point] == 'e':
			self._robo_map[y_point][x_point] = ' '
			return True

		return False

	def _create_road_points(self):
		#начинать именно с 1, 1

		#убираем метки старта и окончания
		for y_point in range(1, len(self._robo_map) - 1):
			for x_point in range(1, len(self._robo_map[y_point]) - 1):
				if self._is_start(coords(y_point, x_point)) == True:
					self._road_points.append(road_point(coords(y_point, x_point), START_POINT))
					print "Find Start"
				if self._is_end(coords(y_point, x_point)) == True:
					self._road_points.append(road_point(coords(y_point, x_point), FINISH_POINT))
					print "Find End"

		#начинать именно с 1, 1

		for y_point in range(1, len(self._robo_map) - 1):
			for x_point in range(1, len(self._robo_map[y_point]) - 1):

				if self._is_X_cross_road(coords(y_point, x_point)) == True:
					self._road_points.append(road_point(coords(y_point, x_point), X_CROSSROAD))
				elif self._is_T_cross_road(coords(y_point, x_point)) == True:
					self._road_points.append(road_point(coords(y_point, x_point), T_CROSSROAD))
				elif self._is_end_road(coords(y_point, x_point)) == True:
					self._road_points.append(road_point(coords(y_point, x_point), END_ROAD))
				elif self._is_corner(coords(y_point, x_point)) == True:
					self._road_points.append(road_point(coords(y_point, x_point), ROAD_CORNER))
				else:
					pass


	def print_road_points(self):
		for x in self._road_points:
			print "--------------------"
			if x.type == X_CROSSROAD:
				print "X_CROSSROAD"
			elif x.type == T_CROSSROAD:
				print "T_CROSSROAD"
			elif x.type == ROAD_CORNER:
				print "ROAD_CORNER"
			elif x.type == START_POINT:
				print "START_POINT"
			elif x.type == FINISH_POINT:
				print "FINISH_POINT"
			else:
				print "END_ROAD"
			print x.x
			print x.y

	def road_points_draw(self):
		for x in self._road_points:
			self._robo_map[x.y][x.x] = 'X'

	def print_map(self):
		for x in self._robo_map:
			for a in x:
				sys.stdout.write(a)
			sys.stdout.write('\n')

#первая координата по y
class coords:
	def __init__(self, y, x):
		self.x = x;
		self.y = y;

class road_point:
	def __init__(self, coord, type):
		self.x = coord.x
		self.y = coord.y
		self.type = type


map_file = open(sys.argv[1], 'r')

my_map = mapBot(map_file)
my_map.print_map()

my_map._create_road_points()
my_map.print_road_points()
my_map.road_points_draw()
my_map.print_map()
#print my_map._is_corner(coords(1, 1))
#print my_map._is_corner(coords(25, 24))
#way_graph = nx.DiGraph()
#way_graph.add
