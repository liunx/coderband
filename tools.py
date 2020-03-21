#!/usr/bin/env python3

import music21
import math


diatonics = {
    'Lydian': [0, 2, 4, 6, 7, 9, 11],
    'Ionian': [0, 2, 4, 5, 7, 9, 11],
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'Dorian': [0, 2, 3, 5, 7, 9, 10],
    'Aeolian': [0, 2, 3, 5, 7, 8, 10],
    'Phrygian': [0, 1, 3, 5, 7, 8, 10],
    'Locrian': [0, 1, 3, 5, 6, 8, 10]
}


melodicMinors = {
    'B' : [0, 1, 3, 4, 6, 8, 10],
    'D' : [0, 1, 3, 5, 7, 9, 10],
    'A' : [0, 2, 3, 5, 6, 8, 10],
    'G' : [0, 2, 4, 5, 7, 8, 10],
    'F' : [0, 2, 4, 6, 7, 9, 10],
    'Eb': [0, 2, 4, 6, 8, 9, 11],
    'C' : [0, 2, 3, 5, 7, 9, 11]
}

diminishedScales = {
    'F': [0, 2, 3, 5, 6, 8, 9, 11],
    'G': [0, 1, 3, 4, 6, 7, 9, 10]
}

wholeToneScales = {'G': [0, 2, 4, 6, 8, 10]}

tuningRatio = [[1, 1], [16, 15], [9, 8], [6, 5], [5, 4], [4, 3],
               [45, 32], [3, 2], [8, 5], [5, 3], [9, 5], [15, 8]]


def scaleVectorCalc(scales):
    cNoteScales = []
    for noteName in scales:
        note = music21.note.Note(noteName)
        cNoteScales.append(note)
    currNoteScales = []
    for i in range(len(scales)):
        scaleVector = []
        if not bool(currNoteScales):
            currNoteScales = cNoteScales
        modeNote = currNoteScales[0]
        modeNoteMidi = modeNote.pitch.midi
        for n in currNoteScales:
            v = n.pitch.midi - modeNoteMidi
            scaleVector.append(v)
        print("\'{}\': {},".format(modeNote.name, scaleVector))
        newNote = modeNote.transpose('P8')
        currNoteScales.pop(0)
        currNoteScales.append(newNote)

def scaleGenerate():
    natureScale = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
    melodicScale = ['C4', 'D4', 'Eb4', 'F4', 'G4', 'A4', 'B4']
    diminishedScale = ['F4', 'G4', 'Ab4', 'A#4', 'B4', 'C#5', 'D5', 'E5']
    wholeToneScale = ['G4', 'A4', 'B4', 'C#5', 'D#5', 'F5']
    scaleVectorCalc(natureScale)
    print("==================")
    scaleVectorCalc(melodicScale)
    print("==================")
    scaleVectorCalc(diminishedScale)
    print("==================")
    scaleVectorCalc(wholeToneScale)

def fifthCircle():
    firstNote = music21.note.Note('F')
    currNote = firstNote
    l = [firstNote.pitch.unicodeName]
    while True:
        n = currNote.transpose('P5')
        p = n.pitch.getEnharmonic()
        if firstNote.pitch.name in [n.name, p.name]:
            break
        if n.pitch.alter == 0:
            l.append(n.pitch.unicodeName)
        else:
            l.append("{}/{}".format(n.pitch.unicodeName, p.unicodeName))
        currNote = n
    print("Fifth Circle:")
    drawCircle(l)


def showTab(tab, indent=8):
    keys = list(tab.keys())
    keys.sort()
    for k in keys:
        if k == keys[-1]:
            last = True
        s = "[{}]".format(k)
        s1 = "  |"
        l = tab[k]
        last = False
        n = 1
        for i in l:
            if n == len(l):
                last = True
            if k in [1, 2]:
                strFormat = "{:-^"  + str(indent) + "}"
            elif k in [3, 4]:
                strFormat = "{:*^"  + str(indent) + "}"
            elif k in [5, 6]:
                strFormat = "{:=^"  + str(indent) + "}"
            s = s + strFormat.format(i)
            if last:
                s = s + "[{}]".format(k)
            else:
                s = s + "|"
            strFormat = "{:^"  + str(indent) + "}"
            s1 = s1 + strFormat.format('')
            s1 = s1 + "|"
            n = n + 1
        print(s)
        if k != keys[-1]:
            print(s1)


def markNotes(l, note, noteNames, pos=False):
    mid = int(len(l) / 2)
    if note.name in noteNames:
        if pos:
            l[mid] = "[ {} ]".format(note.pitch.name)
        else:
            l[mid] = "({})".format(note.pitch.name)
    for i in range(1, mid):
        n = note.transpose(i)
        p = n.pitch.getEnharmonic()
        if n.name in noteNames:
            l[i + mid] = "({})".format(n.pitch.name)
        if p.name in noteNames:
            l[i + mid] = "({})".format(p.name)
    for i in range(1, mid + 1):
        n = note.transpose(-i)
        p = n.pitch.getEnharmonic()
        if n.name in noteNames:
            l[mid - i] = "({})".format(n.pitch.name)
        if p.name in noteNames:
            l[mid - i] = "({})".format(p.name)


def markNumbers(l, num, intervals, pos=False):
    mid = int(len(l) / 2)
    if num in intervals:
        if pos:
            l[mid] = "[ {} ]".format(num)
        else:
            l[mid] = "({})".format(num)
    for i in range(1, mid):
        n = (num + i) % 12
        if n in intervals:
            l[mid + i] = "({})".format(n)
    for i in range(1, mid + 1):
        n = abs(12 + num - i) % 12
        if n in intervals:
            l[mid - i] = "({})".format(n)


def tabChord(line, noteName, romanNum):
    h = 6
    w = 9
    tab = {}
    for i in range(1, h + 1):
        tab[i] = [''] * w
    rf = music21.roman.RomanNumeral(romanNum, noteName)
    noteNames = [n.name for n in rf.notes]
    l = tab[line]
    bassNote = music21.note.Note(noteName)
    markNotes(l, bassNote, noteNames, pos=True)
    currNote = None
    for i in range(line + 1, h + 1):
        if currNote == None:
            currNote = bassNote
        n = currNote.transpose('P5')
        l = tab[i]
        markNotes(l, n, noteNames)
        currNote = n
    currNote = None
    for i in range(line - 1, 0, -1):
        if currNote == None:
            currNote = bassNote
        n = currNote.transpose('P4')
        l = tab[i]
        markNotes(l, n, noteNames)
        currNote = n
    for i in [1, 2]:
        tab[i].insert(0, '')
    for i in [3, 4, 5, 6]:
        tab[i].append('')
    print("\n\nTAB {}:".format(rf.figureAndKey))
    showTab(tab)


def tabScale(line, mode, noteNames):
    h = 6
    w = 8
    tab = {}
    for i in range(1, h + 1):
        tab[i] = [''] * w
    l = tab[line]
    bassNote = music21.note.Note(mode)
    markNotes(l, bassNote, noteNames, pos=True)
    currNote = None
    for i in range(line + 1, h + 1):
        if currNote == None:
            currNote = bassNote
        n = currNote.transpose('P5')
        l = tab[i]
        markNotes(l, n, noteNames)
        currNote = n
    currNote = None
    for i in range(line - 1, 0, -1):
        if currNote == None:
            currNote = bassNote
        n = currNote.transpose('P4')
        l = tab[i]
        markNotes(l, n, noteNames)
        currNote = n
    for i in [1, 2]:
        tab[i].insert(0, '')
    for i in [3, 4, 5, 6]:
        tab[i].append('')
    print("TAB {}:".format(mode))
    showTab(tab)


def tabInterval(line, mode, intervals):
    h = 6
    w = 10
    tab = {}
    for i in range(1, h + 1):
        tab[i] = [''] * w
    l = tab[line]
    print(intervals)
    markNumbers(l, 0, intervals, pos=True)
    currNum = 0
    for i in range(line + 1, h + 1):
        n = (currNum + 5) % 12
        l = tab[i]
        markNumbers(l, n, intervals)
        currNum = n
    currNum = 0
    for i in range(line - 1, 0, -1):
        n = (currNum + 5) % 12
        l = tab[i]
        markNumbers(l, n, intervals)
        currNum = n
    for i in [1, 2]:
        tab[i].insert(0, '')
    for i in [3, 4, 5, 6]:
        tab[i].append('')
    print("TAB {}:".format(mode))
    showTab(tab)


def demo01():
    mode = 'Ionian'
    key = 'C'
    noteNames = []
    firstNote = music21.note.Note(key)
    noteNames.append(firstNote.pitch.unicodeName)
    scaleVectors = diatonics[mode]
    for v in scaleVectors[1:]:
        n = firstNote.transpose(v)
        noteNames.append(n.name)
    for i in range(1, 7):
        tabScale(i, key, noteNames)
        break


def demo02():
    key = 'C'
    for r in ['I7', 'i7']:
        for i in range(1, 7):
            tabChord(i, key, r)


def demo03():
    mode = 'Ionian'
    mode = 'Lydian'
    scaleVectors = diatonics[mode]
    tabInterval(6, mode, scaleVectors)


def triadChords(key, scales):
    for k,v in scales.items():
        vectors = [v[0], v[2], v[4]]
        root = music21.note.Note(key)
        third = root.transpose(v[2])
        fifth = root.transpose(v[4])
        cs = music21.chord.Chord([root, third, fifth])
        print(k, cs.commonName, [n.name for n in cs.notes], vectors)


def seventhChords(key, scales):
    for k,v in scales.items():
        vectors = [v[0], v[2], v[4], v[6]]
        root = music21.note.Note(key)
        third = root.transpose(v[2])
        fifth = root.transpose(v[4])
        seventh = root.transpose(v[6])
        cs = music21.chord.Chord([root, third, fifth, seventh])
        print(k, cs.commonName, [n.name for n in cs.notes], vectors)


def ninthChords(key, scales):
    for k,v in scales.items():
        vectors = [v[0], v[1], v[2], v[4], v[6]]
        root = music21.note.Note(key)
        ninth = root.transpose(v[1])
        third = root.transpose(v[2])
        fifth = root.transpose(v[4])
        seventh = root.transpose(v[6])
        cs = music21.chord.Chord([root, third, fifth, seventh, ninth])
        print(k, cs.commonName, [n.name for n in cs.notes], vectors)


def demo11():
    key = 'C'
    print("\ntriad chords:\n")
    triadChords(key, diatonics)
    triadChords(key, melodicMinors)
    print("\nseventh chords:\n")
    seventhChords(key, diatonics)
    seventhChords(key, melodicMinors)
    print("\nninth chords:\n")
    ninthChords(key, diatonics)
    ninthChords(key, melodicMinors)


def drawCircle(l):
    listLen = len(l)
    a, b = listLen + 1, listLen + 1
    width, height = (a + 1) * 2, (b + 1) * 2
    r = listLen
    map_ = [[' ' for x in range(width)] for y in range(height)]
    # draw the circle
    step = int(360 / listLen)
    i = 0
    for angle in range(0, 360, step):
        x = r * math.sin(math.radians(angle)) + a
        y = r * math.cos(math.radians(angle)) + b
        map_[int(round(y))][int(round(x))] = l[i]
        i = i + 1

    # print the map
    for line in map_:
        print(' '.join(line))


def findModesByNote(noteName):
    note = music21.note.Note(noteName)
    mode = diatonics['C']
    for i in range(len(mode)):
        currVect = mode[i]
        l = []
        for v in mode:
            intv = v - currVect
            n = note.transpose(intv)
            l.append(n.name)
        print(l)


triadChordTable = {
    "Maj": [0, 4, 7],
    "Min": [0, 3, 7],
    "Dim": [0, 3, 6],
    "Aug": [0, 4, 4]
}

seventhChordTable = {
    "Δ": [0, 4, 7, 11],
    "-Δ": [0, 3, 7, 11],
    "-Δ/G": [0, 4,  7, 8, 10],
    "7": [0, 4, 7, 10],
    "-": [0, 3, 7, 10],
    "φ": [0, 3, 6, 10],
    "°": [0, 3, 6, 9]
}

extensionChordTable = {
    "Δ♯4": [0, 4, 6, 7, 11],
    "Δ♯5": [0, 4, 8, 11],
    "7♯5": [0, 4, 8, 10],
    "7♯11": [0, 4, 6, 7, 10],
    "φ♯2": [0, 2, 3, 6, 10],
    "-♭6": [0, 3, 7, 8, 10],
    "7alt": [0, 1, 3, 4, 6, 8, 10],
}

suspendChordTable = {
    "sus": [0, 4, 5, 7, 10],
    "sus♭9": [0, 1, 7, 10],
}

"""
Δφ♭♯°
"""

def chord_demo():
    demo11()


if  __name__ == "__main__":
    chord_demo()
