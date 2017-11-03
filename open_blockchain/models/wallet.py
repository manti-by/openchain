import hashlib

from ecdsa import SigningKey, SECP256k1

from open_blockchain.utils.base import base58CheckEncode
from open_blockchain.models.base import Model, Manager


class WalletManager(Manager):
    pass


class Wallet(Model):

    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def __dict__(self):
        return {
            'private_key': self.private_key,
            'public_key': self.public_key
        }

    def private_key_hex(self):
        return (self.private_key.to_string()).hex()

    def private_key_wif(self):
        return base58CheckEncode(0x80, self.private_key_hex())

    def public_key_hex(self):
        return (self.public_key.to_string()).hex()

    def public_key_uncompressed(self):
        return ('\04' + self.public_key.to_string()).encode('hex')

    @property
    def address(self):
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(self.public_key_uncompressed().decode('hex')).digest())
        return base58CheckEncode(0, ripemd160.digest())
