from unittest import TestCase

from openchain.models.factory import ModelFactory
from openchain.models.transaction import Transaction
from openchain.models.exception import TransactionInvalidPublicKeyException
from openchain.tests import TEST_PRIVATE_KEY, TEST_ANOTHER_PUBLIC_KEY, UNKNOWN_VALID_SIGNATURE_BYTES


class TransactionModelTestCase(TestCase):

    def setUp(self):
        Transaction.objects.delete_all()

    def test_transaction_creation(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction.save()

        self.assertIsInstance(transaction, Transaction)
        Transaction.objects.delete_all()

    def test_transaction_set(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction.save()

        transaction = Transaction(in_address='addr3', out_address='addr4', amount=20.50)
        transaction.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction.save()

        transaction_count = len(Transaction.objects.get())
        self.assertEqual(transaction_count, 2)
        Transaction.objects.delete_all()

    def test_transaction_update_hash(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction.signing(TEST_PRIVATE_KEY.to_string().hex())
        transaction.save()

        transaction.data_hash = None
        self.assertFalse(transaction.is_valid)
        Transaction.objects.delete_all()

    def test_transaction_model_factory(self):
        transaction_model_instance = ModelFactory.get_model('transaction')
        self.assertEqual(transaction_model_instance, Transaction)


class TransactionSigningTestCase(TestCase):

    def setUp(self):
        Transaction.objects.delete_all()

    def test_transaction_signing(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction.signing(TEST_PRIVATE_KEY.to_string().hex())

        self.assertTrue(transaction.is_valid)
        self.assertIsInstance(transaction.__dict__, dict)

    def test_transaction_public_key_exception(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50,
                                  public_key=TEST_ANOTHER_PUBLIC_KEY.to_string().hex())

        with self.assertRaises(TransactionInvalidPublicKeyException):
            transaction.signing(TEST_PRIVATE_KEY.to_string().hex())

    def test_transaction_signature_substitution(self):
        transaction = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        transaction.signing(TEST_PRIVATE_KEY.to_string().hex())

        transaction.signature = UNKNOWN_VALID_SIGNATURE_BYTES
        self.assertFalse(transaction.is_valid)
