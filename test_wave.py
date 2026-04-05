from pywave import Wave
from pysignalsignal import Signal, Sine, Triangle, Square, Sawtooth

import numpy as np


# Synth a simple wave consisting of two sine waves
a = Signal(Sine(440))
b = Signal(Sine(660))
c = a + b

c.visualize()
w = Wave()
w.generate_from_signal(c, duration=2)
w.spectrogram()
w.playback()


# Load a wave from a file
w = Wave()
w.generate_from_file('sounds/ASax-ord-C4-ff-N-N.wav')
w.spectrogram()
w.playback()


# Synth a triangle wave
a = Signal(Triangle(440))
a.visualize()
w = Wave()
w.generate_from_signal(a, duration=2)
w.visualize()
w.spectrogram()
w.playback(0.2)


# Syth a square wave
a = Signal(Square(440))
a.visualize()
w = Wave()
w.generate_from_signal(a, duration=2)
w.visualize()
w.spectrogram()
w.playback(0.2)


# Syth a sawtooth wave
a = Signal(Sawtooth(440))
a.visualize()
w = Wave()
w.generate_from_signal(a, duration=2)
w.visualize()
w.spectrogram()
w.playback(0.2)
