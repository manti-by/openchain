import hashlib


def base58encode(n: str) -> str:
    b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''
    while n > 0:
        result = b58[n % 58] + result
        n //= 58
    return result


def base256decode(s: str) -> str:
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result


def count_leading_zeroes(s: str) -> int:
    count = 0
    for c in s:
        if c == '\0':
            count += 1
        else:
            break
    return count


def base58check_encode(prefix: int, payload: str) -> str:
    s = chr(prefix) + payload
    checksum = hashlib.sha256(s.encode()).digest()[0:4]
    result = s + checksum.hex()
    return '1' * count_leading_zeroes(result) + base58encode(base256decode(result))
