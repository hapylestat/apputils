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


class EnumEx(Enum):
  @classmethod
  def from_name(cls, v: str, default=None):
    return cls._member_map_[v.upper()] if v.upper() in cls._member_map_ else default

  @classmethod
  def from_value(cls, value: str | int | float, default=None):
    for k, v in cls._member_map_.items():
      if v.value == value:
        return cls._member_map_[k]
    return default

  def __str__(self):
    return self.name.lower()
