from pynput import keyboard
import sounddevice as sd
import time
import math

from oscillators import SineOsc, SquareOsc, SawtoothOsc
from voice import Voice

key_mapping = {
    'a': 440,     # A4
    'w': 466.16,  # A#4/Bb4
    's': 493.88,  # B4
    'd': 523.25,  # C5
    'r': 554.37,  # C#5/Db5
    'f': 587.33,  # D5
    't': 622.25,  # D#5/Eb5
    'g': 659.25,  # E5
    'h': 698.46,  # F5
    'u': 739.99,  # F#5/Gb5
    'j': 783.99,  # G5
    'i': 830.61   # G#5/Ab5
}

octave_shift = 0
active_voices = {} # key: Voice instance - this allows us to manage multiple simultaneous notes and their envelopes
keys_down = set() # track currently pressed keys to prevent retriggering on holding down a key
gain = 0.2 # lower gain to prevent clipping when multiple notes are played together

def on_press(key):
    try:
        # Exit on ESC
        if key == keyboard.Key.esc:
            global running
            running = False

        # Octave shift with arrow keys
        elif key == keyboard.Key.up:
            global octave_shift
            octave_shift += 1
            print(f"Octave shift: {octave_shift}")
        elif key == keyboard.Key.down:
            octave_shift -= 1
            print(f"Octave shift: {octave_shift}")

        # Handle note keys
        else:
            k = key.char
            global active_voices, keys_down
            if k in key_mapping and k not in keys_down:
                keys_down.add(k)
                freq = key_mapping[k] * (2 ** octave_shift)
                print(f"Playing frequency: {freq} Hz")
                
                active_voices[k] = Voice(freq, oscillator=SineOsc)

    except Exception as e:
        print("Error in on_press:", e)

def on_release(key):
    try:        
        k = key.char
        global active_voices, keys_down
        if k in keys_down:
            print(f"Key released: {k}")
            active_voices[k].env.trigger_release()
            keys_down.remove(k)
    
    except Exception as e:
        print("Error in on_release:", e)
    

def audio_callback(outdata, frames, time, status):
    global active_voices
    outdata[:] = 0.0
    for i in range(frames):
        for key, v in list(active_voices.items()):
            if not v.active:
                del active_voices[key]
                continue
            sample = v.next_sample() * gain
            sample = math.tanh(sample)
            outdata[i, 0] += sample
        

# Start listening to keyboard events
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

stream = sd.OutputStream(
    channels=1,
    samplerate=44100,
    callback=audio_callback
)
stream.start()
    
running = True
while running:
    time.sleep(0.1)

listener.stop()
stream.stop()
