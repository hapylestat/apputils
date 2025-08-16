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
from typing import Dict


from apputils.json2obj import SerializableObject


class TestObject(SerializableObject):
  data: Dict[str, str] = {}
  data1: dict[str, str] = {}
  listtest: list[list[int]] = []
  test: str = ""


test_json = """
{
  "data": {
    "f1": "v1",
    "f2": "v2"
  },
  "data1": {
    "f1": "v1",
    "f2": ""
  },
  "listtest": ["v1", "v2"]
}
"""

test_yaml = """
data:
  f1: v1
  f2: v2
data1:
  f1: v1
listtest:
  - - 1
    - 2
    - 3
  - - 4
    - 5
"""

test_obj = {
  "data": {
    "f1": "v1",
    "f2": ""
  }
}


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
