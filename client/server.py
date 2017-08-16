import os
import logging

from socket import *

from common.utils import init_logger, string_to_bytes, get_external_address, get_internal_address
from common.stun import OpenInternet, FullCone

logger = logging.getLogger()


if __name__ == "__main__":
    init_logger()
    logger.info('Starting client application')

    nat_type, external_ip, external_port = get_external_address()
    if nat_type not in (OpenInternet, FullCone):
        logger.critical('Your internet connection does not support NAT translation')
        logger.info('Trying to use internal routing')

    if external_ip is None or external_port is None:
        logger.critical('Cant get external client address')
        logger.info('Trying to use internal address')

    internal_ip, internal_port = get_internal_address()
    logger.info('Try to bind client address {}:{}'.format(internal_ip, internal_port))

    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind((internal_ip, internal_port))

    request = string_to_bytes('X-Client-STUN-Address: {}:{}'.format(internal_ip, internal_port))
    logger.info('Send request with address {}:{}'.format(internal_ip, internal_port))

    udp_socket.sendto(request, ('192.168.112.1', 8112))
    data = udp_socket.recvfrom(1024)

    logger.info('Received data')
    logger.info(data)

    udp_socket.close()