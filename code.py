from adafruit_macropad import MacroPad
import asyncio
import usb_hid

from apps.app import MainApp
from apps.davinci import DavinciColor
from apps.desktop import Desktop
from apps.metronome import Metronome
from apps.demo import Demo
from apps.midi import MidiTones, MidiChords

from grid import Grid
from absolute_mouse import AbsoluteMouse

macropad = MacroPad()

def sleep():
	macropad.display_sleep = True
	macropad.pixels.brightness = 0.0

def resume():
	macropad.display_sleep = False
	macropad.pixels.brightness = 0.5

resume()

grid = Grid(macropad)
macropad.grid = grid
macropad.absolute_mouse = AbsoluteMouse(usb_hid.devices[3])
app = MainApp(macropad, [Desktop, Demo, MidiTones, MidiChords, DavinciColor])


async def loop_inputs():
	last_encoder = macropad.encoder

	while True:
		macropad.encoder_switch_debounced.update()
		if macropad.encoder_switch_debounced.pressed:
			if macropad.display_sleep:
				resume()
			else:
				sleep()

		midi_msg = macropad.midi.receive()
		if midi_msg:
			app.on_midi(midi_msg)

		event = macropad.keys.events.get()
		if event:
			key = event.key_number
			app.on_press(key) if event.pressed else app.on_release(key)

		diff = macropad.encoder - last_encoder
		if diff != 0:
			last_encoder = macropad.encoder
			app.on_rotate(diff)

		await asyncio.sleep(0)

#async def main():
#	await asyncio.gather(loop_inputs())

asyncio.run(loop_inputs())
