#!/usr/bin/env python
import io
import os

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages

from .open_blockchain.version import __version__

install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]


def read(fname):
    return io.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


# __version__ variable is read from here. Package can't be imported on execution.
# exec(read('open_blockchain/_version.py'))

setup(
    name='open_blockchain',
    version=__version__,
    description='Open Blockchain Library',
    long_description=read('README.md'),
    author='Alex Manti',
    author_email='manti.by@gmail.com',
    packages=find_packages(exclude=['*.tests']),
    install_requires=reqs,
)
