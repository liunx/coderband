#!/usr/bin/env python3
from lmms import Lmms, Sf2Player


instruments = {
    'piano': {
        'plugin': 'Sf2Player', 
        'src': '/usr/share/sounds/sf2/FluidR3_GM.sf2',
        'patch': '0',
    }
}


class Struct:
    def __init__(self, **args):
        self.__dict__.update(args)


class Composer:
    band = {}
    def __init__(self, project):
        self.project = project

    def addinstrument(self, program):
        inst = instruments[program]
        inst = Struct(**inst) 
        plug = None
        if inst.plugin == 'Sf2Player':
            plug = Sf2Player(inst.src, inst.patch, program)
        elif inst.plugin == 'AudioFileProcessor':
            pass
        elif inst.plugin == 'Kicker':
            pass
        track = plug.track()
        self.band[program] = track
        self.project.addinstrument(track)

    def addbeats(self, beats):
        pass

    def addrhythm(self, rhythm):
        pass

    def addmelody(self, melody):
        pass

    def write(self, fp):
        self.project.write(fp)


if __name__ == "__main__":
    proj = 'data/projects/templates/default.mpt'
    presets = './presets.txt'
    lmms = Lmms(proj)
    lmms.collectpresets(presets)
    composer = Composer(lmms)
    composer.addinstrument('piano')
    composer.write('lmms.mmp')
