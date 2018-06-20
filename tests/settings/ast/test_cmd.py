# coding=utf-8
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2018 Reishin <hapy.lestat@gmail.com>

import unittest

from apputils.settings.ast.cmd import DefaultTokenizer


class ViewsTest(unittest.TestCase):
  def test_tokenizer(self):
    # test_data = ["--longtest=lol", "+5", "fcds", "-f"]
    # tokens = DefaultTokenizer.tokenize(test_data)
    # pass
    data = """
    [
  {
    "name": "local net",
    "net": [
      "10.255.0.1/24"
      ]
  },
  {
    "name": "docker net",
    "net": [
      "192.168.10.1/24"
      ]
  },
  {
    "name": "vpn net",
    "net": [
      "10.255.2.1/24"
      ]
  },
  {
    "name": "vpnDarkDE",
    "net": [
      "10.255.1.248/30"
      ],
    "status": "hide"
  },
  {
    "name": "vpnSangouGB",
    "net": [
       "10.255.1.244/30"
      ],
    "status": "hide"
  }
]
    """
    import json
    d = json.loads(data)

    net_list = []
    for item in d:
      if "status" in item and item["status"] == "hide":
        continue

      net_list.extend(item["net"])

    print(" ".join(net_list))
    pass
