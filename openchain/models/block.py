import json
import time
import collections

from hashlib import sha256

from openchain.models.base import Model, Manager
from openchain.models.blockchain import Blockchain
from openchain.models.exception import BlockInvalidException


class BlockManager(Manager):

    @property
    def blockchain(self):
        return Blockchain(self.queryset)

    def append(self, item, commit=False):
        prev_block = self.search(item.prev_block)
        if prev_block is not None and item.is_valid:
            prev_block.next_block = item.data_hash
            prev_block.save()
            self.queryset.append(item)
            self.save()


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
    def data(self) -> bytes:
        data = {
            'prev': self.prev_block,
            'transactions': self.transactions,
            'timestamp': self.timestamp
        }
        ordered = collections.OrderedDict(sorted(data.items()))
        return json.dumps(ordered).encode()

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

    @property
    def is_valid(self) -> bool:
        hashed_raw_block = sha256(sha256(self.data).digest()).digest()
        if self.data_hash != hashed_raw_block:
            return False
        return self.valid_nonce(self.nonce)

    @property
    def __dict__(self):
        if not self.is_valid:
            raise BlockInvalidException
        return {
            'prev_block': self.prev_block,
            'next_block': self.next_block,
            'data_hash': self.data_hash,
            'nonce': self.nonce,
            'transactions': self.transactions,
            'timestamp': self.timestamp
        }
