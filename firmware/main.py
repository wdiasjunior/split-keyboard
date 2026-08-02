import board
from kb import KMKKeyboard, isRightSide
from kmk.keys import KC
from kmk.hid import HIDModes
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.modules.holdtap import HoldTap
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.lock_status import LockStatus
from kmk.modules.mouse_jiggler import MouseJiggler
from kmk.extensions.LED import LED

splitSide = SplitSide.RIGHT if isRightSide else SplitSide.LEFT

keyboard = KMKKeyboard()
layers = Layers()
holdtap = HoldTap()
split = Split(
  split_side=splitSide,
  split_type=SplitType.UART,
  data_pin=board.GP0,
  data_pin2=board.GP1,
  uart_flip=True,
  use_pio=True,
  uart_interval=10,
  split_flip=False,
  split_target_left=True,
)
jiggler = MouseJiggler(
  period_ms=3000,
  move_step=10,
)
leds = LED(led_pin=[board.GP25])

# capslock led
class LEDLockStatus(LockStatus):
  def set_lock_led(self):
    if not isRightSide:
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
MJ_TOGGLE = KC.MJ_TOGGLE

# led status indicators (layer 2 and jiggler blink)
class LEDStatus:
  def __init__(self):
    self._prev_layer_2 = False
    self._led_on = False
    self._last_toggle_ms = 0
    self._blink_interval = 500

  def during_bootup(self, keyboard):
    leds.set_brightness(0, leds=[0])

  def before_matrix_scan(self, keyboard):
    if not isRightSide:
      if jiggler._is_jiggling:
        from supervisor import ticks_ms
        now = ticks_ms()
        if now - self._last_toggle_ms >= self._blink_interval:
          self._last_toggle_ms = now
          self._led_on = not self._led_on
          leds.set_brightness(50 if self._led_on else 0, leds=[0])
      elif self._led_on:
        self._led_on = False
        leds.set_brightness(0, leds=[0])

  def after_matrix_scan(self, keyboard):
    pass

  def process_key(self, keyboard, key, is_press, int_coord):
    return key

  def before_hid_send(self, keyboard):
    pass

  def after_hid_send(self, keyboard):
    if isRightSide:
      in_layer_2 = 2 in keyboard.active_layers
      if in_layer_2 != self._prev_layer_2:
        self._prev_layer_2 = in_layer_2
        leds.set_brightness(50 if in_layer_2 else 0, leds=[0])

  def on_powersave_enable(self, keyboard):
    pass

  def on_powersave_disable(self, keyboard):
    pass

  def deinit(self, keyboard):
    pass

keyboard.modules.append(layers)
keyboard.modules.append(split)
keyboard.modules.append(holdtap)
keyboard.modules.append(jiggler)
keyboard.modules.append(LEDStatus())
keyboard.extensions.append(leds)
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(LEDLockStatus())

keyboard.debug_enabled = False

# mod keys
_L1Q_ = KC.LCMD(KC.N1) # firefox
_L1W_ = KC.LCMD(KC.N2) # chrome
_L1E_ = KC.LCMD(KC.N3) # file explorer
_L1R_ = KC.LCMD(KC.N4) # atom/pulsar
_L1T_ = KC.LCTL(KC.LALT(KC.T)) # new terminal instance
_L1Y_ = KC.LCTL(KC.LSFT(KC.T)) # new terminal tab/reopen closed browser tab
_L1U_ = KC.LCTL(KC.T) # new browser tab
#
_L1S_ = KC.LCMD(KC.N7) # stremio
_L1D_ = KC.LCMD(KC.N8) # discord
_L1F_ = KC.LCMD(KC.N5) # zed
_L1G_ = KC.LCMD(KC.N9) # toggle active terminal instances
#
_L1B_ = KC.LCMD(KC.N6) # spotify
#

keyboard.keymap = [
  # layer 0 - default qwerty layout
  [
    KC.ESC,  KC.F1,   KC.F2,   KC.F3,  KC.F4,  KC.F5,       KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.SLCK, KC.PSCR, KC.DEL,\
    KC.GRV,  KC.N1,   KC.N2,   KC.N3,  KC.N4,  KC.N5,       KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC,          KC.HOME,\
    KC.TAB,  KC.Q,    KC.W,    KC.E,   KC.R,   KC.T,        KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS,              KC.END,\
    KC.CAPS, KC.A,    KC.S,    KC.D,   KC.F,   KC.G,        KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENTER,                   KC.PGUP,\
    KC.LSFT, KC.Z,    KC.X,    KC.C,   KC.V,   KC.B,        KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLSH, KC.RSFT, KC.UP,                KC.PGDOWN,\
    KC.LCTL, KC.LCMD, KC.LALT,   KC.SPC,   KC.MO(1),        KC.SPC, KC.RALT, KC.MO(1), KC.RCTL, KC.LEFT, KC.DOWN, KC.RIGHT,       KC.RCMD,
  ],
  # layer 1 - media controls and window manager stuff
  [
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.BRID, KC.BRIU,          KC.MPRV, KC.MPLY, KC.MNXT, KC.MUTE, KC.VOLD, KC.VOLU, LAYER_0, KC.PAUS, KC.NO,  KC.NO,\
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,   KC.NO,            KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, MJ_TOGGLE,         LAYER_2, KC.NO,           KC.NO,\
    KC.NO,  _L1Q_, _L1W_, _L1E_, _L1R_,   _L1T_,            _L1Y_, _L1U_, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                         KC.NO,\
    KC.NO,  KC.NO, _L1S_, _L1D_, _L1F_,   _L1G_,            KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                                KC.NO,\
    KC.NO,  KC.NO, KC.NO, KC.NO, KC.NO,   _L1B_,            KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,                                KC.NO,\
    KC.NO,  KC.NO, KC.NO,     KC.NO,    KC.TRNS,            KC.NO, KC.NO, KC.TRNS, KC.NO, KC.NO, KC.NO, KC.NO,                              KC.NO,
  ],
  # layer 2 (gaming) - same as layer 0, but swaps L-super with another L-ctrl to avoid exiting full screen, removed tilde to prevent opening console in games
  [
    KC.ESC,  KC.F1,   KC.F2,   KC.F3,  KC.F4,  KC.F5,       KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.SLCK, KC.PSCR, KC.DEL,\
    KC.NO ,  KC.N1,   KC.N2,   KC.N3,  KC.N4,  KC.N5,       KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS, KC.EQL, KC.BSPC,          KC.HOME,\
    KC.TAB,  KC.Q,    KC.W,    KC.E,   KC.R,   KC.T,        KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS,              KC.END,\
    KC.CAPS, KC.A,    KC.S,    KC.D,   KC.F,   KC.G,        KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, KC.ENTER,                   KC.PGUP,\
    KC.LSFT, KC.Z,    KC.X,    KC.C,   KC.V,   KC.B,        KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLSH, KC.RSFT, KC.UP,                KC.PGDOWN,\
    KC.LCTL, KC.LCTL, KC.LALT,    KC.SPC,    KC.SPC,        KC.SPC, KC.RALT, KC.MO(1), KC.RCTL, KC.LEFT, KC.DOWN, KC.RIGHT,       KC.RCMD,
  ]
]

if __name__ == "__main__":
  keyboard.go(hid_type=HIDModes.USB)
