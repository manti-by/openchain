#!/bin/bash
nohup vagrant ssh blockchain-tracker -c '/vagrant/deploy/scripts/runtracker.sh' > logs/blockchain-tracker.log &
echo "blockchain-tracker runned"

for i in `seq 1 5`
do
   SERVER_NAME="blockchain-client-$i"
   nohup vagrant ssh $SERVER_NAME -c '/vagrant/deploy/scripts/runclient.sh' > logs/$SERVER_NAME.log &
   echo "$SERVER_NAME runned"
done