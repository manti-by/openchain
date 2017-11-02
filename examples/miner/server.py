import logging

from open_blockchain.utils import init_logger, string_to_bytes
from open_blockchain.network import init_socket

logger = logging.getLogger()


if __name__ == "__main__":
    local = True
    logger.info('Starting client application')

    init_logger()
    sock, ip, port = init_socket(local)

    request = string_to_bytes('X-Client-STUN-Address: {}:{}'.format(ip, port))
    logger.info('Send request with address {}:{}'.format(ip, port))

    server_ip = '192.168.112.10'
    if local:
        server_ip = '127.0.0.1'

    sock.sendto(request, (server_ip, 8112))

    while True:
        data, addr = sock.recvfrom(1024)

        logger.info('Received data')
        logger.info(data)

        if not data:
            break

    sock.close()
