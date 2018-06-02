# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2018 Reishin <hapy.lestat@gmail.com>

import unittest

from apputils.views import BaseView


class AddressView(BaseView):
  street_name = None
  city = None
  apartments = None


class PersonView(BaseView):
  name = None
  second_name = None
  age = 0
  addresses = [AddressView]


class ViewsTest(unittest.TestCase):
  PERSON = {
    "name": "Cool name",
    "age": 25,
    "second_name": "cool surname",
    "addresses": [
      {
        "street_name": "cool street",
        "city": "some",
        "apartments": "square x"
      }
    ]
  }

  def test_serialization(self):
    serialized_object = PersonView(**self.PERSON).serialize()
    self.assertEqual(self.PERSON, serialized_object)

  def test_deserialization(self):
    obj = PersonView.deserialize_dict(self.PERSON)
    self.assertEqual(obj.name, self.PERSON["name"])
    self.assertEqual(obj.age, self.PERSON["age"])
    self.assertEqual(obj.second_name, self.PERSON["second_name"])
    self.assertEqual(obj.addresses[0].street_name, self.PERSON["addresses"][0]["street_name"])
    self.assertEqual(obj.addresses[0].city, self.PERSON["addresses"][0]["city"])
    self.assertEqual(obj.addresses[0].apartments, self.PERSON["addresses"][0]["apartments"])

  def test_type_mismatch(self):
    person = dict(self.PERSON)
    person["addresses"] = "nothing"
    with self.assertRaises(TypeError) as context:
      PersonView.deserialize_dict(person)

    self.assertTrue("Wrong data 'nothing' passed for 'AddressView' deserialization" == context.exception.args[0])

  def test_no_such_property(self):
    person = dict(self.PERSON)
    person["new property"] = 0
    with self.assertRaises(TypeError) as context:
      PersonView.deserialize_dict(person)

    self.assertTrue("PersonView doesn't contain properties: new property" == context.exception.args[0])
