#!/usr/bin/env python3

import music21
import copy

music21.environment.set('musicxmlPath', '/usr/bin/musescore')

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


class Staff:
    def __init__(self):
        self.staffInited = {}
        self.stepNames = ['A', 'B', 'C', 'E', 'F', 'G']
        self.a0 = music21.note.Note('A0')
        self.c8 = music21.note.Note('C8')
        for i in range(self.a0.pitch.midi, self.c8.pitch.midi + 1):
            n = music21.note.Note(i)
            if n.pitch.alter == 0:
                self.staffInited[i] = []

    def read(self, chords):
        self.staff = copy.deepcopy(self.staffInited)
        step = 0
        lastMidi = 0
        for notes in chords:
            for n in notes:
                if n == 'R':
                    if lastMidi == 0:
                        continue
                    nt = music21.note.Rest()
                    nt.offset = step
                    self.staff[lastMidi].append(nt)
                    continue
                nt = music21.note.Note(n)
                nt.offset = step
                if nt.pitch.alter > 0:
                    lastMidi = nt.pitch.midi - 1
                elif nt.pitch.alter < 0:
                    lastMidi = nt.pitch.midi + 1
                else:
                    lastMidi = nt.pitch.midi
                self.staff[lastMidi].append(nt)
            step = step + 1
        self.staff['step'] = step

    def show(self, indent=5):
        staffStep = self.staff.pop('step')
        keys = list(self.staff.keys())
        keys.sort()
        keys.reverse()
        print("The sheet:")
        print("_{}_".format("_" * indent * staffStep))
        odd = 0
        for k in keys:
            notes = self.staff[k]
            # remove blank lines
            if not bool(notes):
                continue
            s = "|"
            for step in range(staffStep):
                flag = False
                for n in notes:
                    if n.offset == step:
                        if odd % 2:
                            strFormat = "{:-^"  + str(indent) + "}"
                        else:
                            strFormat = "{:^"  + str(indent) + "}"
                        if n.isRest:
                            s = s + strFormat.format('@')
                        else:
                            s = s + strFormat.format(n.pitch.unicodeNameWithOctave)
                        flag = True
                if not flag:
                    if odd %2:
                        s = s + "-" * indent
                    else:
                        s = s + " " * indent
            s = s + "|"
            odd = odd + 1
            print(s)
        print("|{}|".format("_" * indent * staffStep))


class Harmony:
    def __init__(self, mode):
        self.__mode = mode
        self.__chordList = []

    def mode(self, mode=None):
        if mode:
            self.__mode = mode
        else:
            return self.__mode

    def getChordList(self):
        return self.__chordList

    def scaleItoIV(self, fromChord):
        rootNote = fromChord.third.transpose('m2')
        thirdNote = fromChord.fifth.transpose('M2')
        fifthNote = fromChord.root()
        toChord = music21.chord.Chord([rootNote, thirdNote, fifthNote])
        toChord.closedPosition()
        return toChord

    def scaleIVtoV7(self, fromChord):
        rootNote = fromChord.third.transpose('M-2')
        thirdNote = fromChord.fifth.transpose('m-2')
        seventhNote = fromChord.root()
        toChord = music21.chord.Chord([rootNote, thirdNote, seventhNote])
        toChord.closedPosition()
        return toChord

    def scaleV7toI(self, fromChord):
        rootNote = fromChord.third.transpose('m2')
        thirdNote = fromChord.seventh.transpose('m-2')
        fifthNote = fromChord.root()
        toChord = music21.chord.Chord([rootNote, thirdNote, fifthNote])
        toChord.closedPosition()
        return toChord

    def getNameWithOctaves(self, chord):
        l = []
        l = [n.nameWithOctave for n in chord.notes]
        return l

    def process(self, scaleList, fromChord=None):
        fromScale = None
        toScale = None
        toChord = None
        self.baseLine = []
        self.__chordList = []
        for scale in scaleList:
            if not fromChord:
                fromChord = music21.roman.RomanNumeral(scale, self.__mode)
                continue
            if not fromScale:
                fromScale = scale
                continue
            if not bool(self.__chordList):
                l = self.getNameWithOctaves(fromChord)
                self.__chordList.append(l)
            toScale = scale
            print("from {} ==> {}".format(fromScale, toScale))
            if fromScale == 'I' and toScale == 'IV':
                toChord = self.scaleItoIV(fromChord)
            elif fromScale == 'IV' and toScale == 'V7':
                toChord = self.scaleIVtoV7(fromChord)
            elif fromScale == 'V7' and toScale == 'I':
                toChord = self.scaleV7toI(fromChord)
            fromScale = scale
            self.baseLine.append(toChord.bass())
            fromChord = toChord
            l = self.getNameWithOctaves(fromChord)
            self.__chordList.append(l)


def demo03():
    chords = [['C4', 'E#4', 'G4'], ['C4', 'F4', 'A4'], ['B3', 'D4', 'F4', 'G4'],
              ['C4', 'E-4', 'G4']]
    staff = Staff()
    staff.read(chords)
    staff.show()


def demo04():
    mode = 'C4'
    ts = [['I', 'IV', 'V7', 'I']]
    h = Harmony(mode)
    staff = Staff()
    for l in ts:
        rf = music21.roman.RomanNumeral(l[0], mode)
        rf.inversion(0)
        h.process(l, rf)
        chords = h.getChordList()
        staff.read(chords)
        staff.show()


if  __name__ == "__main__":
    demo04()
