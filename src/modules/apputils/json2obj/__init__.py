#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Github: https://github.com/hapylestat/apputils
#
#

from types import FunctionType, MethodType, BuiltinMethodType, UnionType
from typing import get_type_hints, get_args

import enum
import json

try:
  import yaml
  YAML_ENABLED: bool = True
except ImportError:
  YAML_ENABLED: bool = False


class SODumpType(enum.Enum):
  JSON = 1
  YAML = 2


class SerializableObject(object):
  """
   SerializableObject is a basic class, which providing Object to Dict, Dict to Object conversion with
   basic fields validation.

   For the example we have such dictionary:

   my_dict = {
     name: "Amy",
     age: 18
   }

   and we want to convert this to the object with populated object fields by key:value pairs from dict.
   For that we need to declare object view and describe there expected fields:

   class PersonView(SerializableObject):
     name: str = None
     age: int = None

    Instead of None, we can assign another values, they would be used as default if  data dict will not contain
     such fields.  Now it's time for conversion:

    person = PersonView(serialized_obj=my_dict)


    As second way to initialize view, view fields could be directly passed as constructor arguments:

    person = PersonView(name=name, age=16)

  """

  """
  Any error in de-serialization will trigger ValueError exception
  """
  __strict__: bool = True

  """
  Group an json key by the string.endswith pattern.

  Example JSON:
  {
    'a_url': 'xxxxxxx',
    'b_url': 'yyyyyyy'
  }

  Example class:
   class MyObject(SerializableObject):
     __grouping__ = {
      'uris' : '_url'
     }

  Resulting object:

  MyObject = {
    uris: {
     'a_url': 'xxxxxx',
     'b_url': 'yyyyyy'
    }
  }

  """
  __grouping__: dict = {}

  """
  Map json key to proper PyObject field name.

  For example:
   'a:b' -> 'a_b"

   class MyObject(SerializableObject):
     __mapping__ = {
       'existing_field': 'json_key',
       'a_b' : 'a:b'
     }
  """
  __mapping__: dict = {}


  """
    List of fields to be ignored from serialization/de-serialization
  """
  __ignored_fields__: list[str] = []

  """
  Saves input file type during the initial parsing, to output it in the same format
  """
  __file_type__: SODumpType = SODumpType.JSON

  def __init__(self, serialized_obj: str|dict|object|None = None, **kwargs):
    self.__error__ = []

    if isinstance(serialized_obj, type(self)):
      import copy
      self.__dict__ = copy.deepcopy(serialized_obj.__dict__)
      self.__annotations__ = copy.deepcopy(serialized_obj.__annotations__)
      return

    if isinstance(serialized_obj, str):
      try:
        serialized_obj = json.loads(serialized_obj)
        self.__file_type__ = SODumpType.JSON
      except json.JSONDecodeError:
        pass

    if YAML_ENABLED and isinstance(serialized_obj, str):
      try:
        serialized_obj = yaml.safe_load(serialized_obj)
        self.__file_type__ = SODumpType.YAML
      except yaml.YAMLError:
        pass

    assert serialized_obj is None or isinstance(serialized_obj, dict)

    if len(kwargs) > 0:
      if not serialized_obj:
        serialized_obj = {}
      serialized_obj.update(kwargs)

    if serialized_obj is None:
      return

    self.__deserialize(serialized_obj)

  def __handle_errors(self, clazz: type, d: dict, missing_definitions, missing_annotations):
    for miss_def in missing_definitions:
      v = d[miss_def]
      self.__error__.append(f"{clazz.__name__} class doesn't contain property '{miss_def}: {type(v).__name__}' (value sample:{v})")

    for miss_ann in missing_annotations:
      self.__error__.append(f"{clazz.__name__} class doesn't contain type annotation in the definition '{miss_ann}'")

    if not self.__error__:
      return

    end_line = "\n- "
    raise ValueError(f"""
A number of errors happen:
--------------------------
- {end_line.join(self.__error__)}
""")

  def __deserialize_transform(self, property_value, schema, supress_error: bool = False):
    is_typing_hint = (_type := getattr(schema, "__origin__", None)) is not None
    _type = _type if is_typing_hint else schema
    schema_args = list(get_args(schema)) if is_typing_hint or isinstance(schema, UnionType) else [] if _type is list else [schema]
    schema_len = len(schema_args)
    property_type = schema_args[0] if schema_args else None

    if property_type in (int, float, complex) and isinstance(property_value, str) and property_value == "":
      property_value = 0  # this is really weird fix for bad written API

    if property_type and property_value is not None \
      and not isinstance(property_value, _type) \
      and not isinstance(_type, UnionType) \
      and not (issubclass(_type, enum.Enum) and '_value2member_map_' in _type.__dict__) \
      and not (issubclass(property_type, SerializableObject) and isinstance(property_value, dict)):

      if not supress_error:
        self.__error__.append(
          "Conflicting type in schema and data for object '{}', expecting '{}' but got '{}' (value: {})".format(
            self.__class__.__name__,
            " | ".join([ t.__name__ for t in schema_args]) if isinstance(schema, UnionType) else property_type.__name__,
            type(property_value).__name__,
            property_value
          ))
      return None

    if property_value is None:
      return None
    elif not isinstance(_type, UnionType) and issubclass(_type, enum.Enum):
      if (_map := _type.__dict__['_value2member_map_']) and property_value in _map:
        return _map[property_value]
      self.__error__.append("Enum type '{}' doesn't contain option value '{}'".format(
        _type.__name__, property_value)
      )
      return None
    elif _type is list:
      return [property_type(i) for i in property_value] if property_type else property_value
    elif _type is dict:
      return {k: self.__deserialize_transform(v, schema_args[1] if schema_len == 2 else type(v)) for k, v in property_value.items()}
    elif isinstance(_type, UnionType):   # handle definitions like a: [int|str|MyObj] = 5
      for t in get_args(_type):
        if (__v := self.__deserialize_transform(property_value, t, supress_error=True)) is not None:
          return __v
      self.__error__.append("Cannot resolve Union type '{}' for value '{}'".format(_type, property_value))
      return None
    else:
      return _type(property_value) \
        if _type and property_value is not None and not isinstance(property_value, _type)\
        else property_value

  def __deserialize(self, d: dict):
    self.__error__ = []
    clazz: type = self.__class__
    exclude_types = (FunctionType, property, classmethod, staticmethod)
    properties = {
      k: v for k, v in clazz.__dict__.items()
      if not k.startswith("__")
      and k not in self.__ignored_fields__
      and not isinstance(v, exclude_types)
    }
    annotations = get_type_hints(clazz)

    for property_name, schema in annotations.items():
      if property_name.startswith("__") or property_name in self.__ignored_fields__:
        continue

      try:
        resolved_prop = self.__mapping__[property_name]
        # if mapped alias is not present but original is - use it
        assert not (property_name in d and resolved_prop not in d)
      except (KeyError, AssertionError):
        resolved_prop = property_name

      if resolved_prop not in d:  # Property didn't come with data, setting default value
        self.__setattr__(property_name, properties[property_name])
        continue

      property_value = d[resolved_prop]
      self.__setattr__(property_name, self.__deserialize_transform(property_value, schema))

    missing_definitions = set(d.keys()) - set(annotations.keys()) - set(self.__mapping__.values())
    if self.__grouping__:
      for definition, pattern in self.__grouping__.items():
        ret = {}
        for unknown_def in missing_definitions:
          if unknown_def.endswith(pattern):
            ret[unknown_def] = d[unknown_def]
        if ret:
          self.__setattr__(definition, ret)
          missing_definitions = set(missing_definitions) - set(ret.keys())

    if self.__strict__:
      missing_annotations = set(properties.keys()) - set(annotations.keys())
      self.__handle_errors(clazz, d, missing_definitions, missing_annotations)

  def __serialize_transform(self, item, minimal: bool = False):
    if item is None:
      return None
    elif isinstance(item, SerializableObject) or issubclass(type(item), SerializableObject):
      return item.serialize(minimal=minimal)
    elif isinstance(item, (list, tuple, set)):
      return [self.__serialize_transform(i, minimal=minimal) for i in item]
    elif issubclass(item.__class__, enum.Enum):
      return self.__serialize_transform(item.value, minimal=minimal)
    elif isinstance(item, dict):
      r_obj = {}
      for k, v in list(item.items()):
        if minimal and not v:
          continue
        r_obj[k] = self.__serialize_transform(v, minimal=minimal)
      return r_obj

    return item

  def serialize(self, minimal: bool = False) -> dict:
    all_properties = dict(self.__class__.__dict__)      # first of all we need to move defaults from class
    all_properties.update(dict(self.__dict__))          # now copy over existing properties from the object
    _filter_properties = list(self.__mapping__.keys()) + list(self.__grouping__.keys())

    properties: dict = {k: v for k, v in all_properties.items()
                        if not k.startswith("__")                                     # filter hidden properties
                        and not (k.startswith("_") and "__" in k)                     # filter _Obj__property entities
                        and k not in self.__ignored_fields__                          # filter ignored property
                        and not isinstance(v, (FunctionType, MethodType,
                                               BuiltinMethodType,
                                               property, classmethod))                # ignore functions
                        and k not in _filter_properties                               # exclude "special cases"
                        }

    if self.__mapping__:
      properties.update({a: all_properties[p] for p, a in self.__mapping__.items() if p in all_properties})

    if self.__grouping__:
      for k in self.__grouping__.keys():
        if k in all_properties and isinstance(all_properties[k], dict):
          properties.update(all_properties[k])

    return self.__serialize_transform(properties, minimal=minimal)

  def dump(self, indent: int = None, _type: SODumpType = None, minimal: bool = False):
    if _type is None:
      _type = self.__file_type__

    if _type == SODumpType.YAML:
      if not YAML_ENABLED:
        raise RuntimeError("PyYaml is not installed and it is required for YAML rendering")
      return yaml.safe_dump(self.serialize(minimal), indent=indent)
    else:
      return json.dumps(self.serialize(minimal), indent=indent)

  def to_json(self, indent: int = None, minimal: bool = False) -> str:
    return self.dump(indent, _type=self.__file_type__, minimal=minimal)
