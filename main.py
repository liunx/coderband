#!/usr/bin/env python3

import kivy
kivy.require('1.4.2')
from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')


class Controller(BoxLayout):
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'

class CoderBandApp(App):
    '''The kivy App that runs the main root. All we do is build a catalog
    widget into the root.'''

    def build(self):
        return Controller()

    def on_pause(self):
        return True


if __name__ == "__main__":
    CoderBandApp().run()
