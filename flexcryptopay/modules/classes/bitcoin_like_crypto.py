from abc import abstractmethod
from decimal import Decimal
from os import environ
import datetime
import functools

from flexcryptopay import requests
from flexcryptopay.modules.classes.crypto import Crypto


class BitcoinLikeCrypto(Crypto):
    def balance(self):
        try:
            response = requests.post(
                "http://" + self.gethost(),
                auth=self.get_rpc_credentials(),
                json=self.build_rpc_request("getbalance", "*", 1),
            ).json(parse_float=Decimal)
            balance = response["result"]
        except requests.exceptions.RequestException:
            balance = False

        return balance

    def getstatus(self):
        try:
            response = requests.post(
                "http://" + self.gethost(),
                auth=self.get_rpc_credentials(),
                json=self.build_rpc_request("getblockchaininfo"),
                timeout=10,
            ).json(parse_float=Decimal)

            if response["result"]["headers"] == response["result"]["blocks"]:
                return "Synced"
            else:
                return "Sync In Progress (%.2f%%)" % (
                    response["result"]["verificationprogress"] * 100
                )

        except Exception as e:
            return "Offline"

    def mkpayout(self, destination, amount, fee, subtract_fee_from_amount=False):
        btc_per_kb = "%.8f" % (float(fee) / 100000)

        response = requests.post(
            "http://" + self.gethost(),
            auth=self.get_rpc_credentials(),
            json=self.build_rpc_request("settxfee", btc_per_kb),
        ).json(parse_float=Decimal)
        if response["error"]:
            return response

        response = requests.post(
            "http://" + self.gethost(),
            auth=self.get_rpc_credentials(),
            json=self.build_rpc_request(
                "sendtoaddress",
                destination,
                str(amount.normalize()),
                "",
                "",
                subtract_fee_from_amount,
            ),
        ).json(parse_float=Decimal)

        return response

    def mkaddr(self, **kwargs):
        response = requests.post(
            "http://" + self.gethost(),
            auth=self.get_rpc_credentials(),
            json=self.build_rpc_request("getnewaddress"),
        ).json(parse_float=Decimal)
        addr = response["result"]
        return addr

    def getaddrbytx(self, txid):
        response = requests.post(
            "http://" + self.gethost(),
            auth=self.get_rpc_credentials(),
            json=self.build_rpc_request("gettransaction", txid),
        ).json(parse_float=Decimal)

        if response["error"]:
            raise Exception(
                f"failed to get details of txid {txid}: {response['error']=}"
            )

        details = []
        for i in response["result"]["details"]:
            details.append(
                [
                    i["address"],
                    i["amount"],
                    response["result"]["confirmations"],
                    i["category"],
                ]
            )
        if details:
            return details
        else:
            raise Exception(
                f"failed to find details in txid {txid}: {response['result']}"
            )

    def get_confirmations_by_txid(self, txid):
        _, _, confirmations, _ = self.getaddrbytx(txid)
        return confirmations

    def create_wallet(self, name="flexcryptopay"):
        response = requests.post(
            "http://" + self.gethost(),
            auth=self.get_rpc_credentials(),
            json=self.build_rpc_request("createwallet", name),
        ).json(parse_float=Decimal)
        return response

    def dump_wallet(self):
        now = datetime.datetime.now().strftime("%F_%T")
        fname = f"{now}_{self.crypto}_flexcryptopay_wallet.dat"

        response = requests.post(
            "http://" + self.gethost(),
            auth=self.get_rpc_credentials(),
            json=self.build_rpc_request("backupwallet", f"/backup/{fname}"),
        ).json(parse_float=Decimal)

        host, port = self.gethost().split(":")
        return f"http://{host}:5555/{fname}"

    def get_all_addresses(self):
        response = requests.post(
            "http://" + self.gethost(),
            auth=self.get_rpc_credentials(),
            json=self.build_rpc_request("listreceivedbyaddress", 0, True),
        ).json(parse_float=Decimal)
        return (
            [addr["address"] for addr in response["result"]]
            if response["result"]
            else []
        )

    @property
    def wallet(self):
        return self._wallet.query.filter_by(crypto=self.crypto).first()

    # For internal usage

    def get_rpc_credentials(self):
        username = environ.get(f"{self.crypto}_USERNAME", "flexcryptopay")
        password = environ.get(f"{self.crypto}_PASSWORD", "flexcryptopay")
        return (username, password)

    def build_rpc_request(self, method, *params):
        return {"jsonrpc": "1.0", "id": "flexcryptopay", "method": method, "params": params}
