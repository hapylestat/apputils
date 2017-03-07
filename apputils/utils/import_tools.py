# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

import os
import sys
from collections import OrderedDict

from apputils.core.config.main import Configuration


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


class ModuleArgumentsBuilder(object):
  def __init__(self):
    self._args = {}
    self._default_args = []
    self.__restricted_default_types = [int, str, float, list]
    self.__restricted_types = self.__restricted_default_types + [bool]
    self.__is_default_arg_flag_used = False

  def add_argument(self, name, value_type, item_help, default=None):
    """
    :type name str
    :type value_type Type
    :type item_help str
    :type default Type
    :rtype ModuleArgumentsBuilder
    """
    if value_type and value_type not in self.__restricted_types:
      raise ArgumentException("Named argument couldn't have {} type".format(value_type.__name__))

    if default is not None and not isinstance(default, value_type):
      raise ArgumentException("Invalid default type for argument".format(name))

    if value_type is bool and default is None:
      default = False

    self._args.update({
      name: ModuleArgumentItem(name, value_type, item_help, default)
    })
    return self

  @property
  def arguments(self):
    """
    :rtype dict
    """
    return self._args

  @property
  def default_arguments(self):
    """
    :rtype dict
    :rtype dict
    """
    d = OrderedDict()

    for arg in self._default_args:
      d.update({arg.name: arg})

    return d

  def add_default_argument(self, name, value_type, item_help, default=None):
    """
    :type name str
    :type value_type Type
    :type item_help str
    :type default Type
    :rtype ModuleArgumentsBuilder
    """
    if value_type not in self.__restricted_default_types:
      raise ArgumentException("Positional(default) argument couldn't have {} type".format(value_type.__name__))

    if self.__is_default_arg_flag_used and default is None:
      raise ArgumentException("After defining first default Positional argument, rest should have default value too".format(value_type.__name__))
    elif default is not None:
      self.__is_default_arg_flag_used = True

      if not isinstance(default, value_type):
        raise ArgumentException("Invalid default type for argument".format(name))

    self._default_args.append(ModuleArgumentItem(name, value_type, item_help, default=default))
    return self

  @property
  def has_optional_default_argument(self):
    return self.__is_default_arg_flag_used

  def get_default_argument(self, index):
    """
    :type index int

    :rtype ModuleArgumentItem
    """
    return self._default_args[index]


class ModuleMetaInfo(object):
  def __init__(self, name, item_help="", **kwargs):
    """
    :type name str
    :type kwargs dict
    """
    self._name = name
    self._arguments = ModuleArgumentsBuilder()
    self._help = item_help
    self._kwargs = kwargs

  @property
  def options(self):
    return self._kwargs

  @property
  def name(self):
    return self._name

  @property
  def help(self):
    return self._help

  def get_arguments_builder(self):
    """
    :rtype ModuleArgumentsBuilder
    """
    return self._arguments

  def __convert_value_to_type(self, value, _type):
    if _type is list and isinstance(value, str):
      return value.split(",")
    elif _type is bool and len(value) == 0:
      return True
    else:
      return _type(value)

  def parse_default_arguments(self, default_args_sample):
    """
    :type default_args_sample list
    :rtype dict
    """
    parsed_arguments_dict = {}
    default_arguments = list(self._arguments.default_arguments.values())
    expected_length = len(default_arguments)
    real_length = len(default_args_sample)

    default_args_count = len([item for item in default_arguments if item.default is not None])

    if not self._arguments.has_optional_default_argument and (default_args_sample is None or expected_length != real_length):
      raise ArgumentException("Command require {} positional argument(s), found {}".format(
        expected_length,
        real_length
      ))
    elif self._arguments.has_optional_default_argument and default_args_sample is not None and real_length < expected_length - default_args_count:
      raise ArgumentException("Command require {} or {} positional argument(s), found {}".format(
        expected_length,
        expected_length - default_args_count,
        real_length
      ))

    for index in range(0, expected_length):
      arg_meta = default_arguments[index]
      """:type arg_meta ModuleArgumentItem"""
      try:
        arg = default_args_sample[index]
      except IndexError:
        arg = arg_meta.default

      try:
        if arg_meta.value_type is not None:
          arg = self.__convert_value_to_type(arg, arg_meta.value_type)

        parsed_arguments_dict[arg_meta.name] = arg
      except (TypeError, ValueError):
        raise ArgumentException("Invalid argument type - expected {}, got {}".format(arg_meta.value_type.__name__, type(arg).__name__))

    return parsed_arguments_dict

  def parse_arguments(self, conf):
    """
    :type conf Configuration|dict
    """
    parsed_arguments_dict = {}
    arguments = self._arguments.arguments

    for arg_name in arguments:
      arg_meta = arguments[arg_name]
      """:type arg_meta ModuleArgumentItem"""
      try:
        if arg_meta.value_type is not None:
          arg = self.__convert_value_to_type(conf.get(arg_name), arg_meta.value_type)
        else:
          arg = conf.get(arg_name)
      except KeyError:
        if arg_meta.default is None:
          raise ArgumentException("Command require \"{}\" argument to be set".format(arg_name))

        # ToDo: check default value passed from user?
        arg = arg_meta.default

      parsed_arguments_dict[arg_name] = arg
    return parsed_arguments_dict


class ModulesDiscovery(object):
  def __init__(self, discovery_location_path, module_class_path, file_pattern="_command", module_main_fname="__init__"):
    """
    :type discovery_location_path str
    :type module_class_path str
    :type file_pattern str|None
    :type module_main_fname str
    """

    self._discovery_location_path = discovery_location_path
    self._module_main_fname = module_main_fname

    self._file_pattern = file_pattern
    if self._file_pattern == "":
      self._file_pattern = None

    if os.path.isfile(self._discovery_location_path):
      self._search_dir = os.path.dirname(os.path.abspath(self._discovery_location_path))
    else:
      self._search_dir = self._discovery_location_path

    self._module_class_path = module_class_path
    self._modules = {}

  @property
  def search_dir(self):
    """
    :rtype str
    """
    return self._search_dir

  def collect(self):
    modules = []
    exclude_list = ["pyc", "__init__.py", "__pycache__"]
    required_module_fields = {"__args__", "__module__", self._module_main_fname}

    for name in os.listdir(self._search_dir):
      if name not in exclude_list:
        module = name.split(".")[0]
        if self._file_pattern and self._file_pattern in name:
          modules.append(module)
        elif self._file_pattern is None:
          modules.append(module)

    modules = set(modules)

    for module in modules:
      m = __import__("{0}.{1}".format(self._module_class_path, module)).__dict__[module]
      m_dict = m.__dict__
      metainfo = m_dict["__module__"]
      if not isinstance(metainfo, ModuleMetaInfo):
        continue

      if len(required_module_fields) == len(required_module_fields & set(m_dict.keys())):
        self._modules.update({
          metainfo.name: {
            "entry_point": m_dict[self._module_main_fname],
            "metainfo": metainfo,
            "classpath": m.__name__
          }
        })

  def generate_help(self, filename="", command=""):
    """
    :type command str
    """
    "{} [{}]\n\n".format(filename, "|".join(self.available_command_list))
    help_str = """Available commands:

    """

    command_list = self.available_command_list if command == "" else [command]

    for command in command_list:
      cmd_meta = self.get_command_metainfo(command)
      """:type cmd_meta ModuleMetaInfo"""

      if cmd_meta is None:
        continue

      args = {}
      args.update(cmd_meta.get_arguments_builder().arguments)
      args.update(cmd_meta.get_arguments_builder().default_arguments)

      cmd_arguments_help = {name: value.item_help for name, value in args.items() if value.item_help}

      if len(cmd_arguments_help) > 0:
        help_str += """
        {cmd} [{args}] - {cmd_help}

        Argument details:
        {arg_details}


        """.format(
          cmd=command,
          args=" | ".join(cmd_arguments_help.keys()),
          cmd_help = cmd_meta.help,
          arg_details="\n".join(["{} - {}".format(k, v) for k, v in cmd_arguments_help.items()])
        )

      else:
        help_str += """
        {cmd} - {cmd_help}""".format(
          cmd=command,
          cmd_help=cmd_meta.help
        )

    return help_str

  @property
  def available_command_list(self):
    return list(self._modules.keys())

  def get_command_metainfo(self, command):
    """
    :type command str
    :rtype ModuleMetaInfo
    """
    if command not in self._modules:
      return None

    return self._modules[command]["metainfo"]

  def execute_command(self, default_arg_list=None, **kwargs):
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

      entry_point(**args)
    except ArgumentException as e:
      raise NoCommandException("Application arguments exception: {}\n".format(str(e)))

  if sys.version_info >= (3, 4):
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

  def main(self, configuration):
    """
    :type configuration Configuration
    """
    _custom_func_arguments = {"conf"}
    filename = os.path.basename(os.path.abspath(sys.argv[0]))

    default_arg_list = [item for item in configuration.get("default") if len(item.strip()) != 0]
    if len(default_arg_list) == 0:
      sys.stdout.write(self.generate_help(filename=filename))
      return

    command_name = default_arg_list.pop(0)
    if command_name not in self._modules.keys():
      sys.stdout.write(self.generate_help(filename=filename))
      return

    command = self._modules[command_name]
    entry_point = command["entry_point"]
    class_path = command["classpath"]
    metainfo = command["metainfo"]
    """:type metainfo ModuleMetaInfo"""

    try:
      args = metainfo.parse_default_arguments(default_arg_list)
      args.update(metainfo.parse_arguments(configuration))

      f_args = entry_point.__code__.co_varnames[:entry_point.__code__.co_argcount]

      if len(f_args) - len(set(f_args) & _custom_func_arguments) != len(set(args.keys()) & set(f_args)):
        raise ArgumentException("Function \"{}\" from module {} doesn't implement all arguments in the signature".format(
          entry_point.__name__, class_path
        ))

      if "conf" in f_args:
        args["conf"] = configuration

      entry_point(**args)
    except ArgumentException as e:
      sys.stdout.write("Application arguments exception: {}\n".format(str(e)))
      return


