import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt

try:
	MAP_IMAGE_PATH = sys.argv[1]
except IndexError:
	print("Error: please specify an image.")
	exit(0)
ESCAPE_KEY_CHARACTER = 27
NO_COLOR = -1
NOT_MARKED = -1
BACKGROUND_MARK = -2
SLEEP_TIME_IN_MILLISECONDS = 100
MINIMUM_BORDER_WIDTH_RATIO = 0.15
IMPORTANT_COLOR_HIGH_THRESHOLD = 256 - 35
IMPORTANT_COLOR_LOW_THRESHOLD = 35
MINIMUM_REGION_AREA_RATIO = 0.0005
MAXIMUM_NEIGHBOR_PIXEL_COLOR_DIFFERENCE = 50
INF = 10 ** 30
MAXIMUM_NUMBER_OF_REGIONS = 1000
COLORING_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
DX = [-1, +1, 0, 0]
DY = [0, 0, -1, +1]
SHARPEN_KERNEL = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
MAXIMUM_IMAGE_WIDTH = 1000
MAXIMUM_IMAGE_HEIGHT = 1000

image = cv2.imread(MAP_IMAGE_PATH, cv2.IMREAD_COLOR)
height = len(image)
width = len(image[0])
if width > MAXIMUM_IMAGE_WIDTH or height > MAXIMUM_IMAGE_HEIGHT:
	print("Error: please specify an image with smaller dimensions.")
	exit(0)
total_area = width * height
mark = [[NOT_MARKED for i in range(width)] for j in range(height)]
nodes = []
regions = [[] for i in range(MAXIMUM_NUMBER_OF_REGIONS)]
regions_border = [[] for i in range(MAXIMUM_NUMBER_OF_REGIONS)]
nodes_color = [NO_COLOR for i in range(MAXIMUM_NUMBER_OF_REGIONS)]

class Node:
	def __init__(self, node_id, node_x, node_y):
		self.id = node_id
		self.x = node_x
		self.y = node_y
		self.adj = []
	def add_edge(self, node):
		self.adj.append(node.id)

def apply_threshold():
	for y in range(height):
		for x in range(width):
			b, g, r = image[y][x]
			r, g, b = int(r), int(g), int(b)
			if r + g + b < IMPORTANT_COLOR_LOW_THRESHOLD * 3:
				image[y][x] = (255, 255, 255)
				mark[y][x] = BACKGROUND_MARK
			if r + g + b > IMPORTANT_COLOR_HIGH_THRESHOLD * 3:
				image[y][x] = (255, 255, 255)
				mark[y][x] = BACKGROUND_MARK

def whiten_background():
	for y in range(height):
		for x in range(width):
			if mark[y][x] == NOT_MARKED or mark[y][x] == BACKGROUND_MARK:
				image[y][x] = (255, 255, 255)

def get_all_regions_pixels():
	for y in range(height):
		for x in range(width):
			region_mark = mark[y][x]
			regions[region_mark].append((x, y))
			if is_on_border(x, y):
				regions_border[region_mark].append((x, y))

def find_graph_nodes():
	for y in range(height):
		for x in range(width):
			if mark[y][x] == NOT_MARKED:
				color_area = get_region_area(x, y, NOT_MARKED, len(nodes))
				if color_area > MINIMUM_REGION_AREA_RATIO * total_area:
					nodes.append(Node(len(nodes), x, y))
				else:
					get_region_area(x, y, len(nodes), NOT_MARKED)
	get_all_regions_pixels()

def is_inside(x, y):
	if x < 0 or x >= width or y < 0 or y >= height:
		return False
	return True

def is_on_border(x, y):
	if mark[y][x] == BACKGROUND_MARK:
		return False
	for k in range(4):
		x2 = x + DX[k]
		y2 = y + DY[k]
		if is_inside(x2, y2) and mark[y2][x2] == BACKGROUND_MARK:
			return True
	return False

def same_pixel_colors(x1, y1, x2, y2):
	if not is_inside(x1, y1) or not is_inside(x2, y2):
		return False
	b1, g1, r1 = image[y1][x1]
	b2, g2, r2 = image[y2][x2]
	r1, g1, b1 = int(r1), int(g1), int(b1)
	r2, g2, b2 = int(r2), int(g2), int(b2)
	diff = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
	return diff <= 3 * MAXIMUM_NEIGHBOR_PIXEL_COLOR_DIFFERENCE

def get_region_area(start_x, start_y, src_mark, dst_mark):
	if not is_inside(start_x, start_y) or mark[start_y][start_x] != src_mark:
		return 0
	color_area = 0
	queue = [(start_x, start_y)]
	mark[start_y][start_x] = dst_mark
	while queue:
		x, y = queue.pop(0)
		mark[y][x] = dst_mark
		color_area += 1
		for k in range(4):
			x2 = x + DX[k]
			y2 = y + DY[k]
			if is_inside(x2, y2) and mark[y2][x2] == src_mark and same_pixel_colors(x, y, x2, y2):
				mark[y2][x2] = dst_mark
				queue.append((x2, y2))
	return color_area

def are_adjacent(node1:Node, node2:Node):
	start_x, start_y = node1.x, node1.y
	end_x, end_y = node2.x, node2.y
	min_distance_sqr = INF
	for u in regions_border[mark[start_y][start_x]]:
		for v in regions_border[mark[end_y][end_x]]:
			tmp_distance_sqr = (u[0] - v[0]) * (u[0] - v[0]) + (u[1] - v[1]) * (u[1] - v[1])
			if tmp_distance_sqr < min_distance_sqr:
				min_distance_sqr = tmp_distance_sqr
				start_x, start_y = u[0], u[1] 
				end_x, end_y = v[0], v[1] 
	dx, dy = end_x - start_x, end_y - start_y
	if abs(dx) + abs(dy) <= 1:
		return True
	dx, dy = float(dx), float(dy)
	border_width_threshold = MINIMUM_BORDER_WIDTH_RATIO * (width * width + height * height)
	if min_distance_sqr >= border_width_threshold:
		return False
	total_steps = int(2 * ((width * width + height * height) ** 0.5))
	for i in range(total_steps):
		x = int(start_x + i * dx / total_steps + 0.5)
		y = int(start_y + i * dy / total_steps + 0.5)
		if mark[y][x] >= 0 and (x != start_x or y != start_y) and (x != end_x or y != end_y):
			return False
	return True

def add_graph_edges():
	for i in range(len(nodes)):
		for j in range(len(nodes)):
			if j > i and are_adjacent(nodes[i], nodes[j]):
				nodes[i].add_edge(nodes[j])
				nodes[j].add_edge(nodes[i])

def change_region_color(node:Node, pixel_color):
	region_idx = mark[node.y][node.x]
	for i in range(len(regions[region_idx])):
		x = regions[region_idx][i][0]
		y = regions[region_idx][i][1]
		image[y][x] = pixel_color

def colorize_map(node_index):
	if node_index == len(nodes):
		for i in range(len(nodes)):
			change_region_color(nodes[i], COLORING_COLORS[nodes_color[i]])
		cv2.imshow('Colorized Map', image)
		key = cv2.waitKey(SLEEP_TIME_IN_MILLISECONDS)
		if key == ESCAPE_KEY_CHARACTER:
			cv2.destroyAllWindows()
			exit()
		return
	for i in range(len(COLORING_COLORS)):
		is_color_valid = True
		for u in nodes[node_index].adj:
			if nodes_color[u] == i:
				is_color_valid = False
				break
		if is_color_valid:
			nodes_color[node_index] = i
			colorize_map(node_index + 1)
			nodes_color[node_index] = NO_COLOR

# cv2.imshow('Original Map', image)

print('Please wait for preprocessing...')

apply_threshold()
image = cv2.medianBlur(image, 3)
apply_threshold()
image = cv2.filter2D(image, -1, SHARPEN_KERNEL)
apply_threshold()

find_graph_nodes()
add_graph_edges()

whiten_background()

print('Preprocessing finished.')

# cv2.imshow('Modified Map', image)

colorize_map(0)

cv2.waitKey(0)
cv2.destroyAllWindows()
