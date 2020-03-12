#!/usr/bin/env python3

import music21
import copy


def scaleGenerate(scales):
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
        print("{}Vec = {}".format(str.lower(modeNote.step), scaleVector))
        newNote = modeNote.transpose('P8')
        currNoteScales.pop(0)
        currNoteScales.append(newNote)


if  __name__ == "__main__":
    cScales = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
    cScales1 = ['C4', 'D4', 'Eb4', 'F4', 'G4', 'A4', 'B4']
    scaleGenerate(cScales)
    print("==================")
    scaleGenerate(cScales1)
