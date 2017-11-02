#!/bin/bash
nohup vagrant ssh tracker -c '/vagrant/deploy/scripts/runtracker.sh' > logs/blockchain-tracker.log &
echo "tracker runned"

for i in `seq 1 2`
do
   SERVER_NAME="miner-$i"
   nohup vagrant ssh $SERVER_NAME -c '/vagrant/deploy/scripts/runminer.sh' > logs/$SERVER_NAME.log &
   echo "$SERVER_NAME runned"
done

for i in `seq 1 5`
do
   SERVER_NAME="client-$i"
   nohup vagrant ssh $SERVER_NAME -c '/vagrant/deploy/scripts/runclient.sh' > logs/$SERVER_NAME.log &
   echo "$SERVER_NAME runned"
done