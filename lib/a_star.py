import heapq

class Cell(object):
	def __init__(self, x, y, reachable):
		self.reachable = reachable
		self.x = x
		self.y = y
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0


class AStar(object):
	def __init__(self):
		self.opened = []
		heapq.heapify(self.opened)
		self.closed = set()
		self.cells = []
		self.grid_height = None
		self.grid_width = None

	def init_grid(self, width, height, walls, start, end):
		self.grid_height = height
		self.grid_width = width
		for x in range(self.grid_height):
			for y in range(self.grid_width):
				if [x, y] in walls:
					reachable = False
				else:
					reachable = True
				self.cells.append(Cell(x, y, reachable))
		self.start = self.get_cell(*start)
		self.end = self.get_cell(*end)

	def get_heuristic(self, cell):
		return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

	def get_cell(self, x, y):
		return self.cells[x * self.grid_width + y]

	def get_adjacent_cells(self, cell):
		cells = []
		if cell.x < self.grid_height-1:
			cells.append(self.get_cell(cell.x+1, cell.y))
		if cell.y > 0:
			cells.append(self.get_cell(cell.x, cell.y-1))
		if cell.x > 0:
			cells.append(self.get_cell(cell.x-1, cell.y))
		if cell.y < self.grid_width-1:
			cells.append(self.get_cell(cell.x, cell.y+1))
		return cells

	def get_path(self):
		cell = self.end
		path = [[cell.x, cell.y]]
		while cell.parent is not self.start:
			cell = cell.parent
			path.append([cell.x, cell.y])
		path.append([self.start.x, self.start.y])
		path.reverse()
		return path

	def update_cell(self, adj, cell):
		adj.g = cell.g + 10
		adj.h = self.get_heuristic(adj)
		adj.parent = cell
		adj.f = adj.h + adj.g

	def solve(self):
		# add starting cell to open heap queue
		heapq.heappush(self.opened, (self.start.f, self.start))
		while len(self.opened):
			# pop cell from heap queue
			f, cell = heapq.heappop(self.opened)
			# add cell to closed list so we don't process it twice
			self.closed.add(cell)
			# if ending cell, return found path
			if cell is self.end:
				return self.get_path()
			# get adjacent cells for cell
			adj_cells = self.get_adjacent_cells(cell)
			for adj_cell in adj_cells:
				if adj_cell.reachable and adj_cell not in self.closed:
					if (adj_cell.f, adj_cell) in self.opened:
						# if adj cell in open list, check if current path is
						# better than the one previously found
						# for this adj cell.
						if adj_cell.g > cell.g + 10:
							self.update_cell(adj_cell, cell)	
					else:
						self.update_cell(adj_cell, cell)
						# add adj cell to open list
						heapq.heappush(self.opened, (adj_cell.f, adj_cell))
