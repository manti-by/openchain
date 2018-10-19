import time
import logging
import requests

from requests.exceptions import ConnectionError, Timeout

from common.conf import settings

logger = logging.getLogger()


def connect_to_pool_server(timeout=30, max_attempts=5):
    headers = {'X-Client-Address': 'http://{}:{}'.format(settings['miner_server']['ip'],
                                                         settings['miner_server']['port'])}

    pool_server_address = 'http://{}:{}'.format(
        settings['pool_server']['ip'], settings['pool_server']['port']
    )
    logger.debug('Connecting to pool server {}'.format(pool_server_address))

    shutdown = True
    for _ in range(0, max_attempts):
        try:
            r = requests.post(pool_server_address, headers=headers, timeout=timeout)
            if r.status_code != 200:
                logger.warning('Pool server is currently unavailable, retrying')
                time.sleep(timeout)
                continue

            result = r.json()
            if result['status'] != 200:
                logger.error('Pool server encountered error {}'.format(result['message']))
                shutdown = True
                break

            logger.info('Connected to pool server')
            return result

        except ConnectionError:
            logger.warning('Pool server is currently unavailable, retrying')
            time.sleep(timeout)

        except Timeout:
            logger.warning('Pool server is currently unavailable, retrying')

    if shutdown:
        logger.critical('Can\'t connect to pool server, shutdown the application')
        exit(-1)


def get_generators_list(timeout=30, max_attempts=5):
    pool_server_address = 'http://{}:{}'.format(
        settings['pool_server']['ip'], settings['pool_server']['port']
    )
    logger.debug('Connecting to pool server {}'.format(pool_server_address))

    shutdown = True
    for _ in range(0, max_attempts):
        try:
            r = requests.get(pool_server_address, timeout=timeout)
            if r.status_code != 200:
                logger.warning('Pool server is currently unavailable, retrying')
                time.sleep(timeout)
                continue

            result = r.json()
            if result['status'] != 200:
                logger.error('Pool server encountered error {}'.format(result['message']))
                shutdown = True
                break

            if not result['data']:
                logger.warning(' There are no available miner servers found, retrying')
                time.sleep(timeout)
                continue

            logger.info('Connected to miner server')
            return result

        except ConnectionError:
            logger.warning('Pool server is currently unavailable, retrying')
            time.sleep(timeout)

        except Timeout:
            logger.warning('Pool server is currently unavailable, retrying')

    if shutdown:
        logger.critical('Can\'t connect to pool server, shutdown the application')
        exit(-1)
