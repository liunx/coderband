#!/usr/bin/env python3

import argparse
from music21 import *

coderbandKeys = {'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B'}
coderbandTimeSignatures = {'2/2', '4/4', '3/4', '2/4', '6/8', '3/8'}

coderbandParsedTable = {}


def chordsProgressGenerator(mxl):
    c = converter.parse(mxl)
    s = c.measures(1,1)
    kf = key.Key(coderbandParsedTable['key'])

    for i in coderbandParsedTable['chordProgress']:
        c, q = i.split('_')
        print(c, q)
        rf = roman.RomanNumeral(c, kf)

def chordsProgressParser(s):
    dat_list = s.split()
    k = dat_list[0]
    if k in coderbandKeys:
        dat_list.pop(0)
    else:
        k = 'C'
    coderbandParsedTable['key'] = k
    t = dat_list[0]
    if t in coderbandTimeSignatures:
        dat_list.pop(0)
    else:
        t = '4/4'
    coderbandParsedTable['timeSignature'] = t
    coderbandParsedTable['chordProgress'] = dat_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--song', help='song file')
    parser.add_argument('-m', '--mxl', help='musicxml file')
    args = parser.parse_args()

    with open(args.song) as f:
        s = f.read()
        chordsProgressParser(s)
        chordsProgressGenerator(args.mxl)
