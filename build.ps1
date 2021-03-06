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
#
# Github: https://github.com/hapylestat/apputils
#
#

$MODULES = & "python3" setup.py modules
$modulesList = $MODULES.Split(",")

write-host "Building main module..."
& "python3" setup.py bdist_wheel

foreach ($m in $modulesList) {
    write-host "Building ${m}..."
    & "python3" setup.py bdist_wheel module "${m}"
}

write-host "Cleanup mess..."
rm *.egg-info -Force -Recurse
rm build -Force -Recurse


write-host "=================="
write-host "Modules:"
foreach ($m in $modulesList) {
    write-host "- ${m}"
}