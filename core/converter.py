import music21

class Staff:
    def __init__(self, mode, ts):
        self.key = music21.key.Key(mode)
        self.timeSignature = music21.meter.TimeSignature(ts)
        self.stream = music21.stream.Stream()
        self.stream.append(music21.clef.TrebleClef())
        self.stream.append(self.timeSignature)
        self.stream.append(self.key)
        r = music21.note.Rest(type='whole')
        self.stream.append(r)

    def write_xml(self, filename):
        self.stream.write('musicxml', fp=filename)

    def show_mxml(self):
        self.stream.show()

    def show_text(self):
        self.stream.show('text')

    def add_chord(self, chord, type='whole'):
        ch = music21.chord.Chord(chord, type=type)
        self.stream.append(ch)

    def add_chords(self, chords):
        pass

    def add_note(self, note):
        pass

    def add_notes(self, notes):
        pass

    def add_rest(self):
        r = music21.note.Rest(type='whole')
        self.stream.append(r)

    def add_roman_numeral(self, rn, key, type='half'):
        rf = music21.roman.RomanNumeral(rn, key)
        ch = music21.chord.Chord(rf, type=type)
        ch.addLyric(rn)
        self.stream.append(ch)

    def to_intervals(self, rn, key):
        l = []
        rf = music21.roman.RomanNumeral(rn, key)
        root_midi = rf.pitches[0].midi
        for p in rf.pitches:
            l.append(p.midi - root_midi)
        return l
