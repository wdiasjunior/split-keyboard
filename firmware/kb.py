import board

from storage import getmount

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

driveName = str(getmount('/').label)
isRight = True if driveName.endswith('R') else False

col_pins_left = (board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15)
col_pins_right = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15)

class KMKKeyboard(_KMKKeyboard):
  col_pins = col_pins_right if isRight else col_pins_left
  row_pins = (board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16)

  diode_orientation = DiodeOrientation.COL2ROW

  coord_mapping = [
        0,  1,  2,  3,  4,  5,     60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
        6,  7,  8,  9, 10, 11,     70, 71, 72, 73, 74, 75, 76, 78,     79,
       12, 13, 14, 15, 16, 17,     80, 81, 82, 83, 84, 85, 86, 88,     89,
      18, 19, 20, 21, 22,  23,     90, 91, 92, 93, 94, 95, 97,         99,
     24, 25, 26, 27,  28,  29,     100, 101, 102, 103, 104, 106, 107, 109,
    30, 31, 32,     33,    34,     112, 113, 114, 115, 116, 117, 118, 119,
  ]
