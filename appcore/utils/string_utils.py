# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

import string
import re
from collections import defaultdict


FORMAT_RE = re.compile("\{\{([^{]*)\}\}")


def safe_format(s, **kwargs):
  """
  :type s str
  """
  return string.Formatter().vformat(s, (), defaultdict(str, **kwargs))


def safe_format_sh(s, **kwargs):
  """
  :type s str
  :type kwargs dict
  """

  to_replace = set(kwargs.keys()) & set(FORMAT_RE.findall(s))

  for item in to_replace:
    s = s.replace("{{" + item + "}}", kwargs[item])

  return s

