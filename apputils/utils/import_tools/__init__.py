# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2017 Reishin <hapy.lestat@gmail.com>

import sys
from apputils.utils.import_tools.generic import ArgumentException, ModuleArgumentItem, NoCommandException
from apputils.utils.import_tools.import_tools import ModuleMetaInfo, ModuleArgumentsBuilder

if sys.version_info >= (3, 4):
  from apputils.utils.import_tools.import_tools3k import ModulesDiscovery3k as ModulesDiscovery
else:
  from apputils.utils.import_tools.import_tools import ModulesDiscovery


__all__ = ["ArgumentException", "ModuleArgumentItem", "NoCommandException", "ModulesDiscovery", "ModuleMetaInfo",
           "ModuleArgumentsBuilder"]
