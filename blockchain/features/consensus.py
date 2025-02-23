import random

class Uzol:
    def __init__(self, meno):
        self.meno = meno

    def hlasuj(self, blok):
        return random.choices([True, False], weights=[3, 1], k=1)[0]
