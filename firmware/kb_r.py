import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
  # TODO Comment one of these on each side
  # col_pins = (board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15)
  col_pins = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15)
  row_pins = (board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16)

  # diode_orientation = DiodeOrientation.COLUMNS
  diode_orientation = DiodeOrientation.COL2ROW

  coord_mapping = [
        0,  1,  2,  3,  4,  5,     35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
        6,  7,  8,  9, 10, 11,     45, 46, 47, 48, 49, 50, 51, 52,     53,
       12, 13, 14, 15, 16, 17,     54, 55, 56, 57, 58, 59, 60, 61,     62,
      18, 19, 20, 21, 22,  23,     63, 64, 65, 66, 67, 68, 69,         70,
     24, 25, 26, 27,  28,  29,     71, 72, 73, 74, 75,   76,   77,     78,
    30, 31, 32,     33,    34,     79,     80,   81,   82, 83, 84, 85, 86,
  ]
