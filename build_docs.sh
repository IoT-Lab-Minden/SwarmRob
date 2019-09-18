#! /bin/bash
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
sudo python3 -m pip install sphinx
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/swarmrob/docs
/usr/local/bin/sphinx-apidoc -f -o source/ $DIR/swarmrob
/usr/local/bin/sphinx-build source/ docs/
rm -r $DIR/docs
cp -a $DIR/swarmrob/docs/docs $DIR
rm -r $DIR/swarmrob/docs/docs
