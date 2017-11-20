import json
import collections

from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.keys import BadSignatureError

from openchain.models.base import Model, Manager
from openchain.models.exception import TransactionInvalidPublicKeyException


class TransactionManager(Manager):

    pass


class Transaction(Model):

    in_address = None
    out_address = None
    amount = None
    data_hash = None
    public_key = None
    signature = None

    objects = TransactionManager()

    def __init__(self, in_address: str, out_address: str, amount: float,
                 public_key: str=None, signature: str=None):
        self.in_address = in_address
        self.out_address = out_address
        self.amount = amount
        self.data_hash = sha256(sha256(self.data).digest()).digest()

        if public_key is not None:
            self.public_key = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
        if signature is not None:
            self.signature = bytes.fromhex(signature)

    @property
    def data(self) -> bytes:
        data = {
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount
        }
        ordered = collections.OrderedDict(sorted(data.items()))
        return json.dumps(ordered).encode()

    @property
    def __dict__(self) -> dict:
        unordered = {
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount,
            'public_key': self.public_key.to_string().hex() if self.public_key else None,
            'signature': self.signature.hex()
        }
        return collections.OrderedDict(sorted(unordered.items()))

    def signing(self, private_key: str):
        self.data_hash = sha256(sha256(self.data).digest()).digest()
        signing_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        if self.public_key is None:
            self.public_key = signing_key.verifying_key
        elif self.public_key.to_string() != signing_key.verifying_key.to_string():  # check pre-assigned key
            raise TransactionInvalidPublicKeyException
        if self.signature is None:
            self.signature = signing_key.sign(self.data_hash)

    @property
    def is_valid(self) -> bool:
        if self.public_key is not None and self.signature is not None:
            try:
                hashed_raw_transaction = sha256(sha256(self.data).digest()).digest()
                if self.data_hash != hashed_raw_transaction:
                    return False
                return self.public_key.verify(self.signature, hashed_raw_transaction)
            except BadSignatureError:
                pass
        return False
