import time
import uuid
import logging
import random
import requests

import tornado.ioloop
import tornado.web

from common.conf import settings
from common.utils import init_logger
from common.connection import get_generators_list

from openchain.models.wallet import Wallet
from openchain.models.transaction import Transaction

logger = logging.getLogger()


def generate_and_send_transaction(wallet, miner_list):
    # Randomize transaction generation time
    time.sleep(random.randint(0, 5))

    # Create new transaction
    transaction = Transaction(in_address=wallet.address, out_address=str(uuid.uuid4()),
                              amount=random.randint(0, 50))
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

    result = get_generators_list()

    io_loop = tornado.ioloop.IOLoop.current()
    scheduler = tornado.ioloop.PeriodicCallback(
        lambda: generate_and_send_transaction(wallet, result['data']), 5000
    )

    logger.info('Start transaction generation')
    scheduler.start()
    io_loop.start()
