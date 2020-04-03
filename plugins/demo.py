import numpy as np

class Demo():
    def analysis(self):
        print("demo analysis!!!")

    def composer(self):
        print("demo composer!!!")

def register_module(mods):
    m = Demo()
    mods['Pop'] = m
