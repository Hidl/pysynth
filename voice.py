from oscillators import SineOsc, SquareOsc, SawtoothOsc
from phase_accumulator import PhaseAccumulator

class Voice:
    """
    Represents a single note being played.
    Takes a frequency and an optional oscillator type (default is SineOsc).
    Manages its own phase accumulator and ADSR envelope.
    """
    def __init__(self, freq, sample_rate=44100, oscillator=SineOsc):
        self.sample_rate = sample_rate
        self.phase_accumulator = PhaseAccumulator(freq, sample_rate, oscillator)
        self.env = ADSREnvelope(sample_rate=sample_rate)
        self.active = True

        # When a voice is created, we trigger the envelope to start the attack phase
        self.env.trigger()

    def next_sample(self):
        # Generate the next sample value based on the oscillator and envelope
        if self.active:
            value = self.phase_accumulator.next_sample()
            amp = self.env.next_value()
            value *= amp

            # Marking idle voices as inactive allows for garbage collection in the main audio loop
            if amp <= 0.0 and self.env.state == "idle":
                self.active = False
                return 0.0
            
            return value
        else:
            return 0.0
        
class ADSREnvelope:
    """Simple ADSR envelope generator."""
    def __init__(self, attack=0.01, decay=0.1, sustain=0.7, release=0.5, sample_rate=44100):
        self.attack = attack # in seconds
        self.decay = decay # in seconds
        self.sustain = sustain # level (0 to 1)
        self.release = release # in seconds
        self.sample_rate = sample_rate
        self.state = 'idle'
        self.time = 0 # in samples
        self.level = 0.0
        self.release_from = self.sustain

    def trigger(self):
        self.state = 'attack'
        self.time = 0

    def trigger_release(self):
        if self.state != 'idle':
            self.state = 'release'
            self.release_from = self.level
            self.time = 0

    def next_value(self):
        if self.state == 'attack':
            self.level = min(1.0, self.time / (self.attack * self.sample_rate))
            if self.level >= 1.0:
                self.state = 'decay'
                self.time = 0
        
        elif self.state == 'decay':
            self.level = 1.0 - (1.0 - self.sustain) * (self.time / (self.decay * self.sample_rate))
            if self.level <= self.sustain:
                self.state = 'sustain'
        
        elif self.state == 'sustain':
            self.level = self.sustain
        
        elif self.state == 'release':
            self.level = max(0.0, (self.release_from * (1.0 - (self.time / (self.release * self.sample_rate)))))
            if self.level <= 0.0:
                self.state = 'idle'
        
        else:
            self.level = 0.0
        
        self.time += 1
        return self.level