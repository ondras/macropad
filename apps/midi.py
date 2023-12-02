from action import ModifierAction
from .app import App, MainApp


BASE = 24
OCTAVE = 3
NOTE_NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "H")
TRIAD_MAJOR = (0, 4, 7)
TRIAD_MINOR = (0, 3, 7)
TRIADS_ARE_MAJOR = (1, 0, 0, 1, 1, 0, 0)

SCALE_CHROMATIC = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
SCALE_MAJOR = (0, 2, 4, 5, 7, 9, 11)
SCALE_MINOR = (0, 2, 3, 5, 7, 8, 10)
SCALE_MAJOR_PENTATONIC = (0, 2, 4, 7, 9)
SCALE_MINOR_PENTATONIC = (0, 3, 5, 7, 10)
SCALE_MAJOR_BLUES_HEXATONIC = (0, 2, 3, 4, 7, 9)
SCALE_MAJOR_BLUES_HEXATONIC = (0, 2, 3, 4, 7, 9)
SCALE_MINOR_BLUES_HEXATONIC = (0, 3, 5, 6, 7, 10)

SCALES = [
	{"label":"Chromatic", "scale":SCALE_CHROMATIC},
	{"label":"Major", "scale":SCALE_MAJOR},
	{"label":"Minor", "scale":SCALE_MINOR},
	{"label":"Major 5", "scale":SCALE_MAJOR_PENTATONIC},
	{"label":"Minor 5", "scale":SCALE_MINOR_PENTATONIC},
	{"label":"Major b6", "scale":SCALE_MAJOR_BLUES_HEXATONIC},
	{"label":"Minor b6", "scale":SCALE_MINOR_BLUES_HEXATONIC},
]


def get_midi_note(scale_note, scale):
	overflow = scale_note // len(scale)
	octave = OCTAVE + overflow
	return BASE + 12*octave + scale[scale_note % len(scale)]


def get_midi_notes(scale_note, scale):
	definition = TRIAD_MAJOR if TRIADS_ARE_MAJOR[scale_note] else TRIAD_MINOR
	return [get_midi_note(scale_note, SCALE_MAJOR) + offset for offset in definition]


class MidiChords(App):
	label = "MIDI Chords"
	button_map = [
		None, None, None,
		6, None, None,
		3, 4, 5,
		0, 1, 2
	]

	def __init__(self, macropad):
		super().__init__(macropad)
		self.playing = {}

	def activate(self):
		grid = self.macropad.grid
		px = self.macropad.pixels

		for i, scale_note in enumerate(self.button_map):
			if scale_note is None:
				grid.buttons[i].text = ""
				px[i] = 0x000000
				continue

			chromatic_note = SCALE_MAJOR[scale_note]
			type = "maj" if TRIADS_ARE_MAJOR[scale_note] else "min"
			grid.buttons[i].text = f"{NOTE_NAMES[chromatic_note]}{type}"
			px[i] = 0x00ff00 if TRIADS_ARE_MAJOR[scale_note] else 0xff0000

		self.update_octave()

	def on_press(self, index: int):
		scale_note = self.button_map[index]
		if scale_note is None: return

		midi_notes = get_midi_notes(scale_note, SCALE_MAJOR)
		self.note_on(midi_notes)

	def on_release(self, index: int):
		scale_note = self.button_map[index]
		if scale_note is None: return

		midi_notes = get_midi_notes(scale_note, SCALE_MAJOR)
		self.note_off(midi_notes)

	def note_on(self, midi_notes):
		noteons = []
		for note in midi_notes:
			if note in self.playing:
				self.playing[note] += 1
			else:
				self.playing[note] = 1
				noteons.append(self.macropad.NoteOn(note))
		self.macropad.midi.send(noteons)

	def note_off(self, midi_notes):
		noteoffs = []
		for note in midi_notes:
			count = self.playing[note]
			if count > 1:
				self.playing[note] -= 1
			else:
				self.playing.pop(note)
				noteoffs.append(self.macropad.NoteOff(note))
		self.macropad.midi.send(noteoffs)

	def on_rotate(self, diff:int):
		adjust_octave(diff)
		self.update_octave()

	def update_octave(self):
		self.macropad.grid.title = f"{self.label} o{OCTAVE}"


class MidiTones(App):
	label = "MIDI Tones"
	scale_index = 0
	scale_button = 1
	button_map = [
		9, None, None,
		6, 7, 8,
		3, 4, 5,
		0, 1, 2
	]

	def __init__(self, macropad):
		super().__init__(macropad)
		self.scale_modifier = ModifierAction("")

	@property
	def scale(self):
		return SCALES[self.scale_index]["scale"]

	@scale.setter
	def scale(self, scale_index):
		self.scale_index = scale_index
		self.update_labels()

	def activate(self):
		self.scale = 1
		self.update_octave()

	def update_labels(self):
		grid = self.macropad.grid
		px = self.macropad.pixels
		scale = self.scale

		for i, scale_note in enumerate(self.button_map):
			if i == MainApp.button_index: continue

			if i == self.scale_button:
				grid.buttons[i].text = SCALES[self.scale_index]["label"]
				px[i] = 0x0000ff
				continue

			if scale_note is None:
				grid.buttons[i].text = ""
				px[i] = 0x000000
				continue

			chromatic_note = scale[scale_note % len(scale)]
			grid.buttons[i].text = f"{NOTE_NAMES[chromatic_note]}"
			overflow = scale_note // len(scale)
			px[i] = 0x00ff00 if overflow == 0 else 0xff0000


	def on_press(self, index: int):
		if index == self.scale_button:
			self.scale_modifier.on_press(self, index)
			return

		scale_note = self.button_map[index]
		if scale_note is None: return

		midi_note = get_midi_note(scale_note, self.scale)
		macropad = self.macropad
		macropad.midi.send(macropad.NoteOn(midi_note))

	def on_release(self, index: int):
		if index == self.scale_button:
			self.scale_modifier.on_release(self, index)
			return

		scale_note = self.button_map[index]
		if scale_note is None: return

		midi_note = get_midi_note(scale_note, self.scale)
		macropad = self.macropad
		macropad.midi.send(macropad.NoteOff(midi_note))

	def on_rotate(self, diff:int):
		if self.scale_modifier.active:
			self.scale = (self.scale_index + diff) % len(SCALES)
			return

		adjust_octave(diff)
		self.update_octave()

	def update_octave(self):
		self.macropad.grid.title = f"{self.label} o{OCTAVE}"


def adjust_octave(diff: int):
	global OCTAVE
	OCTAVE = clamp(OCTAVE+diff, 0, 7)

def clamp(val, min_, max_):
	return min(max(val, min_), max_)
