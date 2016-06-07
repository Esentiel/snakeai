import sys
import logging
import math

from lib.a_star import AStar
from lib.flood_fill import count_room

ADDITIONAL_TAIL_ELEMENTS = 2 # head + tail
LOOPS_BEFORE_RISK_FACTOR = 3 # 3 loops for snake before start risking

def push_to_pipe(msg):
	sys.stdout.write(msg)
	sys.stdout.flush()


def safe_remove_from_list(theList, element):
	if element in theList:
		theList.remove(element)


def launch_a_star(nCols, nRows, walls, start, end):
	star = AStar()
	star.init_grid(nCols, nRows, walls, start, end)
	return star.solve()


def get_starting_info():
	params = {}
	params["rows"] = int(raw_input()[5:])
	params["cols"] = int(raw_input()[5:])
	params["time"] = int(raw_input()[5:])
	params["moves"] = int(raw_input()[6:])

	return [params["rows"], params["cols"]]


def reset_map(theMap, snake, walls, start, end):
	del theMap[:]
	del snake[:]
	del walls[:]
	del start[:]
	del end[:]


def get_map(nRows, nCols, theMap, snake, walls, start, end):
	reset_map(theMap, snake, walls, start, end)
	for i in xrange(nRows):
		theMap.append(raw_input())
		if len(theMap[-1]) != nCols:
			sys.exit(0)
		for j in xrange(nCols):
			if theMap[i][j] == '*':
				start.extend([i,j])
			elif theMap[i][j] == '$':
				end.extend([i,j])
			elif theMap[i][j] in ('^','<','>','v'):
				snake.append([i,j])
			elif theMap[i][j] == '#':
				walls.append([i,j])


def find_tail(theMap, snake):
	cell = []
	current_cell = snake[0]
	while True:
		cell = get_prev_cell(theMap, current_cell)
		if len(cell) == 0:
			break
		current_cell = cell

	return current_cell


def cut_tail(theMap, snake, cut_length):
	tail = find_tail(theMap, snake)
	for number in xrange(cut_length):
		new_tail = get_next_cell(theMap, tail)
		safe_remove_from_list(snake, [tail[0], tail[1]])
		tail = new_tail

	return tail


def get_prev_cell(theMap, cell):
	if cell[0] + 2 <= len(theMap):
		if theMap[cell[0] + 1][cell[1]] == '^':
			return [cell[0] + 1, cell[1]]
	if cell[1] + 2 <= len(theMap[0]):
		if theMap[cell[0]][cell[1] + 1] == '<':
			return [cell[0], cell[1] + 1]
	if cell[0] - 1 >= 0:
		if theMap[cell[0] - 1][cell[1]] == 'v':
			return [cell[0] - 1, cell[1]]
	if cell[1] - 1 >= 0:
		if theMap[cell[0]][cell[1] - 1] == '>':
			return [cell[0], cell[1] - 1]

	return []


def get_next_cell(theMap, cell):
	if theMap[cell[0]][cell[1]] == '>':
		return [cell[0], cell[1] + 1]
	elif theMap[cell[0]][cell[1]] == '<':
		return [cell[0], cell[1] - 1]
	elif theMap[cell[0]][cell[1]] == '^':
		return [cell[0] - 1, cell[1]]
	elif theMap[cell[0]][cell[1]] == 'v':
		return [cell[0] + 1, cell[1]]
	return []


def move(path, nRows, nCols, theMap, snake, walls, start, end):
	for idx in xrange(len(path)):
		if idx == 0:
			continue
		if path[idx][0] - path[idx-1][0] == 0:
			if path[idx][1] - path[idx-1][1] == 1:
				move = '>'
			else:
				move = '<'
		elif path[idx][1] - path[idx-1][1] == 0:
			if path[idx][0] - path[idx-1][0] == 1:
				move = 'v'
			else:
				move = '^'
		push_to_pipe(move)
		get_map(nRows, nCols, theMap, snake, walls, start, end)


def get_adjacent_cells(theMap, snake, head):
	prev_cell = get_prev_cell(theMap, head)
	adjacent_cells = []
	if theMap[prev_cell[0]][prev_cell[1]] == '>':
		adjacent_cells = [[head[0], head[1] + 1], [head[0] + 1, head[1]], [head[0] - 1, head[1]]]
	elif theMap[prev_cell[0]][prev_cell[1]] == '<':
		adjacent_cells = [[head[0], head[1] - 1], [head[0] + 1, head[1]], [head[0] - 1, head[1]]]
	elif theMap[prev_cell[0]][prev_cell[1]] == '^':
		adjacent_cells = [[head[0] - 1, head[1]], [head[0], head[1] + 1], [head[0], head[1] - 1]]
	elif theMap[prev_cell[0]][prev_cell[1]] == 'v':
		adjacent_cells = [[head[0] + 1, head[1]], [head[0], head[1] + 1], [head[0], head[1] - 1]]
	appropriate_adjacent_cells = []
	for cell in adjacent_cells:
		if (0 <= cell[0] <= len(theMap) - 1) and (0 <= cell[1] <= len(theMap[0]) - 1):
			if (theMap[cell[0]][cell[1]] == '.'):
				appropriate_adjacent_cells.append(cell)

	return appropriate_adjacent_cells


def stretch_snake(nRows, nCols, theMap, walls, snake,  start, end):
	tail = find_tail(theMap, snake)

	adjacent_cells = get_adjacent_cells(theMap, snake, start)
	max_distance_adj_cell_verified = []
	max_distance_to_food_verified = 0
	
	safe_remove_from_list(snake, tail)
	if start not in snake:
		snake.append(start)

	for cell in adjacent_cells:
		path_to_tail = launch_a_star(nCols, nRows, walls + snake, cell, tail)

		if path_to_tail:
			distance_to_food = math.sqrt(pow(cell[0] - end[0], 2) + pow(cell[1] - end[1], 2))
			if distance_to_food >= max_distance_to_food_verified:
				max_distance_adj_cell_verified = cell
				max_distance_to_food_verified = distance_to_food
	# check if it's possible to move one cell ahead
	if len(max_distance_adj_cell_verified) > 0:
		path = [start, max_distance_adj_cell_verified]
		move(path, nRows, nCols, theMap, snake, walls, start, max_distance_adj_cell_verified)
	else:
		path_to_tail = launch_a_star(nCols, nRows, walls + snake, start, tail)
		if path_to_tail:
			move(path_to_tail, nRows, nCols, theMap, snake, walls, start, tail)
		else:
			# risk branch: when it's not possible to reach the tail
			path_to_food = launch_a_star(nCols, nRows, walls + snake, start, end)
			while not path_to_food:
				adjacent_cells = get_adjacent_cells(theMap, snake, start)
				max_room_verified = []
				max_room = 0

				for cell in adjacent_cells:
					room = count_room(theMap, cell)
					if room >= max_room:
						max_room_verified = cell
						max_room = room

				path = [start, max_room_verified]
				move(path, nRows, nCols, theMap, snake, walls, start, max_room_verified)

				tail = find_tail(theMap, snake)
				safe_remove_from_list(snake, tail)
				path_to_food = launch_a_star(nCols, nRows, walls + snake, start, end)


def main():
	logging.basicConfig(filename='ai.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

	params = get_starting_info()
	nRows = params[0]
	nCols = params[1]

	push_to_pipe("Ok\n")

	theMap = []
	snake = []
	walls = []
	start = []
	end = []
	tail = []
	cells_sum = 0
	moves_wo_food = 0
	old_snake_len = len(snake) + ADDITIONAL_TAIL_ELEMENTS
	
	get_map(nRows, nCols, theMap, snake, walls, start, end)
	cells_sum = (len(snake)+ ADDITIONAL_TAIL_ELEMENTS ) * LOOPS_BEFORE_RISK_FACTOR

	while True:
		# check is it time to risk
		if len(snake) + ADDITIONAL_TAIL_ELEMENTS == old_snake_len:
			moves_wo_food += 1
		else:
			cells_sum = (len(snake) + ADDITIONAL_TAIL_ELEMENTS) * LOOPS_BEFORE_RISK_FACTOR
			moves_wo_food = 0
			old_snake_len = len(snake) + ADDITIONAL_TAIL_ELEMENTS

		path = launch_a_star(nCols, nRows, walls + snake, start, end)

		# risk
		if moves_wo_food > cells_sum:
			if path:
				move(path, nRows, nCols, theMap, snake, walls, start, end)
				moves_wo_food = 0		
				continue

		if path:
			len_snake = len(snake) + ADDITIONAL_TAIL_ELEMENTS
			len_path = len(path)

			if len_snake <= len_path:
				new_snake = path[len_path - len_snake:]
				new_tail = new_snake[0]
			else:
				new_snake = snake[:]
				new_tail = cut_tail(theMap, new_snake, len_path - ADDITIONAL_TAIL_ELEMENTS)
				new_snake += path
			safe_remove_from_list(new_snake, new_tail)

			path_to_tail = launch_a_star(nCols, nRows, walls + new_snake, end, new_tail)
			# is it possible to reach the tail after a food was eaten
			if path_to_tail:
				move(path, nRows, nCols, theMap, snake, walls, start, end)
			else:
				stretch_snake(nRows, nCols, theMap, walls, snake,  start, end)
		else:
			stretch_snake(nRows, nCols, theMap, walls, snake, start, end)


if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		logging.error(str(e))
		sys.exit(1)