Openchain Library
=================

About
-----

Library for creating blockchain networks.

**WARNING:** Currently library in **Alpha** development status. It's a concept of vision, not working library yet.

Author: Alexander Chaika <manti.by@gmail.com>

Source link: https://bitbucket.org/manti_by/openchain

Requirements:

- Base - Python 3.5+, ECSDA, LevelDB
- Development - Flake8
- Examples - Docker, Tornado, PyP2P

Installation
------------

From `PyPi <https://pypi.python.org/pypi/openchain>`_

    $ pip install openchain

From `Bitbucket <https://bitbucket.org/manti_by/openchain>`_

    $ git clone git@bitbucket.org:manti_by/openchain.git

    $ cd openchain/

    $ python setup.py install

Environment variables
---------------------

- $DATABASE_PATH - path to store LevelDB files

Run the examples with Docker
----------------------------

    $ cd examples/

    $ docker build -t mantiby/openchain:latest .

    $ docker swarm init

    $ docker stack deploy -c docker-compose.yml openchain

Run unit tests and coverage
---------------------------

    $ export DATABASE_PATH='/var/tmp/leveldb/test/'

    $ python -m unittest discover -s openchain/tests/ -p '*_tests.py'

    $ coverage run -m unittest discover -s openchain/tests/ -p '*_tests.py'

    $ coverage report -m