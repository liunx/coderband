#!/usr/bin/env python3

from music21 import *
import copy
import json

environment.set('musicxmlPath', '/usr/bin/musescore3')

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



def replaceNote(inNote, origChord, currChord, pitchMap):
    pitchName = inNote.pitch.nameWithOctave
    if pitchName in pitchMap:
        inNote.pitch.nameWithOctave = pitchMap[pitchName]
        return
    # find the closest note
    minSemi = 12
    semiVal = 0
    distTable = []
    semiValMap = {}
    for c in currChord:
        intval = interval.Interval(inNote, c)
        dist = abs(intval.semitones) % 12
        distTable.append(dist)
        if intval.semitones < 0:
            semiVal = -dist
        else:
            semiVal = dist
        semiValMap[dist] = semiVal

    distTable.sort()
    print(distTable)
    for dist in distTable:
        semiVal = semiValMap[dist]
        tmpNote = inNote.transpose(semiVal)
        pitchName = tmpNote.pitch.nameWithOctave
        if pitchName not in pitchMap.values():
            inNote.pitch.nameWithOctave = pitchName
            pitchMap[inNote.pitch.nameWithOctave] = pitchName
            break


def replaceChord(inChord, origChord, currChord, pitchMap):
    oldChord = copy.deepcopy(inChord)
    # find the closest note
    for n in inChord:
        replaceNote(n, origChord, pitchMap)

origKey = 'C'
currKey = 'G'
origScaleDegree = 'I'
currScaleDegree = 'I'

def chordProgress():
    c = converter.parse('piano.mxl')
    s = c.measures(2,2)
    p = s.parts[1]
    m = p[4]
    s = stream.Stream()
    s.append(key.Key(origKey))
    s.append(meter.TimeSignature('4/4'))
    s.append(clef.BassClef())
    s.append(copy.deepcopy(m))
    origChord = roman.RomanNumeral(origScaleDegree, key.Key(origKey))
    currChord = roman.RomanNumeral(currScaleDegree, key.Key(currKey))

    pitchMap = {}
    if currKey != origKey:
        for i in m.iter:
            if type(i) is note.Note:
                replaceNote(i, origChord, currChord, pitchMap)
            elif type(i) is chord.Chord:
                replaceChord(i, origChord, currChord, pitchMap)

    s.append(copy.deepcopy(m))
    s.show()

def demo():
    scaleDegreeProgress = ["I", "IV", "V", "I"]
    scaleDegreeMap = {"I": "C", "IV": "F", "V": "G"}
    kf = key.Key('C')

    c = converter.parse('rythmic_01.mxl')
    treblePart = c.parts[0]
    basePart = c.parts[1]
    with open("rythmic_01.json") as js:
        jsData = json.load(js)

    s = stream.Stream()
    s.append(key.Key(origKey))
    s.append(meter.TimeSignature('4/4'))
    p1 = stream.Part()
    p2 = stream.Part()
    s.insert(0, p1)
    s.insert(0, p2)
    p1.append(clef.TrebleClef())
    p2.append(clef.BassClef())
    for scaleDegree in scaleDegreeProgress:
        pass

    s.show('text')

if  __name__ == "__main__":
    demo()
