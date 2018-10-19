import logging
import logging.config

from array import array

logger = logging.getLogger()


def string_to_bytes(string):
    array_key = array('b')
    array_key.frombytes(string.encode())
    return array_key.tobytes()


def init_logger(settings):
    logging.basicConfig(level=logging.DEBUG)
    logging.config.dictConfig(settings['logging'])
    return logger


def get_address():
    ip = port = interface = None
    return ip, port, interface
