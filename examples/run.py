import os

role = os.getenv('ROLE')
if role == 'pool':
    os.system('python filename.py')
elif role == 'miner':
    os.system('python filename.py')
elif role == 'wallet':
    os.system('python wallet.py')
else:
    print('OS env var ROLE not set')
    exit(-1)
