from oscillators import SineOsc, SquareOsc, SawtoothOsc

class PhaseAccumulator:
    """Simple phase accumulators."""
    def __init__(self, freq, sample_rate=44100, oscillator=SineOsc):
        self.freq = freq
        self.sample_rate = sample_rate
        self.phase = 0.0
        self.oscillator = oscillator()
    
    def next_sample(self):
        """Calculate the next sample value and update the phase."""
        dt = self.freq / self.sample_rate
        value = self.oscillator(self.phase, dt)
        self.phase += dt
        if self.phase > 1.0:
            self.phase -= 1.0
        return value
    
    