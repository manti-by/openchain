import ecdsa
import hashlib

from open_blockchain.utils import base58CheckEncode
from open_blockchain.models.base import Model, Manager


class WalletManager(Manager):
    pass


class Wallet(Model):

    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def __dict__(self):
        return {
            'private_key': self.private_key,
            'public_key': self.public_key
        }

    def private_key_wif(self):
        return base58CheckEncode(0x80, self.private_key.decode('hex'))

    def uncompressed_public_key(self):
        signing_key = ecdsa.SigningKey.from_string(self.private_key.decode('hex'), curve=ecdsa.SECP256k1)
        return ('\04' + signing_key.verifying_key.to_string()).encode('hex')

    @property
    def address(self):
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(self.uncompressed_public_key().decode('hex')).digest())
        return base58CheckEncode(0, ripemd160.digest())
