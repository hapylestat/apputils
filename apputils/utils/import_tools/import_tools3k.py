# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2017 Reishin <hapy.lestat@gmail.com>

from apputils.utils.import_tools.generic import NoCommandException, ArgumentException
from apputils.utils.import_tools.import_tools import ModulesDiscovery


__all__ = ["ModulesDiscovery3k"]


class ModulesDiscovery3k(ModulesDiscovery):
  import asyncio

  @asyncio.coroutine
  def execute_command_async(self, default_arg_list=None, **kwargs):
    """
    :type default_arg_list list
    :type kwargs dict
    """
    _custom_func_arguments = set()

    if default_arg_list is None or len(default_arg_list) == 0:
      raise NoCommandException("No command passed, unable to continue")

    command_name = default_arg_list.pop(0)
    if command_name not in self._modules.keys():
      raise NoCommandException("No such command '{}' found, unable to continue".format(command_name))

    command = self._modules[command_name]
    entry_point = command["entry_point"]
    class_path = command["classpath"]
    metainfo = command["metainfo"]
    """:type metainfo ModuleMetaInfo"""

    try:
      args = metainfo.parse_default_arguments(default_arg_list)
      args.update(metainfo.parse_arguments(kwargs))

      f_args = entry_point.__code__.co_varnames[:entry_point.__code__.co_argcount]

      if len(f_args) - len(set(f_args) & _custom_func_arguments) != len(set(args.keys()) & set(f_args)):
        raise ArgumentException("Function \"{}\" from module {} doesn't implement all arguments in the signature".format(
          entry_point.__name__, class_path
        ))

      yield from entry_point(**args)
    except ArgumentException as e:
      raise NoCommandException("Application arguments exception: {}\n".format(str(e)))
