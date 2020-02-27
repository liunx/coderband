#!/usr/bin/env python3

from music21 import *
import copy
import json

environment.set('musicxmlPath', '/usr/bin/musescore')


scalesMap = {
    'G': {'I': 'G', 'II': 'A', 'III': 'B', 'IV': 'C', 'V': 'D', 'VI': 'E', 'VII': 'F#',
          'i': 'G', 'ii': 'A', 'iii': 'B', 'iv': 'C', 'v': 'D', 'vi': 'E', 'vii': 'F#'},
    'D': {'I': 'D', 'II': 'E', 'III': 'F#', 'IV': 'G', 'V': 'A', 'VI': 'B', 'VII': 'C#',
          'i': 'D', 'ii': 'E', 'iii': 'F#', 'iv': 'G', 'v': 'A', 'vi': 'B', 'vii': 'C#'},
    'A': {'I': 'A', 'II': 'B', 'III': 'C#', 'IV': 'D', 'V': 'E', 'VI': 'F#', 'VII': 'G#',
          'i': 'A', 'ii': 'B', 'iii': 'C#', 'iv': 'D', 'v': 'E', 'vi': 'F#', 'vii': 'G#'},
    'E': {'I': 'E', 'II': 'F#', 'III': 'G#', 'IV': 'A', 'V': 'B', 'VI': 'C#', 'VII': 'D#',
          'i': 'E', 'ii': 'F#', 'iii': 'G#', 'iv': 'A', 'v': 'B', 'vi': 'C#', 'vii': 'D#'},
    'B': {'I': 'B', 'II': 'C#', 'III': 'D#', 'IV': 'E', 'V': 'F#', 'VI': 'G#', 'VII': 'A#',
          'i': 'B', 'ii': 'C#', 'iii': 'D#', 'iv': 'E', 'v': 'F#', 'vi': 'G#', 'vii': 'A#'},
    'F#': {'I': 'F#', 'II': 'G#', 'III': 'A#', 'IV': 'B', 'V': 'C#', 'VI': 'D#', 'VII': 'F',
           'i': 'F#', 'ii': 'G#', 'iii': 'A#', 'iv': 'B', 'v': 'C#', 'vi': 'D#', 'vii': 'F'},
    'C#': {'I': 'C#', 'II': 'D#', 'III': 'F', 'IV': 'F#', 'V': 'G#', 'VI': 'A#', 'VII': 'C',
           'i': 'C#', 'ii': 'D#', 'iii': 'F', 'iv': 'F#', 'v': 'G#', 'vi': 'A#', 'vii': 'C'},
    'G#': {'I': 'G#', 'II': 'A#', 'III': 'C', 'IV': 'C#', 'V': 'D#', 'VI': 'F', 'VII': 'G',
           'i': 'G#', 'ii': 'A#', 'iii': 'C', 'iv': 'C#', 'v': 'D#', 'vi': 'F', 'vii': 'G'},
    'D#': {'I': 'D#', 'II': 'F', 'III': 'G', 'IV': 'G#', 'V': 'A#', 'VI': 'C', 'VII': 'D',
           'i': 'D#', 'ii': 'F', 'iii': 'G', 'iv': 'G#', 'v': 'A#', 'vi': 'C', 'vii': 'D'},
    'A#': {'I': 'A#', 'II': 'C', 'III': 'D', 'IV': 'D#', 'V': 'F', 'VI': 'G', 'VII': 'A',
           'i': 'A#', 'ii': 'C', 'iii': 'D', 'iv': 'D#', 'v': 'F', 'vi': 'G', 'vii': 'A'},
    'F': {'I': 'F', 'II': 'G', 'III': 'A', 'IV': 'A#', 'V': 'C', 'VI': 'D', 'VII': 'E',
          'i': 'F', 'ii': 'G', 'iii': 'A', 'iv': 'A#', 'v': 'C', 'vi': 'D', 'vii': 'E'},
    'C': {'I': 'C', 'II': 'D', 'III': 'E', 'IV': 'F', 'V': 'G', 'VI': 'A', 'VII': 'B',
          'i': 'C', 'ii': 'D', 'iii': 'E', 'iv': 'F', 'v': 'G', 'vi': 'A', 'vii': 'B'}}

triadInversionMap = {
    'P1': [0, 1, 2],
    'P8': [0, 1, 2],
    'm2': [0, 1, 2],
    'M2': [0, 1, 2],
    'm3': [2, 0, 1],
    'M3': [2, 0, 1],
    'P4': [2, 0, 1],
    'd5': [2, 1, 0],
    'P5': [1, 2, 0],
    'm6': [1, 2, 0],
    'M6': [1, 2, 0],
    'm7': [0, 1, 2],
    'M7': [0, 1, 2]}

scaleDegreeMap = {
    'I': ['P1', 'P8'],
    'II': ['m2', 'M2'],
    'III': ['m3', 'M3'],
    'IV': ['P4'],
    'V': ['d5', 'P5'],
    'VI': ['m6', 'M6'],
    'VII': ['m7', 'M7'],
    'i': ['P1', 'P8'],
    'ii': ['m2', 'M2'],
    'iii': ['m3', 'M3'],
    'iv': ['P4'],
    'v': ['d5', 'P5'],
    'vi': ['m6', 'M6'],
    'vii': ['m7', 'M7']}


def debugShow(p):
    s = ""
    for m in p.getElementsByClass(stream.Measure):
        s = s + "|"
        for n in m.notes:
            s = s + " {} ".format(n.pitch)
        s = s + "|\n"
    print(s)

def generateFifthCircle():
    cScales = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    fixScales = {'E#': 'F', 'B#': 'C'}
    currScales = cScales
    scaleDegreeTable1 = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    scaleDegreeTable2 = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
    while True:
        tmpScales = []
        for i in currScales:
            n = note.Note(i)
            nm = n.transpose('P5').name
            if nm in fixScales:
                nm = fixScales[nm]
            tmpScales.append(nm)
        d1 = dict(zip(scaleDegreeTable1, tmpScales))
        d2 = dict(zip(scaleDegreeTable2, tmpScales))
        md = {**d1, **d2}
        print("'{}': {},".format(tmpScales[0], md))
        currScales = tmpScales
        if tmpScales[0] == cScales[0]:
            break

def calcInterval():
    key = 'C'
    a = 'II'
    b = 'V'
    scales = scalesMap[key]
    aIndex = scaleDegreeMap[a]
    bIndex = scaleDegreeMap[b]
    aNote = note.Note(scales[aIndex])
    bNote = note.Note(scales[bIndex])
    print(aNote, bNote)
    i = interval.Interval(aNote, bNote)
    print(i, i.generic.value)
    toInversion = inversionMap[i.generic.value]
    fromInversion = inversionMap[1]
    print("from: {}, to: {}".format(fromInversion, toInversion))
    newMap = dict(zip(fromInversion, toInversion))
    print(newMap)


def loadMusicXml(newKey, xmlFile, jsonFile):
    datMap = {}
    c = converter.parse(xmlFile)
    with open(jsonFile) as js:
        jsData = json.load(js)
    oldKey = jsData['key']
    intv = interval.Interval(note.Note(oldKey), note.Note(newKey))
    c.transpose(intv, inPlace=True)
    p = c.parts[1]
    invs = jsData['inversion']
    for i in range(len(invs)):
        # get notes part
        m = p.measure(invs[i])
        datMap[i] = m

    return datMap

def createPianoScore(myKey):
    s = stream.Stream()
    p2 = stream.Part()
    s.append(p2)
    p2.append(clef.BassClef())
    p2.append(key.Key(myKey))
    p2.append(meter.TimeSignature('4/4'))
    return s

def transposeScore(s, key):
    pass

def appendMeasure(myScore, newMeasure):
    p = myScore[0]
    p.append(newMeasure)

def outputMusicScore(s):
    debugShow(s[0])
    #s.show()

def demo2():
    key = 'C'
    scaleDegreeProgress = ["I", "IV", "V", "III", "VI", "II", "V", "I"]
    scaleDegreeProgress = ["I", "IV", "V", "IV", "I"]
    keyScales = scalesMap[key]
    jsDat = loadMusicXml(key, 'rythmic_01.mxl', 'rythmic_01.json')
    s = createPianoScore(key)
    fromScale = None
    fromInversion = 0
    fromMeasure = None
    toScale = None
    toInversion = 0
    toMeasure = None
    for scale in scaleDegreeProgress:
        if fromScale is None:
            fromScale = scale
        toScale = scale
        fromNote = note.Note(keyScales[fromScale])
        toNote = note.Note(keyScales[toScale])
        intv = interval.Interval(fromNote, toNote)
        if intv.direction < 0:
            intv = intv.reverse()
            t1 = triadInversionMap['P1']
            f1 = triadInversionMap[intv.name]
        else:
            f1 = triadInversionMap['P1']
            t1 = triadInversionMap[intv.name]
        newMap = dict(zip(f1, t1))
        toInversion = newMap[fromInversion]
        print("fromKey: {}, inversion: {}, toKey: {}, inversion: {}, interval: {}"\
              .format(fromNote.name, fromInversion, toNote.name, toInversion, intv.name))
        m = jsDat[toInversion]
        intv = interval.Interval(note.Note(keyScales['I']), toNote)
        m = m.transpose(intv)
        if fromMeasure is None:
            fromMeasure = m
        toMeasure = m

        # compare the lowest pitches
        fromBass = chord.Chord(fromMeasure).bass()
        toBass = chord.Chord(toMeasure).bass()
        intv = interval.Interval(fromBass, toBass)
        semitoneMajor3 = interval.Interval('M3').semitones
        if abs(intv.semitones) > semitoneMajor3:
            if intv.direction < 0:
                m.transpose('P8', inPlace=True)
            else:
                m.transpose('P-8', inPlace=True)

        appendMeasure(s, m)

        fromScale = scale
        fromInversion = toInversion
        fromMeasure = toMeasure

    outputMusicScore(s)


if  __name__ == "__main__":
    demo2()
