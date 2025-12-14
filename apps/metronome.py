from action import ModifierAction
from .app import App
import asyncio


def stop_tone(macropad):
	if macropad._sample is not None and macropad._sample.playing:
		macropad._sample.stop()
#		macropad._sample.deinit()
#		macropad._sample = None


def start_tone(macropad, frequency):
	if not macropad._speaker_enable.value:
		macropad._speaker_enable.value = True
	length = 100
	if length * frequency > 350000:
		length = 350000 // frequency
	macropad._generate_sample(length)
	# Start playing a tone of the specified frequency (hz).
	macropad._sine_wave_sample.sample_rate = int(len(macropad._sine_wave) * frequency)
	if not macropad._sample.playing:
		macropad._sample.play(macropad._sine_wave_sample, loop=True)


class Metronome(App):
	label = "Metronome"
	button_actions = [
		None, None, None,
		None, None, ModifierAction("aaa"),
		None, None, ModifierAction("bbb"),
		None, None, ModifierAction("ccc")
	]

	def __init__(self, macropad):
		super().__init__(macropad)
		self.task = None

	def activate(self):
		super().activate()
		self.task = asyncio.create_task(self.loop())

	def deactivate(self):
		if self.task:
			self.task.cancel()
			self.task = None

	async def loop(self):
		macropad = self.macropad
		sound_delay = 0.5

		while True:
			#macropad.start_tone(800)
			start_tone(macropad, 800)
			await asyncio.sleep(sound_delay)
			macropad.pixels.fill(0xffffff)
			#macropad.stop_tone()
			stop_tone(macropad)
			await asyncio.sleep(1.6 - sound_delay)
			macropad.pixels.fill(0x000000)
