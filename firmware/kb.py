import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
  # TODO Comment one of these on each side
  col_pins = (board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15)
  # col_pins = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15)
  row_pins = (board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16)

  diode_orientation = DiodeOrientation.COLUMNS
  # diode_orientation = DiodeOrientation.COL2ROW

  coord_mapping = [
        0,  1,  2,  3,  4,  5,     44, 43, 42, 41, 40, 39, 38, 37, 36, 35,
        6,  7,  8,  9, 10, 11,     53, 52, 51, 50, 49, 48, 47, 46,     45,
       12, 13, 14, 15, 16, 17,     62, 61, 60, 59, 58, 57, 56, 55,     54,
      18, 19, 20, 21, 22,  23,     70, 69, 68, 67, 66, 65, 64,         63,
     24, 25, 26, 27,  28,  29,     78, 77, 76, 75, 74,   73,   72,     71,
    30, 31, 32,     33,    34,     86,     85,   84,   83, 82, 81, 80, 79,
  ]
