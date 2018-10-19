import os

role = os.getenv('ROLE')
if role in ['pool', 'generator', 'builder', 'wallet']:
    os.system('python {}.py'.format(role))
else:
    print('OS env var ROLE -{}- not set'.format(role))
    exit(-1)
