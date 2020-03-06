#!/usr/bin/env python3

from music21 import *
from pprint import PrettyPrinter

environment.set('musicxmlPath', '/usr/bin/musescore')

pp = PrettyPrinter()
noteList = [['G#', 'A-'], 'A', ['A#', 'B-'], ['B', 'C-'], ['B#', 'C'], ['C#', 'D-'],
            'D', ['D#', 'E-'], ['E', 'F-'], ['E#', 'F'], ['F#', 'G-'], 'G']
noteLen = len(noteList)
up = "↑"
down = "↓"


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
        tn = findClosetNote(n, chordMap.values())
        print("Add missed note {} to {}".format(n, tn))
        for k in chordMap.keys():
            if chordMap[k] == tn:
                chordMap[k] = [tn, n]
                break
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
        if n == fromChord.seventh:
            continue
        # step 1: the closest move
        if n.name not in chordMap:
            for i in seventhIntervals:
                tn = n.transpose(i)
                if tn.name in toChord.pitchNames and tn.name not in chordMap.values():
                    chordMap[n.name] = tn.name
                    break
        # step 2: fix missed notes
        if n.name not in chordMap:
            print("missed note: {}".format(n.name))
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


def createSheet(sheetList, fromNote, toNote):
    for i in range(noteLen):
        s1 = set(fromNote)
        s2 = set(noteList[i])
        inter = set.intersection(s1, s2)
        if bool(inter):
            fromIndex = i
            break

    for i in range(noteLen):
        s1 = set(toNote)
        s2 = set(noteList[i])
        inter = set.intersection(s1, s2)
        if bool(inter):
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

def findClosetNote(fromNote, toNoteList):
    for i in range(noteLen):
        s1 = set(fromNote)
        s2 = set(noteList[i])
        inter = set.intersection(s1, s2)
        if bool(inter):
            fromIndex = i
            break
    # look up
    idx = fromIndex
    upNote = None
    upDist = 0
    for i in range(1, noteLen + 1):
        idx  = (idx + 1) % noteLen
        elem = noteList[idx]
        if type(elem) == list:
            diff = set.intersection(set(elem), set(toNoteList))
            if len(diff) > 0:
                upNote = diff.pop()
                upDist = i
                break
        if elem in toNoteList:
            upNote = elem
            upDist = i
            break
    # look down
    idx = fromIndex
    downNote = None
    downDist = 0
    for i in range(1, noteLen + 1):
        idx  = idx - 1
        elem = noteList[idx]
        if type(elem) == list:
            diff = set.intersection(set(elem), set(toNoteList))
            if len(diff) > 0:
                downNote = diff.pop()
                downDist = i
                break
        if elem in toNoteList:
            downNote = elem
            downDist = i
            break
    # compare
    if upDist < downDist:
        print("The Cloest note {}, semitone {}".format(upNote, upDist))
        return upNote
    else:
        print("The Cloest note {}, semitone {}".format(downNote, downDist))
        return downNote


def flatList(fromList, toList):
    for i in fromList:
        if type(i) == list:
            flatList(i, toList)
        else:
            toList.append(i)


def sheetMusic(sheetList, fromChord, chordMapList):
    i = 0
    for c in fromChord:
        sheetList[i].append(c)
        i = i + 1

    for m in chordMapList:
        toChord = []
        print("fromChord: {}, chordMap: {}".format(fromChord, m.keys()))
        newChord = []
        flatList(fromChord, newChord)
        diff = set.difference(set(newChord), set(m.keys()))
        if bool(diff):
            newChord.remove(diff.pop())
        for n in newChord:
            val= m.get(n)
            toChord.append(val)
        i = 0
        for f,t in zip(newChord, toChord):
            #print("fromNote: {}, toNote: {}".format(f, t))
            l = sheetList[i]
            createSheet(l, f, t)
            i = i + 1
        fromChord = toChord


def outputSheet(sheetList):
    print("Final map:")
    print("===========")
    for l in sheetList:
        s = ""
        for i in l:
            s = s + "{:3}".format(str(i))
        print(s)


def demo02():
    ts1 = ['I', 'V', 'vi', 'iii', 'ii', 'V', 'I']
    ts2 = ['I7', 'V7', 'vi7', 'iii7', 'ii7', 'V7', 'I7']
    ts3 = ['I', 'IV7', 'V7', 'I']

    modeList = ['C', 'C#', 'D-', 'D', 'E-', 'E', 'F',
                'F#', 'G-', 'G', 'A-', 'A', 'B-', 'B']
    modeList = ['C']

    ts4 = [['I', 'V7'], ['I', 'ii7'], ['I', 'iii7'], ['I', 'IV7']]
    ts5 = [['V7', 'I'], ['IV7', 'I'], ['I7', 'V']]

    testList = [ts3]
    inv = 0
    sheetLen = 5

    for m in modeList:
        for ts in testList:
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
            pp.pprint(chordMapList)
            sheetMusic(sheetList, fromChord, chordMapList)
            outputSheet(sheetList)


if  __name__ == "__main__":
    demo02()
