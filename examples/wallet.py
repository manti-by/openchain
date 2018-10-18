import time
import logging
import random
import requests

import tornado.ioloop
import tornado.web

from requests.exceptions import ConnectionError, Timeout

from common.conf import settings
from common.utils import init_logger

from openchain.models.wallet import Wallet
from openchain.models.transaction import Transaction

logger = logging.getLogger()


def connect_to_miner_server(timeout=30, max_attempts=5):
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


def generate_and_send_transaction(wallet, miner_list):
    # Randomize transaction generation time
    time.sleep(random.randint(0, 5))

    # Create new transaction
    transaction = Transaction(in_address=wallet.address, out_address='', amount=random.randint(0, 50))
    transaction.signing(wallet.private_key_hex)
    if transaction.is_valid:
        for miner in miner_list:
            r = requests.post(miner['client_id'], json=transaction.__dict__)
            if r.status_code != 200:
                logger.warning('Error sending transaction, server not responding')
                return

            result = r.json()
            if result['status'] == 200:
                logger.info('Successfully send transaction to {}'.format(miner['client_id']))
            else:
                logger.warning('Error sending transaction: {}'.format(result['message']))
            return


if __name__ == "__main__":
    init_logger(settings)
    logger.info('Starting wallet application')

    wallet_list = Wallet.objects.get()
    if not len(wallet_list):
        logger.info('Creating new wallet')
        wallet = Wallet()
        wallet.save()
    else:
        logger.info('Using existing wallet')
        wallet = wallet_list[0]

    result = connect_to_miner_server()

    io_loop = tornado.ioloop.IOLoop.current()
    scheduler = tornado.ioloop.PeriodicCallback(
        lambda: generate_and_send_transaction(wallet, result['data']), 5000
    )

    logger.info('Start transaction generation')
    scheduler.start()
    io_loop.start()
