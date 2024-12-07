import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from audiolazy import str2midi, midi2str
from midiutil import MIDIFile 
# sample: C-major scale
note_names = ['C1','C2','G2',
             'C3','E3','G3','A3','B3',
             'D4','E4','G4','A4','B4',
             'D5','E5','G5','A5','B5',
             'D6','E6','F#6','G6','A6']


def plot(filename, para1, para2, size_param):
    df = pd.read_csv(filename)
    df = df.sample(frac=0.01)
    df = df.dropna(subset=[para1, para2, size_param])
    df[para1] = -np.log(df[para1] / df[para1].max()) * 100
    df[para2] = df[para2] / df[para2].max() * 1000
    x = df[para1].values
    y = df[para2].values
    sizes = df[size_param].values 

    # sizes = (sizes - np.nanmin(sizes)) / (np.nanmax(sizes) - np.nanmin(sizes)) * 60 + 10 
    # plt.scatter(x, y, s=sizes, alpha=0.7, edgecolors="k", linewidths=0.5)
    # plt.xlabel(para1)
    # plt.ylabel(para2)
    # plt.grid(True)
    # plt.show()

    convert_midi(x, y, sizes)

def convert_midi(x, y, sizes):
    note_midis = [str2midi(n) for n in note_names]
    n_notes = len(note_midis)

    y = map_value(y, min(y), max(y), 0, 1)
    duration_beats = 120
    x = map_value(x, 0, max(x), 0, duration_beats)

    sizes = map_value(sizes, np.min(sizes), np.max(sizes), 10, 127).astype(int)

    midi_data = []
    for v in y:
        note_index = round(map_value(v, 0, 1, n_notes-1, 0)) 
        midi_data.append(note_midis[note_index])


    bpm = 60
    my_midi_file = MIDIFile(1) #one track 
    my_midi_file.addTempo(track=0, time=0, tempo=bpm) 
    #add midi notes
    for i in range(len(x)):
        if sizes[i]:
            my_midi_file.addNote(track=0, channel=0, time=x[i], pitch=midi_data[i], volume=sizes[i], duration=2)
    #create and save the midi file itself
    with open("out.mid", "wb") as f:
        my_midi_file.writeFile(f)



def map_value(value, min_value, max_value, min_result, max_result):
    result = min_result + (value - min_value) / (max_value - min_value) * (max_result - min_result)
    return result
    

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 plot.py <filename> <para1> <para2> <size_param>")
        sys.exit(1)
    
    filename = sys.argv[1]
    para1 = sys.argv[2]
    para2 = sys.argv[3]
    size_param = sys.argv[4]
    plot(filename, para1, para2, size_param)


if __name__ == "__main__":
    main()