#!/usr/bin/env python3

import kivy
import json
kivy.require('1.4.2')
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.parser import global_idmap
from kivy.properties import ObjectProperty, StringProperty, ListProperty

Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '400')


class Controller(BoxLayout):
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

    def do_action(self):
        print("do action!")
        print(self.instruments, self.mode.text)

    def json_save(self):
        pass

    def json_load(self):
        pass


class CoderBandApp(App):
    '''The kivy App that runs the main root. All we do is build a catalog
    widget into the root.'''

    def build(self):
        return Controller()

    def on_pause(self):
        return True


if __name__ == "__main__":
    CoderBandApp().run()
