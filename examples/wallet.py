import time
import logging

from pyp2p.net import Net
from pyp2p.dht_msg import DHT


from .common.conf import settings
from .common.utils import init_logger, string_to_bytes, get_address

logger = logging.getLogger()


def success(connection):
    logger.debug('Successfully connected to pool server')

    request = string_to_bytes('X-Client-STUN-Address: {}:{}'.format(ip, port))
    connection.send_line(request)


def failure(connection):
    logger.debug('Cant connect to pool server, shutdown')


if __name__ == "__main__":
    init_logger(settings)
    logger.debug('Starting wallet application')

    ip, port, interface = get_address()

    client_dht = DHT()
    client_node = Net(dht_node=client_dht, passive_bind=ip, passive_port=port,
                      interface=interface, net_type='direct', debug=1)
    client_node.start()

    logger.debug('Connecting to pool server')

    client_node.unl.connect((settings['pool_server']['ip'], settings['pool_server']['port']), {
        'success': success,
        'failure': failure
    })

    # Start IO loop
    while True:
        for con in client_node:
            for reply in con:
                print(reply)
        time.sleep(1)
