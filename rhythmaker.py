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
    triadIntervals = ['M-2', 'm-2', 'P1', 'm2', 'a1', 'M2']
    chordMap = {}
    for n in fromChord.notes:
        # step 1: the closest move
        if n.name not in chordMap:
            for i in triadIntervals:
                tn = n.transpose(i)
                if tn.name in toChord.pitchNames and tn.name not in chordMap.values():
                    chordMap[n.name] = tn.name
                    break
        # step 2: fix missed notes
        if n.name not in chordMap:
            print("missed note: {}".format(n.name))
            diff = set.difference(set(toChord.pitchNames), set(chordMap.values()))
            if len(diff) == 1:
                chordMap[n.name] = diff.pop()
    # add missed notes
    diff = set.difference(set(toChord.pitchNames), set(chordMap.values()))
    if len(diff) == 1:
        n = diff.pop()
        if n == toChord.root().name:
            print("Warning!!! Missed root note: {}".format(n))
        elif n == toChord.seventh.name:
            print("Warning!!! Missed seventh note: {}".format(n))
        elif n == toChord.fifth.name:
            print("Warning!!! Missed fifth note: {}".format(n))
        elif n == toChord.third.name:
            print("Missed third note: {}, can be ignored!".format(n))
    return chordMap


def seventhToSeventh(fromChord, toChord):
    seventhIntervals = ['M-2', 'm-2', 'P1', 'm2', 'a1', 'M2']
    chordMap = {}
    for n in fromChord.notes:
        # step 1: the closest move
        if n.name not in chordMap:
            for i in seventhIntervals:
                tn = n.transpose(i)
                if tn.name in toChord.pitchNames and tn.name not in chordMap.values():
                    #print(n.pitch.nameWithOctave, tn.pitch.nameWithOctave)
                    chordMap[n.name] = tn.name
                    break
        # step 2: fix missed notes
        if n.name not in chordMap:
            print("missed note: {}".format(n.name))
            diff = set.difference(set(toChord.pitchNames), set(chordMap.values()))
            if len(diff) == 1:
                chordMap[n.name] = diff.pop()
    return chordMap


def seventhToTriad(fromChord, toChord):
    seventhIntervals = ['M-2', 'm-2', 'P1', 'm2', 'a1', 'M2']
    chordMap = {}
    for n in fromChord.notes:
        # step 1: the closest move
        if n.name not in chordMap:
            for i in seventhIntervals:
                tn = n.transpose(i)
                if tn.name in toChord.pitchNames and tn.name not in chordMap.values():
                    #print(n.pitch.nameWithOctave, tn.pitch.nameWithOctave)
                    chordMap[n.name] = tn.name
                    break
        # step 2: fix missed notes
        if n.name not in chordMap:
            print("missed note: {}".format(n.name))
            diff = set.difference(set(toChord.pitchNames), set(chordMap.values()))
            if len(diff) == 1:
                chordMap[n.name] = diff.pop()
    return chordMap


def chordsConnect(mode, scaleList, chordMapList):
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

        print("fromScale: {}, toScale: {}".format(fromScale, toScale))
        if fromRN.isTriad() and toRN.isTriad():
            chordMap = triadToTriad(fromRN, toRN)
        elif fromRN.isSeventh() and toRN.isSeventh():
            chordMap = seventhToSeventh(fromRN, toRN)
        elif fromRN.isTriad() and toRN.isSeventh():
            chordMap = triadToSeventh(fromRN, toRN)
        elif fromRN.isSeventh() and toRN.isTriad():
            chordMap = seventhToTriad(fromRN, toRN)
        else:
            print("Unfinished situation!")
            print("{} ==> {}".format(fromScale, toScale))
            break

        fromRN = toRN
        fromScale = scale
        chordMapList.append(chordMap)

def showText(sheetList, fromNote, toNote):
    noteList = [['G#', 'A-'], 'A', ['A#', 'B-'], ['B', 'C-'], ['B#', 'C'], ['C#', 'D-'],
                'D', ['D#', 'E-'], ['E', 'F-'], ['E#', 'F'], ['F#', 'G-'], 'G']
    noteLen = len(noteList)
    up = "↑"
    down = "↓"

    for i in range(noteLen):
        if noteList[i] == fromNote:
            fromIndex = i
            break
        if type(noteList[i]) == list:
            if fromNote in noteList[i]:
                fromIndex = i
                break

    for i in range(noteLen):
        if noteList[i] == toNote:
            toIndex = i
            break
        if type(noteList[i]) == list:
            if toNote in noteList[i]:
                toIndex = i
                break

    if fromNote == toNote:
        #print("{} = {}".format(fromNote, toNote))
        sheetList.extend(['=', toNote])
        return

    fidx = fromIndex
    tidx = toIndex
    for i in range(1, noteLen + 1):
        fidx  = (fidx + 1) % noteLen
        tidx  = (tidx + 1) % noteLen
        if fidx == toIndex:
            #print("{} {} {}".format(fromNote, up, toNote))
            sheetList.extend([up, toNote])
            break
        elif tidx == fromIndex:
            #print("{} {} {}".format(fromNote, down, toNote))
            sheetList.extend([down, toNote])
            break

def sheetMusic(sheetList, fromChord, chordMapList):
    i = 0
    for c in fromChord:
        sheetList[i].append(c)
        i = i + 1

    for m in chordMapList:
        toChord = []
        for n in fromChord:
            toChord.append(m[n])
        i = 0
        for f,t in zip(fromChord, toChord):
            print("fromNote: {}, toNote: {}".format(f, t))
            l = sheetList[i]
            showText(l, f, t)
            i = i + 1
        fromChord = toChord

def outputSheet(sheetList):
    print("Final map:")
    print("===========")
    for l in sheetList:
        s = ""
        for i in l:
            s = s + "{:3}".format(i)
        print(s)


def demo02():
    ts1 = ['I', 'V', 'vi', 'iii', 'ii', 'V', 'I']
    ts2 = ['I7', 'V7', 'vi7', 'iii7', 'ii7', 'V7', 'I7']
    ts3 = ['I', 'IV7', 'V', 'I']
    ts4 = ['I7', 'IV7', 'V7', 'I7']
    modeList = ['C', 'C#', 'D-', 'D', 'E-', 'E', 'F',
                'F#', 'G-', 'G', 'A-', 'A', 'B-', 'B']
    modeList = ['C']

    ts = ts3
    inv = 0
    sheetLen = 5

    for m in modeList:
        chordMapList = []
        sheetList = [[]] * sheetLen
        for i in range(sheetLen):
            sheetList[i] = []
        print("Mode: {}".format(m))
        chordsConnect(m, ts, chordMapList)
        rf = roman.RomanNumeral(ts[0], m)
        rf.inversion(inv)
        fromChord = rf.pitchNames
        fromChord.reverse()
        sheetMusic(sheetList, fromChord, chordMapList)
        outputSheet(sheetList)


if  __name__ == "__main__":
    demo02()
