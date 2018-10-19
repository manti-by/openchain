import logging

import tornado.ioloop
import tornado.web

from common.conf import settings
from common.utils import init_logger
from common.connection import connect_to_pool_server
from listener.generator import GeneratorListener

from openchain.models.block import Block
from openchain.models.transaction import Transaction

logger = logging.getLogger()


def generate_block():
    logger.info('Start blockchain generation')

    transaction_list = []
    for transaction in Transaction.objects.get():
        transaction_list.append(transaction.__dict__)

    if len(transaction_list):
        logger.debug('Add {} transactions to new block'.format(len(transaction_list)))
        try:
            logger.debug('Read last block hash from file')
            file = open(settings['generator_last_hash'], 'rw')
            last_block_hash = file.read()

            block = Block(last_block_hash, transactions=transaction_list)
            block.generate()
            block.save()

            logger.debug('Save last block hash to file')
            file.write(block.data_hash)
            file.close()

            logger.debug('Delete processed transactions')
            Transaction.objects.delete_all()

            logger.info('Added block with hash {}'.format(block.data_hash))
        except Exception as e:
            logger.error(e)
    else:
        logger.info('Skipping empty block generation')


if __name__ == "__main__":
    init_logger(settings)
    logger.info('Starting the application')

    connect_to_pool_server()

    app = tornado.web.Application([
        (r"/", GeneratorListener),
    ])
    app.listen(settings['generator_server']['port'])

    io_loop = tornado.ioloop.IOLoop.current()
    scheduler = tornado.ioloop.PeriodicCallback(generate_block, 10000)

    logger.info('Listening for connections on {}:{}'.format(settings['miner_server']['ip'],
                                                            settings['miner_server']['port']))
    scheduler.start()
    io_loop.start()
