import json

from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey, SECP256k1

from openchain.models.base import Model, Manager
from openchain.models.exception import TransactionInvalidPublicKeyException, TransactionInvalidSignatureException


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
        if public_key is not None:
            self.public_key = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
        if signature is not None:
            self.signature = bytes.fromhex(signature)

    @property
    def data(self) -> bytes:
        return json.dumps({
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount
        }).encode()

    def signing(self, private_key: str):
        hashed_raw_transaction = sha256(sha256(self.data).digest()).digest()
        signing_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        if self.public_key is None:
            self.public_key = signing_key.verifying_key
        elif self.public_key.to_string() != signing_key.verifying_key.to_string():  # check pre-assigned key
            raise TransactionInvalidPublicKeyException
        if self.signature is None:
            self.signature = signing_key.sign(hashed_raw_transaction)

    @property
    def is_valid(self) -> bool:
        if self.public_key is not None and self.signature is not None:
            hashed_raw_transaction = sha256(sha256(self.data).digest()).digest()
            return self.public_key.verify(self.signature, hashed_raw_transaction)
        return False

    @property
    def __dict__(self) -> dict:
        if not self.is_valid:
            raise TransactionInvalidSignatureException
        return {
            'in_address': self.in_address,
            'out_address': self.out_address,
            'amount': self.amount,
            'public_key': self.public_key.to_string().hex(),
            'signature': self.signature.hex()
        }
