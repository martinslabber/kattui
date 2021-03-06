#!/usr/bin/env python

from setuptools import setup, find_packages

from katversion import get_version

setup(name="kattui",
      version=get_version(),
      description="Karoo Array Telescope Text User Interface",
      packages=find_packages(),
      scripts=["scripts/kat"],
      url='https://github.com/martinslabber/kattui',
      license="BSD",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2",
                   "Topic :: Scientific/Engineering :: Astronomy"],
      platforms=["OS Independent"],
      install_requires=['cmd2',
                        # 'katcp',  # Enabling this here causes problems with
                        # various versions of katcp.
                        ],
      keywords="kat kat7 ska MeerKAT",
      data_files=[('/usr/local/lib/kattui', ['plugins/stop.py']),
                  ('/usr/local/lib/kattui', ['plugins/start.py']), ],
      test_suite="nose.collector")
