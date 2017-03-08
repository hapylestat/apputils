# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2016 Reishin <hapy.lestat@gmail.com>

from apputils.core.singlobj import Singleton, SingletonObject
from apputils.core.logger import aLogger
from apputils.core.config import Configuration
from apputils.core import config

__name__ = "apputils"
__version__ = "0.1.2.3"
__author__ = "Dmytro Grinenko"
__author_mail__ = "hapy.lestat@gmail.com"
__url__ = "https://github.com/hapylestat/apputils"
__copyright__ = "2017, {}".format(__author__)
__all__ = ["Configuration", "config", "aLogger", "Singleton", "SingletonObject"]
