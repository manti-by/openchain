
class BlockInvalidException(Exception):
    """Transaction has invalid data hash"""


class TransactionInvalidPublicKeyException(Exception):
    """Transaction has invalid public key"""


class TransactionInvalidSignatureException(Exception):
    """Transaction has invalid signature"""
