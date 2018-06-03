# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2018 Reishin <hapy.lestat@gmail.com>


import unittest

from apputils.utils import string_utils


class StringUtilsTest(unittest.TestCase):
  def test_safe_format(self):
    s = string_utils.safe_format("{name} test string", name="cool")

    self.assertEqual("cool test string", s)

  def test_safe_string_with_no_variable(self):
    s = string_utils.safe_format("{name} test string")

    self.assertEqual(" test string", s)

  def test_safe_format_sh(self):
    s = string_utils.safe_format_sh("{{name}} test string", name="cool")

    self.assertEqual("cool test string", s)
