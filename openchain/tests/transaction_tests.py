from unittest import TestCase

from openchain.models.transaction import Transaction
from openchain.models.exceptions import TransactionInvalidPublicKeyException, TransactionInvalidSignatureException
from openchain.tests.constants import TEST_PRIVATE_KEY_BYTES, TEST_ANOTHER_PUBLIC_KEY_HEX


class TransactionTestCase(TestCase):

    def test_transaction_signing(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction.signing(TEST_PRIVATE_KEY_BYTES)
        self.assertTrue(transaction.is_valid)

    def test_transaction_public_key_exception(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50,
                                  public_key=TEST_ANOTHER_PUBLIC_KEY_HEX)
        self.assertRaises(TransactionInvalidPublicKeyException,
                          transaction.signing, TEST_PRIVATE_KEY_BYTES)

    def test_transaction_signature_exception(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        self.assertRaises(TransactionInvalidSignatureException,
                          transaction.__dict__)
