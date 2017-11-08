from unittest import TestCase
from ecdsa import SigningKey, VerifyingKey

from openchain.models.wallet import Wallet
from openchain.models.transaction import Transaction


class WalletTestCase(TestCase):

    def test_wallet_creation(self):
        wallet = Wallet()
        self.assertIsInstance(wallet.private_key, SigningKey)
        self.assertIsInstance(wallet.public_key, VerifyingKey)

    def test_sign_transaction_with_wallet(self):
        wallet = Wallet()
        transaction = Transaction(in_address='addr1', out_address='addr2',
                                  amount=10.50, public_key=wallet.public_key)
        transaction.signing(wallet.private_key_bytes)
        self.assertTrue(transaction.is_valid)
