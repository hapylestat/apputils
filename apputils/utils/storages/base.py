# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>


class KeyStore(object):
  """
  Interface for the various KeyStore implementations, required to implement attached storage types.
  """

  def list_keys(self):
    """
    Returns list of the available keys

    :return: List of the keys available in the storage
    :rtype list
    """
    raise NotImplementedError()

  def get(self, key):
    """
    Retrieves previously stored key from the storage

    :return value, stored in the storage
    """
    raise NotImplementedError()

  def set(self, key, value, expire_in=None):
    """
    Function to set or change particular property in the storage

    :param key: key name
    :param value:  value to set
    :param expire_in: seconds to expire key
    :type key str
    :type expire_in int
    """
    raise NotImplementedError()

  def exists(self, key):
    """
    Check if the particular key exists in the storage

    :param key: name of the key which existence need to be checked
    :return:

    :type key str
    :rtype bool
    """
    raise NotImplementedError()

  def delete(self, key):
    """
    Remove specific key from the storage

    :param key: name of the key to be removed
    """
    raise NotImplementedError()
