import numpy as np

def poly_blep(t, dt):

    if t < dt:
        # left edge
        t /= dt
        return t + t - t*t - 1.0

    elif t > 1.0 - dt:
        # right edge
        t = (t - 1.0) / dt
        return t*t + t + t + 1.0

    else:
        return 0.0
    
def poly_blamp(t, dt):
    if t < dt:
        t /= dt
        return t*t*(t/3 - 1/2) + 1/6

    elif t > 1.0 - dt:
        t = (t - 1.0) / dt
        return t*t*(t/3 + 1/2) + 1/6

    else:
        return 0.0
        
class SineOsc():
    """Simple sine wave oscillator."""
    # dt is ignored for sine wave, but we include it for consistency with other oscillators
    def __call__(self, phase, dt):
        return np.sin(2 * np.pi * phase)
    
class SquareOsc():
    """Simple square wave oscillator."""
    def __call__(self, phase, dt):
        value = 1.0 if phase < 0.5 else -1.0
        value += poly_blep(phase, dt)
        value -= poly_blep((phase - 0.5) % 1, dt)
        return value

class SawtoothOsc():
    """Simple sawtooth wave oscillator."""
    def __call__(self, phase, dt):
        value = 2.0 * phase - 1.0
        value -= poly_blep(phase, dt)
        return value
    
class TriangleOsc():
    """Simple triangle wave oscillator."""
    def __call__(self, phase, dt):
        value = 4.0 * abs(phase - 0.5) - 1.0
        value -= poly_blamp(phase, dt)
        value += poly_blamp((phase - 0.5) % 1, dt)
        return value