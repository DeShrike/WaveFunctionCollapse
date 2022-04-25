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
			"rotate90": False,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		# {
		# 	"filename": "./tiles/mondriaan/mondriaan-12.png",
		# 	"rotate90": True,
		# 	"rotate180": True,
		# 	"rotate270": True,
		# 	"flip_vertical": False,
		# 	"flip_horizontal": False,
		# },
		{
			"filename": "./tiles/mondriaan/mondriaan-13.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-14.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-15.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-16.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-17.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
		{
			"filename": "./tiles/mondriaan/mondriaan-18.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": True,
			"flip_horizontal": True,
		},
	]
}

OUTPUT_FILE = "mondriaan.png"
TILESHEET_FILE = "mondriaan-tilesheet.png"

X_TILES = 5 # 640 // 20
Y_TILES = 5 # 480 // 20

def main():
	wfc = WaveFunctionCollapse(silent = False)
	wfc.load_config(CONFIG)
	wfc.create_tilesheet(TILESHEET_FILE)
	for i in range(1000):
		random.seed(i)
		try:
			wfc.collapse(X_TILES, Y_TILES)
			wfc.save(OUTPUT_FILE)
		except Exception as e:
			print(f"   Seed = {i}       ")
			print(e)
			return
		else:
			pass
		finally:
			pass

if __name__ == "__main__":
	main()
