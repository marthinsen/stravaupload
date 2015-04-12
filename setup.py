#!/usr/bin/python
"""Install the stravaupload script

Run

  python setup.py install

to install. Then you can run the script from everywhere by typing

  stravaupload.py

"""

import sys
from distutils.core import setup
from imp import find_module

try:
    find_module('stravalib')
except ImportError:
    print 'The package stravalib is required to install this script'
    sys.exit()

setup(name='StravaUpload',
      version='1.0',
      description='Upload tcs files to Strava',
      author='Eirik Marthinsen',
      author_email='eirikma@gmail.com',
      url='https://github.com/marthinsen/stravaupload',
      scripts=['stravaupload.py'])
