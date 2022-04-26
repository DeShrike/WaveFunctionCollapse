from wfc import WaveFunctionCollapse

CONFIG = {
	"clean_edges": False,
	"overlapping": True,
	"color_divider": 1,
	"tilesheet": {
		"filename": "./tiles/abstract.png",
		"tile_width": 7,
		"tile_height": 7,
	}
}

OUTPUT_FILE = "abstract.png"
TILESHEET_FILE = "abstract-tilesheet.png"

X_TILES = 40
Y_TILES = 40

def main():
	wfc = WaveFunctionCollapse(silent = False)
	wfc.load_config(CONFIG)
	wfc.create_tilesheet(TILESHEET_FILE)
	wfc.collapse(X_TILES, Y_TILES)
	wfc.save(OUTPUT_FILE)

if __name__ == "__main__":
	main()
