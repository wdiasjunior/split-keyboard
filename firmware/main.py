import board
import digitalio
from kb import KMKKeyboard, isRight
from kmk.keys import KC
from kmk.hid import HIDModes
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.lock_status import LockStatus
from kmk.extensions.LED import LED

keyboard = KMKKeyboard()

layers = Layers()

split_side = SplitSide.RIGHT if isRight else SplitSide.LEFT

split = Split(
  split_side=split_side,
  split_type=SplitType.UART,
  data_pin=board.GP0,
  data_pin2=board.GP1,
  uart_flip=True,
  use_pio=True,
  uart_interval=10,
  split_flip=False,
  split_target_left=True,
)

leds = LED(led_pin=[board.GP25])

class LEDLockStatus(LockStatus):
  def set_lock_led(self):
    if not isRight:
      if self.get_caps_lock():
        leds.set_brightness(50, leds=[0])
      else:
        leds.set_brightness(0, leds=[0])

  def after_hid_send(self, sandbox):
    super().after_hid_send(sandbox)
    if self.report_updated:
      self.set_lock_led()

LAYER_0 = KC.TO(0)
LAYER_2 = KC.TO(2)

def set_layer_led_on(key, keyboard, *args):
  if isRight:
    leds.set_brightness(50, leds=[0])

def set_layer_led_off(key, keyboard, *args):
  if isRight:
    leds.set_brightness(0, leds=[0])

LAYER_2.after_press_handler(set_layer_led_on)
LAYER_0.after_press_handler(set_layer_led_off)

keyboard.modules.append(layers)
keyboard.modules.append(split)
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(leds)
keyboard.extensions.append(LEDLockStatus())

keyboard.debug_enabled = True

keyboard.keymap = [
  # layer 0
  [
    KC.ESC,  KC.F1,   KC.F2,   KC.F3,  KC.F4,  KC.F5,       KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.SLCK, KC.PSCR, KC.DEL,\
    KC.GRV,  KC.N1,   KC.N2,   KC.N3,  KC.N4,  KC.N5,       KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC,          KC.HOME,\
    KC.TAB,  KC.Q,    KC.W,    KC.E,   KC.R,   KC.T,        KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS,              KC.END,\
    KC.CAPS, KC.A,    KC.S,    KC.D,   KC.F,   KC.G,        KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENTER,                   KC.PGUP,\
    KC.LSFT, KC.Z,    KC.X,    KC.C,   KC.V,   KC.B,        KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLSH, KC.RSFT, KC.UP,                KC.PGDOWN,\
    KC.LCTL, KC.LCMD, KC.LALT,    KC.SPC,    KC.SPC,        KC.SPC, KC.RALT, KC.MO(1), KC.RCTL, KC.LEFT, KC.DOWN, KC.RIGHT,       KC.RCMD,
  ],
  # layer 1
  [
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.BRID, KC.BRIU,          KC.MPRV, KC.MPLY, KC.MNXT, KC.MUTE, KC.VOLD, KC.VOLU, LAYER_0, KC.PAUS, KC.NO,  KC.NO,\
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,   KC.NO,            KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, LAYER_2, KC.NO,                       KC.NO,\
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,   KC.NO,            KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                         KC.NO,\
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,   KC.NO,            KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                                KC.NO,\
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,   KC.NO,            KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                                KC.NO,\
    KC.NO,  KC.NO, KC.NO,     KC.NO,    KC.NO,              KC.NO, KC.NO, KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO,                              KC.NO,
  ],
  # layer 2 - same as layer 0, but swaps L-super with L-ctrl
  [
    KC.ESC,  KC.F1,   KC.F2,   KC.F3,  KC.F4,  KC.F5,       KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.SLCK, KC.PSCR, KC.DEL,\
    KC.GRV,  KC.N1,   KC.N2,   KC.N3,  KC.N4,  KC.N5,       KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC,          KC.HOME,\
    KC.TAB,  KC.Q,    KC.W,    KC.E,   KC.R,   KC.T,        KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS,              KC.END,\
    KC.CAPS, KC.A,    KC.S,    KC.D,   KC.F,   KC.G,        KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENTER,                   KC.PGUP,\
    KC.LSFT, KC.Z,    KC.X,    KC.C,   KC.V,   KC.B,        KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLSH, KC.RSFT, KC.UP,                KC.PGDOWN,\
    KC.LCMD, KC.LCTL, KC.LALT,    KC.SPC,    KC.SPC,        KC.SPC, KC.RALT, KC.MO(1), KC.RCTL, KC.LEFT, KC.DOWN, KC.RIGHT,       KC.RCMD,
  ]
]

if __name__ == "__main__":
  keyboard.go(hid_type=HIDModes.USB)
