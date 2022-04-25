from wfc import WaveFunctionCollapse

CONFIG = {
	"clean_edges": False,
	"overlapping": False,
	"color_divider": 1,
	"tiles": [
		{
			"filename": "./tiles/circuit/circuit-1.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-2.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-3.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-4.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-5.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-6.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-7.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-8.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-9.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-10.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-11.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-12.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/circuit/circuit-13.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
	]
}

OUTPUT_FILE = "circuit.png"
TILESHEET_FILE = "circuit-tilesheet.png"

X_TILES = 20
Y_TILES = 20

def main():
	wfc = WaveFunctionCollapse(silent = False)
	wfc.load_config(CONFIG)
	wfc.create_tilesheet(TILESHEET_FILE)
	wfc.collapse(X_TILES, Y_TILES)
	wfc.save(OUTPUT_FILE)

if __name__ == "__main__":
	main()
