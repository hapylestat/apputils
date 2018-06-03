# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2019 Reishin <hapy.lestat@gmail.com>

# How versioning works:
#
# Branches:
# master     - can produce only alpha versions with dev build number =>  __version__a.devN
# testing    - can produce beta builds and RC candidates (commit msg should contain [RC]) => __version__b|rc.devN
# production - produces release build => __version_.N

__version__ = "0.1.3"
