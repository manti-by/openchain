from unittest import TestCase

from openchain.models.transaction import Transaction
from openchain.models.exception import TransactionInvalidPublicKeyException, TransactionInvalidSignatureException
from openchain.tests import TEST_PRIVATE_KEY_BYTES, TEST_ANOTHER_PUBLIC_KEY


class TransactionTestCase(TestCase):

    def test_transaction_signing(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction.signing(TEST_PRIVATE_KEY_BYTES)
        self.assertTrue(transaction.is_valid)

    def test_transaction_public_key_exception(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50,
                                  public_key=TEST_ANOTHER_PUBLIC_KEY)
        with self.assertRaises(TransactionInvalidPublicKeyException):
            transaction.signing(TEST_PRIVATE_KEY_BYTES)

    def test_transaction_signature_exception(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        with self.assertRaises(TransactionInvalidSignatureException):
            self.assertIsInstance(transaction.__dict__, dict)
