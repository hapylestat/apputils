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
from enum import Enum
from datetime import datetime, timezone

from apputils.json2obj import SerializableObject


class TestEnum(Enum):
  TEST1 = 0
  TEST2 = 1
  TEST3 = "dad"


class TestObject(SerializableObject):
  tt: TestEnum = TestEnum.TEST1
  test: str | int | float = ""
  creation_time: datetime = None


test_json = """
{
  "test": 5.9,
  "tt": 1,
  "creation_time": 1765361826.792195
}
"""

test_yaml = """
test: 5
tt: 1
creation_time: 1765361826.792195
"""


def main():
  obj = TestObject(test_yaml)
  a = obj.serialize()

  print("===================================")
  print(a)
  print('------------------------------------')
  print(obj.dump(minimal=False))
  print('====================================')


if __name__ == '__main__':
  main()
