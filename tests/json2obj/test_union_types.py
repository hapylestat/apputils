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
import unittest
from typing import Optional, Union

from apputils.json2obj import SerializableObject


# --- Models using native X | Y syntax (Python 3.10+) ---

class NativeUnionSimple(SerializableObject):
  value: str | int = None


class NativeUnionThree(SerializableObject):
  value: str | int | float = None


class NativeUnionOptional(SerializableObject):
  value: str | None = None


# --- Models using typing.Union / typing.Optional ---

class TypingUnionSimple(SerializableObject):
  value: Union[str, int] = None


class TypingUnionThree(SerializableObject):
  value: Union[str, int, float] = None


class TypingUnionOptional(SerializableObject):
  value: Optional[str] = None


# --- Model mixing both in the same class ---

class MixedUnions(SerializableObject):
  native: str | int = None
  typed: Union[str, float] = None


class TestNativeUnionType(unittest.TestCase):
  """Tests for X | Y syntax (types.UnionType, Python 3.10+)."""

  def test_receives_first_type(self):
    obj = NativeUnionSimple('{"value": "hello"}')
    self.assertEqual(obj.value, "hello")
    self.assertIsInstance(obj.value, str)

  def test_receives_second_type(self):
    obj = NativeUnionSimple('{"value": 42}')
    self.assertEqual(obj.value, 42)
    self.assertIsInstance(obj.value, int)

  def test_three_types_str(self):
    obj = NativeUnionThree('{"value": "text"}')
    self.assertEqual(obj.value, "text")

  def test_three_types_int(self):
    obj = NativeUnionThree('{"value": 7}')
    self.assertEqual(obj.value, 7)

  def test_three_types_float(self):
    obj = NativeUnionThree('{"value": 3.14}')
    self.assertEqual(obj.value, 3.14)

  def test_optional_with_value(self):
    obj = NativeUnionOptional('{"value": "present"}')
    self.assertEqual(obj.value, "present")

  def test_optional_with_null(self):
    obj = NativeUnionOptional('{"value": null}')
    self.assertIsNone(obj.value)

  def test_default_when_missing(self):
    obj = NativeUnionSimple('{}')
    self.assertIsNone(obj.value)

  def test_roundtrip(self):
    obj = NativeUnionSimple('{"value": "roundtrip"}')
    self.assertEqual(obj.serialize(), {"value": "roundtrip"})


class TestTypingUnionType(unittest.TestCase):
  """Tests for typing.Union[X, Y] annotation style."""

  def test_receives_first_type(self):
    obj = TypingUnionSimple('{"value": "hello"}')
    self.assertEqual(obj.value, "hello")
    self.assertIsInstance(obj.value, str)

  def test_receives_second_type(self):
    obj = TypingUnionSimple('{"value": 42}')
    self.assertEqual(obj.value, 42)
    self.assertIsInstance(obj.value, int)

  def test_three_types_str(self):
    obj = TypingUnionThree('{"value": "text"}')
    self.assertEqual(obj.value, "text")

  def test_three_types_int(self):
    obj = TypingUnionThree('{"value": 7}')
    self.assertEqual(obj.value, 7)

  def test_three_types_float(self):
    obj = TypingUnionThree('{"value": 3.14}')
    self.assertEqual(obj.value, 3.14)

  def test_optional_with_value(self):
    obj = TypingUnionOptional('{"value": "present"}')
    self.assertEqual(obj.value, "present")

  def test_optional_with_null(self):
    obj = TypingUnionOptional('{"value": null}')
    self.assertIsNone(obj.value)

  def test_default_when_missing(self):
    obj = TypingUnionSimple('{}')
    self.assertIsNone(obj.value)

  def test_roundtrip(self):
    obj = TypingUnionSimple('{"value": "roundtrip"}')
    self.assertEqual(obj.serialize(), {"value": "roundtrip"})


class TestMixedUnionTypes(unittest.TestCase):
  """Tests mixing both annotation styles in the same class."""

  def test_both_fields_str(self):
    obj = MixedUnions('{"native": "a", "typed": "b"}')
    self.assertEqual(obj.native, "a")
    self.assertEqual(obj.typed, "b")

  def test_native_int_typed_float(self):
    obj = MixedUnions('{"native": 1, "typed": 2.5}')
    self.assertEqual(obj.native, 1)
    self.assertAlmostEqual(obj.typed, 2.5)

  def test_partial_missing(self):
    obj = MixedUnions('{"native": 99}')
    self.assertEqual(obj.native, 99)
    self.assertIsNone(obj.typed)


if __name__ == "__main__":
  unittest.main()

