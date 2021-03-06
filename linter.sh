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
rm -R lint
mkdir -p lint
find swarmrob -name '*.py' | xargs -I{} sh -c 'mkdir -p lint/$(dirname $1); pylint $1 --py3k > "lint/$1.lint"' -- {}
