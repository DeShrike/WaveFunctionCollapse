import cv2
import numpy as np
import random

TILE_NAMES = [
	"./tiles/simple/wfc-1.png",
	"./tiles/simple/wfc-2.png",
	"./tiles/simple/wfc-3.png",
	"./tiles/simple/wfc-4.png"
]

TILE_NAMES = [
	"./tiles/wfc-a.png",
	"./tiles/wfc-b.png",
	"./tiles/wfc-c.png",
	"./tiles/wfc-d.png",
	"./tiles/wfc-e.png",
	"./tiles/wfc-f.png",
	"./tiles/wfc-g.png",
	"./tiles/wfc-h.png",
	"./tiles/wfc-i.png",
	"./tiles/wfc-j.png",
	"./tiles/wfc-k.png",
	"./tiles/wfc-l.png",
]

TILE_NAMESX = [
	"./tiles/redblue/wfc-2c-1.png",
	"./tiles/redblue/wfc-2c-2.png",
	"./tiles/redblue/wfc-2c-3.png",
	"./tiles/redblue/wfc-2c-4.png",
	"./tiles/redblue/wfc-2c-5.png",
	"./tiles/redblue/wfc-2c-6.png",
	"./tiles/redblue/wfc-2c-7.png",
	"./tiles/redblue/wfc-2c-8.png",
	"./tiles/redblue/wfc-2c-9.png",
	"./tiles/redblue/wfc-2c-10.png",
	"./tiles/redblue/wfc-2c-11.png",
	"./tiles/redblue/wfc-2c-12.png",
]

TILE_NAMESX = [
	"./tiles/circuit/circuit-1.png",
	"./tiles/circuit/circuit-2.png",
	"./tiles/circuit/circuit-3.png",
	"./tiles/circuit/circuit-4.png",
	"./tiles/circuit/circuit-5.png",
	"./tiles/circuit/circuit-6.png",
	"./tiles/circuit/circuit-7.png",
	"./tiles/circuit/circuit-8.png",
	"./tiles/circuit/circuit-9.png",
	"./tiles/circuit/circuit-10.png",
	#"./tiles/circuit/circuit-11.png",
	#"./tiles/circuit/circuit-12.png",
	"./tiles/circuit/circuit-13.png",
]

TILE_NAMES = [
   "./tiles/rgb/rgb-1.png",
   "./tiles/rgb/rgb-2.png",
   "./tiles/rgb/rgb-3.png",
   "./tiles/rgb/rgb-4.png",
   "./tiles/rgb/rgb-5.png",
   "./tiles/rgb/rgb-6.png",
   "./tiles/rgb/rgb-7.png",
   "./tiles/rgb/rgb-8.png",
   "./tiles/rgb/rgb-9.png",
]

CLEAR = u"\u001b[2J"
HIDECURSOR = u"\u001b[?25l"
SHOWCURSOR = u"\u001b[?25h"

OUTPUT_FILE = "wfc.png"

COLOR_DIVIDER = 1

X_TILES = 25
Y_TILES = 20

DEBUG = True

# OVERLAPPING = False

class Wave():

	def __init__(self, possibilities):
		self.ix = None
		self.possibilities = possibilities

class WaveFunctionCollapse():

	def __init__(self, *, silent: bool = True, clean_edges: bool = False):
		self.tiles = []
		self.tile_data = {}
		self.silent = silent
		self.clean_edges = clean_edges

		self.left_side_data = {}
		self.right_side_data = {}
		self.top_side_data = {}
		self.bottom_side_data = {}

		self.tile_width = None
		self.tile_height = None
		self.tile_bpp = None

	def process_tile(self, tile):
		if self.tile_width is None:
			self.tile_width = np.shape(tile)[1]

		if self.tile_height is None:
			self.tile_height = np.shape(tile)[0]

		if self.tile_bpp is None:
			self.tile_bpp = np.shape(tile)[2]

		if self.tile_width != np.shape(tile)[1] or self.tile_height != np.shape(tile)[0] or self.tile_bpp != np.shape(tile)[2]:
			raise Exception(f"All tiles must have the same size and depth ({self.tile_width}x{self.tile_height}*{self.tile_bpp})")

		top_row = np.copy(tile[0])
		top_flat = tuple(list(top_row.reshape((self.tile_width * self.tile_bpp,))))

		bottom_row = np.copy(tile[-1])
		bottom_flat = tuple(list(bottom_row.reshape((self.tile_width * self.tile_bpp,))))

		tile = np.rot90(tile, axes=(1, 0))
		left_row = np.copy(tile[0])
		left_flat = tuple(list(left_row.reshape((self.tile_height * self.tile_bpp,))))

		right_row = np.copy(tile[-1])
		right_flat = tuple(list(right_row.reshape((self.tile_height * self.tile_bpp,))))

		tile = np.rot90(tile, -1, axes=(1, 0))

		self.tiles.append(np.copy(tile))
		tile_ix = len(self.tiles) - 1
		self.tile_data[tile_ix] = {
			"top": top_flat,
			"bottom": bottom_flat,
			"left": left_flat,
			"right": right_flat
		}

		if top_flat in self.top_side_data:
			self.top_side_data[top_flat].append(tile_ix)
		else:
			self.top_side_data[top_flat] = [tile_ix]

		if bottom_flat in self.bottom_side_data:
			self.bottom_side_data[bottom_flat].append(tile_ix)
		else:
			self.bottom_side_data[bottom_flat] = [tile_ix]

		if left_flat in self.left_side_data:
			self.left_side_data[left_flat].append(tile_ix)
		else:
			self.left_side_data[left_flat] = [tile_ix]

		if right_flat in self.right_side_data:
			self.right_side_data[right_flat].append(tile_ix)
		else:
			self.right_side_data[right_flat] = [tile_ix]

	def load_tiles(self, tile_names):
		for tile_name in tile_names:
			self.print(f"Loading tile {tile_name}")
			img = cv2.imread(tile_name)
			for _ in range(4):
				self.process_tile(img)
				img = np.rot90(img, axes=(1, 0))

		self.horizontal_border_side = tuple([255] * (self.tile_width * self.tile_bpp))
		self.vertical_border_side = tuple([255] * (self.tile_height * self.tile_bpp))

	def try_find_tile_for(self, x: int, y: int) -> int:

		top_ix = None
		bottom_ix = None
		left_ix = None
		right_ix = None
		if x > 0:
			left_ix = self.tile_grid[y][x - 1].ix
		if x < self.x_tiles - 1:
			right_ix = self.tile_grid[y][x + 1].ix
		if y > 0:
			top_ix = self.tile_grid[y - 1][x].ix
		if y < self.y_tiles - 1:
			bottom_ix = self.tile_grid[y + 1][x].ix

		top_side = None
		bottom_side = None
		left_side = None
		right_side = None

		if left_ix is not None:
			left_side = self.tile_data[left_ix]["right"]
		elif x == 0 and self.clean_edges:
			left_side = self.vertical_border_side

		if right_ix is not None:
			right_side = self.tile_data[right_ix]["left"]
		elif x == self.x_tiles - 1 and self.clean_edges:
			right_side = self.vertical_border_side

		if top_ix is not None:
			top_side = self.tile_data[top_ix]["bottom"]
		elif y == 0 and self.clean_edges:
			top_side = self.horizontal_border_side

		if bottom_ix is not None:
			bottom_side = self.tile_data[bottom_ix]["top"]
		elif y == self.y_tiles - 1 and self.clean_edges:
			bottom_side = self.horizontal_border_side

		# todo
		possibilities = set([ix for ix in range(len(self.tiles))])

		if left_side is not None:
			if left_side not in self.left_side_data:
				return []
			poss = self.left_side_data[left_side]
			possibilities = possibilities.intersection(poss)

		if right_side is not None:
			if right_side not in self.right_side_data:
				return []
			poss = self.right_side_data[right_side]
			possibilities = possibilities.intersection(poss)

		if top_side is not None:
			if top_side not in self.top_side_data:
				return []
			poss = self.top_side_data[top_side]
			possibilities = possibilities.intersection(poss)

		if bottom_side is not None:
			if bottom_side not in self.bottom_side_data:
				return []
			poss = self.bottom_side_data[bottom_side]
			possibilities = possibilities.intersection(poss)

		return list(possibilities)

	def neighbors(self, x: int, y: int):
		if x > 0:
			yield (x - 1, y)
		if x < self.x_tiles - 1:
			yield (x + 1, y)
		if y > 0:
			yield (x, y - 1)
		if y < self.y_tiles - 1:
			yield (x, y + 1)

	def update_neighbours(self, x: int, y: int):
		for nx, ny in self.neighbors(x, y):
			if self.tile_grid[ny][nx].ix is None:
				t = self.tile_grid[ny][nx]
				t.possibilities = self.try_find_tile_for(nx, ny)

	def find_pos_lowest_entropy(self):
		lowest = 1_000
		lx = None
		ly = None
		for y in range(self.y_tiles):
			for x in range(self.x_tiles):
				if self.tile_grid[y][x].ix is None:
					pc = len(self.tile_grid[y][x].possibilities)
					if pc < lowest:
						lowest = pc
						lx = x
						ly = y

		return (lx, ly)

	def generate(self, x_tiles: int, y_tiles: int):
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles

		possibilities = [ix for ix in range(len(self.tiles))]
		self.tile_grid = [[Wave(possibilities) for _ in range(self.x_tiles)] for _ in range(y_tiles)]
		if self.clean_edges:
			for x in range(self.x_tiles):
				for y in range(self.y_tiles):
					self.tile_grid[y][x].possibilities = self.try_find_tile_for(x, y)
		# pick a random starting spot
		x = random.randint(0, x_tiles - 1)
		y = random.randint(0, y_tiles - 1)

		t = self.tile_grid[y][x]
		t.ix = random.choice(t.possibilities)
		self.update_neighbours(x, y)

		if DEBUG:
			print(CLEAR, end="")
			print(HIDECURSOR, end="")

		while True:
			if DEBUG:
				print(u"\u001b[1;1H", end="")

			x, y = self.find_pos_lowest_entropy()
			if x is None:
				break
			t = self.tile_grid[y][x]
			if len(t.possibilities) == 0:
				print(f" ERROR: {x}, {y}    ")
				t.ix = 0
				return
			else:
				t.ix = random.choice(t.possibilities)
			self.update_neighbours(x, y)

			if DEBUG:
				self.print_grid()
				#a = input()

	def generate_old_2(self, x_tiles: int, y_tiles: int):
		"""
		Iterative backtracking.
		Very slow under certain conditions.
		"""
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles

		self.tile_grid = [[None for _ in range(self.x_tiles)] for _ in range(y_tiles)]

		# pick a random starting spot
		x = random.randint(0, x_tiles - 1)
		y = random.randint(0, y_tiles - 1)
		queue = [(x, y)]
		path = []
		if DEBUG:
			print(CLEAR, end="")
			print(HIDECURSOR, end="")
		while len(queue) > 0:
			if DEBUG:
				print(u"\u001b[1;1H", end="")
			#print("================================")
			x, y = queue.pop(0)
			if self.tile_grid[y][x] is not None:
				continue
			#print(f"Trying {x},{y}")
			possibilities = self.try_find_tile_for(x, y)
			if len(possibilities) == 0:
				#print("initial None")
				queue.append((x, y))
				while True:
					x, y, possibilities = path.pop()
					#print(x, y, possibilities)
					if len(possibilities) > 0:
						ix = random.choice(possibilities)
						possibilities.remove(ix)
						self.tile_grid[y][x] = ix
						path.append([x, y, possibilities])
						break
					else:
						if (x, y) not in queue:
							#print(f"none, appending {x},{y} to queue")
							queue.append((x, y))
						self.tile_grid[y][x] = None
			else:
				ix = random.choice(possibilities)
				possibilities.remove(ix)
				self.tile_grid[y][x] = ix
				path.append([x, y, possibilities])
				for nx, ny in self.neighbors(x, y):
					if self.tile_grid[ny][nx] is None and (nx, ny) not in queue:
						#print(f"Appending neighbor {nx},{ny} to queue")
						queue.append((nx, ny))
			if DEBUG:
				self.print_grid()
			#print(f"Path: {len(path)}  Queue: {len(queue)} ")
			#print(queue)
			# a = input()
		if DEBUG:
			print(SHOWCURSOR)

	def print_grid(self):
		for y in range(self.y_tiles):
			for x in range(self.x_tiles):
				if self.tile_grid[y][x].ix is None:
					print("..", end=" ")
				else:
					print(f"{self.tile_grid[y][x].ix:2}", end=" ")
			print("")

	def generate_old(self, x_tiles: int, y_tiles: int):
		"""
		Non-backtracking.
		Possible missing spots.
		"""
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles

		self.tile_grid = [[None for _ in range(self.x_tiles)] for _ in range(y_tiles)]

		for y in range(self.y_tiles):
			for x in range(self.x_tiles):
				if self.tile_grid[y][x] is not None:
					continue
				self.tile_grid[y][x] = self.try_find_tile_for(x, y)

	def build_output(self):
		output_shape = (self.tile_height * self.y_tiles, self.tile_width * self.x_tiles, self.tile_bpp)
		self.print(f"Building image - Width: {self.tile_width * self.x_tiles}, Height: {self.tile_height * self.y_tiles}")
		self.output = np.zeros(output_shape, np.uint8)
		for y in range(self.y_tiles):
			for x in range(self.x_tiles):
				px = x * self.tile_width
				py = y * self.tile_height
				if self.tile_grid[y][x].ix is None:
					continue
				this_tile = self.tiles[self.tile_grid[y][x].ix]
				self.output[py:py + self.tile_height, px:px + self.tile_width, 0:self.tile_bpp] = this_tile

	def save(self, filename: str):
		self.build_output()
		self.print(f"Saving {filename}")
		cv2.imwrite(filename, self.output)

	def print(self, message: str):
		if not self.silent:
			print(message)


def main():
	wfc = WaveFunctionCollapse(silent = False, clean_edges = False)
	wfc.load_tiles(TILE_NAMES)
	wfc.generate(X_TILES, Y_TILES)
	wfc.save(OUTPUT_FILE)

if __name__ == "__main__":
	main()
