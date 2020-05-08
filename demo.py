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


if __name__ == "__main__":
    demo14()
