import json

from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import sigencode_der, sigdecode_der
from hashlib import sha256

from openchain.models.base import Model, Manager


class TransactionException(Exception):
    """Transaction has invalid signature"""


class TransactionManager(Manager):
    pass


class Transaction(Model):

    in_address = None
    out_address = None
    amount = None
    public_key = None
    signature = None

    objects = TransactionManager()

    def __init__(self, in_address: str, out_address: str, amount: float,
                 public_key: str=None, signature: str=None):
        self.in_address = in_address
        self.out_address = out_address
        self.amount = amount
        self.public_key = public_key
        self.signature = signature

    def signing(self, private_key: str):
        data = json.dumps({
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount
        }).encode()
        hashed_raw_transaction = sha256(sha256(data).digest()).digest()
        signing_key = SigningKey.from_string(private_key, curve=SECP256k1)

        self.public_key = signing_key.verifying_key.to_string()
        self.signature = signing_key.sign_digest(hashed_raw_transaction, sigencode=sigencode_der)

    @property
    def is_valid(self) -> bool:
        if self.public_key is not None and self.signature is not None:
            verifying_key = VerifyingKey.from_string(self.public_key, curve=SECP256k1)
            return verifying_key.verify(self.signature, verifying_key.to_string())
        return False

    @property
    def pk(self):
        return self.signature

    def __dict__(self) -> dict:
        if not self.is_valid:
            raise TransactionException
        return {
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount,
            'public_key': self.public_key,
            'signature': self.signature
        }
