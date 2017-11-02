import time
import hashlib
import logging

from open_blockchain.models.base import Model, Manager
from open_blockchain.utils import string_to_bytes

logger = logging.getLogger()


class BlockManager(Manager):
    pass


class Block(Model):

    _tx = []

    id = None
    hash = None
    prev = None
    next = None
    root = None

    objects = BlockManager()

    def __init__(self, prev):
        self.prev = prev
        self.timestamp = time.time()

    def __bytes__(self) -> bytes:
        return string_to_bytes(self.__str__())

    def __str__(self) -> str:
        data = '[%s]' % ', '.join([i.__str__() for i in self._tx])
        return '{{"hash": {},"prev": {}, "data": "{}", "timestamp": {}}}'.format(self.hash, self.prev,
                                                                                 data, self.timestamp)

    @property
    def is_valid(self) -> bool:
        return self.hash is not None

    def generate(self):
        self.hash = hashlib.sha256({'prev': self.prev, 'data': self._tx, 'timestamp': self.timestamp})

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the Proof
        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: True if correct, False if not.
        """

        guess = '{}{}'.format(last_proof, proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def save(self):
        if self.is_valid:
            logger.debug('Generate new block {}'.format(self.hash))
            super().save()
