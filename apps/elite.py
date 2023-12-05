from adafruit_hid.keycode import Keycode
from action import RainbowAction, KeyboardAction
from .app import App
from adafruit_hid.consumer_control_code import ConsumerControlCode


class Elite(App):
	label = "Elite Dangerous"
	button_actions = [
		KeyboardAction("FSD", [Keycode.J], color=0x00ff00), None, None,
		KeyboardAction("Landing gear", [Keycode.L], color=0x00ff00), None, KeyboardAction("Silent", [Keycode.DELETE], color=0xff0000),
		KeyboardAction("Lights", [Keycode.INSERT], color=0xffff00), KeyboardAction("Cargo", [Keycode.HOME]), KeyboardAction("Night", [Keycode.END]),
		KeyboardAction("GalMap", [Keycode.COMMA], color=0x0000ff), KeyboardAction("SysMap", [Keycode.PERIOD], color=0x0000ff), KeyboardAction("FSS", [Keycode.QUOTE], color=0x0000ff)
	]
