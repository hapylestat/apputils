from abc import abstractmethod, ABCMeta
from enum import Enum
from datetime import datetime
from types import UnionType
from typing import Callable, Any, Generator, Union



class TransformationItem(object):
  def __init__(self,
               serialize_condition: Callable[[object], bool],
               deserialize_condition: Callable[[type, object], bool],
               serialize: Callable[[object], object],
               deserialize: Callable[[type, object], object],
               is_serialize_chain: Callable[[], bool],
               is_deserialize_chain: Callable[[], bool]
               ):

    self.serialize_condition = serialize_condition
    self.deserialize_condition = deserialize_condition
    self.serialize = serialize
    self.deserialize = deserialize
    self.is_serialize_chain = is_serialize_chain
    self.is_deserialize_chain = is_deserialize_chain



class TransformationItemAbstract(TransformationItem, metaclass=ABCMeta):
  def __init__(self):
    super().__init__(self.serialize_condition,
                     self.deserialize_condition,
                     self.serialize,
                     self.deserialize,
                     self.is_serialize_chain,
                     self.is_deserialize_chain
                     )

  @abstractmethod
  def serialize_condition(self, obj: object) -> bool:
    raise NotImplementedError()

  @abstractmethod
  def deserialize_condition(self, expected_type: type, obj: object) -> bool:
    raise NotImplementedError()

  @abstractmethod
  def serialize(self, obj: object) -> object:
    raise NotImplementedError()

  @abstractmethod
  def deserialize(self, expected_type: type, obj: object) -> object:
    raise NotImplementedError()

  @abstractmethod
  def is_serialize_chain(self) -> bool:
    raise NotImplementedError()

  @abstractmethod
  def is_deserialize_chain(self) -> bool:
    raise NotImplementedError()



class TransformationsRegistry(object):
  def __init__(self):
    self._transformations: list[TransformationItem] = []

  def register_transformation(self, transformation: TransformationItem) -> None:
    self._transformations.append(transformation)

  @property
  def items(self) -> Generator[TransformationItem, Any, None]:
    for transformation in self._transformations:
      yield transformation

  def serialize(self, obj: object) -> object | None:
    for transformation in self._transformations:
      if transformation.serialize_condition(obj):
        return transformation.serialize(obj)
    return None

  def deserialize(self, expected_type: type, obj: object) -> object | None:
    for transformation in self._transformations:
      if transformation.deserialize_condition(expected_type, obj):
        return transformation.deserialize(expected_type, obj)
    return None

  def need_chain_serialize(self, obj: object) -> bool:
    for transformation in self._transformations:
      if transformation.serialize_condition(obj):
        return transformation.is_serialize_chain()
    return False

  def need_chain_deserialize(self, expected_type: type, obj: object) -> bool:
    for transformation in self._transformations:
      if transformation.deserialize_condition(expected_type, obj):
        return transformation.is_deserialize_chain()
    return False



# ===========================================
#          Transformation Abstracts
# ===========================================


class DateTimeTransformation(TransformationItemAbstract):
  """
  Adds support for datetime serialization/deserialization
  """
  def serialize_condition(self, obj: datetime) -> bool:
    return isinstance(obj, datetime)

  def deserialize_condition(self, expected_type: type, obj: object) -> bool:
    return expected_type is datetime and isinstance(obj, float)

  def serialize(self, obj: datetime) -> object:
    return obj.timestamp()

  def deserialize(self, expected_type, obj: float) -> object:
    return datetime.fromtimestamp(obj)

  def is_serialize_chain(self) -> bool:
    return False

  def is_deserialize_chain(self) -> bool:
    return False


class StringNumberTransformation(TransformationItemAbstract):
  """
  Adds support for number serialization/deserialization from strings
  """
  def serialize_condition(self, obj: object) -> bool:
    return False

  def deserialize_condition(self, expected_type: type, obj: object) -> bool:
    return expected_type in (int, float, complex) and isinstance(obj, str)

  def serialize(self, obj: object) -> object:
    return obj

  def deserialize(self, expected_type: type, obj: object) -> object:
    if isinstance(obj, str) and obj == "":
      return expected_type(0)
    return expected_type(obj)

  def is_serialize_chain(self) -> bool:
    return False

  def is_deserialize_chain(self) -> bool:
    return False


class EnumTransformation(TransformationItemAbstract):
  """
  Adds support for Enum serialization/deserialization
  """
  def serialize_condition(self, obj: object) -> bool:
    return issubclass(obj.__class__, Enum)

  def deserialize_condition(self, expected_type: type, obj: object) -> bool:
    return not isinstance(expected_type, UnionType) and issubclass(expected_type, Enum)\
      and '_value2member_map_' in expected_type.__dict__

  def serialize(self, obj: Enum) -> object:
    return obj.value

  def deserialize(self, expected_type: type, obj: object) -> object|None:
    if (_map := expected_type.__dict__['_value2member_map_']) and obj in _map:
      return _map[obj]
    raise ValueError("Enum type '{}' doesn't contain option value '{}'".format(expected_type.__name__, obj))

  def is_serialize_chain(self) -> bool:
    return True

  def is_deserialize_chain(self) -> bool:
    return False



transformations = TransformationsRegistry()

transformations.register_transformation(DateTimeTransformation())
transformations.register_transformation(StringNumberTransformation())
transformations.register_transformation(EnumTransformation())
