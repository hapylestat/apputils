# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2016 Reishin <hapy.lestat@gmail.com>

from appcore.core.singlobj import Singleton, SingletonObject
from appcore.core.logger import aLogger
from appcore.core.config import Configuration
from appcore.core import config

__name__ = "appcore"
__version__ = "0.1.2.1"
__author__ = "Dmytro Grinenko"
__author_mail__ = "hapy.lestat@gmail.com"
__url__ = "https://github.com/hapylestat/appcore"

__all__ = ["Configuration", "config", "aLogger", "Singleton", "SingletonObject"]
