import board
from kmk.bootcfg import bootcfg
from kb import isRightSide

enableUSB = True if isRightSide else False

bootcfg(
  sense=board.GP10, # column
  source=board.GP21, # row
  storage=enableUSB,
  mouse=True,
  midi=False,
  usb_id=('KMK Keyboards', 'Split Ortholinear Keyboard'),
)
