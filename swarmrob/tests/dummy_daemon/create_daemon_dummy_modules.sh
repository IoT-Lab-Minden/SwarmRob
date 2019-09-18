#!/bin/bash
# Copyright 2018,2019 Aljoscha Pörtner
# Copyright 2019 André Kirsch

# This file is part of SwarmRob.

# SwarmRob is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SwarmRob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SwarmRob.  If not, see <https://www.gnu.org/licenses/>.
for fn in `cat daemon_dummy_modules.txt`; do
    echo "Copy module $fn"
    sudo rm -R daemon_dummy/$fn
    sudo cp -a ../../swarmrob/$fn daemon_dummy/$fn
done
