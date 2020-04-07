
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Composer:
    def __init__(self, args):
        self.cfg = Struct(**args)

    def add_params(self):
        pass

    def analysis(self):
        pass

    def composer(self):
        pass

    def orchestrate(self):
        pass

    def rhythm(self):
        pass

    def melody(self):
        pass

    def chord(self):
        pass

    def percussion(self):
        pass

