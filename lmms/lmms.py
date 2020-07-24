#!/usr/bin/env python3

import sys
import re
import json
from os import path
from lxml import etree
from music21 import tinyNotation, chord, note


class AudioFileProcessor:
    _preset='data/presets/AudioFileProcessor/default.xpf'
    def __init__(self, src, name):
        tree = etree.parse(self._preset)
        pt = tree.xpath('/lmms-project/instrumenttracksettings')[0]
        pt.tag = 'track'
        pt.attrib['name'] = name
        elem = pt.xpath('instrumenttrack/instrument/audiofileprocessor')[0]
        elem.attrib['src'] = src
        self.presettrack = pt

    def track(self):
        return self.presettrack

    def setparam(self, param):
        pass

    def getparam(self):
        pass


class Sf2Player:
    _preset='data/presets/Sf2Player/default.xpf'
    def __init__(self, src, patch, name):
        tree = etree.parse(self._preset)
        pt = tree.xpath('/lmms-project/instrumenttracksettings')[0]
        pt.tag = 'track'
        pt.attrib['name'] = name
        elem = pt.xpath('instrumenttrack/instrument/sf2player')[0]
        elem.attrib['src'] = src
        elem.attrib['patch'] = patch
        self.presettrack = pt

    def track(self):
        return self.presettrack

    def setparam(self, param):
        pass

    def getparam(self):
        pass


class Kicker:
    _preset='data/presets/Kicker/default.xpf'
    def __init__(self, name):
        tree = etree.parse(self._preset)
        pt = tree.xpath('/lmms-project/instrumenttracksettings')[0]
        pt.tag = 'track'
        pt.attrib['name'] = name
        self.presettrack = pt

    def track(self):
        return self.presettrack

    def setparam(self, param):
        pass

    def getparam(self):
        pass


class ChordState(tinyNotation.State):
    def affectTokenAfterParse(self, n):
        super(ChordState, self).affectTokenAfterParse(n)
        return None  # do not append Note object

    def end(self):
        ch = chord.Chord(self.affectedTokens)
        ch.duration = self.affectedTokens[0].duration
        return ch


class Lmms:
    presets = {}
    unit = 12
    steps = 16
    beattracks = 1

    def __init__(self, project):
        self.project = etree.parse(project)

    def write(self, file):
        self.project.write(file, encoding='utf-8', xml_declaration=True)

    def collectpresets(self, file):
        with open(file) as f:
            for l in f:
                l = l.strip()
                s = re.sub('.*data/presets/', '', l)
                s = re.sub('(.xpf|.xiz)', '', s)
                nm = re.sub('/', '.', s)
                absp = path.abspath(l)
                self.presets[nm] = absp

    def listpresets(self):
        return list(self.presets.keys())

    def addpreset(self, track, preset):
        tree = etree.parse(self.presets.get(preset))
        pt = tree.xpath(
            '/lmms-project/instrumenttracksettings/instrumenttrack')[0]
        track.append(pt)
        return pt

    def addbeatpreset(self, preset, name):
        tracks = self.project.xpath('/lmms-project/song/trackcontainer/track[@type="1"]')
        self.beattracks = len(tracks)
        track = tracks[0]
        t = track.xpath('bbtrack/trackcontainer')[0]
        tree = etree.parse(self.presets.get(preset))
        pt = tree.xpath('/lmms-project/instrumenttracksettings')[0]
        pt.tag = 'track'
        pt.attrib['name'] = name
        t.append(pt)
        return pt

    def addtrack(self, name):
        parent = self.project.xpath('/lmms-project/song/trackcontainer')[0]
        track = etree.Element('track', type='0', name=name, muted='0', solo='0')
        parent.append(track)
        return track

    def addinstrument(self, inst):
        parent = self.project.xpath('/lmms-project/song/trackcontainer')[0]
        parent.append(inst)

    def findtrack(self, name):
        track = self.project.xpath(
            '/lmms-project/song/trackcontainer/track[@name="{}"]'.format(name))[0]
        return track

    def _addpattern(self, track, _type, pos):
        pattern = etree.Element('pattern', pos=pos, muted='0', steps='16')
        pattern.attrib['name'] = track.attrib['name']
        pattern.attrib['type'] = _type
        track.append(pattern)
        return pattern

    def addpattern(self, track):
        return self._addpattern(track, '1', '0')

    def addbeatpattern(self, track):
        pos = 0
        for i in range(self.beattracks):
            self._addpattern(track, '0', str(int(pos)))
            pos = pos + self.steps * self.unit

    def addnotes(self, pattern, notes):
        steps = int(pattern.attrib['steps'])
        tnc = tinyNotation.Converter(notes)
        tnc.bracketStateMapping['chord'] = ChordState
        s = tnc.parse().stream
        offset = 0
        for m in s:
            for n in m:
                if type(n) != note.Note:
                    continue
                elem = etree.Element('note', key="0", pan="0", len="0", vol="141", pos="0")
                elem.attrib['key'] = str(n.pitch.midi)
                elem.attrib['pos'] = str(int(offset + self.unit * n.offset * 4))
                elem.attrib['len'] = str(int(self.unit * n.quarterLength * 4))
                pattern.append(elem)
            offset = offset + (self.unit * steps)

    def addbeatnotes(self, pattern, notes):
        offset = 0
        for n in notes:
            if n == 1:
                elem = etree.Element('note', pos="0", len="-192", key="57", vol="100", pan="0")
                elem.attrib['pos'] = str(int(offset))
                pattern.append(elem)
            offset = offset + self.unit

    def _addbbtrack(self, track):
        t = etree.Element('bbtrack')
        #self._addbbtrackcontainer(t)
        track.append(t)

    def _addbbtrackcontainer(self, track):
        t = etree.Element('trackcontainer', width="640", x="610", y="5", maximized="0",
                          height="400", visible="0", type="bbtrackcontainer", minimized="0")
        track.append(t)

    def addbeattrack(self, name):
        parent = self.project.xpath('/lmms-project/song/trackcontainer')[0]
        track = etree.Element(
            'track', type='1', name=name, muted='0', solo='0')
        self._addbbtrack(track)
        parent.append(track)
        return track

    def findbeattrack(self, name):
        track = self.project.xpath(
            '/lmms-project/song/trackcontainer/track[@name="{}"]'.format(name))[0]
        return track

    def addbbtco(self, track, offset, count):
        for i in range(count):
            pos = str((i + offset) * self.unit * self.steps)
            bbtco = etree.Element(
                'bbtco', color="4286611584", pos=pos, name="", muted="0", len="192", usestyle="1")
            track.append(bbtco)

    def addautomationtrack(self, name):
        pass

    def findautomationtrack(self, name):
        pass

    def addautomationpattern(self, name):
        pass

    def findautomationpattern(self, name):
        pass

    def removetrack(self, track):
        root = self.project.getroot()
        root.remove(track)

    def changesteps(self, track, steps):
        self.steps = steps
        pass

    def muted(self, track, val):
        track.attrib['muted'] = str(val)

    def changebpm(self, bpm):
        head = self.project.xpath('/lmms-project/head')[0]
        head.attrib['bpm'] = str(bpm)

    def getbeatpattern(self, beattrack, presettrack):
        tracks =  self.project.xpath('/lmms-project/song/trackcontainer/track[@type="1"]')
        index = tracks.index(beattrack)
        patterns = presettrack.xpath('pattern')
        return patterns[index]

    def getdefaultbeattrack(self):
        return self.project.xpath('/lmms-project/song/trackcontainer/track[@type="1"]')[0]


def demo01():
    proj = 'data/projects/templates/default.mpt'
    presets = './presets.txt'
    lmms = Lmms(proj)
    lmms.collectpresets(presets)

    track = lmms.addtrack('Audio')
    lmms.addpreset(track, 'AudioFileProcessor.default')
    pattern = lmms.addpattern(track)
    notes = "tinyNotation: 4/4 c8 d e f g a b c' trip{a4 b c}'"
    lmms.addnotes(pattern, notes)

    b01track = lmms.addbeattrack('Beat01')
    lmms.addbbtco(b01track, 0, 4)

    kicker = lmms.addbeatpreset('Kicker.default', 'Kicker')
    lmms.addbeatpattern(kicker)

    dftrack = lmms.getdefaultbeattrack()
    lmms.addbbtco(dftrack, 4, 4)

    notes = [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]
    pattern = lmms.getbeatpattern(b01track, kicker)
    lmms.addbeatnotes(pattern, notes)

    notes = [0,1,0,0,1,1,0,0,1,1,0,0,1,0,0,0]
    pattern = lmms.getbeatpattern(dftrack, kicker)
    lmms.addbeatnotes(pattern, notes)
    lmms.write('demo01.mmp')


if __name__ == "__main__":
    demo01()
