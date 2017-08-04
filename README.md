Blockchain App
==============


About
-----

Blockchain test app.

Author: Alex Manti <manti.by@gmail.com>

Source link: https://bitbucket.org/manti_by/blockchain

Requirements:

    Ubuntu 16, Python, PostgreSQL, Memcache, Redis


Installation
-------------

1. Install environment (second line for staging servers):

        $ sudo apt-get install -y git python-pip python-dev python-six    
        $ sudo apt-get install -y nginx supervisor postgresql libpq-dev


2. Install [Redis server](https://redis.io/download)


3. Install project dependencies:

        $ cd ../
        $ virtualenv --no-site-packages --prompt="bchain-tracker-" venv-tracker
        $ source venv/bin/activate
        $ pip install -r src/tracker/requirements.txt
        


4. Create database for tracker:

        $ sudo -u postgres psql -c "CREATE DATABASE bchain;"
        $ sudo -u postgres psql -c "CREATE USER bchain WITH PASSWORD 'pa55word';"
        $ sudo -u postgres psql -c "ALTER ROLE bchain SET client_encoding TO 'utf8';"
        $ sudo -u postgres psql -c "ALTER ROLE bchain SET default_transaction_isolation TO 'read committed';"
        $ sudo -u postgres psql -c "ALTER ROLE bchain SET timezone TO 'UTC';"
        $ sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE bchain TO bchain;"

