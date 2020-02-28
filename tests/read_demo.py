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
    'C-': {'I': 'C-', 'II': 'D-', 'III': 'E-', 'IV': 'F-', 'V': 'G-', 'VI': 'A-', 'VII': 'B-',
          'i': 'C-', 'ii': 'D-', 'iii': 'E-', 'iv': 'F-', 'v': 'G-', 'vi': 'A-', 'vii': 'B-'},
    'F#': {'I': 'F#', 'II': 'G#', 'III': 'A#', 'IV': 'B', 'V': 'C#', 'VI': 'D#', 'VII': 'E#',
           'i': 'F#', 'ii': 'G#', 'iii': 'A#', 'iv': 'B', 'v': 'C#', 'vi': 'D#', 'vii': 'E#'},
    'G-': {'I': 'G-', 'II': 'A-', 'III': 'B-', 'IV': 'C-', 'V': 'D-', 'VI': 'E-', 'VII': 'F',
           'i': 'G-', 'ii': 'A-', 'iii': 'B-', 'iv': 'C-', 'v': 'D-', 'vi': 'E-', 'vii': 'F'},
    'C#': {'I': 'C#', 'II': 'D#', 'III': 'E#', 'IV': 'F#', 'V': 'G#', 'VI': 'A#', 'VII': 'B#',
           'i': 'C#', 'ii': 'D#', 'iii': 'E#', 'iv': 'F#', 'v': 'G#', 'vi': 'A#', 'vii': 'B#'},
    'D-': {'I': 'D-', 'II': 'E-', 'III': 'F', 'IV': 'G-', 'V': 'A-', 'VI': 'B-', 'VII': 'C',
           'i': 'D-', 'ii': 'E-', 'iii': 'F', 'iv': 'G-', 'v': 'A-', 'vi': 'B-', 'vii': 'C'},
    'A-': {'I': 'A-', 'II': 'B-', 'III': 'C', 'IV': 'D-', 'V': 'E-', 'VI': 'F', 'VII': 'G-',
           'i': 'A-', 'ii': 'B-', 'iii': 'C', 'iv': 'D-', 'v': 'E-', 'vi': 'F', 'vii': 'G-'},
    'E-': {'I': 'E-', 'II': 'F', 'III': 'G', 'IV': 'A-', 'V': 'B-', 'VI': 'C', 'VII': 'D',
           'i': 'E-', 'ii': 'F', 'iii': 'G', 'iv': 'A-', 'v': 'B-', 'vi': 'C', 'vii': 'D'},
    'B-': {'I': 'B-', 'II': 'C', 'III': 'D', 'IV': 'E-', 'V': 'F', 'VI': 'G', 'VII': 'A',
           'i': 'B-', 'ii': 'C', 'iii': 'D', 'iv': 'E-', 'v': 'F', 'vi': 'G', 'vii': 'A'},
    'F': {'I': 'F', 'II': 'G', 'III': 'A', 'IV': 'B-', 'V': 'C', 'VI': 'D', 'VII': 'E',
          'i': 'F', 'ii': 'G', 'iii': 'A', 'iv': 'B-', 'v': 'C', 'vi': 'D', 'vii': 'E'},
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
            if type(n) == note.Note:
                s = s + " {} ".format(n.pitch)
            elif type(n) == chord.Chord:
                s = s + "{"
                for n1 in n.notes:
                    s = s + " {} ".format(n1.pitch)
                s = s + "} "
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

    tp = c.parts[0]
    bp = c.parts[1]
    invs = jsData['inversion']
    for i in range(len(invs)):
        tm = tp.measure(invs[i])
        bm = bp.measure(invs[i])
        datMap[i] = [tm, bm]

    return datMap

def createPianoScore(myKey):
    s = stream.Stream()
    p1 = stream.PartStaff()
    p1.partName = "Treble"
    p1.append(clef.TrebleClef())
    p1.append(key.Key(myKey))
    p1.append(meter.TimeSignature('4/4'))

    p2 = stream.PartStaff()
    p2.partName = "Base"
    p2.append(clef.BassClef())
    p2.append(key.Key(myKey))
    p2.append(meter.TimeSignature('4/4'))

    s.append(p1)
    s.append(p2)
    return s

def transposeScore(s, key):
    pass

def measureAppend(scores, measures):
    for p, m in zip(scores, measures):
        p.append(m)

def outputMusicScore(s):
    for p in s:
        debugShow(p)
    #s.show('text')

def chordAttribChange(measure, scaleTo, keyNew):
    if len(measure.notes) == 0:
        return
    chordTo = roman.RomanNumeral(scaleTo, keyNew)
    scaleFrom = chordTo.romanNumeralAlone.upper()
    chordFrom = roman.RomanNumeral(scaleFrom, keyNew)

    thirdNameFrom = chordFrom.third.name
    thirdNameTo = chordTo.third.name
    if chordFrom.isMajorTriad() and chordTo.isMinorTriad():
        for n in measure.notes:
            if type(n) == note.Note:
                if n.name == thirdNameFrom:
                    n.name = thirdNameTo
            elif type(n) == chord.Chord:
                for n1 in n.notes:
                    if n1.name == thirdNameFrom:
                        n1.name = thirdNameTo


def measureTranspose(measureFrom, measureTo):
    if len(measureFrom.notes) == 0 or len(measureTo.notes) == 0:
        return
    bassFrom = chord.Chord(measureFrom.notes).bass()
    bassTo = chord.Chord(measureTo.notes).bass()
    intv = interval.Interval(bassFrom, bassTo)
    semitoneMajor3 = interval.Interval('M3').semitones
    if abs(intv.semitones) > semitoneMajor3:
        if intv.direction < 0:
            measureTo.transpose('P8', inPlace=True)
        else:
            measureTo.transpose('P-8', inPlace=True)


def scoreProcess(scaleDegreeProgress, keyNew, jsDat, s):
    keyScales = scalesMap[keyNew]
    scaleFrom = None
    inversionFrom = 0
    measureFrom = None
    scaleTo = None
    inversionTo = 0
    measureTo = None
    for scale in scaleDegreeProgress:
        if scaleFrom is None:
            scaleFrom = scale
        scaleTo = scale
        fromNote = note.Note(keyScales[scaleFrom])
        toNote = note.Note(keyScales[scaleTo])
        # fix argument chords
        intv = interval.Interval(fromNote, toNote)
        if intv.name not in triadInversionMap:
            intv = interval.Interval(intv.semitones)
        if intv.direction < 0:
            intv = intv.reverse()
            t1 = triadInversionMap['P1']
            f1 = triadInversionMap[intv.name]
        else:
            f1 = triadInversionMap['P1']
            t1 = triadInversionMap[intv.name]
        newMap = dict(zip(f1, t1))
        inversionTo = newMap[inversionFrom]
        intv = interval.Interval(note.Note(keyScales['I']), toNote)
        tm = jsDat[inversionTo][0]
        bm = jsDat[inversionTo][1]
        tm = tm.transpose(intv)
        bm = bm.transpose(intv)
        if measureFrom is None:
            measureFrom = [tm, bm]
        measureTo = [tm, bm]
        for f, t in zip(measureFrom, measureTo):
            measureTranspose(f, t)
            chordAttribChange(t, scaleTo, keyNew)
        measureAppend(s, measureTo)

        scaleFrom = scale
        inversionFrom = inversionTo
        measureFrom = measureTo



if  __name__ == "__main__":
    xmlFile = '../musiclib/piano/rythmic_06.mxl'
    jsFile = '../musiclib/piano/rythmic_06.json'
    debug = True
    if not debug:
        keysNew = scalesMap.keys()
        scaleDegreeProgress = [["I", "IV", "V", "iii", "vi", "ii", "V", "I"],
                               ["I", "IV", "V", "I"],
                               ["vi", "ii", "V", "I"],
                               ["I", "vi", "ii", "V"],
                               ["ii", "V", "I"],
                               ["I", "IV", "ii", "V", "I"]]
    else:
        keysNew = ['C']
        scaleDegreeProgress = [["I", "IV", "V", "iii", "vi", "ii", "V", "I"]]

    for k in keysNew:
        print("======================= {} ==============================".format(k))
        for scales in scaleDegreeProgress:
            jsDat = loadMusicXml(k, xmlFile, jsFile)
            scores = createPianoScore(k)
            scoreProcess(scales, k, jsDat, scores)
            outputMusicScore(scores)
            print("=========================================================")
