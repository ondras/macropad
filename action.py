import asyncio
import colorsys


class Action:
	def __init__(self, label="?"):
		self.label = label


class ButtonAction(Action):
	def __init__(self, label, color=0xffffff):
		super().__init__(label)
		self.color = color

	def on_press(self, app, index: int):
		print("press", index)

	def on_release(self, app, index: int):
		print("release", index)


class EncoderAction(Action):
	def on_rotate(self, app, diff):
		print(f"rotate {diff}")


class ModifierAction(ButtonAction):
	active = False

	def on_press(self, app, index):
		app.macropad.grid.show_arrows()
		app.macropad.grid.invert_on(index)
		self.active = True

	def on_release(self, app, index):
		app.macropad.grid.hide_arrows()
		app.macropad.grid.invert_off(index)
		self.active = False


async def loop(macropad, index):
	hue = 0
	while True:
		macropad.pixels[index] = colorsys.hsv_to_rgb(hue, 1, 1)
		hue = hue+0.01
		hue = hue % 1
		await asyncio.sleep(0.01)


class RainbowAction(ButtonAction):
	def __init__(self, label="rainbow"):
		super().__init__(label)

	def on_press(self, app, index: int):
		self.task = asyncio.create_task(loop(app.macropad, index))

	def on_release(self, app, index: int):
		self.task.cancel()


class KeyboardAction(ButtonAction):
	def __init__(self, label="key", keys=[], *args, **kwargs):
		super().__init__(label, *args, **kwargs)
		self.keys = keys

	def on_press(self, app, index: int):
		macropad = app.macropad

		for item in self.keys:
			if isinstance(item, str):
				macropad.keyboard_layout.write(item)
			elif isinstance(item, int):
				macropad.keyboard.press(item)

		macropad.keyboard.release_all()