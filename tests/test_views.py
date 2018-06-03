# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2018 Reishin <hapy.lestat@gmail.com>

import unittest

from apputils.views import BaseView
from copy import deepcopy


class IncomeView(BaseView):
  work1 = None
  work2 = None


class AddressView(BaseView):
  street_name = None
  city = None
  apartments = ["Default", "Default 1"]
  buildings = []


class PersonView(BaseView):
  name = None
  second_name = None
  age = 0
  addresses = [AddressView]
  income = IncomeView


class ViewsTest(unittest.TestCase):
  PERSON = {
    "name": "Cool name",
    "age": 25,
    "second_name": "cool surname",
    "addresses": [
      {
        "street_name": "cool street",
        "city": "some",
        "apartments": ["square x"],
        "buildings": []
      }
    ],
    "income": {
      "work1": 500,
      "work2": 300
    }
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
    person = deepcopy(self.PERSON)
    person["addresses"] = "nothing"
    with self.assertRaises(TypeError) as context:
      PersonView.deserialize_dict(person)

    self.assertTrue("Wrong data 'nothing' passed for 'AddressView' deserialization" == context.exception.args[0])

  def test_no_such_property(self):
    person = deepcopy(self.PERSON)
    person["new property"] = 0
    with self.assertRaises(TypeError) as context:
      PersonView.deserialize_dict(person)

    self.assertTrue("PersonView doesn't contain properties: new property" == context.exception.args[0])

  def test_non_existing_deserialization_ignore(self):
    person = deepcopy(self.PERSON)
    person["vdsv"] = "nothing"

    try:
      PersonView.deserialize_dict(person, ignore_non_existing=True)
    except TypeError:
      self.assertTrue(False)

  def test_non_existing_deserialization_ignore_subparse(self):
    person = deepcopy(self.PERSON)
    person["addresses"][0]["cfvsd"] = "fds"

    try:
      PersonView.deserialize_dict(person, ignore_non_existing=True)
    except TypeError:
      self.assertTrue(False)

  def test_wrong_type_deserialize(self):
    data = "random invalid data"
    IncomeView.deserialize_dict(data, ignore_non_existing=True)

  def test_empty_view_serialization(self):
    blank_address = AddressView(street_name=None, city=None, apartments=None, buildings=None)
    person = PersonView()
    person.addresses = [blank_address]

    serialized_obj = person.serialize(null_values=False)

    self.assertEqual(serialized_obj["addresses"], [])

  def test_base_class_should_be_ignored(self):
    blank_address = AddressView(street_name=None, city=None, apartments=None)
    person = PersonView()
    person.addresses = [blank_address, AddressView]

    serialized_obj = person.serialize(null_values=False)

    self.assertEqual(serialized_obj["addresses"], [{'buildings': []}])

  def test_not_full_deserialization(self):
    person = deepcopy(self.PERSON)
    del person["name"]
    del person["age"]
    del person["addresses"]

    obj = PersonView.deserialize_dict(person)
    person["name"] = PersonView.name
    person["age"] = PersonView.age
    person["addresses"] = []

    self.assertEqual(obj.serialize(null_values=True), person)
