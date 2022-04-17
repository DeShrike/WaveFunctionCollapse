import cv2
import numpy as np
import random

TILE_NAMES = [
	"./tiles/wfc-1.png",
	"./tiles/wfc-2.png",
	"./tiles/wfc-3.png",
	"./tiles/wfc-4.png"
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

TILE_NAMES = [
	"./tiles/wfc-2c-1.png",
	"./tiles/wfc-2c-2.png",
	"./tiles/wfc-2c-3.png",
	"./tiles/wfc-2c-4.png",
	"./tiles/wfc-2c-5.png",
	"./tiles/wfc-2c-6.png",
	"./tiles/wfc-2c-7.png",
	"./tiles/wfc-2c-8.png",
	"./tiles/wfc-2c-9.png",
	"./tiles/wfc-2c-10.png",
	"./tiles/wfc-2c-11.png",
	"./tiles/wfc-2c-12.png",
]

OUTPUT_FILE = "wfc.png"

COLOR_DIVIDER = 1

X_TILES = 160
Y_TILES = 120

# OVERLAPPING = False

class WaveFunctionCollapse():

	def __init__(self, *, silent: bool = True):
		self.tiles = []
		self.tile_data = {}
		self.silent = silent

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

		tile = np.rot90(tile, axes=(1, 0))
		left_row = np.copy(tile[0])
		left_flat = tuple(list(left_row.reshape((self.tile_height * self.tile_bpp,))))

		tile = np.rot90(tile, axes=(1, 0))
		bottom_row = np.copy(tile[0])
		bottom_flat = tuple(list(bottom_row.reshape((self.tile_width * self.tile_bpp,))))

		tile = np.rot90(tile, axes=(1, 0))
		right_row = np.copy(tile[0])
		right_flat = tuple(list(right_row.reshape((self.tile_height * self.tile_bpp,))))

		tile = np.rot90(tile, axes=(1, 0))

		self.tiles.append(np.copy(tile))
		tile_ix = len(self.tiles) - 1
		self.tile_data[tile_ix] = {"top": top_flat, "bottom": bottom_flat, "left": left_flat, "right": right_flat}

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
			left_ix = self.tile_grid[y][x - 1]
		if x < self.x_tiles - 1:
			right_ix = self.tile_grid[y][x + 1]
		if y > 0:
			top_ix = self.tile_grid[y - 1][x]
		if y < self.y_tiles - 1:
			bottom_ix = self.tile_grid[y + 1][x]

		top_side = None
		bottom_side = None
		left_side = None
		right_side = None

		if left_ix is not None:
			left_side = self.tile_data[left_ix]["right"]
		elif x == 0:
			left_side = self.vertical_border_side

		if right_ix is not None:
			right_side = self.tile_data[right_ix]["left"]
		elif x == self.x_tiles - 1:
			right_side = self.vertical_border_side

		if top_ix is not None:
			top_side = self.tile_data[top_ix]["bottom"]
		elif y == 0:
			top_side = self.horizontal_border_side

		if bottom_ix is not None:
			bottom_side = self.tile_data[bottom_ix]["top"]
		elif y == self.y_tiles - 1:
			bottom_side = self.horizontal_border_side

		# todo
		possibilities = set([ix for ix in range(len(self.tiles))])

		if left_side is not None:
			poss = self.left_side_data[left_side]
			possibilities = possibilities.intersection(poss)

		if right_side is not None:
			poss = self.right_side_data[right_side]
			possibilities = possibilities.intersection(poss)

		if top_side is not None:
			poss = self.top_side_data[top_side]
			possibilities = possibilities.intersection(poss)

		if bottom_side is not None:
			poss = self.bottom_side_data[bottom_side]
			possibilities = possibilities.intersection(poss)

		if len(possibilities) == 0:
			return None

		ix = random.choice(list(possibilities))

		return ix

	def generate(self, x_tiles: int, y_tiles: int):
		self.x_tiles = x_tiles
		self.y_tiles = y_tiles

		self.tile_grid = [[None for _ in range(self.x_tiles)] for _ in range(y_tiles)]

		# pick random tile for top-left
		# self.tile_grid[0][0] = random.randint(0, len(self.tiles) - 1)
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
				if self.tile_grid[y][x] is None:
					continue
				this_tile = self.tiles[self.tile_grid[y][x]]
				self.output[py:py + self.tile_height, px:px + self.tile_width, 0:self.tile_bpp] = this_tile

	def save(self, filename: str):
		self.build_output()
		self.print(f"Saving {filename}")
		cv2.imwrite(filename, self.output)

	def print(self, message: str):
		if not self.silent:
			print(message)


def main():
	wfc = WaveFunctionCollapse(silent = False)
	wfc.load_tiles(TILE_NAMES)
	wfc.generate(X_TILES, Y_TILES)
	wfc.save(OUTPUT_FILE)

if __name__ == "__main__":
	main()
