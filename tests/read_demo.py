#!/usr/bin/env python3

from music21 import *
import copy

def read_xml():
    c = converter.parse('demo.xml')
    p = c.parts[0]
    p2 = p.transpose('P-8')
    #k = key.Key('D')
    #p2.insert(0, k)
    f2 = p2.flat
    f2.show('text')
    f2.show()

def tiny_note():
    s = converter.parse('tinyNotation: 4/4 C8 E8 G8 E8 G8 E8 G8 E8')
    s.show()



def replaceNote(inNote, chordStateMap):
    origChord = roman.RomanNumeral(origScaleDegree, key.Key(origNoteName))
    currChord = roman.RomanNumeral(currScaleDegree, key.Key(currNoteName))

    # find the closest note
    minSemi = 12
    semiVal = 0
    for c in currChord:
        intval = interval.Interval(inNote, c)
        dist = abs(intval.semitones) % 12
        if dist < minSemi:
            minSemi = dist
            if intval.semitones < 0:
                ndist = -dist
            else:
                semiVal = dist
    # check chordStateMap, avoid conflicts
    if chordStateMap[inNote.name] == 0:
        chordStateMap[inNote.name] = 1
    else:
        # recalculate the semitones
        minSemi = 12
        semiVal = 0
        for c in currChord:
            intval = interval.Interval(inNote, c)
            dist = abs(intval.semitones) % 12
            if dist < minSemi and dist != 0:
                minSemi = dist
                if intval.semitones < 0:
                    ndist = -dist
                else:
                    ndist = dist
    inNote.transpose(semiVal, inPlace=True)


def replaceChord(inChord, chordStateMap):
    oldChord = copy.deepcopy(inChord)
    # find the closest note
    for n in inChord:
        replaceNote(n, chordStateMap)

origNoteName = 'C'
currNoteName = 'G'
origScaleDegree = 'I'
currScaleDegree = 'I'

def chordProgress():
    c = converter.parse('piano.mxl')
    s = c.measures(2,2)
    p = s.parts[1]
    m = p[4]
    s = stream.Stream()
    s.append(key.Key('C'))
    s.append(meter.TimeSignature('4/4'))
    s.append(clef.BassClef())
    s.append(copy.deepcopy(m))
    origChord = roman.RomanNumeral(origScaleDegree, key.Key(origNoteName))
    currChord = roman.RomanNumeral(currScaleDegree, key.Key(currNoteName))

    chordStateMap = {}
    for c in origChord:
        chordStateMap[c.name] = 0

    for i in m.iter:
        if type(i) is note.Note:
            replaceNote(i, chordStateMap)
        elif type(i) is chord.Chord:
            replaceChord(i, chordStateMap)

    s.append(copy.deepcopy(m))
    s.show('text')


if __name__ == "__main__":
    chordProgress()
