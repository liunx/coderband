#!/usr/bin/env python3

import json
import numpy as np
from fractions import Fraction
from lib.music_theory import FreqRatio
import lib.tools


class Composor():
    style = 0
    tension = 0
    instruments = []
    def __init__(self, params):
        self.style = params.get('style')
        self.tension = params.get('tension')
        self.instruments = params.get('instruments')

    def analysis(self):
        pass

    def compose(self):
        pass


def json_save(filepath, dat):
    with open(filepath, 'w') as f:
        json.dump(dat, f)

def json_load(filepath):
    dat = {}
    with open(filepath) as f:
        dat = json.load(f)
    return dat


if __name__ == "__main__":
    pass
