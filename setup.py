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
    packages=setuptools.find_packages(exclude=['tests*']),
)
