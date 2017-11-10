import hashlib

from ecdsa import VerifyingKey, SigningKey, SECP256k1

from openchain.utils.base import base58check_encode
from openchain.models.base import Model, Manager


class WalletManager(Manager):

    pass


class Wallet(Model):

    private_key = None
    public_key = None

    objects = WalletManager

    def __init__(self, private_key: SigningKey=None, public_key: VerifyingKey=None):
        self.private_key = SigningKey.generate(curve=SECP256k1) if private_key is None else private_key
        self.public_key = self.private_key.get_verifying_key() if public_key is None else public_key

    @property
    def __dict__(self) -> dict:
        return {
            'private_key': self.private_key,
            'public_key': self.public_key
        }

    @property
    def private_key_hex(self) -> str:
        return (self.private_key.to_string()).hex()

    @property
    def private_key_bytes(self) -> bytes:
        return bytes.fromhex(self.private_key_hex)

    @property
    def public_key_hex(self) -> str:
        return (self.public_key.to_string()).hex()

    @property
    def public_key_bytes(self) -> bytes:
        return bytes.fromhex(self.public_key_hex)

    @property
    def address(self) -> str:
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(self.public_key_bytes).digest())
        return base58check_encode(0, ripemd160.digest())
