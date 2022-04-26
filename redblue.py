from wfc import WaveFunctionCollapse

CONFIG = {
	"clean_edges": False,
	"overlapping": False,
	"color_divider": 1,
	"tiles": [
		{
			"filename": "./tiles/redblue/wfc-2c-1.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/redblue/wfc-2c-2.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		# {
		# 	"filename": "./tiles/redblue/wfc-2c-3.png",
		# 	"rotate90": False,
		# 	"rotate180": False,
		# 	"rotate270": False,
		# 	"flip_vertical": False,
		# 	"flip_horizontal": False,
		# },
		{
			"filename": "./tiles/redblue/wfc-2c-4.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/redblue/wfc-2c-5.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/redblue/wfc-2c-6.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		# {
		# 	"filename": "./tiles/redblue/wfc-2c-7.png",
		# 	"rotate90": True,
		# 	"rotate180": True,
		# 	"rotate270": True,
		# 	"flip_vertical": False,
		# 	"flip_horizontal": False,
		# },
		# {
		# 	"filename": "./tiles/redblue/wfc-2c-8.png",
		# 	"rotate90": True,
		# 	"rotate180": True,
		# 	"rotate270": True,
		# 	"flip_vertical": False,
		# 	"flip_horizontal": False,
		# },
		# {
		# 	"filename": "./tiles/redblue/wfc-2c-9.png",
		# 	"rotate90": True,
		# 	"rotate180": True,
		# 	"rotate270": True,
		# 	"flip_vertical": False,
		# 	"flip_horizontal": False,
		# },
		# {
		# 	"filename": "./tiles/redblue/wfc-2c-10.png",
		# 	"rotate90": False,
		# 	"rotate180": False,
		# 	"rotate270": False,
		# 	"flip_vertical": True,
		# 	"flip_horizontal": True,
		# },
		# {
		# 	"filename": "./tiles/redblue/wfc-2c-11.png",
		# 	"rotate90": True,
		# 	"rotate180": True,
		# 	"rotate270": True,
		# 	"flip_vertical": False,
		# 	"flip_horizontal": False,
		# },
		# {
		# 	"filename": "./tiles/redblue/wfc-2c-12.png",
		# 	"rotate90": True,
		# 	"rotate180": True,
		# 	"rotate270": True,
		# 	"flip_vertical": False,
		# 	"flip_horizontal": False,
		# },
	]
}

OUTPUT_FILE = "redblue.png"
TILESHEET_FILE = "redblue-tilesheet.png"

X_TILES = 50
Y_TILES = 50

def main():
	wfc = WaveFunctionCollapse(silent = False)
	wfc.load_config(CONFIG)
	wfc.create_tilesheet(TILESHEET_FILE)
	wfc.collapse(X_TILES, Y_TILES)
	wfc.save(OUTPUT_FILE)

if __name__ == "__main__":
	main()
