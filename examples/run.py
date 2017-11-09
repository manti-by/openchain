import os

role = os.getenv('ROLE')
if role in ['pool', 'miner', 'wallet']:
    os.system('python3 {}.py'.format(role))
else:
    print('OS env var ROLE not set')
    exit(-1)
