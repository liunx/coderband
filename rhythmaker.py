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
        self.__chordList = []
        self.chordIntervals = ['M-2', 'm-2', 'P1', 'm2', 'a1', 'M2']

    def mode(self, mode=None):
        if mode:
            self.__mode = mode
        else:
            return self.__mode

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
        return chordMap

    def triadToSeventh(self, fromChord, toChord):
        chordMap = {}
        transNotes = []
        transNoteNames = []
        for n in fromChord.notes:
            # step 1: the closest move
            if n.name not in chordMap:
                for i in self.chordIntervals:
                    tn = n.transpose(i)
                    if tn.name in toChord.pitchNames and tn.name not in transNoteNames:
                        chordMap[n.name] = [i, tn.name]
                        transNoteNames.append(tn.name)
                        transNotes.append(tn)
                        break
            # step 2: fix missed notes
            if n.name not in chordMap:
                print("missed note: {}".format(n.name))
        # step 3: fix no matched note from seventh
        diff = set.difference(set(toChord.pitchNames), set(transNoteNames))
        if len(diff) == 1:
            missNoteName = diff.pop()
            missNoteOffset = music21.note.Note(missNoteName).pitch.midi % 12
            transNoteMidis = [n.pitch.midi for n in transNotes]
            maxMidi = max(transNoteMidis)
            for i in range(maxMidi - 12, maxMidi):
                if i % 12 == missNoteOffset:
                    missNote = music21.note.Note(i)
                    break
            print("Add: {}".format(missNote.pitch.nameWithOctave))
        return chordMap

    def seventhToSeventh(self, fromChord, toChord):
        chordMap = {}
        transNotes = []
        transNoteNames = []
        for n in fromChord.notes:
            # step 1: the closest move
            if n.name not in chordMap:
                for i in self.chordIntervals:
                    tn = n.transpose(i)
                    if tn.name in toChord.pitchNames and tn.name not in transNoteNames:
                        chordMap[n.name] = [i, tn.name]
                        transNoteNames.append(tn.name)
                        transNotes.append(tn)
                        break
            # step 2: fix missed notes
            if n.name not in chordMap:
                diff = set.difference(set(toChord.pitchNames), set(transNoteNames))
                if len(diff) == 1:
                    missNoteName = diff.pop()
                    missNote = None
                    missNoteOffset = music21.note.Note(missNoteName).pitch.midi % 12
                    transNoteMidis = [n.pitch.midi for n in transNotes]
                    minMidi = min(transNoteMidis)
                    for i in range(minMidi, minMidi + 12):
                        if i % 12 == missNoteOffset:
                            missNote = music21.note.Note(i)
                            break
                    if missNote == None:
                        print("missNote {} is None!".format(missNoteName))
                        print(transNoteMidis)
                    i = music21.interval.Interval(n, missNote)
                    chordMap[n.name] = [i.directedName, missNote.name]
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
        self.__chordList = []
        self.__chordList.append([n.pitch.nameWithOctave for n in startChord.notes])
        currChord = startChord
        for chordMap in self.chordMapList:
            ll = []
            for n in currChord.notes:
                intv = chordMap.get(n.name)[0]
                tn = n.transpose(intv)
                ll.append(tn.pitch.nameWithOctave)
            currChord = music21.chord.Chord(ll)
            self.__chordList.append(ll)
        return self.__chordList


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
    mode = 'C4'
    ts3 = [['I', 'IV', 'V', 'I'],
          ['I', 'V', 'vi', 'iii', 'ii', 'V', 'I']]
    ts7 = [['I7', 'IV7', 'V7', 'I7'],
          ['ii7', 'V7', 'I7'],
          ['I7', 'IV7', 'V7'],
          ['I7', 'V7', 'vi7', 'iii7', 'ii7', 'V7', 'I7']]
    ts7 = [['I7', 'V7', 'vi7', 'iii7', 'ii7', 'V7', 'I7']]
    h = Harmony(mode)
    staff = Staff()
    for i in ts3:
        h.process(i)
        h.debug()
        rf = music21.roman.RomanNumeral(i[0], mode)
        rf.inversion(1)
        l = h.chords(rf)
        staff.read(l)
        staff.show()


if  __name__ == "__main__":
    demo04()
