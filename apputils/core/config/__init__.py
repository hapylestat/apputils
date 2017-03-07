# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

from apputils.core.config.ast import CommandLineAST
from apputils.core.config.main import Configuration


__all__ = ["CommandLineAST", "Configuration"]


class ModuleHelpItem(object):
  def __init__(self, argument, cmd_help, is_default=False):
    """
    :type argument str
    :type cmd_help str
    :type is_default bool
    """
    self.__argument = argument
    self.__cmd_help = cmd_help
    self.__is_default = is_default

  @property
  def argument(self):
    """
    :rtype str
    """
    return self.__argument

  @property
  def cmd_help(self):
    """

    :rtype str
    """
    return self.__cmd_help

  @property
  def is_default(self):
    """
    :rtype bool
    """
    return self.is_default

  def __str__(self):
    return "{} - {}".format(self.__argument, self.__cmd_help)

  def __repr__(self):
    return self.__str__()


class ModuleHelpBuilder(object):
  def __init__(self, name):
    """
    :type name str
    """
    self.__name = name
    self.__arguments = []

  def add_argument(self, argument_name, argument_help, is_default=False):
    """
    :type argument_name str
    :type argument_help str
    :type is_default bool
    :rtype ModuleHelpBuilder
    """
    self.__arguments.append(ModuleHelpItem(argument_name, argument_help, is_default=is_default))
    return self

  def __str__(self):
    import os
    return os.linesep.join(self.__arguments)

  def __repr__(self):
    return self.__str__()


class CommandRouter(object):
  def __init__(self, path):
    import os
    self.__path = os.path.dirname(os.path.abspath(path))

  def route(self):
    pass
