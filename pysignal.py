import matplotlib.pyplot as plt
import numpy as np

class Signal:
    """
    Signal class to represent a signal: (a) mathematical function(s) that represents sound. 
    It can be evaluated at any point in time.
    It can be any number of mathematical functions, which will be added at evaluate.
    """

    def __init__(self, *functions):
        self.functions = functions

    def __add__(self, other):
        self.functions += other.functions
        return self

    def evaluate(self, t):
        return sum(f(t) for f in self.functions)
    
    def visualize(self, period = 1/60, fs = 44100):
        
        t = np.arange(0, period, 1/fs)
        y = [self.evaluate(ti) for ti in t]

        plt.plot(t, y)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Signal Visualization')
        plt.grid()
        plt.show()

class Sine:
    """Simple sine wave oscillator."""
    def __init__(self, freq, amp=1.0):
        self.freq = freq
        self.amp = amp

    def __call__(self, t):
        return self.amp * np.sin(2 * np.pi * self.freq * t)

class Triangle:
    """Simple triangle wave oscillator."""
    def __init__(self, freq, amp=1.0):
        self.freq = freq
        self.amp = amp

    def __call__(self, t):
        return self.amp * (2/np.pi) * np.arcsin(np.sin(2*np.pi*self.freq*t))
    
class Square:
    """Simple square wave oscillator."""
    def __init__(self, freq, amp=1.0):
        self.freq = freq
        self.amp = amp

    def __call__(self, t):
        return self.amp * np.sign(np.sin(2 * np.pi * self.freq * t))
    
class Sawtooth:
    """Simple sawtooth wave oscillator."""
    def __init__(self, freq, amp=1.0):
        self.freq = freq
        self.amp = amp

    def __call__(self, t):
        return self.amp * (2 * (t * self.freq - np.floor(0.5 + t * self.freq)))
