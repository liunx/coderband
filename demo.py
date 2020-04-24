#!/usr/bin/env python3

import numpy as np
import core.tools as tools
import core.music_theory as theory
import core.converter as convt

def demo03():
    key = 'C'
    obj = theory.Scales()
    notes = obj.to_scales(key, 'ionian')
    print(notes)
    for m in ['gong', 'shang', 'jue', 'zhi', 'yu']:
        notes = obj.to_scales(key, m)
        print(notes)
    for m in ['melodic minor', 'phrygidorian', 'lydian augmented', 'lydian dominant', 'melodic major', 'aeolocrian', 'altered scale']:
        notes = obj.to_scales(key, m)
        print(notes)
    notes = obj.to_scales(key, 'bebop major')
    print(notes)
    notes = obj.to_scales(key, 'bebop dominant')
    print(notes)

def demo06():
    key = 'G'
    obj = theory.Chord()
    chords = obj.to_chord(key, 'maj7')
    print(chords)
    chords = obj.to_chord(key, 'min7')
    print(chords)

def demo07():
    key = 'C'
    ts = '4/4'
    obj = theory.Chord()
    staff = convt.Staff(key, ts)
    chord = obj.to_chord(key, 'maj7')
    staff.add_chord(chord, type='whole')
    chord = obj.to_chord(key, 'min7')
    staff.add_chord(chord, type='whole')
    chord = ['G', 'E', 'C']
    staff.add_chord(chord, type='whole')
    staff.show_mxml()

def demo08():
    roman_numerals = ['io', 'i', 'I', 'I+', 'io7', 'i-7', 'i7', 'I-7', 'I7', 'I+7']
    key = 'C4'
    ts = '4/4'
    staff = convt.Staff(key, ts)
    for rn in roman_numerals:
        staff.add_roman_numeral(rn, key)
    staff.show_text()


def demo09():
    roman_numerals = ['io', 'i', 'I', 'I+', 'io7', 'i-7', 'i7', 'I-7', 'I7', 'I+7']
    key = 'C4'
    ts = '4/4'
    fr = theory.FreqRatio()
    staff = convt.Staff(key, ts)
    frmap = {}
    for rn in roman_numerals:
        intervals = staff.to_intervals(rn, key)
        prod = fr.calc_freq_radio_size(intervals)
        #print("{:4}: {:>20}".format(rn, prod))
        frmap[prod] = rn
    keys = list(frmap.keys())
    keys.sort()
    for k in keys:
        print("{:4}: {:>20}".format(frmap[k], k))

def math_demo():
    ay = np.array([1, 5, 1])
    print(ay.mean(), ay.var(), ay.std())
    ay = np.array([1, 5, 1, 1])
    print(ay.mean(), ay.var(), ay.std())

def demo10():
    fr = theory.FreqRatio()
    l = fr.chromatic_freq_sizes()
    print(l)


if __name__ == "__main__":
    demo10()
    #math_demo()
