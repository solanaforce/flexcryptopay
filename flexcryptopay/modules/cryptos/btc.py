from flexcryptopay.modules.classes.bitcoin_like_crypto import BitcoinLikeCrypto


class btc(BitcoinLikeCrypto):
    fee_description = "sat/vByte"

    def __init__(self):
        self.crypto = "BTC"

    def getname(self):
        return "Bitcoin"

    def gethost(self):
        return "bitcoind:8332"
