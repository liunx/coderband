import numpy as np
from fractions import Fraction

class FreqRatio():
    FREQ_RATIOS = ['1/1', '16/15', '9/8', '6/5', '5/4', '4/3',
                   '45/32', '3/2', '8/5', '5/3', '9/5', '15/8']

    def __init__(self):
        pass

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


class Chord():
    # | full name | short name | intervals | consonance | tension |
    CHORD_TABLE = [
        ['major triad', [''], [0, 4, 7], 0, 0],
        ['minor triad', ['m'], [0, 3, 7], 0, 0],
        ['diminished triad', ['dim'], [0, 3, 6], 0, 0],
        ['augmented triad', ['aug'], [0, 4, 8], 0, 0],
        ['major seventh', ['Δ'], [0, 4, 7, 11], 0, 0],
        ['minor-augmented seventh', ['-Δ'], [0, 3, 7, 11], 0, 0],
        ['dominant seventh', ['7'], [0, 4, 7, 10], 0, 0],
        ['minor seventh', ['-'], [0, 3, 7, 10], 0, 0],
        ['half-diminished seventh', ['φ'], [0, 3, 6, 10], 0, 0],
        ['diminished seventh', ['°'], [0, 3, 6, 9], 0, 0],
        ['augmented major seventh', ['Δ♯5'], [0, 4, 8, 11], 0, 0],
        ['augmented seventh', ['7♯5'], [0, 4, 8, 10], 0, 0]
    ]

    def __init__(self):
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
