import core.tools as Tools

class Pop():
    def __init__(self, cfg):
        self.cfg = cfg

    def analysis(self):
        print("{} analysis!!!".format(__name__))
        print(self.cfg)

    def composer(self):
        print("{} composer!!!".format(__name__))


def register_module(mods):
    m = Pop
    mods['Pop'] = m
