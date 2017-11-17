
class BlockchainTreeChildCollisionException(Exception):
    """Blockchain node has two different childs"""


class BlockchainTreeParentCollisionException(Exception):
    """Blockchain node has two different parents"""


class BlockInvalidException(Exception):
    """Block is invalid"""


class TransactionInvalidPublicKeyException(Exception):
    """Transaction has invalid public key"""


class TransactionInvalidSignatureException(Exception):
    """Transaction has invalid signature"""
