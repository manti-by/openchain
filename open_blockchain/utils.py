import hashlib
import logging
import logging.config

from array import array

from open_blockchain.conf import settings

logger = logging.getLogger()


def string_to_bytes(string):
    array_key = array('b')
    array_key.frombytes(string.encode())
    return array_key.tobytes()


def init_logger():
    logging.basicConfig(level=logging.DEBUG)
    logging.config.dictConfig(settings['logging'])

    return logger


def base58encode(n):
    b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''
    while n > 0:
        result = b58[n % 58] + result
        n /= 58
    return result


# Will be used to decode raw bytes and then encode them to the base58
def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result


def countLeadingZeroes(s):
    count = 0
    for c in s:
        if c == '\0':
            count += 1
        else:
            break
    return count


def base58CheckEncode(prefix, payload):
    s = chr(prefix) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    return '1' * countLeadingZeroes(result) + base58encode(base256decode(result))
