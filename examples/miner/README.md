Blockchain Miner
==================


About
-----

Blockchain miner app.

Author: Alex Manti <manti.by@gmail.com>

Source link: https://bitbucket.org/manti_by/blockchain

Requirements:

    Ubuntu 16, Python 3, Gunicorn, LevelDB


Installation
-------------

1. Install environment:

        sudo apt-get install -y git python-pip python-dev python-six
        sudo apt-get install -y nginx libsnappy-dev


2. Install LevelDB:

        wget https://github.com/google/leveldb/archive/v1.20.tar.gz
        tar -xzf v1.20.tar.gz -C leveldb-1.20
        cd leveldb-1.20
        make
        sudo cp out-static/lib* out-shared/libleveldb.so.1.20 /usr/local/lib/
        sudo ln -s /usr/local/lib/libleveldb.so.1.20 /usr/local/lib/libleveldb.so
        sudo ln -s /usr/local/lib/libleveldb.so.1.20 /usr/local/lib/libleveldb.so.1
        cd include/
        sudo cp -r leveldb /usr/local/include/
        sudo ldconfig


3. Install project dependencies:

        $ virtualenv -p python3 --no-site-packages --prompt="tracker-" ../../venv-tracker
        $ source ../../venv-tracker/bin/activate
        $ pip install -r requirements.txt
