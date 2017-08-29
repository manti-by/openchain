import os
import re
import logging
import logging.config

from array import array
from socket import *

from common.conf import settings
from common.stun import get_ip_info, OpenInternet, FullCone

logger = logging.getLogger()


def string_to_bytes(string):
    array_key = array('b')
    array_key.frombytes(string.encode())
    return array_key.tobytes()


def init_logger():
    logging.basicConfig(level=logging.DEBUG)
    logging.config.dictConfig(settings['logging'])

    return logger


def init_socket():
    nat_type, ip, port = get_ip_info()
    if nat_type not in (OpenInternet, FullCone):
        logger.critical('Your internet connection does not support NAT translation')
        logger.info('Trying to use internal routing')

    if ip is None or port is None:
        logger.critical('Cant get external client address')
        ip = '0.0.0.0'
        port = 8112

    logger.info('Trying to bind address {}:{}'.format(ip, port))

    sock = socket()
    sock.bind((ip, port))
    sock.listen(1)

    return sock.accept()


def get_client_id(request)->str:
    return request.headers.get('X-Client-STUN-Address', '{}:8112'.format(request.remote_ip))
