import cv2
import numpy as np
from matplotlib import pyplot as plt
import resource, sys
from time import sleep
resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))
sys.setrecursionlimit(10 ** 6)

BORDER_WIDTH_FACTOR_THRESHOLD = 0.15
THRESHOLD_HIGH = 256 * 3 - 128
THRESHOLD_LOW = 30
MINIMUM_AREA_FACTOR = 0.0001
DX = [-1, +1, 0, 0]
DY = [0, 0, -1, +1]
COLORING_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

class Node:
	def __init__(self, node_id, node_x, node_y):
		self.id = node_id
		self.x = node_x
		self.y = node_y
		self.adj = []
	def add_edge(self, node):
		self.adj.append(node.id)
	def __repr__(self):
		return "(" + str(self.id) + ", " + str(self.x) + ", " + str(self.y) + ", " + str(self.adj) + ")"

image = cv2.imread('map.jpg', cv2.IMREAD_COLOR)
height = len(image)
width = len(image[0])
mark = [[-1 for i in range(width)] for j in range(height)]
nodes = []
regions = [[] for i in range(width * height)]
regions_border = [[] for i in range(width * height)]
nodes_color = [-1 for i in range(width * height)]

def is_pixel_important(x, y):
	b, g, r = image[y][x]
	r = int(r)
	g = int(g)
	b = int(b)
	return r + g + b <= THRESHOLD_HIGH and r + g + b >= THRESHOLD_LOW

def find_graph_nodes():
	for y in range(height):
		for x in range(width):
			if mark[y][x] == -1 and is_pixel_important(x, y):
				color_area = get_color_area(x, y, len(nodes))
				if color_area >= MINIMUM_AREA_FACTOR * width * height:
					nodes.append(Node(len(nodes), x, y))

def is_inside(x, y):
	if x < 0 or x >= width or y < 0 or y >= height:
		return False
	return True

def is_on_border(x, y):
	if not is_pixel_important(x, y):
		return False
	for k in range(4):
		x2 = x + DX[k]
		y2 = y + DY[k]
		if is_inside(x2, y2) and not is_pixel_important(x2, y2):
			return True
	return False

def get_color_area(x, y, color):
	if not is_inside(x, y) or mark[y][x] != -1 or not is_pixel_important(x, y):
		return 0
	mark[y][x] = color
	color_area = 1
	regions[color].append((x, y))
	if is_on_border(x, y):
		regions_border[color].append((x, y))
	for k in range(4):
		x2 = x + DX[k]
		y2 = y + DY[k]
		if is_inside(x2, y2) and mark[y2][x2] == -1 and is_pixel_important(x2, y2):
			color_area += get_color_area(x2, y2, color)
	return color_area

def are_adjacent(node1, node2):
	start_x = node1.x
	start_y = node1.y
	end_x = node2.x
	end_y = node2.y
	min_distance = 10 ** 20
	for u in regions_border[mark[start_y][start_x]]:
		for v in regions_border[mark[end_y][end_x]]:
			tmp_distance = ((u[0] - v[0]) * (u[0] - v[0]) + (u[1] - v[1]) * (u[1] - v[1]))
			if tmp_distance < min_distance:
				min_distance = tmp_distance
				start_x = u[0] 
				start_y = u[1]
				end_x = v[0] 
				end_y = v[1]
	min_distance = min_distance ** 0.5
	dx = end_x - start_x
	dy = end_y - start_y
	total_steps = int(2 * ((width * width + height * height) ** 0.5))
	last_x = start_x
	last_y = start_y
	borders = 0
	for i in range(total_steps):
		x = int(start_x + i * dx / total_steps + 0.5)
		y = int(start_y + i * dy / total_steps + 0.5)
		if not is_pixel_important(x, y) and is_pixel_important(last_x, last_y):
			borders += 1
		last_x = x
		last_y = y
	border_width_threshold = BORDER_WIDTH_FACTOR_THRESHOLD * (width * width + height * height) ** 0.5
	if borders <= 1 and min_distance < border_width_threshold:
		return True
	return False

def add_edges():
	for i in range(len(nodes)):
		for j in range(len(nodes)):
			if j > i and are_adjacent(nodes[i], nodes[j]):
				nodes[i].add_edge(nodes[j])
				nodes[j].add_edge(nodes[i])

def change_region_color(node, pixel_color):
	global image
	region_idx = mark[node.y][node.x]
	for i in range(len(regions[region_idx])):
		x = regions[region_idx][i][0]
		y = regions[region_idx][i][1]
		image[y][x] = pixel_color

def colorize_map(index):
	if index == len(nodes):
		for i in range(len(nodes)):
			change_region_color(nodes[i], COLORING_COLORS[nodes_color[i]])
		cv2.imshow('Colorized Image', image)
		key = cv2.waitKey(50)
		if key == 27:
			cv2.destroyAllWindows()
			exit()
		return
	for i in range(4):
		valid = True
		for u in nodes[index].adj:
			if nodes_color[u] == i:
				valid = False
				break
		if valid:
			nodes_color[index] = i
			colorize_map(index + 1)
			nodes_color[index] = -1

find_graph_nodes()
add_edges()

cv2.imshow('Image', image)

colorize_map(0)

cv2.waitKey(0)
cv2.destroyAllWindows()
