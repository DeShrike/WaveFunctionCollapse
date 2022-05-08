from wfc import WaveFunctionCollapse
import random

CONFIG = {
	"clean_edges": False,
	"overlapping": False,
	"color_divider": 1,
	"tiles": [
		{
			"filename": "./tiles/mondriaan/mondriaan-1.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-2.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-3.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-4.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},

		{
			"filename": "./tiles/mondriaan/mondriaan-1a.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-2a.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-3a.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-4a.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},

		{
			"filename": "./tiles/mondriaan/mondriaan-5.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-6.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-7.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-8.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-9.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-10.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-11.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-12.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
	]
}

OUTPUT_FILE = "mondriaan.png"
TILESHEET_FILE = "mondriaan-tilesheet.png"

X_TILES = 40 # 640 // 20
Y_TILES = 40 # 480 // 20

def main():
	wfc = WaveFunctionCollapse(silent = False)
	wfc.load_config(CONFIG)
	wfc.create_tilesheet(TILESHEET_FILE)
	wfc.collapse(X_TILES, Y_TILES)
	wfc.save(OUTPUT_FILE)

if __name__ == "__main__":
	main()
