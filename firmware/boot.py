import digitalio
import board
from kmk.bootcfg import bootcfg
from kb import KMKKeyboard, isRight

enableUSB = True if isRight else False

bootcfg(
  sense=board.GP10,  # column
  source=board.GP21, # row
  storage=enableUSB,
  usb_id=('KMK Keyboards', 'Split Ortho Board'),
)
