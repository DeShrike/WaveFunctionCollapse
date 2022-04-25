from wfc import WaveFunctionCollapse

CONFIG = {
	"clean_edges": False,
	"overlapping": False,
	"color_divider": 1,
	"tiles": [
		{
			"filename": "./tiles/rgb/rgb-1.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-2.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-3.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-4.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-5.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-6.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-7.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-8.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-9.png",
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/rgb/rgb-10.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-11.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-12.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-13.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-14.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-15.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-16.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-17.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/rgb/rgb-18.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
			{
			"filename": "./tiles/rgb/rgb-19.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
	]
}

OUTPUT_FILE = "rgb.png"
TILESHEET_FILE = "rgb-tilesheet.png"

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
