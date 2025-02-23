class SmartContract:
    def __init__(self, minimalna_uroven_schvalenia=2):
        self.minimalna_uroven_schvalenia = minimalna_uroven_schvalenia

    def schval_akciu(self, uroven_schvalenia):
        return uroven_schvalenia >= self.minimalna_uroven_schvalenia
