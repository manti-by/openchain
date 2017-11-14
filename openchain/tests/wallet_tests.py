from unittest import TestCase
from ecdsa import SigningKey, VerifyingKey

from openchain.models.wallet import Wallet
from openchain.models.transaction import Transaction


class WalletTestCase(TestCase):

    def setUp(self):
        Wallet.objects.delete_all()

    def test_wallet_creation(self):
        wallet = Wallet()
        wallet.save()

        self.assertIsInstance(wallet.private_key, SigningKey)
        self.assertIsInstance(wallet.public_key, VerifyingKey)

        Wallet.objects.delete_all()

    def test_sign_transaction_with_wallet(self):
        wallet = Wallet()
        wallet.save()

        transaction = Transaction(in_address='addr1', out_address='addr2',
                                  amount=10.50, public_key=wallet.public_key.to_string().hex())
        transaction.signing(wallet.private_key_hex)
        self.assertTrue(transaction.is_valid)

        Wallet.objects.delete_all()
        Transaction.objects.delete_all()

    def test_wallet_properties(self):
        wallet = Wallet()
        wallet.save()

        self.assertIsInstance(wallet.private_key_hex, str)
        self.assertIsInstance(wallet.private_key_bytes, bytes)
        self.assertIsInstance(wallet.public_key_hex, str)
        self.assertIsInstance(wallet.public_key_bytes, bytes)
        self.assertIsInstance(wallet.address, str)

        Wallet.objects.delete_all()
