import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

import wave

class Wave:

    """
    A class to represent an audio wave, allowing generation from signals or files, normalization, and playback.
    Use for one-shot playback application or file loading, not real-time synthesis.
    """

    def __init__(self, wave: np.ndarray = np.array([]), sample_rate: int = 44100):
        self.wave = wave
        self.sample_rate = sample_rate

    def generate_from_signal(self, signal, duration):

        """Generate a wave of length duration from a given signal object."""

        t = np.arange(0, duration, 1/self.sample_rate)
        self.wave = np.array([signal.evaluate(ti) for ti in t])
        self.normalize()

    def generate_from_file(self, file_path):

        """Generate a wave from an audio file."""

        with wave.open(file_path, 'rb') as wf:
            self.sample_rate = wf.getframerate()
            n_frames = wf.getnframes()
            audio_data = wf.readframes(n_frames)
            self.wave = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            self.normalize()

    def normalize(self):
        
        """Normalize the wave to the range [-1, 1] to prevent clipping during playback."""
        
        max_amp = np.max(np.abs(self.wave))
        if max_amp > 0:
            self.wave = self.wave / max_amp

    def visualize(self):
        
        t = np.arange(0, len(self.wave) / self.sample_rate, 1/self.sample_rate)

        plt.plot(t, self.wave)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Signal Visualization')
        plt.grid()
        plt.show()

    def spectrogram(self, window_size=1024, hop_size=512):

        """Generate a spectrogram of the wave using the specified parameters."""

        samples = self.wave  # your Wave class should store this as a 1D numpy array

        # Window function (Hann is standard)
        window = np.hanning(window_size)

        # Number of windows
        num_windows = 1 + (len(samples) - window_size) // hop_size

        # Prepare output matrix
        spec = np.zeros((num_windows, window_size // 2 + 1), dtype=np.float32)

        # Compute STFT
        for i in range(num_windows):
            start = i * hop_size
            frame = samples[start:start + window_size] * window
            fft = np.fft.rfft(frame)
            spec[i, :] = np.abs(fft)

        # Time and frequency axes
        times = np.arange(num_windows) * (hop_size / self.sample_rate)
        freqs = np.fft.rfftfreq(window_size, 1/self.sample_rate)

        plt.figure(figsize=(10, 6))
        plt.imshow(
            spec.T,
            origin='lower',
            aspect='auto',
            extent=[times[0], times[-1], freqs[0], freqs[-1]],
            cmap='magma'
        )
        plt.yscale('log')
        plt.ylim(freqs[1], freqs[-1])
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.title("Spectrogram")
        plt.colorbar(label="Magnitude")
        plt.show()

        
    def playback(self, master_volume=.2):

        """Play the wave using the specified master volume."""

        sd.play(self.wave * master_volume, samplerate=self.sample_rate, blocksize=2048)
        sd.wait()