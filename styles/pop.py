from core import Composer

class Pop(Composer):
    support_styles = ['50s']
    def __init__(self, cfg):
        super().__init__(cfg)

    def add_params(self):
        return self.support_styles

    def analysis(self):
        print("{} analysis!!!".format(__name__))
        print(self.cfg.chord_progress)

    def composer(self):
        print("{} composer!!!".format(__name__))
        cfg = self.cfg
        if cfg.chord_progress == '50s':
            return ['I', 'vi', 'IV', 'V']


def register_module(mods):
    m = Pop
    mods['Pop'] = m
