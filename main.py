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
import matplotlib.pyplot as plt

class robot:
	def __init__(self, ):
		self.v_direction = coords()


class mapBot:
	def __init__(self, map_file):
		self._robo_map = []
		self._start_finish_points = []
		self._road_points = []
		#для обращения к нодам по графам
		self._reverse_set = []
		self._nodes_counter = 0
		#складываем все в массив массивов
		for x in map_file.readlines():
			b = x.replace('\n', '')
			self._robo_map.append(list(b))

		#print self._robo_map

		self._way_graph = nx.DiGraph()
		#_way_graph.add_node()

	def _create_road_graph(self):
		self._way_graph_labels = {}
		for i, x in enumerate(self._road_points):
			#print "new x: %d %d" % (x.y, x.x)
			neighbors = self._find_nearest_points(x)

			"""self._way_graph.add_node(self._nodes_counter)
			self._nodes_counter = self._nodes_counter + 1
			if self._nodes_counter > 3:
				self._way_graph.add_edge(self._nodes_counter - 2, self._nodes_counter - 1)"""
			for w in neighbors:
				#узел начала
				#print self._road_points[i]

				self._road_points[i].add_output_node(self._nodes_counter, self._road_points.index(w))
				self._reverse_set.append(i)
				self._way_graph.add_node(self._nodes_counter)
				self._way_graph_labels[self._nodes_counter] = str(self._nodes_counter) + "(" + str(x.y) + " " + str(x.x) + ")"
				self._nodes_counter = self._nodes_counter + 1

				#узел соответсвующий концу
				self._road_points[self._road_points.index(w)].add_input_node(self._nodes_counter, i)
				self._reverse_set.append(self._road_points.index(w))
				self._way_graph.add_node(self._nodes_counter)
				self._way_graph_labels[self._nodes_counter] = str(self._nodes_counter)  + "(" + str(w.y) + " " + str(w.x) + ")"
				self._nodes_counter = self._nodes_counter + 1

				#строим дугу
				self._way_graph.add_edge(self._nodes_counter - 2, self._nodes_counter - 1)

			#if self._nodes_counter > 100:
			#	break

		for b in self._road_points:
			for i in b.corresponding_nodes_input:
				for j in b.corresponding_nodes_output:
					self._way_graph.add_edge(i[0], j[0])

	def find_shortest_way(self, source, destination):
		if (source in self._road_points) == False:
			print "ERROR: no source point in _road_points"
			return None

		if (destination in self._road_points) == False:
			print "ERROR: no destination point in _road_points"
			return None

		#добавление стартового узла
		self._way_graph.add_node(self._nodes_counter)

		for x in source.corresponding_nodes_output:
			self._way_graph.add_edge(self._nodes_counter, x[0])
		self._nodes_counter = self._nodes_counter + 1
		#добавление конечного узла
		self._way_graph.add_node(self._nodes_counter)

		for x in destination.corresponding_nodes_input:
			self._way_graph.add_edge(x[0], self._nodes_counter)

		self._nodes_counter = self._nodes_counter + 1

		path = nx.shortest_path(self._way_graph, self._nodes_counter - 2, self._nodes_counter - 1)
		print "path by :"
		print path

		path.pop(0)
		path.pop(len(path) - 1)

		#не забываем удалить вершины
		self._nodes_counter = self._nodes_counter - 1
		self._way_graph.remove_node(self._nodes_counter)
		self._nodes_counter = self._nodes_counter - 1
		self._way_graph.remove_node(self._nodes_counter)

		print path
		self.print_path(path)

		real_path = []
		last = None
		#получаем путь по вершинам реальным
		for x in path:
			if last == None:
				last = self._reverse_set[x]
				real_path.append(self._road_points(self._reverse_set[x]))
			elif last != self._reverse_set[x]:
				real_path.append(self._road_points(self._reverse_set[x]))
				last = self._reverse_set[x]

		print "real_path:"
		print real_path

		return real_path

	def remove_way(self, cur_point, from_source_point, to_dest_point):
		if (cur_point in self._road_points) == False:
			print "ERROR: no cur_point in self._road_points"

		if (from_source_point in self._road_points) == False:
			print "ERROR: no from_source_point in self._road_points"

		if (to_dest_point in self._road_points) == False:
			print "ERROR: no to_dest_point in self._road_points"

		from_index = self._road_points.index(from_source_point)
		to_index = self._road_points.index(to_dest_point)

		from_node = None
		to_node = None

		for x in cur_point.corresponding_nodes_input:
			if x[1] == from_index:
				from_node = x[0]
				break

		for x in cur_point.corresponding_nodes_output:
			if x[1] == from_index:
				to_node = x[0]
				break

		self._way_graph.remove_edge((from_node, to_node))

	def find_test_path(self):
		self.find_shortest_way(self._road_points[0], self._road_points[6])
	def _is_pass(self, coord):
		if self._robo_map[coord.y][coord.x] == ' ':
			return True

		if self._robo_map[coord.y][coord.x] == 'X':
			return True

		return False

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
					self._start_finish_points.append(road_point(coords(y_point, x_point), START_POINT))
					print "Find Start"
				if self._is_end(coords(y_point, x_point)) == True:
					self._start_finish_points.append(road_point(coords(y_point, x_point), FINISH_POINT))
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

		for x in self._start_finish_points:
			flag = True
			for w in self._road_points:
				if x.x == w.x and x.y == w.y:
					print "find the same road_point"
					flag = False
					#то есть точка старта финиша совпавдает с какой-то точкой на карте

			if flag == True:
				self._road_points.append(x)




	def _find_nearest_points(self, point):
		#up и left в верхнем левом угле
		point_x = point.x
		point_y = point.y

		#print "Vertical List"
		vertical_list = [x for x in self._road_points if x.x == point_x]
		#self.print_road_points(vertical_list)

		#print "Horizontal List"
		horizontal_list = [x for x in self._road_points if x.y == point_y]
		#self.print_road_points(horizontal_list)

		nearest_down = point
		nearest_up = point

		nearest_left = point
		nearest_right = point

		#ищем по вертикали
		for x in vertical_list:
			if x.y == point_y:
				continue

			if x.y > point_y and self._is_pass(coords(point_y + 1, point_x)):
				if nearest_down.y == point_y:
					nearest_down = x
				elif x.y - point_y < nearest_down.y - point_y:
					nearest_down = x
			elif x.y < point_y and self._is_pass(coords(point_y - 1, point_x)):
				if nearest_up.y == point_y:
					nearest_up = x
				elif point_y - x.y < point_y - nearest_down.y:
					nearest_up = x

		#ищем по горизонтали
		for x in horizontal_list:
			if x.x == point_x:
				continue

			if x.x > point_x and self._is_pass(coords(point_y, point_x + 1)):
				if nearest_right.x == point_x:
					nearest_right = x
				elif x.x - point_x < nearest_right.x - point_x:
					nearest_right = x


			elif x.x  < point_x and self._is_pass(coords(point_y, point_x - 1)):
				if nearest_left.x == point_x:
					nearest_left = x
				elif point_x - x.x < point_x - nearest_left.x:
					nearest_left = x

		"""print "nearest_up:"
		self.print_road_points([nearest_up])
		print '\n'
		print "nearest_down:"
		self.print_road_points([nearest_down])
		print '\n'
		print "nearest_left:"
		self.print_road_points([nearest_left])
		print '\n'
		print "nearest_right:"
		self.print_road_points([nearest_right])
		print '\n'"""

		res = []

		if nearest_up != point:
			res.append(nearest_up)
		if nearest_down != point:
			res.append(nearest_down)
		if nearest_left != point:
			res.append(nearest_left)
		if nearest_right != point:
			res.append(nearest_right)

		#print res
		return res




	def print_start_finish_points(self):
		self.print_road_points(self._start_finish_points)

	def print_road_points(self, points_array = None):
		if points_array == None:
			points_array = self._road_points
		for i, x in enumerate(points_array):
			print "--------------------"
			print "number: %d" % (i)
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
			print x.y
			print x.x

	def draw_road_points(self):
		for x in self._road_points:
			self._robo_map[x.y][x.x] = 'X'

	#for ivan
	def get_road_points(self):
		return self._road_points

	def get_way(self, source, dest):
		return self.find_shortest_way(source, dest)
	def print_map(self):
		for x in self._robo_map:
			for a in x:
				sys.stdout.write(a)
			sys.stdout.write('\n')

	def print_path(self, path):
		for x in path:
			print "node: %d coords: %d %d" % (x, self._road_points[self._reverse_set[x]].y, self._road_points[self._reverse_set[x]].x)

	def draw_graph(self):
		pos=nx.spring_layout(self._way_graph,iterations=20)
		#pos = nx.circular_layout(self._way_graph)
		nx.draw(self._way_graph,pos,  node_size = 1000, labels = self._way_graph_labels, k = 0.2, nodecolor='r',edge_color='b')
		#nx.draw(self._way_graph,pos,  node_size = 10, k = 0.01, nodecolor='r',edge_color='b')
		#nx.draw(self._way_graph)
		#plt.savefig("roads.png")
		plt.show()

	def print_matrix(self):
		A = nx.adjacency_matrix(self._way_graph)
		#print(A.toarray())
		#for
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
		self.corresponding_nodes_input = []
		self.corresponding_nodes_output = []

	def add_output_node(self, node, end_road_point):
		self.corresponding_nodes_output.append([node, end_road_point])

	def add_input_node(self, node, from_road_point):
		self.corresponding_nodes_input.append(node, from_road_point)


map_file = open(sys.argv[1], 'r')

my_map = mapBot(map_file)
my_map.print_map()

my_map._create_road_points()
my_map.print_road_points()
my_map.draw_road_points()

print "Start and Finish"

my_map.print_start_finish_points()
my_map.print_map()

#my_map._find_nearest_points(road_point(coords(1, 1), X_CROSSROAD))
my_map._create_road_graph()
#my_map.draw_graph()
my_map.find_test_path()
#print my_map._is_corner(coords(1, 1))
#print my_map._is_corner(coords(25, 24))
