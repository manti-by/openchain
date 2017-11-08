import logging

from socket import socket

from openchain.utils.stun import get_ip_info, OpenInternet, FullCone

logger = logging.getLogger()


def init_socket():
    nat_type, ip, port = get_ip_info()
    if nat_type not in (OpenInternet, FullCone):
        logger.critical('Your internet connection does not support NAT translation')
        logger.info('Trying to use internal routing')

    if ip is None or port is None:
        logger.critical('Cant get external client address')
        local = True

    if local:
        ip = '0.0.0.0'
        port = 8113

    logger.info('Trying to bind address {}:{}'.format(ip, port))

    sock = socket()
    sock.bind((ip, port))

    return sock, ip, port


def get_client_id(request)->str:
    return request.headers.get('X-Client-STUN-Address', '{}:8112'.format(request.remote_ip))
