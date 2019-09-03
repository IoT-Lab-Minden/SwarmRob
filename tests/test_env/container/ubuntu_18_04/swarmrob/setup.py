#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018,2019 Aljoscha Pörtner
# Copyright 2019 André Kirsch
# This file is part of SwarmRob.
#
# SwarmRob is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SwarmRob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SwarmRob.  If not, see <https://www.gnu.org/licenses/>.

import os

from setuptools import setup

setup(
    name="Swarmrob-Full",
    version="0.1.1",
    author="Aljoscha Poertner",
    author_email="aljoscha.poertner@fh-bielefeld.de",
    description="An Orchestration Tool for Container-based Robot Applications",
    license="GPL v3",
    url="https://github.com/aljoschap/swarmrob",
    packages=['swarmrob', 'swarmengine', 'services', 'dockerengine', 'logger', 'gortools',
              'utils', 'costs'],
    entry_points={
        'console_scripts': ['swarmrob = swarmrob.swarmrob:main']
    },
    scripts=['scripts/start_swarmrob_nameservice.sh'],
    data_files=[
        ('/swarmrob/scripts', ['scripts/start_swarmrob_nameservice.sh']),
        ('/swarmrob/', ['requirements.txt'])
        # ('/usr/lib/systemd/system', ['scripts/swarmrobd.service','scripts/swarmrobns.service']),
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
