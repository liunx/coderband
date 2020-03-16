#!/usr/bin/env python3

import music21


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


def showTab(tab, indent=6):
    keys = list(tab.keys())
    keys.sort()
    for k in keys:
        s = "[{}]".format(k)
        l = tab[k]
        for i in l:
            strFormat = "{:-^"  + str(indent) + "}"
            s = s + strFormat.format(i)
            s = s + "|"
        print(s)


def markNotes(l, note, chord, pos=False):
    mid = int(len(l) / 2)
    if note.name in chord:
        if pos:
            l[mid] = "[ {} ]".format(note.name)
        else:
            l[mid] = "({})".format(note.name)
    for i in range(1, mid):
        n = note.transpose(i)
        p = n.pitch.getEnharmonic()
        if n.name in chord:
            l[i + mid] = "({})".format(n.name)
        if p.name in chord:
            l[i + mid] = "({})".format(p.name)
    for i in range(1, mid + 1):
        n = note.transpose(-i)
        p = n.pitch.getEnharmonic()
        if n.name in chord:
            l[mid - i] = "({})".format(n.name)
        if p.name in chord:
            l[mid - i] = "({})".format(p.name)


def tabCalculate(line, noteName, romanNum):
    h = 6
    w = 7
    tab = {}
    for i in range(1, h + 1):
        tab[i] = [''] * w
    rf = music21.roman.RomanNumeral(romanNum, noteName)
    chord = [n.name for n in rf.notes]
    l = tab[line]
    bassNote = music21.note.Note(noteName)
    markNotes(l, bassNote, chord, pos=True)
    currNote = None
    for i in range(line + 1, h + 1):
        if currNote == None:
            currNote = bassNote
        n = currNote.transpose('P5')
        l = tab[i]
        markNotes(l, n, chord)
        currNote = n
    currNote = None
    for i in range(line - 1, 0, -1):
        if currNote == None:
            currNote = bassNote
        n = currNote.transpose('P4')
        l = tab[i]
        markNotes(l, n, chord)
        currNote = n
    for i in [1, 2]:
        tab[i].insert(0, '')
    for i in [3, 4, 5, 6]:
        tab[i].append('')
    print("TAB {}:".format(rf.figureAndKey))
    showTab(tab)


if  __name__ == "__main__":
    for i in range(1, 7):
        tabCalculate(i, 'C', 'I7')
