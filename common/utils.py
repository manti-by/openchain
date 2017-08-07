import os
import re
import logging
import logging.config

from array import array

from common.conf import settings
from common.stun import get_ip_info

logger = logging.getLogger()


def string_to_bytes(string):
    array_key = array('b')
    array_key.frombytes(string.encode())
    return array_key.tobytes()


def init_logger():
    logging.basicConfig(level=logging.DEBUG)
    logging.config.dictConfig(settings['logging'])


def get_client_id(request)->str:
    return request.headers.get('X-Client-STUN-Address', None)


def get_internal_address(adapter='enp2s0'):
    try:
        search_string = os.popen('ip addr show {}'.format(adapter)).read()
        match = re.search(re.compile(r'(?<=inet )(.*)(?=\/)', re.M), search_string)
        return match.group(1), 8112
    except:
        logger.warning('Failed to get internal address')
        return None, None


def get_external_address():
    try:
        nat_type, ip, port = get_ip_info()
        return nat_type, ip, port
    except:
        logger.warning('Failed to get external address')
        return None, None, None
