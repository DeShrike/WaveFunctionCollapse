import logging
import cv2
import numpy as np
import random
import math
import sys

# debug, info, warning, error, critical

# logging.basicConfig(level=logging.DEBUG,
# 					filename="wfc.log",
# 					filemode="w",
# 					format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")

# logger = logging.getLogger(__name__)
# handler = logging.FileHandler("test.log")
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.info("Test")

# %(funcName)s
# %(lineno)d
# %(module)s
# %(filename)s

CLEAR = u"\u001b[2J"
HIDECURSOR = u"\u001b[?25l"
SHOWCURSOR = u"\u001b[?25h"

DEBUG = False

class Wave():

	def __init__(self, possibilities):
		self.ix = None
		self.possibilities = possibilities

class WaveFunctionCollapse():

	def __init__(self, *, silent: bool = True):
		self.tiles = []
		self.tile_data = {}
		self.silent = silent
		self.clean_edges = False
		self.backtrack_limit = 5000

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

		for t in self.tiles:
			if np.array_equal(t, tile):
				return

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

	def load_tiles(self, config):
		for tile in config["tiles"]:
			tile_name = tile["filename"]
			img = cv2.imread(tile_name)
			self.process_tile(img)
			img90 = np.rot90(img, 1, axes=(1, 0))
			img180 = np.rot90(img, 2, axes=(1, 0))
			img270 = np.rot90(img, 3, axes=(1, 0))
			flipud = np.flipud(img)
			fliplr = np.fliplr(img)
			if tile["rotate90"]:
				self.process_tile(img90)
			if tile["rotate180"]:
				self.process_tile(img180)
			if tile["rotate270"]:
				self.process_tile(img270)
			if tile["flip_vertical"]:
				self.process_tile(fliplr)
			if tile["flip_horizontal"]:
				self.process_tile(flipud)

	def generate_overlapped_tiles(self, config):
		sheet = config["tilesheet"]
		sheet_name = sheet["filename"]
		self.print(f"Loading sheet {sheet_name}")
		img = cv2.imread(sheet_name)
		tile_x = sheet["tile_width"]
		tile_y = sheet["tile_height"]
		sheet_x = img.shape[1]
		sheet_y = img.shape[0]
		self.print(f"Sheet: {sheet_x} x {sheet_y}  - Tile: {tile_x} x {tile_y}")
		for y in range(sheet_y - tile_y):
			for x in range(sheet_x - tile_x):
				tile = img[y:y + tile_y, x:x + tile_x, :]
				self.process_tile(tile)

	def load_config(self, config):
		self.color_divider = config["color_divider"]
		self.overlapping = config["overlapping"]
		self.clean_edges = config["clean_edges"]
		self.clean_edges = False # Not implemented

		if self.overlapping:
			self.generate_overlapped_tiles(config)
		else:
			self.load_tiles(config)

	def create_tilesheet(self, filename: str):
		count = len(self.tiles)
		w = round(math.sqrt(count))
		h = count // w + 1

		output_shape = ((self.tile_height + 1) * h + 1, (self.tile_width + 1) * w + 1, self.tile_bpp)
		self.print(f"{count} tiles")
		self.print(f"Building tilesheet {w} x {h} - Width: {output_shape[1]}, Height: {output_shape[0]}")
		output = np.zeros(output_shape, np.uint8)

		for ix, tile in enumerate(self.tiles):
			tx = ix % w
			ty = ix // w
			ttx = tx * (self.tile_width + 1) + 1
			tty = ty * (self.tile_height + 1) + 1
			output[tty:tty + self.tile_height, ttx:ttx + self.tile_width, 0:self.tile_bpp] = tile

		self.print(f"Saving {filename}")
		cv2.imwrite(filename, output)

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

	def reset_neighbours(self, x: int, y: int):
		for nx, ny in self.neighbors(x, y):
			if self.tile_grid[ny][nx].ix is None:
				t = self.tile_grid[ny][nx]
				t.possibilities = self.all_possibilities[:]

	def find_pos_lowest_entropy(self):
		lowest = 1_000_000
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

	def collapse(self, x_tiles: int, y_tiles: int):
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles
		self.print("Collapsing...")

		queue = []
		backtracks = 0

		self.all_possibilities = [ix for ix in range(len(self.tiles))]
		self.tile_grid = [[Wave(self.all_possibilities[:]) for _ in range(self.x_tiles)] for _ in range(y_tiles)]

		"""
		if self.clean_edges:
			for x in range(self.x_tiles):
				for y in range(self.y_tiles):
					self.tile_grid[y][x].possibilities = self.try_find_tile_for(x, y)
		"""

		for _ in range(2):
			x = random.randint(0, self.x_tiles - 1)
			y = random.randint(0, self.y_tiles - 1)
			if self.tile_grid[y][x].ix is None:
				self.tile_grid[y][x].ix = random.randint(0, len(self.tiles) - 1)
				self.update_neighbours(x, y)
				queue.append((x, y))

		while True:
			x, y = self.find_pos_lowest_entropy()
			if x is None:
				break
			t = self.tile_grid[y][x]

			no_possibilities = len(t.possibilities) == 0
			if no_possibilities:
				self.reset_neighbours(x, y)
				self.tile_grid[y][x].possibilities = self.try_find_tile_for(x, y)

			while no_possibilities:
				x, y = queue.pop()
				self.reset_neighbours(x, y)
				backtracks += 1
				if backtracks > self.backtrack_limit:
					return
				t = self.tile_grid[y][x]
				no_possibilities = len(t.possibilities) == 0
				t.ix = None

			t.ix = random.choice(t.possibilities)
			t.possibilities.remove(t.ix)
			queue.append((x, y))

			self.update_neighbours(x, y)

	def print_grid(self):
		for y in range(self.y_tiles):
			for x in range(self.x_tiles):
				if self.tile_grid[y][x].ix is None:
					print("..", end=" ")
				else:
					print(f"{self.tile_grid[y][x].ix:2}", end=" ")
			print("")

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
	pass

if __name__ == "__main__":
	main()
