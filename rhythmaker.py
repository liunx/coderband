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
        r = note.Rest(type='whole')
        self.stream.append(r)

    def createRhythmic(self, scale):
        rf = roman.RomanNumeral(scale, self.key)
        ms = stream.Measure()
        bc = self.timeSignature.beatCount
        for i in range(bc):
            c = chord.Chord(rf, type='quarter')
            ms.append(c)
        self.stream.append(ms)

    def changeMode(self, mode):
        self.key = key.Key(mode)

    def changeTimeSignature(self, ts):
        self.timeSignature = meter.TimeSignature(ts)

    def show(self):
        self.stream.makeMeasures()
        self.stream.makeNotation()
        self.stream.show('text')

def demo():
    testDat = ['I7', 'IV7', 'V7', 'iii7', 'vi7', 'ii7', 'V7', 'I7']
    rhym = Rhythmic('C', '4/4')
    for i in testDat:
        rhym.createRhythmic(i)
    rhym.show()

def triadToTriad(fromChord, toChord):
    triadIntervals = ['M-2', 'm-2', 'P1', 'm2', 'a1', 'M2']
    chordMap = {}
    for n in fromChord.notes:
        # step 1: the closest move
        if n.name not in chordMap:
            for i in triadIntervals:
                tn = n.transpose(i)
                if tn.name in toChord.pitchNames and tn.name not in chordMap.values():
                    print(n.pitch.nameWithOctave, tn.pitch.nameWithOctave)
                    chordMap[n.name] = tn.name
                    break
        # step 2: fix missed notes
        if n.name not in chordMap:
            print("missed note: {}".format(n.name))
            diff = set.difference(set(toChord.pitchNames), set(chordMap.values()))
            if len(diff) == 1:
                chordMap[n.name] = diff.pop()
    return chordMap

def triadToSeventh(fromChord, toChord):
    chordMap = {}
    return chordMap

def seventhToSeventh(fromChord, toChord):
    seventhIntervals = ['m-3', 'M-2', 'm-2', 'P1', 'm2', 'a1', 'M2', 'm3']
    chordMap = {}
    for n in fromChord.notes:
        # step 1: the closest move
        if n.name not in chordMap:
            for i in seventhIntervals:
                tn = n.transpose(i)
                if tn.name in toChord.pitchNames and tn.name not in chordMap.values():
                    print(n.pitch.nameWithOctave, tn.pitch.nameWithOctave)
                    chordMap[n.name] = tn.name
                    break
        # step 2: fix missed notes
        if n.name not in chordMap:
            #print("missed note: {}".format(n.name))
            diff = set.difference(set(toChord.pitchNames), set(chordMap.values()))
            if len(diff) == 1:
                chordMap[n.name] = diff.pop()
    return chordMap


def seventhToTriad(fromChord, toChord):
    pass

def chordsConnect():
    mode = 'C4'
    ts1 = ['I', 'V', 'vi', 'iii', 'ii', 'V', 'I']
    ts2 = ['I7', 'V7', 'vi7', 'iii7', 'ii7', 'V7', 'I7']
    ts3 = ['I', 'IV', 'V7', 'I']
    ts4 = ['I7', 'IV7', 'V7', 'I7']
    scaleList = ts1

    fromRN = None
    fromScale = None
    toRN = None
    toScale = None
    chordMap = {}
    for scale in scaleList:
        if not bool(fromRN):
            fromRN = roman.RomanNumeral(scale, mode)
            fromScale = scale
            continue
        toRN = roman.RomanNumeral(scale, mode)
        toScale = scale
        if fromRN.isTriad() and toRN.isTriad():
            chordMap = triadToTriad(fromRN, toRN)
        elif fromRN.isSeventh() and toRN.isSeventh():
            chordMap = seventhToSeventh(fromRN, toRN)
        else:
            print("Unfinished situation!")
            print("{} ==> {}".format(fromScale, toScale))
            break

        print("====| {} --> {}".format(fromScale, toScale))
        keys = list(chordMap.keys())
        keys.reverse()
        for k in keys:
            print("Map: {} ==> {}".format(k, chordMap.get(k)))
        fromRN = toRN
        fromScale = scale


if  __name__ == "__main__":
    chordsConnect()
