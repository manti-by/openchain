#!/usr/bin/env python
import io
import os

from setuptools import setup, find_packages

from openchain import __version__


def read(file_name):
    return io.open(os.path.join(os.path.dirname(__file__), file_name), encoding='utf-8').read()


exec(read('openchain/__init__.py'))

setup(
    name='openchain',
    version=__version__,
    description='Openchain Library',
    long_description=read('README.rst'),
    url='https://bitbucket.org/manti_by/openchain/',
    author='Alexander Chaika',
    author_email='manti.by@gmail.com',
    license='BSD',
    python_requires='>=3.6',
    packages=find_packages(exclude=['*.tests']),
    install_requires=[
        'ecdsa>=0.13,<0.14'
        'leveldb>=0.194,<0.195',
        'plyvel>=1.0.5,<1.1.0',
        'xxhash>=1.2.0,<1.3.0'
    ],
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='blockchain',
)
