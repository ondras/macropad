from action import ModifierAction


class App:
	label = ""
	button_actions = [
		None, None, None,
		None, None, None,
		None, None, None,
		None, None, None
	]

	def __init__(self, macropad):
		self.macropad = macropad
		self.tasks = {}

	def activate(self):
		grid = self.macropad.grid
		grid.title = self.label

		px = self.macropad.pixels
		ba = self.button_actions
		for i in range(len(ba)):
			grid.buttons[i].text = ba[i].label if ba[i] else ""
			color = 0x000000
			if ba[i] and ba[i].color: color = ba[i].color
			px[i] = color


	def deactivate(self):
		pass

	def on_press(self, index: int):
		ba = self.button_actions[index]
		if ba: ba.on_press(self, index)

	def on_release(self, index: int):
		ba = self.button_actions[index]
		if ba: ba.on_release(self, index)

	def on_rotate(self, diff: int):
		pass

	def on_midi(self, message):
		print(f"midi {message}")


class MainApp(App):
	button_index = 2
	button_action = ModifierAction("App")

	def __init__(self, macropad, ctors):
		super().__init__(macropad)
		self.app = None
		self.ctors = ctors
		self.switch(0)

	def switch(self, index: int):
		if self.app: self.app.deactivate()

		self.index = self.preview_index = index
		app = self.ctors[index](self.macropad)
		app.activate()
		self.app = app

		self.macropad.pixels[self.button_index] = 0xffffff
		self.macropad.grid.buttons[self.button_index].text = self.button_action.label


	def on_rotate(self, diff: int):
		if not self.button_action.active:
			return self.app.on_rotate(diff)

		self.preview_index = (self.preview_index + diff) % len(self.ctors)
		self.macropad.grid.title = self.ctors[self.preview_index].label

	def on_press(self, index: int):
		if index == self.button_index:
			self.button_action.on_press(self, index)
		else:
			self.app.on_press(index)

	def on_release(self, index: int):
		if index == self.button_index:
			self.button_action.on_release(self, index)
			if self.preview_index != self.index: self.switch(self.preview_index)
		else:
			self.app.on_release(index)

	@property
	def label(self):
		return self.app.label
