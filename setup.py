#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)
    config.add_subpackage('pyFIR')
    return config

def main():
    from numpy.distutils.core import setup
    setup(name='pyfir',
          version='0.1',
          description='Simple tool to do FIR analysis on fMRI data',
          author='Gilles de Hollander',
          author_email='gilles.de.hollander@gmail.com',
          url='http://www.gillesdehollander.nl',
          packages=['pyFIR'],
          configuration=configuration
         )

if __name__ == '__main__':
    main()
