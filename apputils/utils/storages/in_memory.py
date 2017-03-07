from threading import Lock
from datetime import datetime, timedelta

from apputils.utils.storages.base import KeyStore


class InMemoryItemValue(object):
  _lock = None
  """:type _lock Lock"""

  def __init__(self, value=None, expire_in=None):
    self._lock = Lock()
    self._value = value
    self._expire_in = None
    self._expire_in_time = None

    self.update_expire_time(expire_in)

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, val):
    self._lock.acquire()
    self._value = val
    self._expire_in = datetime.now() + timedelta(seconds=float(self._expire_in_time)) if self._expire_in_time else None
    self._lock.release()

  def update_expire_time(self, t):
    self._expire_in_time = t

  @property
  def is_expired(self):
    return (self._expire_in - datetime.now()).days < 0 if self._expire_in else False


class InMemoryKeyStore(KeyStore):
  """
  In-memory storage to keep key-value pairs with possibility to set expiration time for them.
  """

  def __init__(self):
    """
    Initialize key store
    """
    super(InMemoryKeyStore, self).__init__()

    self._keystore = {}

  def delete(self, key):
    """
    Remove specific key from the storage

    :param key: name of the key to be removed
    """
    self._keystore.pop(key, None)

  def list_keys(self):
    """
    Returns list of the available keys

    :return: List of the keys available in the storage
    :rtype list
    """
    return [k for k, el in self._keystore.items() if not el.is_expired]

  def set(self, key, value, expire_in=None):
    """
    Function to set or change particular property in the storage

    :param key: key name
    :param value:  value to set
    :param expire_in: seconds to expire key
    :type key str
    :type expire_in int
    """
    if key not in self._keystore:
      self._keystore[key] = InMemoryItemValue(expire_in=expire_in)

    k = self._keystore[key]
    """:type k InMemoryItemValue"""
    k.update_expire_time(expire_in)
    k.value = value

  def get(self, key):
    """
    Retrieves previously stored key from the storage

    :return value, stored in the storage
    """
    if key not in self._keystore:
      return None

    rec = self._keystore[key]
    """:type rec InMemoryItemValue"""

    if rec.is_expired:
      self.delete(key)
      return None

    return rec.value

  def exists(self, key):
    """
    Check if the particular key exists in the storage

    :param key: name of the key which existence need to be checked
    :return:

    :type key str
    :rtype bool
    """
    if key in self._keystore and not self._keystore[key].is_expired:
      return True
    elif key in self._keystore and self._keystore[key].is_expired:
      self.delete(key)
      return False

    return False
