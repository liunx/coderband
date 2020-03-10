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


def demo02():
    ts1 = ['I', 'V', 'vi', 'iii', 'ii', 'V', 'I']
    ts2 = ['I7', 'V7', 'vi7', 'iii7', 'ii7', 'V7', 'I7']
    ts3 = ['I', 'IV', 'V7', 'I']

    modeList = ['C', 'C#', 'D-', 'D', 'E-', 'E', 'F',
                'F#', 'G-', 'G', 'A-', 'A', 'B-', 'B']
    modeList = ['C']

    ts4 = [['I', 'V7'], ['I', 'ii7'], ['I', 'iii7'], ['I', 'IV7']]
    ts5 = [['V7', 'I'], ['IV7', 'I'], ['I7', 'V']]


class Staff:
    def __init__(self):
        self.staffInited = {}
        self.a0 = music21.note.Note('A0')
        self.c8 = music21.note.Note('C8')
        for i in range(self.a0.pitch.midi, self.c8.pitch.midi + 1):
            self.staffInited[i] = []

    def read(self, chords):
        self.staff = copy.deepcopy(self.staffInited)
        step = 0
        for notes in chords:
            for n in notes:
                nt = music21.note.Note(n)
                nt.offset = step
                self.staff[nt.pitch.midi].append(nt)
            step = step + 1
        self.staff['step'] = step

    def show(self):
        staffStep = self.staff.pop('step')
        i = self.a0.pitch.midi
        for i in range(self.a0.pitch.midi, self.c8.pitch.midi + 1):
            if bool(self.staff[i]):
                break
            self.staff.pop(i)

        for i in range(self.c8.pitch.midi, self.a0.pitch.midi - 1, -1):
            if bool(self.staff[i]):
                break
            self.staff.pop(i)

        keys = list(self.staff.keys())
        keys.sort()
        keys.reverse()
        print("The sheet:")
        print("_{}_".format("____" * staffStep))
        odd = 0
        for k in keys:
            notes = self.staff[k]
            if not bool(notes):
                continue
            s = "|"
            for step in range(staffStep):
                flag = False
                for n in notes:
                    if n.offset == step:
                        if odd % 2:
                            s = s + "{:-^4}".format(n.pitch.nameWithOctave)
                        else:
                            s = s + "{:^4}".format(n.pitch.nameWithOctave)
                        flag = True
                if not flag:
                    if odd %2:
                        s = s + "----"
                    else:
                        s = s + "    "
            s = s + "|"
            odd = odd + 1
            print(s)
        print("|{}|".format("____" * staffStep))


class Harmony:
    def __init__(self, mode):
        self.__mode = mode
        self.chordIntervals = ['M-2', 'm-2', 'P1', 'm2', 'a1', 'M2']

    def mode(self, mode=None):
        if mode:
            self.__mode = mode
        else:
            return self.__mode

    def flatList(self, fromList, toList):
        for i in fromList:
            if type(i) == list:
                self.flatList(i, toList)
            else:
                toList.append(i)

    def interval(self, fromName, toName):
        fromNote = music21.note.Note(fromName)
        toNote = music21.note.Note(toName)
        p4 = music21.interval.Interval('P4')
        up = False
        intv = music21.interval.Interval(fromNote, toNote)
        if intv.direction.value < 0:
            intv = intv.reverse()
            up = True
        if intv.semitones > p4.semitones:
            intv = music21.interval.subtract(['P8', intv])
        if up:
            intv = intv.reverse()
        return intv.name

    def triadToTriad(self, fromChord, toChord):
        chordMap = {}
        transNotes = []
        for n in fromChord.notes:
            # step 1: the closest move
            if n.name not in chordMap:
                for i in self.chordIntervals:
                    tn = n.transpose(i)
                    if tn.name in toChord.pitchNames and tn.name not in transNotes:
                        chordMap[n.name] = [i, tn.name]
                        transNotes.append(tn.name)
                        break
            # step 2: fix missed notes
            if n.name not in chordMap:
                print("!!!Missed note: {}".format(n.name))
                diff = set.difference(set(toChord.pitchNames), set(transNotes))
                if len(diff) == 1:
                    missed = diff.pop()
                    intv = self.interval(n.name, missed)
                    chordMap[n.name] = [intv.name, missed]
        return chordMap


    def triadToSeventh(self, fromChord, toChord):
        chordMap = {}
        for n in fromChord.notes:
            # step 1: the closest move
            if n.name not in chordMap:
                for i in self.chordIntervals:
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
            # enlarge the search range
            #tn = findClosetNote(n, chordMap.values())
            print("Add missed note {} to {}".format(n, tn))
            for k in chordMap.keys():
                if chordMap[k] == tn:
                    chordMap[k] = [tn, n]
                    break
        return chordMap


    def seventhToSeventh(self, fromChord, toChord):
        chordMap = {}
        for n in fromChord.notes:
            # step 1: the closest move
            if n.name not in chordMap:
                for i in self.chordIntervals:
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


    def seventhToTriad(self, fromChord, toChord):
        chordMap = {}
        for n in fromChord.notes:
            if n == fromChord.seventh:
                continue
            # step 1: the closest move
            if n.name not in chordMap:
                for i in self.chordIntervals:
                    tn = n.transpose(i)
                    if tn.name in toChord.pitchNames and tn.name not in chordMap.values():
                        chordMap[n.name] = tn.name
                        break
            # step 2: fix missed notes
            if n.name not in chordMap:
                print("missed note: {}".format(n.name))
        return chordMap

    def process(self, scaleList, fromChord=None):
        self.chordMapList = []
        fromScale = None
        for scale in scaleList:
            if not bool(fromChord):
                fromChord = music21.roman.RomanNumeral(scale, self.__mode)
                fromScale = scale
                continue

            print("from {} ==> {}".format(fromScale, scale))
            fromChord = music21.roman.RomanNumeral(fromScale, self.__mode)
            toChord = music21.roman.RomanNumeral(scale,self.__mode)

            if fromChord.isTriad() and toChord.isTriad():
                chordMap = self.triadToTriad(fromChord, toChord)
            elif fromChord.isSeventh() and toChord.isSeventh():
                chordMap = self.seventhToSeventh(fromChord, toChord)
            elif fromChord.isTriad() and toChord.isSeventh():
                chordMap = self.triadToSeventh(fromChord, toChord)
            elif fromChord.isSeventh() and toChord.isTriad():
                chordMap = self.seventhToTriad(fromChord, toChord)
            else:
                print("Unfinished situation!")
                print("{} ==> {}".format(fromScale, scale))
            fromScale = scale
            self.chordMapList.append(chordMap)

    def debug(self):
        print(self.chordMapList)

    def chords(self, startChord):
        l = []
        l.append([n.pitch.nameWithOctave for n in startChord.notes])
        currChord = startChord
        for chordMap in self.chordMapList:
            ll = []
            for n in currChord.notes:
                intv = chordMap.get(n.name)[0]
                tn = n.transpose(intv)
                ll.append(tn.pitch.nameWithOctave)
            currChord = music21.chord.Chord(ll)
            l.append(ll)
        return l


def demo03():
    chords = [['C4', 'E4', 'G4'], ['C4', 'F4', 'A4'], ['B3', 'F4', 'G4'],
              ['C4', 'E4', 'G4'], ['C4', 'E4', 'G4'], ['C4', 'F4', 'A4'],
              ['C4', 'E4', 'G4'], ['C4', 'E4', 'G4'], ['C4', 'F4', 'A4'],
              ['B3', 'F4', 'G4'], ['C4', 'E4', 'G4']]
    staff = Staff()
    staff.read(chords)
    staff.show()
    staff.read(chords)
    staff.show()


def demo04():
    ts = ['I', 'IV', 'V7', 'I']
    ts = ['I', 'V', 'vi', 'iii', 'ii', 'V', 'I']
    h = Harmony('C4')
    staff = Staff()
    h.process(ts)
    #h.debug()
    cs = music21.chord.Chord('C4 E4 G4')
    l = h.chords(cs)
    staff.read(l)
    staff.show()


if  __name__ == "__main__":
    demo04()
