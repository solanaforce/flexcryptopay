from abc import abstractmethod
from os import environ
import json
from flexcryptopay import requests
import datetime
from collections import namedtuple
from decimal import Decimal
from flask import current_app as app
from flexcryptopay.modules.classes.crypto import Crypto
from flexcryptopay.modules.classes.ethereum import Ethereum


class Bnb(Ethereum):
    network_currency = "BNB"

    def gethost(self):
        host = environ.get("BNB_API_SERVER_HOST", "bnb-flexcryptopay")
        port = environ.get("BNB_SERVER_PORT", "6000")
        return f"{host}:{port}"

    def get_auth_creds(self):
        username = environ.get(f"BNB_USERNAME", "flexcryptopay")
        password = environ.get(f"BNB_PASSWORD", "flexcryptopay")
        return (username, password)

    def mkpayout(self, destination, amount, fee, subtract_fee_from_amount=False):
        if self.crypto == self.network_currency and subtract_fee_from_amount:
            fee = Decimal(self.estimate_tx_fee(amount)["fee"])
            if fee >= amount:
                return f"Payout failed: not enought BNB to pay for transaction. Need {fee}, balance {amount}"
            else:
                amount -= fee
        response = requests.post(
            f"http://{self.gethost()}/{self.crypto}/payout/{destination}/{amount}",
            auth=self.get_auth_creds(),
        ).json(parse_float=Decimal)
        return response

    def getstatus(self):
        try:
            response = requests.post(
                f"http://{self.gethost()}/{self.crypto}/status",
                auth=self.get_auth_creds(),
            ).json(parse_float=Decimal)
            block_ts = response["last_block_timestamp"]
            now_ts = int(datetime.datetime.now().timestamp())

            delta = abs(now_ts - block_ts)
            block_interval = 12
            if delta < block_interval * 10:
                return "Synced"
            else:
                return "Sync In Progress (%d blocks behind)" % (delta // block_interval)

        except Exception as e:
            return "Offline"
