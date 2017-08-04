import os
import re

from array import array

from app.stun import get_ip_info


def string_to_bytes(string):
    array_key = array('b')
    array_key.frombytes(string.encode())
    return array_key.tobytes()


def get_ip_address():
    return re.search(re.compile(r'(?<=inet )(.*)(?=\/)', re.M), os.popen('ip addr show enp2s0').read()).groups()[0]


def get_address(use_stun=False):
    if use_stun:
        nat_type, ip, port = get_ip_info()
    else:
        ip = get_ip_address()
        port = 8112
    return ip, port
