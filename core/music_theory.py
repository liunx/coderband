import numpy as np
from fractions import Fraction
from collections import namedtuple


# | prefer name | other names | intervals |
DIATONIC_SCALES = [
    ['ionian mode', ['mjaor scale'], [0, 2, 4, 5, 7, 9, 11]],
    ['dorian mode', [], [0, 2, 3, 5, 7, 9, 10]],
    ['phrygian mode', [], [0, 1, 3, 5, 7, 8, 10]],
    ['lydian mode', [], [0, 2, 4, 6, 7, 9, 11]],
    ['mixolydian scale', [], [0, 2, 4, 5, 7, 9, 10]],
    ['aeolian mode', ['nature minor mode'], [0, 2, 3, 5, 7, 8, 10]],
    ['locrian mode', [], [0, 1, 3, 5, 6, 8, 10]]
]

# | prefer name | other names | intervals | index to diatonic scale | operations |
MELODIC_MINOR_SCALES = [
    ['ascending melodic minor', [], [0, 2, 3, 5, 7, 9, 11], DIATONIC_SCALES[0], ['3-']],
    ['phrygidorian', ['phrygian ♮6', 'dorian ♭2', 'assyrian'], [0, 1, 3, 5, 7, 9, 10],  DIATONIC_SCALES[1], ['2-']],
    ['lydian augmented', ['lydian ♯5'], [0, 2, 4, 6, 8, 9, 11],  DIATONIC_SCALES[3], ['5+']],
    ['lydian dominant', ['lydian ♭7', 'acoustic scale', 'mixolydian ♯4', 'overtone', 'lydomyxian'], [0, 2, 4, 6, 7, 9, 10],  DIATONIC_SCALES[3], ['7-']],
    ['melodic major', ['mixolydian ♭6', 'fifth mode of melodic minor', 'hindu', 'myxaeolian'], [0, 2, 4, 5, 7, 8, 10],  DIATONIC_SCALES[4], ['6-']],
    ['aeolocrian', ['locrian ♮2', 'half-diminished'], [0, 2, 3, 5, 6, 8, 10],  DIATONIC_SCALES[6], ['2+']],
    ['altered scale', ['super locrian', 'altered dominant scale'], [0, 1, 3, 4, 6, 8, 10],  DIATONIC_SCALES[6], ['4-']]
]

BEBOP_SCALES = [
    ['bebop dominant scale', [], [0, 2, 4, 5, 7, 9, 10, 11], DIATONIC_SCALES[4], ['add7+']],
    ['bebop major scale', [], [0, 2, 4, 5, 7, 8, 9, 11], DIATONIC_SCALES[0], ['add5+']]
]

PENTATONE_SCALES = [
    ['major pentatonic scale', ['gong'], [0, 2, 4, 7, 9], DIATONIC_SCALES[0], ['omit4', 'omit7']],
    ['egyptian', ['suspended', 'shang'], [0, 2, 5, 7, 10], DIATONIC_SCALES[1], ['omit3', 'omit6']],
    ['blues minor', ['man gong', 'jue'], [0, 3, 5, 8, 10], DIATONIC_SCALES[2], ['omit2', 'omit5']],
    ['blues major', ['Ritsusen', 'yo scale', 'zhi'], [0, 2, 5, 7, 9], DIATONIC_SCALES[4], ['omit3', 'omit7']],
    ['minor pentatonic', ['yu'], [0, 3, 5, 7, 10], DIATONIC_SCALES[5], ['omit2', 'omit6']]
]

HEPTATONIC_SCALES = [
    # diatonic scales
    ['ionian mode (major scale)', [0, 2, 4, 5, 7, 9, 11]],
    ['dorian mode', [0, 2, 3, 5, 7, 9, 10]],
    ['phrygian mode', [0, 1, 3, 5, 7, 8, 10]],
    ['lydian mode', [0, 2, 4, 6, 7, 9, 11]],
    ['mixolydian scale', [0, 2, 4, 5, 7, 9, 10]],
    ['aeolian mode (nature minor mode)', [0, 2, 3, 5, 7, 8, 10]],
    ['locrian mode', [0, 1, 3, 5, 6, 8, 10]],
    # TODO
    ['adonai malakh scale', [0, 2, 4, 5, 7, 8, 10]],
    ['algerian scale', [0, 2, 3, 6, 7, 8, 11]],
    ['altered scale', [0, 1, 3, 4, 6, 8, 10]],
    ['double harmonic scale', [0, 1, 4, 5, 7, 8, 11]],
    ['enigmatic scale', [0, 1, 4, 6, 8, 10, 11]],
    ['flamenco mode', [0, 1, 4, 5, 7, 8, 11]],
    ['gypsy scale', [0, 2, 3, 6, 7, 8, 10]],
    ['half diminished scale', [0, 2, 3, 5, 6, 8, 10]],
    ['harmonic major scale', [0, 2, 4, 5, 7, 8, 11]],
    ['harmonic minor scale', [0, 2, 3, 5, 7, 8, 11]],
    ['hungarian gypsy scale', [0, 2, 3, 6, 7, 8, 11]],
    ['hungarian minor scale', [0, 2, 3, 6, 7, 8, 11]],
    ['lydian augmented scale', [0, 2, 4, 6, 8, 9, 11]],
    ['major locran scale', [0, 2, 4, 5, 6, 8, 10]],
    ['melodic minor scale (ascending)', [0, 2, 3, 5, 7, 9, 11]],
    ['neapolitan major scale', [0, 1, 3, 5, 7, 9, 11]],
    ['neapolitan minor scale', [0, 1, 3, 5, 7, 8, 11]],
    ['persian scale', [0, 1, 4, 5, 6, 8, 11]],
    ['phrygian dominant scale', [0, 1, 4, 5, 7, 8, 10]],
    ['ukranian dorian scale', [0, 2, 3, 6, 7, 9, 10]]
]

SCALES_COLLECTION = [
    ['acoustic scale', [0, 2, 4, 6, 7, 9]],
    ['adonai malakh scale', [0, 2, 4, 5, 7, 8, 10]],
    ['aeolian mode', [0, 2, 3, 5, 7, 8, 10]],
    ['nature minor mode', [0, 2, 3, 5, 7, 8, 10]],
    ['algerian scale', [0, 2, 3, 6, 7, 8, 11]],
    ['altered scale', [0, 1, 3, 4, 6, 8, 10]],
    ['augmented scale', [0, 3, 4, 7, 8, 11]],
    ['bebop dominant scale', [0, 2, 4, 5, 7, 9, 10, 11]],
    ['blues scale', [0, 3, 5, 6, 7, 10]],
    ['chromatic scale', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]],
    ['dorian mode', [0, 2, 3, 5, 7, 9, 10]],
    ['double harmonic scale', [0, 1, 4, 5, 7, 8, 11]],
    ['enigmatic scale', [0, 1, 4, 6, 8, 10, 11]],
    ['flamenco mode', [0, 1, 4, 5, 7, 8, 11]],
    ['gypsy scale', [0, 2, 3, 6, 7, 8, 10]],
    ['half diminished scale', [0, 2, 3, 5, 6, 8, 10]],
    ['harmonic major scale', [0, 2, 4, 5, 7, 8, 11]],
    ['harmonic minor scale', [0, 2, 3, 5, 7, 8, 11]],
    ['hirajoshi scale', [0, 2, 3, 7, 8]],
    ['hungarian gypsy scale', [0, 2, 3, 6, 7, 8, 11]],
    ['hungarian minor scale', [0, 2, 3, 6, 7, 8, 11]],
    ['insen scale', [0, 1, 5, 7, 10]],
    ['ionian mode', [0, 2, 4, 5, 7, 9, 11]],
    ['major scale', [0, 2, 4, 5, 7, 9, 11]],
    ['istrian scale', [0, 1, 3, 4, 6, 7]],
    ['iwato scale', [0, 1, 5, 6, 10]],
    ['locrian mode', [0, 1, 3, 5, 6, 8, 10]],
    ['lydian augmented scale', [0, 2, 4, 6, 8, 9, 11]],
    ['lydian mode', [0, 2, 4, 6, 7, 9, 11]],
    ['major bepop scale', [0, 2, 4, 5, 7, 8, 9, 11]],
    ['major locran scale', [0, 2, 4, 5, 6, 8, 10]],
    ['major pentatonic scale', [0, 2, 4, 7, 9]],
    ['melodic minor scale', [0, 2, 3, 5, 7, 8, 9, 10, 11]],
    ['melodic minor scale (ascending)', [0, 2, 3, 5, 7, 9, 11]],
    ['minor pentatonic scale', [0, 3, 5, 7, 10]],
    ['mixolydian scale', [0, 2, 4, 5, 7, 9, 10]],
    ['neapolitan major scale', [0, 1, 3, 5, 7, 9, 11]],
    ['neapolitan minor scale', [0, 1, 3, 5, 7, 8, 11]],
    ['octatonic scale', [0, 2, 3, 5, 6, 8, 9, 11]],
    ['persian scale', [0, 1, 4, 5, 6, 8, 11]],
    ['phrygian dominant scale', [0, 1, 4, 5, 7, 8, 10]],
    ['phrygian mode', [0, 1, 3, 5, 7, 8, 10]],
    ['prometheus scale', [0, 2, 4, 6, 9, 10]],
    ['tritone scale', [0, 1, 4, 6, 7, 10]],
    ['ukranian dorian scale', [0, 2, 3, 6, 7, 9, 10]],
    ['whole tone scale', [0, 2, 4, 6, 8, 10]]
]

# | full name | short names | intervals | scale names |
CHORDS_TABLE = [
    # triad chords
    ['major triad', ['M'], [0, 4, 7], ['ionian']],
    ['minor triad', ['m'], [0, 3, 7], ['aeolian']],
    ['augmented triad', ['aug'], [0, 4, 8], ['lydian augmented']],
    ['diminished triad', ['dim'], [0, 3, 6], ['locrian']],
    # seventh chords
    ['diminished seventh', ['°'], [0, 3, 6, 9], [1, 3, 5, 7]],
    ['half-diminished seventh', ['φ'], [0, 3, 6, 10], ['locrian']],
    ['minor seventh', ['-'], [0, 3, 7, 10], ['dorian']],
    ['minor major seventh', ['-Δ'], [0, 3, 7, 11], ['melodic minor']],
    ['dominant seventh', ['7'], [0, 4, 7, 10], ['mixolydian']],
    ['major seventh', ['Δ'], [0, 4, 7, 11], ['ionian']],
    ['augmented seventh', ['7♯5'], [0, 4, 8, 10], ['melodic major']],
    ['augmented major seventh', ['Δ♯5'], [0, 4, 8, 11], ['lydian augmented']],
    # extented chords
    ['dominant ninth', ['9'], [0, 2, 4, 7, 10], ['mixolydian']],
    ['dominant eleventh', ['11'], [0, 2, 4, 5, 7, 10], ['mixolydian']],
    ['dominant thirteenth', ['13'], [0, 2, 4, 5, 7, 9, 10], ['mixolydian']],
    # atered chords
    ['seventh augmented fifth', ['7♯5'], [0, 4, 8, 10], ['melodic major']],
    ['seventh minor ninth', ['7♭9'], [0, 1, 4, 7, 10], ['phrygian dominant']],
    ['seventh sharp ninth', ['7♯9'], [0, 3, 4, 7, 10], [1, 2, 3, 5, 7]],
    ['seventh augmented eleventh', ['7♯11'], [0, 2, 4, 6, 7, 10]],
    ['seventh diminished thirteenth', ['7♭13'], [0, 2, 4, 5, 7, 8, 10]],
    ['half-diminished seventh', ['φ'], [0, 3, 6, 10], [1, 3, 5, 7]],
    # added tone chords
    ['add nine', ['add9'], [0, 2, 4, 7], [1, 2, 3, 5]],
    ['add fourth', ['add11'], [0, 4, 5, 7], [1, 3, 4, 5]],
    ['add sixth', ['6'], [0, 4, 7, 9], [1, 3, 5, 6]],
    ['six-nine', ['6/9'], [0, 2, 4, 7, 9], [1, 2, 3, 5, 6]],
    ['seven-six', ['7/6'], [0, 4, 7, 9, 10], [1, 3, 5, 6, 7]],
    ['mixed-third', ['--'], [0, 3, 4, 7], [1, 2, 3, 5]],
    # suspended chords
    ['suspended second', ['sus2'], [0, 2, 7], [1, 2, 5]],
    ['suspended fourth', ['sus4'], [0, 5, 7], [1, 4, 5]],
    ['jazz sus', ['9sus4'], [0, 4, 5, 7, 10], [1, 3, 4, 5, 7]]
]


class FreqRatio():
    FREQ_RATIOS = ['1/1', '16/15', '9/8', '6/5', '5/4', '4/3',
                   '45/32', '3/2', '8/5', '5/3', '9/5', '15/8']

    def __init__(self):
        pass

    def chromatic_freq_sizes(self):
        l = []
        for fr in self.FREQ_RATIOS:
            f = Fraction(fr)
            n = f.numerator
            d = f.denominator
            l.append(n * d)
        return l

    def calc_freq_radio_size(self, intervals):
        l = list(intervals)
        l.sort()
        denominators = []
        numerators = []
        for i in l:
            f = Fraction(self.FREQ_RATIOS[i])
            denominators.append(f.denominator)
            numerators.append(f.numerator)
        lcm = np.lcm.reduce(denominators)
        total = []
        for d,n in zip(denominators, numerators):
            total.append(n * (lcm / d))
        prod = np.prod(total)
        return prod


SCALES_QUERY_TABLE = {
    'ionian': ['diatonic', DIATONIC_SCALES[0]],
    'dorian': ['diatonic', DIATONIC_SCALES[1]],
    'phrygian': ['diatonic', DIATONIC_SCALES[2]],
    'lydian': ['diatonic', DIATONIC_SCALES[3]],
    'mixolydian': ['diatonic', DIATONIC_SCALES[4]],
    'aeolian': ['diatonic', DIATONIC_SCALES[5]],
    'locrian': ['diatonic', DIATONIC_SCALES[6]],
    'melodic minor': ['melodic', MELODIC_MINOR_SCALES[0]],
    'lydian dominant': ['melodic', MELODIC_MINOR_SCALES[3]],
    'melodic major': ['melodic', MELODIC_MINOR_SCALES[4]],
    'aeolocrian': ['melodic', MELODIC_MINOR_SCALES[5]],
    'altered scale': ['melodic', MELODIC_MINOR_SCALES[6]],
    'gong': ['pentatone', PENTATONE_SCALES[0]],
    'shang': ['pentatone', PENTATONE_SCALES[1]],
    'jue': ['pentatone', PENTATONE_SCALES[2]],
    'zhi': ['pentatone', PENTATONE_SCALES[3]],
    'yu': ['pentatone', PENTATONE_SCALES[4]],
    'bebop dominant': ['bebop', BEBOP_SCALES[0]],
    'bebop major': ['bebop', BEBOP_SCALES[1]],
}


class Scales:
    diatonic_scales = ['C', 0, 'D', 0, 'E', 'F', 0, 'G', 0, 'A', 0, 'B']
    scales_query_table = SCALES_QUERY_TABLE

    def __init__(self):
        pass

    def rotate(self, n, l, right=False):
        llen = len(l)
        if right:
            return l[-n:] + l[:-n]
        n1 = (llen - n) % llen
        return l[-n1:] + l[:-n1]

    def get_accidentals(self, key):
        alter = 0
        if len(key) > 1:
            ct = key.count('-')
            if ct > 0:
                alter = -ct
            ct = key.count('#')
            if ct > 0:
                alter = ct
        return alter

    def __query(self, mode):
        return self.scales_query_table[mode]

    def flat_list(self, l, output_list):
        for i in l:
            if type(i) == list:
                self.flat_list(i, output_list)
            else:
                output_list.append(i)

    def to_diatonic_scales(self, key, query):
        intervals = query[2]
        alter = self.get_accidentals(key)
        step = key[0]
        scale_count = len(self.diatonic_scales)
        idx = self.diatonic_scales.index(step)
        rotated_scales = self.rotate(idx, self.diatonic_scales)
        index_list = []
        scale_steps = []
        for i in range(scale_count):
            if type(rotated_scales[i]) == str:
                index_list.append(i)
                scale_steps.append(rotated_scales[i])
        a1 = np.array(index_list)
        a2 = np.array(intervals)
        dist = a2 - a1 + alter
        notes = []
        for n,d in zip(scale_steps, dist):
            if d > 0:
                note = "{}{}".format(n, '#' * d)
            elif d < 0:
                note = "{}{}".format(n, '-' * -d)
            else:
                note = n
            notes.append(note)
        return notes

    def filter_digit(self, s):
        num = int(''.join(filter(str.isdigit, s)))
        return num

    def update_accidental(self, note, alter):
        step = note[0]
        curr_alter = self.get_accidentals(note)
        final_alter = curr_alter + alter
        if final_alter > 0:
            nt = "{}{}".format(step, '#' * final_alter)
        elif final_alter < 0:
            nt = "{}{}".format(step, '-' * -final_alter)
        else:
            nt = step
        return nt

    def notes_operate(self, notes, opts):
        for opt in opts:
            if opt.count('omit') > 0:
                idx = self.filter_digit(opt)
                notes[idx - 1] = 0
            elif opt.count('add') > 0:
                idx = self.filter_digit(opt)
                alter = self.get_accidentals(opt)
                n = notes[idx - 1]
                nt = self.update_accidental(n, alter)
                if alter > 0:
                    notes[idx - 1] = [n, nt]
                else:
                    notes[idx - 1] = [nt, n]
            else:
                idx = self.filter_digit(opt)
                alter = self.get_accidentals(opt)
                n = notes[idx - 1]
                nt = self.update_accidental(n, alter)
                notes[idx - 1] = nt
        notes = list(filter(lambda a: a != 0, notes))
        final_notes = []
        self.flat_list(notes, final_notes)
        return final_notes

    def to_pentatone_scales(self, key, query):
        notes = []
        opts = query[4]
        notes = self.to_diatonic_scales(key, query[3])
        notes = self.notes_operate(notes, opts)
        return notes

    def to_bebop_scales(self, key, query):
        notes = []
        opts = query[4]
        notes = self.to_diatonic_scales(key, query[3])
        notes = self.notes_operate(notes, opts)
        return notes

    def to_scales(self, key, mode):
        query = self.__query(mode)
        notes = []
        if query[0] == 'diatonic':
            notes = self.to_diatonic_scales(key, query[1])
        elif query[0] == 'pentatone':
            notes = self.to_pentatone_scales(key, query[1])
        elif query[0] == 'melodic':
            notes = self.to_diatonic_scales(key, query[1])
        elif query[0] == 'bebop':
            notes = self.to_bebop_scales(key, query[1])
        return notes


CHORDS_QUERY_TABLE = {
    'maj': ['triad', CHORDS_TABLE[0]],
    'min': ['triad', CHORDS_TABLE[1]],
    'maj7': ['seventh', CHORDS_TABLE[9]],
    'min7': ['seventh', CHORDS_TABLE[6]],
}


class Chord(Scales):
    chords_query_table = CHORDS_QUERY_TABLE
    ChordsTable = namedtuple('ChordsTable', ['common_name', 'short_names',
                                             'intervals', 'scale_names'])

    def __init__(self):
        pass

    def __query(self, mode):
        return self.chords_query_table[mode]

    def to_triad(self, scales):
        chord = [scales[0], scales[2], scales[4]]
        return chord

    def to_seventh(self, scales):
        chord = [scales[0], scales[2], scales[4], scales[6]]
        return chord

    def to_chord(self, key, mode):
        query = self.__query(mode)
        chords_table = self.ChordsTable._make(query[1])
        scales = self.to_scales(key, chords_table.scale_names[0])
        chord = []
        if query[0] == 'triad':
            chord = self.to_triad(scales)
        elif query[0] == 'seventh':
            chord = self.to_seventh(scales)
        return chord


class RomanNumeral(Chord):
    roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

    def __init__(self, key):
        self.__notes = self.to_scales(key, 'diatonic')

    def parser(self, rn):
        offset = rn[0]
        pass

    def to_note(self, rn):
        pass

    def to_chord(self, rn):
        pass


class ChordProgression():
    # | genre | chord progression | expression |
    CHORD_PROGRESSION_TABLE = [
        ["50' progression", ['I', 'vi', 'IV', 'V'], 0],
        ["50' progression", ['I', 'vi', 'ii', 'V'], 1],
        ["50' progression", ['I', 'V', 'vi', 'IV'], 2]
    ]

    def __init__(self):
        pass


class Style():
    STYLES = ['Folk song', 'Hip hop', 'Jazz', 'Latin', 'Pop', 'R&B and soul', 'Rock',
              'Classical music', 'Country']


class Instruments():
    pass
