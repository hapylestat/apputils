# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2018 Reishin <hapy.lestat@gmail.com>


# spy notation sample:
#  http://docopt.org/
#  https://softwareengineering.stackexchange.com/questions/307467/what-are-good-habits-for-designing-command-line-arguments


class DefaultLanguage(object):
  """
   Arguments rule definition:
   { name, type, delimiter, value delimiter}
  """

  argument_types = {
    "long": "--",
    "short": "-",
    "default": None
  }

  value_delimiters = {
    "short": [" "],
    "long": ["=", " "],
    "default": []
  }


class AbstractTokenizer(object):

  @classmethod
  def language_definition(cls):
    raise NotImplementedError()

  @classmethod
  def tokenize(cls, obj):
    """
    :type obj object
    """
    raise NotImplementedError()

  @classmethod
  def make_iterable(cls, obj):
    """
    :type obj object
    """
    raise NotImplementedError()


class DefaultTokenizer(AbstractTokenizer):

  @classmethod
  def language_definition(cls):
    """
    :rtype DefaultLanguage
    """
    return DefaultLanguage

  @classmethod
  def tokenize(cls, obj):
    """
    Convert input data to tokens

    :type obj list|set|tuple
    """
    tokens = {}

    try:
      token_iterator = cls.make_iterable(obj)
      _lang = cls.language_definition()
      tokens = {k: [] for k in _lang.argument_types}

      prev, current = None, next(token_iterator)

      while True:
        token = [None, None]
        arg_type = None

        for arg_type in _lang.argument_types:
          arg_start_seq = _lang.argument_types[arg_type]
          arg_delimiters = _lang.value_delimiters[arg_type]

          if prev is None and arg_start_seq is None:  # just start to scan and got "default" token
            token[1] = current
            break
          elif arg_start_seq is None and prev[0] is None:  # next default token
            token[1] = current
            break
          elif arg_start_seq is None and prev[0] is not None:  # default token used after non-default tokens
            token[1] = current
            break
          elif arg_start_seq is None:  # value of non-default token
            prev[1] = current
            token = None
            break
          elif current[:len(arg_start_seq)] == arg_start_seq:
            token[0] = current[len(arg_start_seq):]

            for delimiter in arg_delimiters:
              if delimiter == " ":
                continue

              if delimiter in token[0]:
                _delim = str(token[0]).partition(delimiter)
                token = [_delim[0], _delim[2]]
                break
            break

        if token:
          tokens[arg_type].append(token)

        prev, current = token, next(token_iterator)
    except StopIteration:
      return tokens

  @classmethod
  def make_iterable(cls, obj):
    """
    :type obj list|set|tuple
    """
    try:
      return iter(list(obj))
    except TypeError:
      raise TypeError("Default tokenizer require iterable object to be passed")


class CommandLineAST(object):
  """
  Command line samples:

  app.py [default arguments
  """
  def __init__(self):
    self.__ast_tree = {}

  def parse(self, argv, tokenizer=DefaultTokenizer):
    """
    Parse command line to out tree

    :type argv object
    :type tokenizer AbstractTokenizer
    """
    args = tokenizer.tokenize(argv)
    _lang = tokenizer.language_definition()

    #
    # for param in self.__args:
    #   if self._is_default_arg(param):
    #     self.__out_tree[self.__default_arg_tag].append(param.strip())
    #   else:
    #     param = param.lstrip("-").partition('=')
    #     if len(param) == 3:
    #       self.__parse_one_param(param)
    pass


