######################################################
# this file is home to all the logic that is used by
# Musical Key Finder to analyze music using the CREPE
# neural network and determine what key a certain sample
# is in.
#
#   Author: Dylan Miessner
######################################################

# handle some imports
import crepe # pretrained pitch prediction model
from scipy.io import wavfile # to use wavfiles with crepe
import wave # to record wav files
from scipy.io.wavfile import write
import sounddevice as sd # to access microphone and utilize audio files
import numpy as np
import soundfile as sf # play back audio files
from math import log2, pow
import collections

np.seterr(divide='ignore', invalid='ignore')

# function to handle recording audio and saving it to a temp folder.
def record_audio(filename):
    fs = 44100  # Sample rate
    seconds = 10  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, myrecording)  # Save as WAV file 
    write('./wav_recordings/output.wav', fs, myrecording)

# uses the crepe prediction model to determine the frequencies and graph a plot
def analyze_audio(filename):
    sr, audio = wavfile.read(filename)
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
    crepe.process_file(filename, output='./recording_analysis', save_plot=True, save_activation=True, plot_voicing=True)

    notes = determine_notes(frequency, confidence)
    key = determine_key(notes)

    return key

def play_audio(filename):
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    # status = sd.wait()

def determine_notes(frequency, confidence):
    A4 = 440
    C0 = A4*pow(2, -4.75)
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    notes_in_sample = []
    i = 0
    for frequencies in frequency:
        if confidence[i] >= 0.92:
            h = round(12*log2(frequencies/C0))
            octave = h // 12
            n = h % 12
            notes_in_sample.append(notes[n] + str(octave))

        i+=1

    return notes_in_sample

def determine_key(notes):
    # first step is create a set of your notes
    note_set = list(set(notes))

    # after that you need to clean the string to make sure it is sorted
    # and that the octaves are removed, because we no longer care about them
    i = 0
    for note in note_set:
        note_set[i] = note[:-1]
        i+=1
    
    note_set = list(set(note_set))
    note_set.sort()
    print(note_set)

    # the follow is hardcoded lists of what a key should contain, which are then
    # checked against our, now clean, list of notes
    key = 'Unknown, please record a clearer sample, or contact Dylan Miessner'

    C = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    D = ['A', 'B', 'C#', 'D', 'E', 'F#', 'G']
    E = ["A", "B", "C#", "D#", "E", "F#", "G#"]
    F = ["A", "A#", "C", "D", "E", "F", "G"]
    G = ["A", "B", "C", "D", "E", "F#", "G"]
    A = ["A", "B", "C#", "D", "E", "F#", "G#"]
    B = ["A#", "B", "C#", "D#", "E", "F#", "G#"]
    Csharp = ["A#", "C", "C#", "D#", "F", "F#", "G#"]
    Dsharp = ["A#", "C", "D", "D#", "F", "G", "G#"]
    Fsharp = ["A#", "B", "C#", "D#", "F", "F#", "G#"]
    Gsharp = ["A#", "C", "C#", "D#", "F", "G","G#"]
    Asharp = ["A", "A#", "C", "D", "D#", "F", "G"]
    Chromatic = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']


    if collections.Counter(note_set) == collections.Counter(C) or set(note_set).issubset(set(C)):
        key = "C"

    elif collections.Counter(note_set) == collections.Counter(D) or set(note_set).issubset(set(D)):
        key = "D"

    elif collections.Counter(note_set) == collections.Counter(E) or set(note_set).issubset(set(E)):
        key = "D"

    elif collections.Counter(note_set) == collections.Counter(F) or set(note_set).issubset(set(F)):
        key = "F"

    elif collections.Counter(note_set) == collections.Counter(G) or set(note_set).issubset(set(G)):
        key = "G"

    elif collections.Counter(note_set) == collections.Counter(A) or set(note_set).issubset(set(A)):
        key = "A"

    elif collections.Counter(note_set) == collections.Counter(B) or set(note_set).issubset(set(B)):
        key = "B"

    elif collections.Counter(note_set) == collections.Counter(Csharp) or set(note_set).issubset(set(Csharp)):
        key = "C#"

    elif collections.Counter(note_set) == collections.Counter(Dsharp) or set(note_set).issubset(set(Dsharp)):
        key = "D#"

    elif collections.Counter(note_set) == collections.Counter(Fsharp) or set(note_set).issubset(set(Fsharp)):
        key = "F#"

    elif collections.Counter(note_set) == collections.Counter(Gsharp) or set(note_set).issubset(set(Gsharp)):
        key = "G#"

    elif collections.Counter(note_set) == collections.Counter(Asharp) or set(note_set).issubset(set(Asharp)):
        key = "A#"

    elif collections.Counter(note_set) == collections.Counter(Chromatic):
        key = "Chromatic"
    
    return key

