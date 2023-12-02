import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

WHITE = 0xFFFFFF
BLACK = 0x000000
LH = 12


class Grid:
	def __init__(self, macropad):
		display = macropad.display

		KEY_COUNT = macropad.keys.key_count
		W = display.width
		H = display.height
		COLS = 3

		group = displayio.Group()
		buttons = []
		for key_index in range(KEY_COUNT):
			x = key_index % COLS
			y = key_index // COLS
			bottom_offset = (3 - y) * (LH + 1)
			key = label.Label(terminalio.FONT, color=WHITE, anchored_position=(W * x/2, H - bottom_offset), anchor_point=(x/2, 1))
			group.append(key)
			buttons.append(key)

		group.append(Rect(0, 0, W, LH, fill=WHITE))

		title = label.Label(terminalio.FONT, color=BLACK, anchored_position=(W//2, 0), anchor_point=(0.5, 0))
		group.append(title)

		arrows = [
			label.Label(terminalio.FONT, color=BLACK, anchored_position=(0, 0), anchor_point=(0, 0)),
			label.Label(terminalio.FONT, color=BLACK, anchored_position=(W, 0), anchor_point=(1, 0))
		]
		group.append(arrows[0])
		group.append(arrows[1])

		display.root_group = group

		self.display = display
		self.nodes = {
			"buttons": buttons,
			"arrows": arrows,
			"title": title
		}

	@property
	def buttons(self):
		return self.nodes["buttons"]

	def show_arrows(self):
		arrows = self.nodes["arrows"]
		arrows[0].text = "<<"
		arrows[1].text = ">>"

	def hide_arrows(self):
		arrows = self.nodes["arrows"]
		arrows[0].text = ""
		arrows[1].text = ""

	def invert_on(self, index: int):
		node = self.nodes["buttons"][index]
		node.color = BLACK
		node.background_color = WHITE

	def invert_off(self, index: int):
		node = self.nodes["buttons"][index]
		node.color = WHITE
		node.background_color = BLACK

	@property
	def title(self):
		return self.nodes["title"].text

	@title.setter
	def title(self, title: string):
		self.nodes["title"].text = title
