#!/usr/bin/env python3

import music21


natureScales = {
    'C': [0, 2, 4, 5, 7, 9, 11],
    'D': [0, 2, 3, 5, 7, 9, 10],
    'E': [0, 1, 3, 5, 7, 8, 10],
    'F': [0, 2, 4, 6, 7, 9, 11],
    'G': [0, 2, 4, 5, 7, 9, 10],
    'A': [0, 2, 3, 5, 7, 8, 10],
    'B': [0, 1, 3, 5, 6, 8, 10]
}

melodicScales = {
    'C': [0, 2, 3, 5, 7, 9, 11],
    'D': [0, 1, 3, 5, 7, 9, 10],
    'Eb': [0, 2, 4, 6, 8, 9, 11],
    'F': [0, 2, 4, 6, 7, 9, 10],
    'G': [0, 2, 4, 5, 7, 8, 10],
    'A': [0, 2, 3, 5, 6, 8, 10],
    'B': [0, 1, 3, 4, 6, 8, 10],

}

diminishedScales = {
    'F': [0, 2, 3, 5, 6, 8, 9, 11],
    'G': [0, 1, 3, 4, 6, 7, 9, 10]
}

wholeToneScales = {'G': [0, 2, 4, 6, 8, 10]}


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
    print(firstNote.name)
    while True:
        n = currNote.transpose('P5')
        p = n.pitch.getEnharmonic()
        if firstNote.pitch.name in [n.name, p.name]:
            break
        if n.pitch.alter == 0:
            print(n.name)
        else:
            print("{}/{}".format(n.name, p.name))
        currNote = n


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
            l[mid] = "[ {} ]".format(note.pitch.unicodeName)
        else:
            l[mid] = "({})".format(note.pitch.unicodeName)
    for i in range(1, mid):
        n = note.transpose(i)
        p = n.pitch.getEnharmonic()
        if n.name in noteNames:
            l[i + mid] = "({})".format(n.pitch.unicodeName)
        if p.name in noteNames:
            l[i + mid] = "({})".format(p.unicodeName)
    for i in range(1, mid + 1):
        n = note.transpose(-i)
        p = n.pitch.getEnharmonic()
        if n.name in noteNames:
            l[mid - i] = "({})".format(n.pitch.unicodeName)
        if p.name in noteNames:
            l[mid - i] = "({})".format(p.unicodeName)


def tabNoteNamess(line, noteName, romanNum):
    h = 6
    w = 7
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
    print("TAB {}:".format(rf.figureAndKey))
    showTab(tab)


def tabScales(line, mode, noteNames):
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


def demo01():
    mode = 'F'
    line = 1
    noteNames = []
    firstNote = music21.note.Note(mode)
    noteNames.append(firstNote.pitch.unicodeName)
    scaleVectors = natureScales[mode]
    for v in scaleVectors[1:]:
        n = firstNote.transpose(v)
        noteNames.append(n.name)
    print(noteNames)
    for i in range(1, 7):
        tabScales(i, mode, noteNames)
        break


def triadChords(scales):
    for k,v in scales.items():
        vectors = [v[0], v[2], v[4]]
        root = music21.note.Note(k)
        third = root.transpose(v[2])
        fifth = root.transpose(v[4])
        cs = music21.chord.Chord([root, third, fifth])
        print(k, cs.commonName, [n.name for n in cs.notes], vectors)


def seventhChords(scales):
    for k,v in scales.items():
        vectors = [v[0], v[2], v[4], v[6]]
        root = music21.note.Note(k)
        third = root.transpose(v[2])
        fifth = root.transpose(v[4])
        seventh = root.transpose(v[6])
        cs = music21.chord.Chord([root, third, fifth, seventh])
        print(k, cs.commonName, [n.name for n in cs.notes], vectors)


def ninthChords(scales):
    for k,v in scales.items():
        vectors = [v[0], v[1], v[2], v[4], v[6]]
        root = music21.note.Note(k)
        ninth = root.transpose(v[1])
        third = root.transpose(v[2])
        fifth = root.transpose(v[4])
        seventh = root.transpose(v[6])
        cs = music21.chord.Chord([root, third, fifth, seventh, ninth])
        print(k, cs.commonName, [n.name for n in cs.notes], vectors)


def demo02():
    if False:
        print("\ntriad chords:\n")
        triadChords(natureScales)
        triadChords(melodicScales)
        print("\nseventh chords:\n")
        seventhChords(natureScales)
        seventhChords(melodicScales)
    print("\nninth chords:\n")
    ninthChords(natureScales)
    ninthChords(melodicScales)


if  __name__ == "__main__":
    demo02()
