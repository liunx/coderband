#!/usr/bin/env python3

import argparse
import copy
from music21 import *

environment.set('musicxmlPath', '/usr/bin/musescore')
environment.set('midiPath', '/usr/bin/timidity')
environment.set('graphicsPath', '/usr/bin/ristretto')

coderband_keys = {'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B'}
coderband_time_signatures = {'2/2', '4/4', '3/4', '2/4', '6/8', '3/8'}

coderband_parsed_table = {}

coderband_rhythmic_style_table = {}


def _build_triad_rhythmic_map(c, rhythmic_map):
    if c.isTriad():
        curr_octave = 2
        curr_pitch_class = -1
        n = note.Note(c.root().name)
        if n.pitch.pitchClass > curr_pitch_class:
            n.octave = curr_octave
        else:
            n.octave = curr_octave + 1

        curr_pitch_class = n.pitch.pitchClass
        rhythmic_map[1] = n

        n = note.Note(c.third.name)
        if n.pitch.pitchClass > curr_pitch_class:
            n.octave = curr_octave
        else:
            n.octave = curr_octave + 1

        curr_pitch_class = n.pitch.pitchClass
        rhythmic_map[2] = n

        n = note.Note(c.fifth.name)
        if n.pitch.pitchClass > curr_pitch_class:
            n.octave = curr_octave
        else:
            n.octave = curr_octave + 1

        curr_pitch_class = n.pitch.pitchClass
        rhythmic_map[3] = n

        curr_octave = 3
        curr_pitch_class = -1
        n = note.Note(c.root().name)
        if n.pitch.pitchClass > curr_pitch_class:
            n.octave = curr_octave
        else:
            n.octave = curr_octave + 1

        curr_pitch_class = n.pitch.pitchClass
        rhythmic_map[4] = n

        n = note.Note(c.third.name)
        if n.pitch.pitchClass > curr_pitch_class:
            n.octave = curr_octave
        else:
            n.octave = curr_octave + 1

        curr_pitch_class = n.pitch.pitchClass
        rhythmic_map[5] = n

        n = note.Note(c.fifth.name)
        if n.pitch.pitchClass > curr_pitch_class:
            n.octave = curr_octave
        else:
            n.octave = curr_octave + 1

        curr_pitch_class = n.pitch.pitchClass
        rhythmic_map[6] = n


# p - part, c - chord, t - time signature
def coderband_rhythmic_generator(p, c, t):
    rhythmic_style = [1, 2, 3, 4, 5, 4, 3, 2]
    rhythmic_map = {}

    _build_triad_rhythmic_map(c, rhythmic_map)

    for i in rhythmic_style:
        n = rhythmic_map[i]
        n.quarterLength = t / len(rhythmic_style)
        p.append(copy.copy(n))

def coderband_generator():
    s = stream.Stream()
    p1 = stream.Part()
    p2 = stream.Part()
    s.insert(0, p1)
    s.insert(0, p2)
    kf = key.Key(coderband_parsed_table['key'])
    p1.clef = clef.TrebleClef()
    p1.insert(0, meter.TimeSignature(coderband_parsed_table['time_signature']))
    p1.insert(0, kf)
    p2.clef = clef.BassClef()
    p2.insert(0, meter.TimeSignature(coderband_parsed_table['time_signature']))
    p2.insert(0, kf)

    for i in coderband_parsed_table['chord_progress']:
        c, q = i.split('_')
        rf2 = roman.RomanNumeral(c, kf)
        rf2.duration.quarterLength = float(q)
        coderband_rhythmic_generator(p2, rf2, float(q))

    s.show()
    #s.write('musicxml', fp='demo.xml')

def coderband_parser(s):
    dat_list = s.split()
    k = dat_list[0]
    if k in coderband_keys:
        dat_list.pop(0)
    else:
        k = 'C'
    coderband_parsed_table['key'] = k
    t = dat_list[0]
    if t in coderband_time_signatures:
        dat_list.pop(0)
    else:
        t = '4/4'
    coderband_parsed_table['time_signature'] = t
    coderband_parsed_table['chord_progress'] = dat_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file')
    args = parser.parse_args()

    with open(args.input) as f:
        s = f.read()
        coderband_parser(s)
        coderband_generator()
