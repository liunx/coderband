#!/usr/bin/env python3

from music21 import *

environment.set('musicxmlPath', '/usr/bin/musescore')

class Rhythmic:
    def __init__(self, mode, ts):
        self.key = key.Key(mode)
        self.timeSignature = meter.TimeSignature(ts)
        self.stream = stream.Stream()
        self.stream.append(clef.BassClef())
        self.stream.append(self.timeSignature)
        self.stream.append(self.key)
        r = note.Rest()
        r.duration.quarterLength = self.timeSignature.beatCount
        self.stream.append(stream.Measure(r))

    def createRhythmic(self, scale):
        rf = roman.RomanNumeral(scale, self.key)
        ms = stream.Measure()
        bc = self.timeSignature.beatCount
        for i in range(bc):
            c = chord.Chord(rf)
            #c.quarterLength = 1.0 / bc
            ms.append(c)
        self.stream.append(ms)

    def changeMode(self, mode):
        self.key = key.Key(mode)

    def changeTimeSignature(self, ts):
        self.timeSignature = meter.TimeSignature(ts)

    def show(self):
        self.stream.show()


if  __name__ == "__main__":
    testDat = ['I7', 'IV7', 'V7', 'iii7', 'vi7', 'ii7', 'V7', 'I7']
    rhym = Rhythmic('C', '4/4')
    for i in testDat:
        rhym.createRhythmic(i)
    rhym.show()
