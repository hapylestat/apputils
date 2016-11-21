# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2016 Reishin <hapy.lestat@gmail.com>

import types


class ConfigObject(object):
  def __init__(self, serialized_obj=None, **kwargs):
    """
    :type tree dict
    """
    if len(kwargs) > 0:
      self._handle_initialization(kwargs)
    else:
      self._handle_deserialization(serialized_obj)

  def _handle_initialization(self, kwargs):
    props = dir(self)
    for item in kwargs:
      if item not in props:
        continue
      self.__setattr__(item, kwargs[item])

  def _handle_deserialization(self, serialized_obj=None):
    if serialized_obj is not None:
      if self.__class__ is serialized_obj.__class__:
        self.__dict__ = serialized_obj.__dict__
      else:
        self.deserialize(serialized_obj)
        self.clean()

  def __isclass(self, obj):
    try:
      issubclass(obj, object)
    except TypeError:
      return False
    else:
      return True

  def clean(self):
    """
    Replace not de-serialized types with none
    :return:
    """
    for item in dir(self):
      attr = self.__getattribute__(item)
      if item[:2] != "__" and self.__isclass(attr) and issubclass(attr, ConfigObject):
        self.__setattr__(item, None)
      elif item[:2] != "__" and isinstance(attr, list) and len(attr) == 1 and \
        self.__isclass(attr[0]) and issubclass(attr[0], ConfigObject):
        self.__setattr__(item, [])

  def deserialize(self, d):
    """
    :type d dict
    """
    if isinstance(d, dict):
      for k, v in d.items():
        if k not in self.__class__.__dict__:
          raise RuntimeError(self.__class__.__name__ + " doesn't contain property " + k)
        attr_type = self.__class__.__dict__[k]
        if isinstance(attr_type, list) and len(attr_type) > 0 and issubclass(attr_type[0], ConfigObject):
          obj_list = []
          if isinstance(v, list):
            for vItem in v:
              obj_list.append(attr_type[0](vItem))
          else:
            obj_list.append(attr_type[0](v))
          self.__setattr__(k, obj_list)
        elif self.__isclass(attr_type) and issubclass(attr_type, ConfigObject):
          self.__setattr__(k, attr_type(v))
        else:
          self.__setattr__(k, v)

  def serialize(self):
    """
    :rtype: dict
    """
    ret = {}

    # first of all we need to move defaults from class
    properties = dict(self.__class__.__dict__)
    properties.update(dict(self.__dict__))

    properties = {k: v for k, v in properties.items() if k[:1] != "_"}

    for k, v in properties.items():
      if v is not None:
        if isinstance(v, list) and len(v) > 0:
          v_result = []
          for v_item in v:
            if issubclass(v_item.__class__, ConfigObject):
              v_result.append(v_item.serialize())
            elif issubclass(v_item, ConfigObject):
              v_result.append(v_item().serialize())
            else:
              v_result.append(v_item)
          ret[k] = v_result
        elif issubclass(v.__class__, ConfigObject):  # here we have instance of an class
          ret[k] = v.serialize()
        elif self.__isclass(v) and issubclass(v, ConfigObject):  # here is an class itself
          ret[k] = v().serialize()
        else:
          ret[k] = v

    return ret
