# macropad
My [Adafruit Macropad](https://www.adafruit.com/product/5128) setup. Written in CircuitPython. Clone and copy files to your CircuitPython drive.

## Dependencies

Put these into `lib/`:

```
adafruit_display_shapes/
adafruit_display_text/
adafruit_hid/
adafruit_midi/
asyncio/
adafruit_debouncer.mpy
adafruit_macropad.mpy
adafruit_simple_text_display.mpy
adafruit_ticks.mpy
colorsys.mpy
neopixel.mpy
```

## Features / apps

Switch individual apps by holding button #2 (top-right) and rotating the rotary encoder.

### Desktop

<img src="https://github.com/ondras/macropad/assets/192172/b3b8eb26-a0cc-4f9a-b0e3-dc2a237a3622" width="400" />

Contains keyboard shortcuts, mostly for `git` workflows. Rotary encoder adjusts volume.

### DaVinci Color

<img src="https://github.com/ondras/macropad/assets/192172/88967621-0ff0-43a2-8a7a-371ef88b7e3f" width="400" />

Used for color grading in DaVinci Resolve. Hold modifier keys (Lift / Gamma / Gain / Offset / Saturation) and rotate the rotary encoder. Hold down both a modifier *and* a color key to perform the adjustment on one color channel.

**Note:** There is no API to control DaVinci Resolve. To circumvent this, the macropad acts as an *absolute mouse hid device* and fakes mouse movement; to move individual sliders, this virtual cursor moves to their pre-computed position. This means that the functionality is dependent on:

  - screen size (`SCREEN` in `davinci.py`)
  - taskbar height (`TASKBAR` in `davinci.py`)
  - the willingness of your OS to accept an absolute mouse hid device (tested on W11 only)

### MIDI Tones

<img src="https://github.com/ondras/macropad/assets/192172/c730dd72-af87-4e8f-b844-8f079e631820" width="400" />

Play individual MIDI notes. Rotary encoder adjusts octave. Scales are always C-based; use software (such as [midi-juggler](https://ondras.github.io/midi-juggler/)) to transpose. Top-center button can be used to switch scales:

  - harmonic major
  - natural minor
  - major/minor pentatonic
  - major/minor blues hexatonic

### MIDI Chords

<img src="https://github.com/ondras/macropad/assets/192172/6ab730cd-6dca-4f83-a637-4c237fdbdfac" width="400" />

Play MIDI chord triads. Rotary encoder adjusts octave.

### Elite: Dangerous

<img src="https://github.com/ondras/macropad/assets/192172/ca8fc3df-7806-4a19-9f4d-bc126bc767ba" width="400" />

Some useful keyboard shortcuts: FSD, FSS, Galaxy/system map, Ship lights/nightvision, Cold running, Cargo scoop, Landing gear
