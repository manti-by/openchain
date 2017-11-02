#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt autoclean && sudo apt autoremove
sudo apt install -y git python-pip python-dev python3-dev python-six virtualenv nginx libsnappy-dev
sudo pip install --upgrade pip

cd /home/ubuntu/ && cp /vagrant/deploy/leveldb-1.20.tar.gz /home/ubuntu/
tar -xzf leveldb-1.20.tar.gz && cd leveldb-1.20/
make
sudo cp out-static/lib* out-shared/libleveldb.so.1.20 /usr/local/lib/
sudo ln -s /usr/local/lib/libleveldb.so.1.20 /usr/local/lib/libleveldb.so
sudo ln -s /usr/local/lib/libleveldb.so.1.20 /usr/local/lib/libleveldb.so.1
cd include/
sudo cp -r leveldb /usr/local/include/
sudo ldconfig

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure --frontend=noninteractive locales

cd /home/ubuntu/
virtualenv -p python3 --no-site-packages --prompt="venv-" /home/ubuntu/venv/
source /home/ubuntu/venv/bin/activate
pip install -r /home/ubuntu/app/requirements.txt