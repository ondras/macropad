class AbsoluteMouse:
	LEFT_BUTTON = 1
	RIGHT_BUTTON = 2
	MIDDLE_BUTTON = 4

	def __init__(self, device) -> None:
		self._mouse_device = device
		self.report = bytearray(6)


	def press(self, buttons: int) -> None:
		self.report[0] |= buttons
		self._send_no_move()

	def release(self, buttons: int) -> None:
		self.report[0] &= ~buttons
		self._send_no_move()

	def release_all(self) -> None:
		self.report[0] = 0
		self._send_no_move()

	def click(self, buttons: int) -> None:
		self.press(buttons)
		self.release(buttons)

	def move(self, x: int = 0, y: int = 0, wheel: int = 0) -> None:
		"""Move the mouse and turn the wheel as directed.
		:param x: Set pointer on x axis. 32767 = 100% to the right
		:param y: Set pointer on y axis. 32767 = 100% to the bottom
		:param wheel: Rotate the wheel this amount. Negative is toward the user, positive
			is away from the user. The scrolling effect depends on the host.
		"""

		while wheel != 0:
			partial_wheel = self._limit(wheel)
			self.report[5] = partial_wheel & 0xFF
			self._mouse_device.send_report(self.report)
			wheel -= partial_wheel

		x = self._limit_coord(x)
		y = self._limit_coord(y)
		x1, x2 = x.to_bytes(2, "little")
		y1, y2 = y.to_bytes(2, "little")
		self.report[1] = x1
		self.report[2] = x2
		self.report[3] = y1
		self.report[4] = y2
		self._mouse_device.send_report(self.report)

	def _send_no_move(self) -> None:
		self.report[1] = 0
		self.report[2] = 0
		self.report[3] = 0
		self.report[4] = 0
		self._mouse_device.send_report(self.report)

	@staticmethod
	def _limit(dist: int) -> int:
		return min(127, max(-127, dist))

	@staticmethod
	def _limit_coord(coord):
		return min(32767, max(0, coord))