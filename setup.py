#!/usr/bin/python
"""Install the stravaupload script

Run

  python setup.py install

to install. Then you can run the script from everywhere by typing

  stravaupload.py

"""

from setuptools import setup

setup(name='StravaUpload',
      version='1.0',
      description='Upload files to Strava',
      author='Eirik Marthinsen',
      author_email='eirikma@gmail.com',
      url='https://github.com/marthinsen/stravaupload',
      scripts=['stravaupload.py'],
      install_requires=[
          'stravalib'
      ])
