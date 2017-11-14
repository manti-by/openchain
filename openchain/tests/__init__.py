import os

from unittest import TestCase
from ecdsa import SigningKey, VerifyingKey, SECP256k1


TEST_PRIVATE_KEY_HEX = 'ef3eb92784e801c1a41e6b9affaf3451ed442145e9baf126ed44ec936fac6686'
TEST_PRIVATE_KEY_BYTES = bytes.fromhex(TEST_PRIVATE_KEY_HEX)
TEST_PRIVATE_KEY = SigningKey.from_string(TEST_PRIVATE_KEY_BYTES, curve=SECP256k1)


TEST_PUBLIC_KEY = TEST_PRIVATE_KEY.get_verifying_key()
TEST_PUBLIC_KEY_HEX = (TEST_PUBLIC_KEY.to_string()).hex()
TEST_PUBLIC_KEY_BYTES = bytes.fromhex(TEST_PUBLIC_KEY_HEX)


TEST_ANOTHER_PUBLIC_KEY_HEX = '7cfa4a6a0bdab48788028ae9c06c9d6bc597461cc141c29c6322e96cc21511cb' \
                              '98ea9ccc7eecc362ecfc36f6e0899906477cb052fb0cb78c0a622a33c9d7dd72'
TEST_ANOTHER_PUBLIC_KEY_BYTES = bytes.fromhex(TEST_ANOTHER_PUBLIC_KEY_HEX)
TEST_ANOTHER_PUBLIC_KEY = VerifyingKey.from_string(TEST_ANOTHER_PUBLIC_KEY_BYTES, curve=SECP256k1)


class BaseTestCase(TestCase):

    pass
