from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from action import ModifierAction, KeyboardAction
from .app import App
import usb_hid


HID_MAX = 32767
SCREEN = (1920, 1080)

def screen_to_hid(screen_x, screen_y):
	return (
		int(HID_MAX * (screen_x / SCREEN[0])),
		int(HID_MAX * (screen_y / SCREEN[1])),
	)


#class PageAction(ModifierAction):
#	pages = [
#		{label: "Media", key: [Keycode.SHIFT, "2"]},
#		{label: "Cut", key: [Keycode.SHIFT, "3"]},
#		{label: "Edit", key: [Keycode.SHIFT, "4"]},
#		{label: "Fusion", key: [Keycode.SHIFT, "5"]},
#		{label: "Color", key: [Keycode.SHIFT, "6"]},
#		{label: "Fairlight", key: [Keycode.SHIFT, "7"]},
#		{label: "Deliver", key: [Keycode.SHIFT, "8"]},
#	]

def FEATURE_X(index):
	return 88 + index*155

TASKBAR = 48
FEATURE_Y = -56
PX_PER_NOTCH = 5
COLOR_OFFSET_Y = -20

FEATURES = {
	"lift": {
		"label": "Lift",
		"x": FEATURE_X(0),
		"y": FEATURE_Y,
		"colors": { "red": -19, "green": 19, "blue": 56 }
	},
	"gamma": {
		"label": "Gamma",
		"x": FEATURE_X(1),
		"y": FEATURE_Y,
		"colors": { "red": -19, "green": 19, "blue": 56 }
	},
	"gain": {
		"label": "Gain",
		"x": FEATURE_X(2),
		"y": FEATURE_Y,
		"colors": { "red": -19, "green": 19, "blue": 56 }
	},
	"offset": {
		"label": "Offset",
		"x": FEATURE_X(3),
		"y": FEATURE_Y,
		"colors": { "red": -50, "green": 0, "blue": 50 }
	},
	"saturation": {
		"label": "Sat",
		"x": FEATURE_X(2),
		"y": -18,
		"colors": {}
	}
}

COLORS = {
	"red": {
		"label": "Red",
		"color": 0xff0000
	},
	"green": {
		"label": "Green",
		"color": 0x00ff00
	},
	"blue": {
		"label": "Blue",
		"color": 0x0000ff
	}
}


def move_mouse(mouse, position):
	hidx, hidy = screen_to_hid(*position)

	mouse = usb_hid.devices[3]
	x1, x2 = hidx.to_bytes(2, "little")
	y1, y2 = hidy.to_bytes(2, "little")
	report = bytearray(6)
	report[1] = x1
	report[2] = x2
	report[3] = y1
	report[4] = y2
	mouse.send_report(report)


def get_feature_position(type):
	spec = FEATURES[type]
	x = spec["x"]
	y = SCREEN[1] + spec["y"] - TASKBAR
	return (x, y)

def get_color_position(feature_type, color_type):
	spec = FEATURES[feature_type]
	(x, y) = get_feature_position(feature_type)
	x += spec["colors"][color_type]
	y += COLOR_OFFSET_Y
	return (x, y)


class ColorAction(ModifierAction):
	def __init__(self, type: str):
		spec = COLORS[type]
		super().__init__(spec["label"], spec["color"])
		self.type = type

	def on_press(self, app, index: int):
		super().on_press(app, index)
		app.on_press_color(self.type)

	def on_release(self, app, index: int):
		super().on_release(app, index)
		app.on_release_color(self.type)


class FeatureAction(ModifierAction):
	def __init__(self, type: str):
		spec = FEATURES[type]
		super().__init__(spec["label"])
		self.type = type

	def on_press(self, app, index: int):
		super().on_press(app, index)
		app.on_press_feature(self.type)


	def on_release(self, app, index: int):
		super().on_release(app, index)
		app.on_release_feature(self.type)


class DavinciColor(App):
	label = "DaVinci Color"

	button_actions = [
		KeyboardAction("Reset", [Keycode.SHIFT, Keycode.HOME]), None, None,
		FeatureAction("lift"), FeatureAction("gamma"), FeatureAction("gain"),
		FeatureAction("offset"), None, FeatureAction("saturation"),
		ColorAction("red"), ColorAction("green"), ColorAction("blue")
	]

	def __init__(self, macropad):
		super().__init__(macropad)
		self.feature = None

	def on_rotate(self, diff: int):
		if not self.feature: return
		self.macropad.mouse.move(x=diff*PX_PER_NOTCH)

	def on_press_feature(self, feature: str):
		if self.feature: return
		self.feature = feature
		pos = get_feature_position(feature)
		self.press_mouse_at(pos)

	def on_release_feature(self, feature: str):
		self.macropad.mouse.release(Mouse.LEFT_BUTTON)
		self.feature = None

	def on_press_color(self, color: str):
		if not self.feature: return
		spec = FEATURES[self.feature]
		if not spec["colors"]: return

		pos = get_color_position(self.feature, color)
		self.press_mouse_at(pos)

	def on_release_color(self, color: str):
		pass

	def press_mouse_at(self, position):
		hidx, hidy = screen_to_hid(*position)
		self.macropad.mouse.release(Mouse.LEFT_BUTTON)
		self.macropad.absolute_mouse.move(hidx, hidy)
		self.macropad.mouse.press(Mouse.LEFT_BUTTON)
