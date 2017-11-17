from unittest import TestCase

from openchain.models.transaction import Transaction

from openchain.models.block import Block
from openchain.tests import TEST_PRIVATE_KEY


class BlockTestCase(TestCase):

    def setUp(self):
        Block.objects.delete_all()
        Transaction.objects.delete_all()

    def test_block_creation(self):
        block = Block('Genesis block')
        block.save()

        self.assertIsInstance(block, Block)

        Block.objects.delete_all()

    def test_block_generation(self):
        block = Block('Genesis block')
        block.generate()

        self.assertTrue(block.is_valid)
        self.assertNotEquals(block.nonce, 0)

        Block.objects.delete_all()

    def test_block_transactions(self):
        transaction_01 = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction_01.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction_01.save()

        transaction_02 = Transaction(in_address='addr3', out_address='addr4', amount=20.50)
        transaction_02.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction_02.save()

        block = Block('Genesis block', transactions=[transaction_01, transaction_02])
        block.generate()
        block.save()

        self.assertTrue(block.is_valid)
        self.assertNotEquals(block.nonce, 0)

        Block.objects.delete_all()
        Transaction.objects.delete_all()
