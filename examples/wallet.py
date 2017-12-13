import json
import logging
import random
import requests

import tornado.ioloop
import tornado.web

from examples.common.conf import settings
from examples.common.utils import init_logger

from openchain.models.wallet import Wallet
from openchain.models.transaction import Transaction

logger = logging.getLogger()


def generate_and_send_transaction(wallet, miner_list):
    transaction = Transaction(in_address=wallet.address, out_address='', amount=random.randint(0, 50))
    transaction.signing(wallet.private_key_hex)
    if transaction.is_valid:
        for miner in miner_list:
            r = requests.post(miner['client_id'], transaction.__dict__)
            result = json.loads(r.json)
            if result['status'] == 200:
                logger.debug('[WALLET] Successfully send transaction')
            else:
                logger.debug('[WALLET] Error sending transaction: {}'.format(result['message']))


if __name__ == "__main__":
    init_logger(settings)
    logger.debug('[WALLET] Starting wallet application')

    wallet_list = Wallet.objects.get()
    if not len(wallet_list):
        logger.debug('[WALLET] Creating new wallet')
        wallet = Wallet()
        wallet.save()
    else:
        logger.debug('[WALLET] Using existing wallet')
        wallet = wallet_list[0]

    logger.debug('[WALLET] Connecting to pool server')
    r = requests.get('http://{}:{}'.format(settings['pool_server']['ip'],
                                           settings['pool_server']['port']))
    miner_list = json.loads(r.json())
    if not miner_list:
        logger.debug('[WALLET] There are no available miner server found, shutdown application')
        exit(0)

    logger.debug('[WALLET] Start transaction generation')

    main_loop = tornado.ioloop.IOLoop.instance()
    scheduled_loop = tornado.ioloop.PeriodicCallback(lambda: generate_and_send_transaction(wallet, miner_list),
                                                     9000, io_loop=main_loop)
    scheduled_loop.start()
    main_loop.start()