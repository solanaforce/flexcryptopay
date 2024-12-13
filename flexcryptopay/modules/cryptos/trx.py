import os

from flexcryptopay.modules.classes.tron_token import TronToken


class trx(TronToken):
    _display_name = "Tron TRX"

    def __init__(self):
        self.crypto = "TRX"

    def getname(self):
        return "Tron"
