import json
import logging
import requests

import tornado.ioloop
import tornado.web

from examples.common.conf import settings
from examples.common.utils import init_logger
from examples.listener.miner import MinerListener

from openchain.models.block import Block
from openchain.models.transaction import Transaction

logger = logging.getLogger()


def generate_blockchain():
    transaction_list = []
    for transaction in Transaction.objects.get():
        transaction_list.append(transaction.__dict__)

    block = Block(Block.objects.blockchain.last_block_hash, transactions=transaction_list)
    block.generate()
    block.save()

    Transaction.objects.delete_all()


if __name__ == "__main__":
    init_logger(settings)
    logger.debug('[MINER] Starting wallet application')

    blockchain = Block.objects.blockchain
    if blockchain is not None:
        logger.debug('[MINER] Blockchain loaded')
    else:
        # TODO: Add genesis block
        pass

    logger.debug('[MINER] Announcing address to pool server')

    headers = {'X-Client-Address': 'http://{}:{}'.format(settings['miner_server']['ip'],
                                                         settings['miner_server']['port'])}
    r = requests.post('http://{}:{}'.format(settings['pool_server']['ip'],
                                            settings['pool_server']['port']), headers=headers)

    result = json.loads(r.json())
    if result['status'] != 200:
        logger.debug('[MINER] Cant connect to pool server, shutdown the application')
        exit(0)

    app = tornado.web.Application([
        (r"/", MinerListener),
    ])
    app.listen(settings['miner_server']['port'], address=settings['miner_server']['ip'])

    main_loop = tornado.ioloop.IOLoop.instance()
    scheduled_loop = tornado.ioloop.PeriodicCallback(generate_blockchain, 60000, io_loop=main_loop)

    logger.debug('[MINER] Start blockchain generation')
    scheduled_loop.start()

    logger.debug('[MINER] Listening for connections on {}:{}'.format(settings['miner_server']['ip'],
                                                                     settings['miner_server']['port']))
    main_loop.start()