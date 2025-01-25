# settings.py
import json

SETTINGS_JSON = r'''
{
  "colors": {
    "WHITE": [255, 255, 255],
    "BLACK": [0, 0, 0],
    "GRAY": [200, 200, 200],
    "RED": [255, 0, 0],
    "GREEN": [0, 255, 0],
    "PURPLE": [128, 0, 128]
  },
  "width": 1600,
  "height": 720,
  "fps": 30,
  "tile_size": 60,
  "board_cols": 10,
  "board_rows": 8,
  "margin_top": 100
}
'''

_data = json.loads(SETTINGS_JSON)

WHITE  = tuple(_data["colors"]["WHITE"])
BLACK  = tuple(_data["colors"]["BLACK"])
GRAY   = tuple(_data["colors"]["GRAY"])
RED    = tuple(_data["colors"]["RED"])
GREEN  = tuple(_data["colors"]["GREEN"])
PURPLE = tuple(_data["colors"]["PURPLE"])

WIDTH       = _data["width"]
HEIGHT      = _data["height"]
FPS         = _data["fps"]
TILE_SIZE   = _data["tile_size"]
BOARD_COLS  = _data["board_cols"]
BOARD_ROWS  = _data["board_rows"]
MARGIN_TOP  = _data["margin_top"]

SHIP_INTERIOR_COLS = 8
SHIP_INTERIOR_ROWS = 8
