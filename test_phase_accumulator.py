import numpy as np
import matplotlib.pyplot as plt
from phase_accumulator import PhaseAccumulator
from oscillators import SineOsc, SquareOsc, SawtoothOsc, TriangleOsc
from pywave import Wave

def test_phase_accumulator():
    # Generate a signal and visualize
    
    sample_rate = 44100
    duration = 0.01  # seconds
    freq = 440  # A4 note
    
    # Create phase accumulators for different oscillators
    sine_acc = PhaseAccumulator(freq, sample_rate, SineOsc)
    square_acc = PhaseAccumulator(freq, sample_rate, SquareOsc)
    saw_acc = PhaseAccumulator(freq, sample_rate, SawtoothOsc)
    triangle_acc = PhaseAccumulator(freq, sample_rate, TriangleOsc)
    
    # Generate samples
    sine_samples = [sine_acc.next_sample() for _ in range(int(sample_rate * duration))]
    square_samples = [square_acc.next_sample() for _ in range(int(sample_rate * duration))]
    saw_samples = [saw_acc.next_sample() for _ in range(int(sample_rate * duration))]
    triangle_samples = [triangle_acc.next_sample() for _ in range(int(sample_rate * duration))]
    
    # Plot the waveforms
    time = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(4, 1, 1)
    plt.title("Sine Wave")
    plt.plot(time, sine_samples)
    
    plt.subplot(4, 1, 2)
    plt.title("Square Wave")
    plt.plot(time, square_samples)
    
    plt.subplot(4, 1, 3)
    plt.title("Sawtooth Wave")
    plt.plot(time, saw_samples)
    
    plt.subplot(4, 1, 4)
    plt.title("Triangle Wave")
    plt.plot(time, triangle_samples)
    
    plt.tight_layout()
    plt.show()

def test_phase_accumulator2():
    # Generate signal and visualize spectogram
    sample_rate = 44100
    duration = 0.1  # seconds
    freq = 440  # A4 note

    square_acc = PhaseAccumulator(freq, sample_rate, SquareOsc)
    square_samples = [square_acc.next_sample() for _ in range(int(sample_rate * duration))]
    w = Wave(wave = square_samples, sample_rate=sample_rate)
    w.spectrogram()

if __name__ == "__main__":
    test_phase_accumulator2()
