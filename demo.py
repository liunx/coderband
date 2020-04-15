#!/usr/bin/env python3

import numpy as np
from collections import namedtuple
import core.tools as tools
import core.music_theory as theory

class Base:
    def __init__(self):
        pass

    def __query(self):
        print("query from Base")

    def hello(self):
        self.__query()


class Demo(Base):
    def __init__(self):
        pass

    def __query(self):
        print("query from Demo")



def demo03():
    key = 'C'
    obj = theory.Scales()
    notes = obj.to_scales(key, 'ionian')
    print(notes)
    for m in ['gong', 'shang', 'jue', 'zhi', 'yu']:
        notes = obj.to_scales(key, m)
        print(notes)
    for m in ['melodic minor', 'phrygidorian', 'lydian augmented', 'lydian dominant', 'melodic major', 'aeolocrian', 'altered scale']:
        notes = obj.to_scales(key, m)
        print(notes)
    notes = obj.to_scales(key, 'bebop major')
    print(notes)
    notes = obj.to_scales(key, 'bebop dominant')
    print(notes)


def demo04():
    demo = Demo()
    demo.hello()


def demo05():
    User = namedtuple('User', ['name', 'sex', 'age'])
    user = User._make(['Tom', 'male', 21])
    print(user)



def demo06():
    key = 'C'
    obj = theory.Chord()
    chords = obj.to_chord(key, 'maj7')
    print(chords)
    chords = obj.to_chord(key, 'min7')
    print(chords)


if __name__ == "__main__":
    demo06()
