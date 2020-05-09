#!/usr/bin/env python3

import numpy as np
import core.tools as tools
import core.music_theory as theory
import core.converter as convt
import random
import time

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


def demo08():
    roman_numerals = ['io', 'i', 'I', 'I+', 'io7', 'i-7', 'i7', 'I-7', 'I7', 'I+7']
    roman_numerals = ['io', 'i', 'I', 'I+', 'I7', 'I+7']
    key = 'C4'
    ts = '4/4'
    staff = convt.Staff(key, ts)
    for rn in roman_numerals:
        staff.add_roman_numeral(rn, key, type='whole')
        staff.add_rest()
    staff.show_midi()


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
    ay = np.array([1, 5, 4, 1])
    print(ay, ay.mean(), ay.var(), ay.std())
    ay = np.array([1, 4, 5, 1])
    print(ay, ay.mean(), ay.var(), ay.std())
    ay = np.array([1, 1, 4, 5])
    print(ay, ay.mean(), ay.var(), ay.std())
    ay = np.array([1, 1, 5, 4])
    print(ay, ay.mean(), ay.var(), ay.std())


def demo10():
    fr = theory.FreqRatio()
    l = fr.chromatic_freq_sizes()
    freq_map = dict(zip(l, roman_degrees))
    l.sort()
    for i in l:
        print('{:6}: {}'.format(i, freq_map[i]))


roman_degrees = ['I', '-II', 'II', '-III', 'III', 'IV', '-V', 'V', '-VI', 'VI', '-VII', 'VII']
chord_qualities = ['', 'm', '7', 'm-7', '-7']

def demo13():
    degree_weights = [5.0, 3.0, 2.0, 2.0, 4.0, 6.0, 1.0, 8.0, 1.0, 6.0, 2.0, 1.0]
    quality_weights = [1.0, 1.0, 0.5, 0.5, 0.7]
    kv = 4
    i = 0
    while True:
        degrees = random.choices(roman_degrees, weights=degree_weights, k=kv)
        for x in range(10):
            qualities = random.choices(chord_qualities, weights=quality_weights, k=kv)
            s = ''
            for d,q in zip(degrees, qualities):
                if bool(q) and q[0] == 'm':
                    d = d.lower()
                    n = '{}{}'.format(d, q[1:])
                    s = s + '{:8}'.format(n)
                else:
                    n = '{}{}'.format(d, q[1:])
                    s = s + '{:8}'.format(n)

            try:
                print('{:10}: {}'.format(i, s))
                time.sleep(0.0001)
            except KeyboardInterrupt:
                return

        i = i + 1


def demo14():
    degree_weights = [5.0, 3.0, 2.0, 2.0, 4.0, 6.0, 1.0, 8.0, 1.0, 6.0, 2.0, 1.0]
    kv = 4
    key = 'C4'
    ts = '4/4'
    staff = convt.Staff(key, ts)
    for i in range(100):
        degrees = random.choices(roman_degrees, weights=degree_weights, k=kv)
        for rn in degrees:
            staff.add_roman_numeral(rn, key)
        staff.add_rest()

    #staff.show_text()
    staff.write_xml('./chord_progress.xml')


chord_progressions = [
    ['I', 'IV', 'V', 'I'],
    ['I', 'V', 'IV', 'I'],
    ['I', 'IV', 'V', 'IV'],
    ['I', 'vi', 'IV', 'V'],
    ['I', 'V', 'vi', 'IV'],
    ['I', 'IV', 'vi', 'V'],
    ['I', 'vi', 'ii', 'V'],
    ['I', 'vi7', 'ii7', 'V7'],
    ['I', 'VI', 'ii', 'V'],
    ['I', 'VI7', 'ii7', 'V7'],
    ['I', 'VI', 'II', 'V'],
    ['I', 'VI7', 'II7', 'V7'],
    ['ii', 'V', 'I', 'vi'],
    ['ii', 'V7', 'I', 'vi'],
    ['iii', 'vi', 'ii', 'V'],
    ['iii7', 'vi7', 'ii7', 'V7'],
    ['ii', 'V', 'I', 'IV'],
    ['ii7', 'V7', 'I', 'IV'],
    ['I', 'V', 'ii', 'IV'],
    ['I', 'ii', 'IV', 'I'],
    ['ii', 'IV', 'I', 'I'],
    ['I', '-VII', 'IV', 'I'],
    ['I', 'V', '-VII', 'IV'],
    ['i', 'III', '-VII', 'i'],
    ['i', 'III', '-VII', 'IV'],
    ['i', 'III', '-VII', 'iv'],
    ['i', '-VII', '-VI', 'V'],
    ['I', 'V', 'vi', 'IV'],
    ['I', 'IV', 'I', 'V'],
]

cp01 = [
    ['I', 'IV', 'V7', 'I'],
    ['i7', 'iv7', 'v7', 'i7'],
    ['I-7', 'IV-7', 'V-7', 'I-7'],
    ['I7', 'IV7', 'V7', 'I7'],
    ['i', 'iv', 'v', 'i'],
    ['I', 'IV', 'V', 'I'],
]

cp02 = [
    ['I', 'II', 'III', 'IV'],
    ['i', 'ii', 'iii', 'iv'],
]

def show_midi(key, ts, l):
    key = 'C3'
    ts = '4/4'
    staff = convt.Staff(key, ts)
    for p in l:
        for rn in p:
            staff.add_roman_numeral(rn, key)
        staff.add_rest()
    staff.show_midi()


def demo15():
    key = 'C3'
    ts = '4/4'
    show_midi(key, ts, cp02)


if __name__ == "__main__":
    demo15()
    #demo08()
