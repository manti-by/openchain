import time
import logging
import requests

import tornado.ioloop
import tornado.web

from requests.exceptions import ConnectionError, Timeout

from common.conf import settings
from common.utils import init_logger
from listener.miner import MinerListener

from openchain.models.block import Block
from openchain.models.factory import BlockchainFactory
from openchain.models.transaction import Transaction

logger = logging.getLogger()
logger_verbose = logging.getLogger('verbose')


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


def generate_blockchain():
    logger.info('Start blockchain generation')

    transaction_list = []
    for transaction in Transaction.objects.get():
        transaction_list.append(transaction.__dict__)

    if len(transaction_list):
        logger.debug('Transaction list count {}'.format(len(transaction_list)))
        try:
            block_list = Block.objects.get()
            logger.debug('Block list count {}'.format(len(block_list)))

            block_chain = BlockchainFactory.build_blockchain(block_list)
            logger.debug('Last block hash {}'.format(block_chain.last_block_hash))

            block = Block(block_chain.last_block_hash, transactions=transaction_list)
            block.generate()
            block.save()

            logger.debug('Delete processed transactions')
            Transaction.objects.delete_all()

            logger.info('Added block with {} transactions'.format(len(transaction_list)))
        except Exception as e:
            logger_verbose.error(e)
    else:
        logger.info('Skipping empty block generation')


if __name__ == "__main__":
    init_logger(settings)
    logger.info('Starting the application')

    blockchain = BlockchainFactory.build_blockchain(Block.objects.get())
    logger.info('Blockchain loaded with {} blocks'.format(len(blockchain.block_list)))

    connect_to_pool_server()

    app = tornado.web.Application([
        (r"/", MinerListener),
    ])
    app.listen(settings['miner_server']['port'])

    io_loop = tornado.ioloop.IOLoop.current()
    scheduler = tornado.ioloop.PeriodicCallback(generate_blockchain, 10000)

    logger.info('Listening for connections on {}:{}'.format(settings['miner_server']['ip'],
                                                            settings['miner_server']['port']))
    scheduler.start()
    io_loop.start()
