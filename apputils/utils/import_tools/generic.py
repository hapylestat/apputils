# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2017 Reishin <hapy.lestat@gmail.com>


class ArgumentException(Exception):
  pass


class NoCommandException(Exception):
  pass


class ModuleArgumentItem(object):
  name = None
  value_type = None
  item_help = None
  default = None

  def __init__(self, name, value_type, item_help, default=None):
    """
    :type name str
    :type value_type Type
    :type item_help str
    :type default Type
    """
    self.name = name
    self.value_type = value_type
    self.item_help = item_help
    self.default = default
