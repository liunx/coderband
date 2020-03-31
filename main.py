#!/usr/bin/env python3

import json
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.parser import global_idmap
from kivy.properties import ObjectProperty, StringProperty, ListProperty
kivy.require('1.4.2')

Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '400')


class Controller(BoxLayout):
    config = 'coderband.cfg'
    mode = ObjectProperty()
    time_signature = ObjectProperty()
    style = ObjectProperty()
    instruments = ListProperty()
    rhythm_pattern = ObjectProperty()
    chord_progress = ObjectProperty()
    tempo = ObjectProperty()
    dynamics = ObjectProperty()
    swing = ObjectProperty()
    timbre = ObjectProperty()
    humanlize = ObjectProperty()
    expression = ObjectProperty()
    improvisation = ObjectProperty()

    def build_map(self):
        d = {}
        d['mode'] = self.mode.text
        d['time_signature'] = self.time_signature.text
        d['style'] = self.style.text
        d['instrument'] = list(self.instruments)
        d['rhythm_pattern'] = self.rhythm_pattern.text
        d['chord_progress'] = self.chord_progress.text
        d['tempo'] = self.tempo.value
        d['dynamics'] = self.dynamics.value
        d['swing'] = self.swing.value
        d['timbre'] = self.timbre.value
        d['humanlize'] = self.humanlize.value
        d['expression'] = self.expression.value
        d['improvisation'] = self.improvisation.value
        return d

    def do_action(self, action):
        d = self.build_map()
        if action == 'done':
            pass
        elif action == 'save':
            self.json_save(d)
        elif action == 'load':
            self.json_load()

    def json_save(self, dat):
        with open(self.config, 'w') as f:
            json.dump(dat, f)

    def json_load(self):
        dat = {}
        with open(self.config) as f:
            dat = json.load(f)
        return dat


class CoderBandApp(App):
    '''The kivy App that runs the main root. All we do is build a catalog
    widget into the root.'''

    def build(self):
        return Controller()

    def on_pause(self):
        return True


if __name__ == "__main__":
    CoderBandApp().run()
