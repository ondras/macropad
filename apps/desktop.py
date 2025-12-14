from adafruit_hid.keycode import Keycode
from action import RainbowAction, KeyboardAction
from .app import App
from adafruit_hid.consumer_control_code import ConsumerControlCode


mic_colors = [0xff0000, 0x00ff00]

class MicAction(KeyboardAction):

	def __init__(self):
		super().__init__("Mic", [Keycode.CONTROL, Keycode.SHIFT, Keycode.M], color=mic_colors[1])
		self.on = True

	def on_press(self, app, index: int):
		super().on_press(app, index)
		self.on = not self.on
		app.macropad.pixels[index] = mic_colors[int(self.on)]


class Desktop(App):
	label = "Desktop"
	button_actions = [
		None, None, None,
		KeyboardAction("Push", ["git push", Keycode.ENTER]), KeyboardAction("Status", ["git status", Keycode.ENTER]), None,
		KeyboardAction("Pull", ["git pull", Keycode.ENTER]), KeyboardAction("Diff", ["git diff", Keycode.ENTER]), KeyboardAction("Commit", ['git commit -am ""', Keycode.LEFT_ARROW]),
		KeyboardAction("Blank", [Keycode.CONTROL, Keycode.SHIFT, Keycode.S], color=0xff0000), None, MicAction()
	]

	def on_rotate(self, diff: int):
		self.macropad.consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT if diff > 0 else ConsumerControlCode.VOLUME_DECREMENT)
