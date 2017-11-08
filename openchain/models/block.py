import json
import time

from hashlib import sha256

from openchain.models.base import Model, Manager


class BlockManager(Manager):

    def model_from_dict(self, data):
        return Block(**data)


class Block(Model):

    prev_block = None
    next_block = None
    data_hash = None
    nonce = 0
    transactions = []
    timestamp = None

    objects = BlockManager

    def __init__(self, prev_block: str, next_block: str=None, data_hash: str=None,
                 transactions: list=None, timestamp: float=None):
        self.prev_block = prev_block
        if next_block is not None:
            self.next_block = next_block
        if data_hash is not None:
            self.data_hash = data_hash
        if transactions is not None:
            self.transactions = transactions
        if timestamp is not None:
            self.timestamp = timestamp

    @property
    def __dict__(self):
        return {
            'prev_block': self.prev_block,
            'next_block': self.next_block,
            'data_hash': self.data_hash,
            'nonce': self.nonce,
            'transactions': self.transactions,
            'timestamp': self.timestamp
        }

    @property
    def is_valid(self) -> bool:
        return self.data_hash is not None

    @property
    def data(self) -> bytes:
        return json.dumps({
            'prev': self.prev_block,
            'transactions': self.transactions,
            'timestamp': self.timestamp
        }).encode()

    def generate(self):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the data hash
         - p is the data hash, and p' is the new proof
        """

        self.data_hash = sha256(sha256(self.data).digest()).digest()
        while self.valid_nonce(self.nonce) is False:
            self.nonce += 1
        if self.timestamp is None:
            self.timestamp = time.time()

    def valid_nonce(self, nonce: int) -> bool:
        """
        Validates the Nonce
        :param nonce: Current Nonce
        :return: True if correct, False if not.
        """

        guess = '{}{}'.format(self.data_hash, nonce).encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def save(self):
        if not self.is_valid:
            self.generate()
        super().save()
