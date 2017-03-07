# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

from apputils.core.logger import aLogger


class CommandLineAST(object):
  def __init__(self, args, out_tree):
    """
    :arg args List of arguments to parse
    :arg out_tree Hash map tree, already initialized at least with root element

    :type out_tree dict
    :type args list
    """
    self.__default_arg_tag = "default"
    self._log = aLogger.getLogger(self.__class__.__name__, default_level=aLogger.Level.error)
    self.__args = list(args)
    self.__out_tree = out_tree

  def parse(self):
    """
    Parse command line to out tree
    """
    if self.__out_tree is None:
      raise RuntimeError("Could'n use empty out tree as ast storage")

    if isinstance(self.__out_tree, dict):
      self.__out_tree[self.__default_arg_tag] = []

    if len(self.__args) >= 1:
      self.__args.pop(0)
      self._log.info("Passed commandline arguments: %s", self.__args)

    for param in self.__args:
      if self._is_default_arg(param):
        self.__out_tree[self.__default_arg_tag].append(param.strip())
      else:
        param = param.lstrip("-").partition('=')
        if len(param) == 3:
          self.__parse_one_param(param)

  def _is_default_arg(self, param):
    """
    Check if passed arg belongs to default type
    :type param str
    :rtype bool
    """
    param = param.strip()
    restricted_symbols = ["=", "-"]
    for symbol in restricted_symbols:
      if symbol in param[:1]:
        return False

    return True

  def __set_node(self, node, key, value):
    if not isinstance(node, dict):
      self._log.error("Invalid assignment to {0}", key)
      return

    if key in node and isinstance(node[key], dict) and not isinstance(value, dict):
      self._log.error("Invalid assignment to {0}", key)
      return

    node[key] = value

  def __parse_one_param(self, param):
    """
    :argument param tuple which represents arg name, delimiter, arg value
    :type param tuple
    """
    self._log.debug("Parse param \'%s\' with value \'%s\'", param[0], param[2])
    keys = param[0].split('.')
    if len(keys) == 1:  # parse root element
      self._log.debug("Replacing param \'%s\' to value \'%s\'", keys[0], param[2])
      self.__set_node(self.__out_tree, keys[0], param[2])
    elif len(keys) > 0:
      item = self.__out_tree
      for i in range(0, len(keys)):
        key = keys[i]
        is_last_key = i == len(keys) - 1
        if key not in item:
          self.__set_node(item, key, "" if is_last_key else {})

        if is_last_key and key in item and not isinstance(item[key], dict):
          self.__set_node(item, key, param[2])
        elif key in item and isinstance(item, dict):
          item = item[key]
        else:
          self._log.error("Couldn't recognise parameter \'%s\'", param[0])
          break
    else:
      self._log.error("Couldn't recognise parameter \'%s\'", param[0])
