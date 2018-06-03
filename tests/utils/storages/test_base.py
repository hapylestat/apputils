# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2018 Reishin <hapy.lestat@gmail.com>

from unittest import TestCase

from apputils.utils.storages.base import KeyStore


class BaseStorageTest(TestCase):
  def test_list_keys(self):
    store = KeyStore()
    with self.assertRaises(NotImplementedError):
      store.list_keys()

  def test_get(self):
    store = KeyStore()
    with self.assertRaises(NotImplementedError):
      store.get(None)

  def test_set(self):
    store = KeyStore()
    with self.assertRaises(NotImplementedError):
      store.set("", None)

  def test_exists(self):
    store = KeyStore()
    with self.assertRaises(NotImplementedError):
      store.exists("")

  def test_delete(self):
    store = KeyStore()
    with self.assertRaises(NotImplementedError):
      store.delete("")
