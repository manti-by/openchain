from unittest import TestCase

from open_blockchain.models.transaction import Transaction

TEST_PRIVATE_KEY_HEX = 'ef3eb92784e801c1a41e6b9affaf3451ed442145e9baf126ed44ec936fac6686'
TEST_PRIVATE_KEY_RAW = bytes.fromhex(TEST_PRIVATE_KEY_HEX)


class TransactionTestCase(TestCase):

    def test_transaction(self):
        t = Transaction(in_address='addr1', out_address='addr2', amount=10.50)
        t.signing(TEST_PRIVATE_KEY_RAW)
        self.assertTrue(t.is_valid)
