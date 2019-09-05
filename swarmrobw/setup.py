#!/usr/bin/env python
import os
from setuptools import setup

setup(
    name = "Swarmrob-Worker",
    version = "0.1",
    author = "Aljoscha Poertner",
    author_email = "aljoscha.poertner@fh-bielefeld.de",
    description = "An Orchestration Tool for Container-based Robot Applications",
    license = "BSD",
    url = "https://github.com/aljoschap/swarmrob",
    packages=['swarmrob', 'swarmengine','dockerengine','logger','utils'],
    entry_points = {
        'console_scripts' : ['swarmrob-worker = swarmrob.swarmrob:main']
    },
    data_files = [
    ('/swarmrob',['scripts/swarmrob.conf']),
    ],
    classifiers=[
        "License :: OSI Approved :: GPL v3 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ],
    dependency_links=[
        'https://pypi.python.org/simple/'
    ]
)
