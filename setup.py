#!/usr/bin/env python
import io
import os

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages

from openchain import __version__

install_requirements = parse_requirements('requirements.txt', session=PipSession())
requirements = [str(ir.req) for ir in install_requirements]


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
    python_requires='>=3.5',
    packages=find_packages(exclude=['*.tests']),
    install_requires=requirements,
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='blockchain',
)
