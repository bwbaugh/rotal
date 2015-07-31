# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import setuptools

import rotal


setuptools.setup(
    name='rotal',
    version=rotal.__version__,
    description='Get a running count of occurrences from a stream.',
    long_description=open('README.rst').read(),
    author='Wesley Baugh',
    author_email='wesley@bwbaugh.com',
    url='https://github.com/bwbaugh/rotal',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'rotal = rotal.cli:main',
        ],
    },
)
