from action import RainbowAction, ModifierAction, ButtonAction
from .app import App


class TestAction(ButtonAction):
	def on_press(self, app, index: int):
		mouse = app.macropad.mouse
		mouse.move(x=3000)
		mouse.move(y=3000)


class Demo(App):
	label = "Demo"
	button_actions = [
		RainbowAction(), TestAction("mouse"), None,
		RainbowAction(), None, ModifierAction("aaa"),
		RainbowAction(), None, ModifierAction("bbb"),
		RainbowAction(), None, ModifierAction("ccc")
	]
