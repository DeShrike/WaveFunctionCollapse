from wfc import WaveFunctionCollapse

CONFIG = {
	"clean_edges": False,
	"overlapping": True,
	"color_divider": 1,
	"tilesheet": {
		"filename": "./tiles/skyline.png",
		"tile_width": 6,
		"tile_height": 6,
	}
}

OUTPUT_FILE = "skyline.png"
TILESHEET_FILE = "skyline-tilesheet.png"

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
