import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from audiolazy import str2midi
from midiutil import MIDIFile 


# Pre-defined note names to map values to MIDI notes
NOTE_NAMES = [
    'C1', 'C2', 'G2',
    'C3', 'E3', 'G3', 'A3', 'B3',
    'D4', 'E4', 'G4', 'A4', 'B4',
    'D5', 'E5', 'G5', 'A5', 'B5',
    'D6', 'E6', 'F#6', 'G6', 'A6',
]



def convert_to_midi(filename, parameter_x, parameter_y, size_param, sample_fraction=0.003):
    df = pd.read_csv(filename)
    df = df.sample(frac=sample_fraction)

    # Drop rows with missing values in key parameters
    df = df.dropna(subset=[parameter_x, parameter_y, size_param])


    # Enhanced the data so it is more sparsely spaced
    df[parameter_x] = -np.log(df[parameter_x] / df[parameter_x].max()) * 500
    df[parameter_y] = (df[parameter_y] / df[parameter_y].max()) * 5000

    x_values = df[parameter_x].values # distance to the stars (parsecs)
    y_values = df[parameter_y].values # magnitude
    sizes = -df[size_param].values # bigger means bluer and hotter -> volume 

    # visualize the data before converting to MIDI:
    visualize_data(x_values, y_values, sizes, parameter_x, parameter_y)

    create_midi_file(x_values, y_values, sizes, filename="out.mid")


def create_midi_file(x, y, sizes, filename="out.mid", duration_beats=120, bpm=60):
    # Convert note names to MIDI note numbers
    note_midis = [str2midi(n) for n in NOTE_NAMES]
    n_notes = len(note_midis)

    y_norm = map_value(y, np.min(y), np.max(y), 0, 1)
    x_mapped = map_value(x, 0, np.max(x), 0, duration_beats)

    # Map sizes to MIDI velocities (10 to 127)
    sizes_mapped = map_value(sizes, np.min(sizes), np.max(sizes), 10, 127).astype(int)

    midi_notes = []
    for val in y_norm:
        # higher y -> lower note_index, reverse the mapping:
        map_value(val, 0, 1, n_notes-1, 0)
        note_index = round(map_value(val, 0, 1, n_notes-1, 0))
        midi_notes.append(note_midis[note_index])
    
    my_midi_file = MIDIFile(numTracks=1)
    my_midi_file.addTempo(track=0, time=0, tempo=bpm)

    # Add notes to the MIDI track
    for i in range(len(x_mapped)):
        volume = sizes_mapped[i]
        if volume > 0:
            # Using a fixed duration of 2 beats per note, can be changed as needed
            my_midi_file.addNote(track=0, channel=0, time=x_mapped[i], 
                                 pitch=midi_notes[i], volume=volume, duration=2)

    # Write the MIDI file to disk
    with open(filename, "wb") as f:
        my_midi_file.writeFile(f)
    print(f"MIDI file '{filename}' created successfully.")


def map_value(value, min_value, max_value, min_result, max_result):
    return min_result + (value - min_value) / (max_value - min_value) * (max_result - min_result)


def visualize_data(x, y, sizes, xlabel, ylabel):
    # Normalize sizes for plotting, if desired
    sizes_norm = (sizes - np.nanmin(sizes)) / (np.nanmax(sizes) - np.nanmin(sizes)) * 100 + 10
    plt.scatter(x, y, s=sizes_norm, alpha=0.7, edgecolors="k", linewidths=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.title("Data visualization")
    plt.show()


def main():
    if len(sys.argv) != 5:
        print("Usage: python3 plot.py <filename> <para1> <para2> <size_param>")
        sys.exit(1)
    
    filename = sys.argv[1]
    para1 = sys.argv[2]
    para2 = sys.argv[3]
    size_param = sys.argv[4]

    convert_to_midi(filename, para1, para2, size_param)

if __name__ == "__main__":
    main()
