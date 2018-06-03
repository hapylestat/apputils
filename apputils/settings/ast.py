# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

import logging


class CommandLineAST(object):
  def __init__(self, args, out_tree):
    """
    :arg args List of arguments to parse
    :arg out_tree Hash map tree, already initialized at least with root element

    :type out_tree dict
    :type args list
    """
    self.__default_arg_tag = "default"
    self._log = logging.Logger(CommandLineAST.__class__.__name__)
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
      raise TypeError("Invalid assignment to {0}".format(key))

    if key in node and isinstance(node[key], dict) and not isinstance(value, dict):
      raise TypeError("Invalid assignment to {0}".format(key))

    node[key] = value

  def __parse_one_param(self, param):
    """
    :argument param tuple which represents arg name, delimiter, arg value
    :type param tuple
    """
    keys = param[0].split('.')
    if len(keys) == 1:  # parse root element
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
          break
    else:
      raise TypeError("Couldn't recognise parameter \'{}\'".format(param[0]))
