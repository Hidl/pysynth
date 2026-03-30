from wave import Wave
from signal import Signal, SineOsc

import numpy as np

a = Signal(SineOsc(440))
b = Signal(SineOsc(660))
c = a + b

w = Wave()
w.generate_from_signal(c, duration=2)
w.spectrogram()