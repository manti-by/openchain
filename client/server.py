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
        exit(os.EX_PROTOCOL)

    if external_ip is None or external_port is None:
        logger.critical('Cant get external client address')
        exit(os.EX_PROTOCOL)

    internal_ip, internal_port = get_internal_address()
    logger.info('Try to bind client address {}:{}'.format(internal_ip, internal_port))

    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind((internal_ip, internal_port))

    request = string_to_bytes('X-Client-STUN-Address: {}:{}'.format(internal_ip, internal_port))
    udp_socket.sendto(request, ('127.0.0.1', 8112))
    data = udp_socket.recvfrom(1024)
    print(data)

    udp_socket.close()