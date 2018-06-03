# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2018 Reishin <hapy.lestat@gmail.com>

from datetime import datetime
from unittest import mock, TestCase

from apputils.utils.storages import in_memory


class InMemoryStorageTest(TestCase):
  def test_store_value(self):
    store = in_memory.InMemoryKeyStore()
    key = "test key"
    value = "test value"
    store.set(key, value)

    self.assertTrue(store.exists(key))
    self.assertEqual(store.get(key), value)

  def test_delete_key(self):
    store = in_memory.InMemoryKeyStore()
    key = "test key"
    value = "test value"
    store.set(key, value)

    self.assertTrue(store.exists(key))

    store.delete(key)

    self.assertFalse(store.exists(key))

  def test_key_expiration(self):
    store = in_memory.InMemoryKeyStore()
    key = "test key"
    value = "test value"

    with mock.patch.object(in_memory, "datetime") as time_mock:
      time_mock.now.return_value = datetime(2000, 1, 1)
      store.set(key, value, expire_in=360)
      self.assertTrue(store.exists(key))

      time_mock.now.return_value = datetime(2000, 1, 2)
      self.assertFalse(store.exists(key))

  def test_list_keys(self):
    store = in_memory.InMemoryKeyStore()
    key = "test key"
    value = "test value"

    store.set(key, value)

    self.assertEqual(store.list_keys(), [key])

  def test_get_missing_key(self):
    store = in_memory.InMemoryKeyStore()
    self.assertFalse(store.get("missing"))

  def test_get_expired_key(self):
    store = in_memory.InMemoryKeyStore()
    key = "test key"
    value = "test value"

    with mock.patch.object(in_memory, "datetime") as time_mock:
      time_mock.now.return_value = datetime(2000, 1, 1)
      store.set(key, value, expire_in=360)
      self.assertTrue(store.get(key))

      time_mock.now.return_value = datetime(2000, 1, 2)
      self.assertFalse(store.get(key))
