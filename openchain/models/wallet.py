import collections
import hashlib

from ecdsa import VerifyingKey, SigningKey, SECP256k1

from openchain.utils.base import base58check_encode
from openchain.models.base import Model, Manager


class WalletManager(Manager):

    pass


class Wallet(Model):

    private_key = None
    public_key = None

    objects = WalletManager()

    def __init__(self, private_key: str=None, public_key: str=None):
        if private_key is None:
            self.private_key = SigningKey.generate(curve=SECP256k1)
        else:
            self.private_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)

        if public_key is None:
            self.public_key = self.private_key.get_verifying_key()
        else:
            self.public_key = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)

    @property
    def __dict__(self) -> dict:
        unordered = {
            'private_key': self.private_key.to_string().hex(),
            'public_key': self.public_key.to_string().hex()
        }
        return collections.OrderedDict(sorted(unordered.items()))

    @property
    def private_key_hex(self) -> str:
        return self.private_key.to_string().hex()

    @property
    def private_key_bytes(self) -> bytes:
        return bytes.fromhex(self.private_key_hex)

    @property
    def public_key_hex(self) -> str:
        return self.public_key.to_string().hex()

    @property
    def public_key_bytes(self) -> bytes:
        return bytes.fromhex(self.public_key_hex)

    @property
    def address(self) -> str:
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(self.public_key_bytes).digest())
        return base58check_encode(0, ripemd160.digest().hex())
