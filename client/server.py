import logging

from socket import *

from common.utils import init_logger, string_to_bytes, init_socket

logger = logging.getLogger()


if __name__ == "__main__":
    logger.info('Starting client application')

    init_logger()
    sock, address = init_socket()

    print(address)

    request = string_to_bytes('X-Client-STUN-Address: {}:{}'.format(address))
    logger.info('Send request with address {}:{}'.format(address))

    sock.sendto(request, ('192.168.112.10', 8112))
    data = sock.recvfrom(1024)

    logger.info('Received data')
    logger.info(data)

    sock.close()
