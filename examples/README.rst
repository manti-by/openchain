Examples for Openchain Library
==============================

About
-----

Openchain is a library for creating blockchain networks. This README shows how to use it.

Author: Alexander Chaika <manti.by@gmail.com>

Library repo: https://bitbucket.org/manti_by/openchain

Requirements:

    Python 3.5+, ECSDA, LevelDB/Plyvel, Docker, Tornado

Installation
------------

Install system libraries

    $ sudo apt install python3-dev libleveldb-dev

Install package from `PyPi <https://pypi.python.org/pypi/openchain>`_

    $ pip install openchain


Run the examples with Docker
----------------------------

    $ cd examples/

    $ docker build -t mantiby/openchain:latest .

    $ docker-compose up/down