#!/usr/bin/env python3

import music21
import copy
import random
from rhythmaker import Staff

natureScaleVectList = [[0, 2, 4, 5, 7, 9, 11],
                       [0, 2, 3, 5, 7, 9, 10],
                       [0, 1, 3, 5, 7, 8, 10],
                       [0, 2, 4, 6, 7, 9, 11],
                       [0, 2, 4, 5, 7, 9, 10],
                       [0, 2, 3, 5, 7, 8, 10],
                       [0, 1, 3, 5, 6, 8, 10]]

melodicScaleVectList = [[0, 2, 3, 5, 7, 9, 11],
                        [0, 1, 3, 5, 7, 9, 10],
                        [0, 2, 4, 6, 8, 9, 11],
                        [0, 2, 4, 6, 7, 9, 10],
                        [0, 2, 4, 5, 7, 8, 10],
                        [0, 2, 3, 5, 6, 8, 10],
                        [0, 1, 3, 4, 6, 8, 10]]

diminishedScaleVectList = [[0, 2, 3, 5, 6, 8, 9, 11],
                           [0, 1, 3, 4, 6, 7, 9, 10]]

wholeToneScaleVectList = [[0, 2, 4, 6, 8, 10]]


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
        print("{},".format(scaleVector))
        newNote = modeNote.transpose('P8')
        currNoteScales.pop(0)
        currNoteScales.append(newNote)

def demo01():
    natureScale = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
    melodicScale = ['C4', 'D4', 'Eb4', 'F4', 'G4', 'A4', 'B4']
    diminishedScale = ['F4', 'G4', 'Ab4', 'A#4', 'B4', 'C#5', 'D5', 'E5']
    wholeToneScale = ['G4', 'A4', 'B4', 'C#5', 'D#5', 'F5']
    scaleGenerate(natureScale)
    print("==================")
    scaleGenerate(melodicScale)
    print("==================")
    scaleGenerate(diminishedScale)
    print("==================")
    scaleGenerate(wholeToneScale)

def melody(scaleList, mode):
    for l in scaleList:
        scaleNotes = []
        noteNames = []
        noteSteps = []
        modeNote = music21.note.Note(mode)
        for i in l:
            n = modeNote.transpose(i)
            if n.step in noteSteps:
                n.pitch.getEnharmonic(inPlace=True)
            scaleNotes.append(n)
            noteNames.append(n.name)
            noteSteps.append(n.step)
        noteNames.insert(0, 'R')
        print(noteNames)

class Melody:
    def __init__(self, mode='C4', noteRange=8):
        self.__modeNote = music21.note.Note(mode)
        self.__noteIndexList = [i for i in range(noteRange)]

    def mode(self, mode=None):
        if not mode:
            return self.__modeNote.name
        self.__modeNote = music21.note.Note(mode)

    def range(self, noteRange=0):
        if not noteRange:
            return len(self.__noteIndexList)
        self.__noteIndexList = [i for i in range(noteRange)]

    def toScaleNotes(self, scaleVectList):
        noteSteps = []
        scaleNotes = [music21.note.Rest()]
        for i in scaleVectList:
            n = self.__modeNote.transpose(i)
            if n.step in noteSteps:
                n.pitch.getEnharmonic(inPlace=True)
            scaleNotes.append(n)
            noteSteps.append(n.step)
        return scaleNotes

    def random(self, noteAmount):
        self.__randomIndexList = random.choices(self.__noteIndexList, k=noteAmount)
        return self.__randomIndexList

    def melody(self, scaleVectList):
        melodyList = []
        scaleNotes = self.toScaleNotes(scaleVectList)
        for i in self.__randomIndexList:
            n = scaleNotes[i]
            if n.isRest:
                melodyList.append(['R'])
            else:
                melodyList.append([n.pitch.nameWithOctave])

        return melodyList



if  __name__ == "__main__":
    staff = Staff()
    m = Melody()
    m.random(16)
    for l in natureScaleVectList:
        ml = m.melody(l)
        print(ml)
        staff.read(ml)
        staff.show()
