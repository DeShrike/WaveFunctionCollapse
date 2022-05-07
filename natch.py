from wfc import WaveFunctionCollapse

CONFIG = {
	"clean_edges": False,
	"overlapping": True,
	"color_divider": 1,
	"tilesheet": {
		"filename": "./tiles/natch.png",
		"tile_width": 10,
		"tile_height": 10,
	}
}

OUTPUT_FILE = "natch.png"
TILESHEET_FILE = "natch-tilesheet.png"

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
