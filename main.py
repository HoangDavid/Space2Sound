import pandas as pd
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import mido

# Load the dataset
url = 'data/htru2/HTRU_2.csv'
column_names = [
    'Mean_IP', 'Std_IP', 'Kurtosis_IP', 'Skewness_IP',
    'Mean_DM', 'Std_DM', 'Kurtosis_DM', 'Skewness_DM', 'Class'
]
data = pd.read_csv(url, names=column_names)

# Extract the 'Mean_IP' column (first 1000 rows)
mean_ip = data['Mean_IP'].values[:500]

# Normalize the mean IP values to a range suitable for MIDI note numbers (21 to 108, piano range)
min_midi = 21  # Minimum MIDI note (A0)
max_midi = 108  # Maximum MIDI note (C8)
norm_mean_ip = (mean_ip - mean_ip.min()) / (mean_ip.max() - mean_ip.min())
midi_notes = (min_midi + (max_midi - min_midi) * norm_mean_ip).astype(int)

# Create a MIDI file
midi_file = mido.MidiFile()
track = mido.MidiTrack()
midi_file.tracks.append(track)

# Add notes to the MIDI track
duration = 480  # Duration of each note in ticks
for note in midi_notes:
    track.append(mido.Message('note_on', note=note, velocity=64, time=0))
    track.append(mido.Message('note_off', note=note, velocity=64, time=duration))

# Save the MIDI file
midi_file.save("pulsar_sonification_nasa_style.mid")