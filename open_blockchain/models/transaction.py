import ecdsa
import hashlib

from open_blockchain.models.base import Model, Manager


class TransactionException(Exception):
    """Transaction not signed"""


class TransactionManager(Manager):
    pass


class Transaction(Model):

    in_address = None
    out_address = None
    amount = None
    public_key = None
    signature = None

    objects = TransactionManager()

    def __init__(self, in_address, out_address, amount):
        self.in_address = in_address
        self.out_address = out_address
        self.amount = amount

    def signing(self, private_key):
        data = {
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount
        }
        hashed_raw_tx = hashlib.sha256(hashlib.sha256(data).digest()).digest()
        signing_key = ecdsa.SigningKey.from_string(private_key.decode("hex"), curve=ecdsa.SECP256k1)

        self.public_key = ('\04' + signing_key.verifying_key.to_string()).encode("hex")
        self.signature = signing_key.sign_digest(hashed_raw_tx, sigencode=ecdsa.util.sigencode_der)

    def __dict__(self):
        if self.public_key is None or self.signature is None:
            raise TransactionException
        return {
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount,
            'public_key': self.public_key,
            'signature': self.signature
        }
