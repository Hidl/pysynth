from signal import Signal, SineOsc

a = Signal(SineOsc(440))
b = Signal(SineOsc(880))
c = a + b

c.visualize()