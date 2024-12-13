from flexcryptopay.modules.classes.avalanche import Avalanche


class avax(Avalanche):
    def __init__(self):
        self.crypto = "AVAX"

    def getname(self):
        return "AVAX"
