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
    'P5': [2, 1, 0],
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
    #scaleDegreeProgress = ["I", "ii", "iii", "IV", "V", "vi", "VII", "I"]
    scaleDegreeProgress = ["II", "VII", "I"]
    keyIntervalMap = {"C": "P1", "C#": "A1", "D": "M2", "D#": "A2", "E": "M3", "F": "P4", "F#": "A4", "G": "P5", "G#": "A5", "A": "M6", "A#": "A6", "B": "M7"}
    fromKey = 'C'
    toKey = 'C'

    c = converter.parse('rythmic_01.mxl')

    # transpose to new key
    i = interval.Interval(note.Note(fromKey), note.Note(toKey))
    delta = interval.Interval('P4')
    if i.semitones > delta.semitones:
        i = interval.subtract([i, "P8"])
    c.transpose(i, inPlace=True)
    treblePart = c.parts[0]
    basePart = c.parts[1]
    with open("rythmic_01.json") as js:
        jsData = json.load(js)

    s = stream.Stream()
    s.append(key.Key(toKey))
    s.append(meter.TimeSignature('4/4'))
    p1 = stream.Part()
    p2 = stream.Part()
    s.append(p1)
    s.append(p2)
    p1.append(clef.TrebleClef())
    p1.append(key.Key(toKey))
    p1.append(meter.TimeSignature('4/4'))
    p2.append(clef.BassClef())
    p2.append(key.Key(toKey))
    p2.append(meter.TimeSignature('4/4'))

    fromScaleDegree = {"scaleDegree": None, "inversion": 0}
    toScaleDegree = {"scaleDegree": None, "inversion": 0}

    for scaleDegree in scaleDegreeProgress:
        if fromScaleDegree['scaleDegree'] is None:
            fromScaleDegree['scaleDegree'] = scaleDegree
        if toScaleDegree['scaleDegree'] is None:
            toScaleDegree['scaleDegree'] = scaleDegree

        if scaleDegree in majorScaleDegreeMap:
            intv = majorScaleDegreeMap[scaleDegree]
        elif scaleDegree in minorScaleDegreeMap:
            intv = minorScaleDegreeMap[scaleDegree]
        else:
            print("Undefined sacle degree: {}".format(scaleDegree))

        if intv in ["P1", "M2", "M3"]:
            tp = treblePart.measure(2)
            bp = basePart.measure(2)
        if intv in ["P4"]:
            tp = treblePart.measure(4)
            bp = basePart.measure(4)
        if intv in ["P5"]:
            tp = treblePart.measure(3)
            bp = basePart.measure(3)
            intv = interval.subtract([intv, "P8"])
        if intv in ["M6", "M7"]:
            tp = treblePart.measure(3)
            bp = basePart.measure(3)
            #intv = interval.subtract([intv, "P8"])
        p1.append(tp.transpose(intv))
        p2.append(bp.transpose(intv))

    #s.show('text')
    debugShow(p2)

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


def loadMusicXml(xmlFile, jsonFile):
    datMap = {}
    c = converter.parse(xmlFile)
    with open(jsonFile) as js:
        jsData = json.load(js)
    print(jsData)
    invs = jsData['inversion']
    for i in range(len(invs)):
        datMap[i] = c.measure(invs[i])

    return datMap

def createPianoScore(myKey):
    s = stream.Stream()
    p1 = stream.Part()
    p2 = stream.Part()
    s.append(p1)
    s.append(p2)
    p1.append(clef.TrebleClef())
    p1.append(key.Key(myKey))
    p1.append(meter.TimeSignature('4/4'))
    p2.append(clef.BassClef())
    p2.append(key.Key(myKey))
    p2.append(meter.TimeSignature('4/4'))
    return s

def transposeScore(oldScore, intv):
    pass

def appendScore(myScore, newScore):
    newScore.show('text')

def outputMusicScore(s):
    s.show('text')

def demo2():
    key = 'C'
    scaleDegreeProgress = ["I", "vi", "IV", "V", "ii", "V", "I"]
    keyScales = scalesMap[key]
    jsDat = loadMusicXml('rythmic_01.mxl', 'rythmic_01.json')
    s = createPianoScore('C')
    fromScale = None
    fromInversion = 0
    toScale = None
    toInversion = 0
    for scale in scaleDegreeProgress:
        if fromScale is None:
            fromScale = scale
        toScale = scale
        fromNote = note.Note(keyScales[fromScale])
        toNote = note.Note(keyScales[toScale])
        intv = interval.Interval(fromNote, toNote)
        print(fromNote.name, toNote.name, intv.name)
        if intv.direction < 0:
            intv.reverse()
        f1 = triadInversionMap['P1']
        t1 = triadInversionMap[intv.name]
        newMap = dict(zip(f1, t1))
        print("new map: {}".format(newMap))
        toInversion = newMap[fromInversion]
        print("Inversion: from {} to {}".format(fromInversion, toInversion))
        s1 = jsDat[toInversion]
        appendScore(s, s1)

        fromScale = scale
        fromInversion = toInversion

    outputMusicScore(s)


if  __name__ == "__main__":
    demo2()
