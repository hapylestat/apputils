#!/usr/bin/env python3

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import sys
import os
import re
import shutil
from typing import List

from setuptools import find_packages, setup

root_dir = os.path.abspath(os.path.dirname(__file__))
_author = "hapylestat@apache.org"


class Module(object):
  def __init__(self, app_name: str, name: str, version: str,  path: str):
    self.app_name = app_name
    self.name = name
    self.version = version
    self.path = path

  @property
  def full_name(self) -> str:
    return f"{self.app_name}-{self.name}"

  @property
  def package_name(self) -> str:
    return f"{self.app_name}.{self.name}"

  def __str__(self):
    return f"{self.full_name}-{self.version} ({self.name}-{self.version} -> {self.path})"


def normalize_path(path: str) -> str:
  return path.replace("/", os.path.sep)


def read(*parts):
  # auto-detects file encoding
  with codecs.open(os.path.sep.join(parts), 'r') as fp:
    return fp.read()


def find_tag(tags: str or List[str], *file_paths: str, use_import: bool = False):
  result_list: List[str] = []
  if isinstance(tags, str):
    tags = [tags]

  if use_import:
    import importlib
    _path = ".".join(file_paths)
    if _path.endswith(".py"):
      _path = _path[:-3]
    m = importlib.import_module(_path)

    for t in tags:
      if f"__{t}__" in m.__dict__:
        result_list.append(m.__dict__[f"__{t}__"])
  else:
    tag_file = read(*file_paths)
    for t in tags:
      tag_match = re.search(
        rf"^__{t}__ = ['\"]([^'\"]*)['\"]",
        tag_file,
        re.M,
      )
      if tag_match:
        result_list.append(tag_match.group(1))

  if len(result_list) != len(tags):
    raise RuntimeError(f"Unable to find some tag from the list: {', '.join(tags)}")

  return result_list


def load_requirements(path: str = "") -> List[str]:
  try:
    data = read(os.path.join(path, "requirements.txt"))
  except Exception:
    data = ""

  return data.split("\n")


def discover_modules(app_name: str, app_version: str, _modules_path: str, root_dir: str) -> List[Module]:
  modules_path = normalize_path(os.path.join(root_dir, _modules_path, app_name))
  _modules: List[Module] = []

  for module in os.listdir(modules_path):
    if module.startswith("__"):
      continue

    full_module_path = os.path.join(modules_path, module)
    if not os.path.isdir(full_module_path):
      continue

    try:
      _path = full_module_path.split(os.path.sep) + ["__init__.py"]
      _name = module
    except (RuntimeError or IOError):
      continue
    _modules.append(Module(app_name, _name, app_version, full_module_path))

  return _modules


def install_main_application(_app_name: str, _app_version: str, modules: List[Module]):
  extras_require = {}
  my_path = os.path.abspath(os.path.join(root_dir, "src/main"))

  for m in modules:
    _m_name = m.name.lower()
    extras_require[_m_name] = [m.full_name]

  setup(
    name=_app_name,
    version=_app_version,
    description="AppUtils Core package",
    long_description="AppUtils Core Application",
    license='ASF',
    classifiers=[
      "Programming Language :: Python",
      f"Programming Language :: Python :: {sys.version_info.major}",
      f"Programming Language :: Python :: {sys.version_info.major}.{sys.version_info.minor}",
    ],
    author=_author,
    package_dir={"": my_path},
    packages=find_packages(
      where=my_path,
      exclude=["contrib", "docs", "tests*", "tasks"],
    ),
    extras_require=extras_require,
    install_requires=load_requirements(),
    zip_safe=True,
    python_requires='>=3.8',
    setup_requires=[
      'setuptools',
      'wheel',
    ]
  )


def install_module(app_name: str, app_version: str,_modules_path: str, module: Module):
  packages = [n for n in find_packages(where=_modules_path) if module.full_name.replace("-", ".") in n]

  setup(
    name=module.full_name,
    version=app_version,
    description=f"AppUtils {module.name} package",
    long_description=f"AppUtils {module.name} Application",
    license='ASF',
    classifiers=[
      "Programming Language :: Python",
      f"Programming Language :: Python :: {sys.version_info.major}",
      f"Programming Language :: Python :: {sys.version_info.major}.{sys.version_info.minor}",
    ],
    author=_author,
    package_dir={module.package_name: module.path},
    packages=packages,
    install_requires=load_requirements(module.path) + [
      f"{app_name}=={app_version}"
    ],
    zip_safe=True,
    python_requires='>=3.12',
    setup_requires=[
      'setuptools',
      'wheel',
    ]
  )


def cleanup():
  try:
    shutil.rmtree(os.path.join(root_dir, "build"), ignore_errors=True)
  except FileNotFoundError:
    pass


def main():
  cleanup()
  debug_build: str = os.getenv("DEBUG_BUILD", "")

  _modules_path: str = os.path.abspath(os.path.join(root_dir, "src/modules"))
  app_name, app_version = find_tag(
    ["app_name", "app_version"],
    "src", "main", "apputils", "__init__.py",
    use_import=True
  )

  modules = discover_modules(app_name, app_version, _modules_path, root_dir)

  cmd = sys.argv
  module_name: str = ""
  if 'modules' in cmd:
    print(",".join([m.name for m in modules]))
    return

  if debug_build:
    print(f"!! This is debug build with number {debug_build} !!")
    app_version = f"{app_version}.dev{debug_build}"

  try:
    i = cmd.index("module")
    if i > 0 and len(cmd) > i+1:
      module_name = cmd[i+1]
      sys.argv.pop(i+1)
      sys.argv.pop(i)

    for m in modules:
      if module_name and module_name == m.name:
        print(f"==> Creating package for {m.full_name}:{m.version}...")
        install_module(app_name, app_version, _modules_path, m)
        return
  except ValueError:
    print("==> Building main package")
    install_main_application(app_name, app_version, modules)


main()
