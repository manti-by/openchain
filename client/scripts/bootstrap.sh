#!/bin/sh
sudo apt-get install -y git python-pip python-dev python-six
sudo apt-get install -y nginx libsnappy-dev

wget https://github.com/google/leveldb/archive/v1.20.tar.gz
tar -xzf v1.20.tar.gz -C leveldb-1.20
cd leveldb-1.20/
make
sudo cp out-static/lib* out-shared/libleveldb.so.1.20 /usr/local/lib/
sudo ln -s /usr/local/lib/libleveldb.so.1.20 /usr/local/lib/libleveldb.so
sudo ln -s /usr/local/lib/libleveldb.so.1.20 /usr/local/lib/libleveldb.so.1
cd include/
sudo cp -r leveldb /usr/local/include/
sudo ldconfig

cd /home/vagrant/
virtualenv -p python3 --no-site-packages --prompt="venv-" venv
source venv/bin/activate
pip install -r /home/vagrant/app/client/requirements.txt