import time
import math
import threading

import sounddevice as sd

from oscillators import SineOsc
from voice import Voice

note_mapping = {
    'A': 440,
    'A#': 466.16,
    'B': 493.88,
    'C': 523.25,
    'C#': 554.37,
    'D': 587.33,
    'D#': 622.25,
    'E': 659.25,
    'F': 698.46,
    'F#': 739.99,
    'G': 783.99,
    'G#': 830.61
}

class SequencerClock(threading.Thread):
    def __init__(self, bpm, callback):
        super().__init__()
        self.bpm = bpm
        self.step_time = 60.0 / bpm
        self.callback = callback
        self.running = False

    def run(self):
        self.running = True
        next_time = time.perf_counter()

        while self.running:
            now = time.perf_counter()
            if now >= next_time:
                self.callback()  # trigger sequencer step
                next_time += self.step_time
            else:
                time.sleep(0.0005)  # tiny sleep to reduce CPU load

    def stop(self):
        self.running = False

class Step:
    """A step class to handle chords and single notes in a unified way."""
    def __init__(self, notes, duration=1.0):
        self.notes = [i[0:-1] for i in notes] # Extract note names without octave, e.g. "C4" -> "C"
        self.octave = [int(i[-1]) - 4 for i in notes] # Extract octave from note names, e.g. "C4" -> "4"
        self.duration = duration # [0, 1] where 1 is a whole note, 0.5 is a half note, etc.

class Loop:
    """A simple loop class to manage repeating sequences."""
    def __init__(self, size = 4, bpm = 120, sequence = None):
        self.size = size
        self.index = 0
        self.bpm = bpm
        self.steplength = 60 / bpm # in seconds
        self.data = sequence if sequence is not None else [Step(["C3"])] * size
    
    def step(self):
        event = self.data[self.index]
        self.index = (self.index + 1) % self.size
        return event
    # Sequence will be a list (of lists) of note names or Chord instances, one per step
    # The inner list increases the tempo of the notes, so [["C3", "C3", "C3"], [], [], []] will first play a triple C3, then rest for 3 steps
    # Chord instances can be used to play multiple notes at once, so [Chord(["C3", "E3", "G3"]), [], [], []] will play a C major chord on the first step, then rest for 3 steps

def main():

    sequence = [
        Step(["C4", "E4", "G4"], duration=1.0), # C major chord for 1 whole note
        Step(["D4"], duration=0.5), # D4 for 1 half note
        Step(["E3"], duration=0.5), # E3 for 1 half note
        Step(["F3", "A3"], duration=1.0), # F3 and A3 together for 1 whole note
    ]

    loop = Loop(size=4, bpm=120, sequence=sequence)
    active_voices = [] # This will hold currently active voices so we can manage their lifetimes

    def on_step():
        step = loop.step()
        
        for i, note in enumerate(step.notes):
            freq = note_mapping.get(note, 440) * (2 ** step.octave[i])
            voice = Voice(freq, oscillator=SineOsc)
            active_voices.append(voice)
            release_time = step.duration * loop.steplength
            threading.Timer(release_time, voice.env.trigger_release).start()
        

    clock = SequencerClock(loop.bpm, on_step)

    def audio_callback(outdata, frames, time, status):
        outdata[:] = 0.0
        for i in range(frames):
            for v in active_voices:
                if not v.active:
                    continue
                sample = v.next_sample() * 0.2
                sample = math.tanh(sample)
                outdata[i, 0] += sample
        active_voices[:] = [v for v in active_voices if v.active]

    stream = sd.OutputStream(
        channels=1,
        samplerate=44100,
        callback=audio_callback
    )

    clock.start()
    stream.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        clock.stop()
        stream.stop()
        stream.close()

if __name__ == "__main__":
    main()