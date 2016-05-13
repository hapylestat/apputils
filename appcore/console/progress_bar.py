# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>


import sys
import time
import os
from appcore.console import get_terminal_size
from appcore.utils import safe_format


class ProgressBarFormat(object):
  PROGRESS_FORMAT_DEFAULT = "{begin_line}{text} {percents_done:>3}% [{filled}{empty}] {value}/{max}  {items_per_sec} i/s"
  PROGRESS_FORMAT_SHORT = "{begin_line}{text} {percents_done:>3}% [{filled}{empty}] {value}/{max}"
  PROGRESS_FORMAT_SIMPLE = "{begin_line}{text} [{filled}{empty}] {percents_done:>3}%"
  PROGRESS_FORMAT_STATUS = "{begin_line}{text}: |{filled}{empty}| {percents_done:>3}%  {value}/{max}   [{status}]"
  PROGRESS_FORMAT_STATUS_SIMPLE = "{begin_line}|{filled}{empty}| {percents_done:>3}%   [{status}]"


class ProgressBarOptions(object):
  def __init__(self, fill_char="=", blank_char=" ", progress_format=ProgressBarFormat.PROGRESS_FORMAT_DEFAULT):
    """
    :type fill_char str
    :type blank_char str
    :type progress_format str
    """
    self._fill_char = fill_char
    self._blank_char = blank_char
    self._progress_format = progress_format

  @property
  def fill_char(self):
    return self._fill_char

  @property
  def blank_char(self):
    return self._blank_char

  @property
  def progress_format(self):
    return self._progress_format


class ProgressBar(object):
  def __init__(self, text, width, options=ProgressBarOptions()):
    """
    Create ProgressBar object

    :argument text Text of the ProgressBar
    :argument options Format of progress Bar

    :type text str
    :type width int
    :type options ProgressBarOptions
    """
    self._text = text
    self._status = ""
    self._width = width
    self._max = float(0)
    c = get_terminal_size(fallback=(80, 24))
    self._console_width = c[0]
    self._value = 0
    self._prev_time = 0
    self._items_per_sec = 0
    self._items_per_sec_prev = 0
    self._begin_line_character = '\r'
    self._options = options
    self.stdout = sys.stdout

  @property
  def _width(self):
    """
    :rtype float
    """
    return self.__width

  @_width.setter
  def _width(self, value):
    """
    :type value float
    """
    self.__width = float(value)

  @property
  def _max(self):
    """
    :rtype float
    """
    return self.__max

  @_max.setter
  def _max(self, value):
    """
    :type value float
    """
    self.__max = float(value)

  def start(self, max_val):
    """
    :arg max_val Maximum value
    :type max_val int
    """
    self._max = max_val
    self._fill_empty()
    self._value = 0
    self.progress(0)
    self._items_per_sec = 0
    self._items_per_sec_prev = 0
    self._prev_time = time.time()

  def _calc_percent_done(self, value):
    """
    :type value float
    """
    return int(value / self._max * 100)

  def _calc_filled_space(self, percents):
    """
    :type percents int
    """
    return int((self._width / 100) * percents)

  def _calc_empty_space(self, percents):
    """
    :type percents int
    """
    return int(self._width - self._calc_filled_space(percents))

  def _fill_empty(self):
    data = " " * (self._console_width - len(self._begin_line_character))
    self.stdout.write(self._begin_line_character + data)
    self.stdout.flush()

  def progress(self, value, new_status=None):
    """
    :type value int
    :type new_status str
    """
    if new_status is not None:
      # if new text is shorter, then we need fill previously used place
      space_fillers = len(self._status) - len(new_status) if self._status and len(self._status) - len(new_status) > 0 else 0
      self._status = new_status + " " * space_fillers

    total_secs = round(time.time() - self._prev_time)
    secs = total_secs % 60
    if secs >= 1:
      self._items_per_sec = self._value - self._items_per_sec_prev
      self._items_per_sec_prev = self._value
      self._prev_time = time.time()

    percent_done = self._calc_percent_done(value)
    filled = self._options.fill_char * int(self._calc_filled_space(percent_done))
    empty = self._options.blank_char * int(self._calc_empty_space(percent_done))
    if value > self._max:
      filled = self._options.fill_char * int(self._width)

    kwargs = {
      "begin_line": self._begin_line_character,
      "text": self._text,
      "status": self._status,
      "filled": filled,
      "empty": empty,
      "value": int(value),
      "max": int(self._max),
      "items_per_sec": int(self._items_per_sec),
      "percents_done": percent_done
    }

    self.stdout.write(safe_format(self._options.progress_format, **kwargs))
    self.stdout.flush()

  def progress_inc(self, step=1, new_status=None):
    """
    :type step int
    :type new_status str
    """
    self._value += step
    self.progress(self._value, new_status=new_status)

  def stop(self, hide_progress=False, new_status=None):
    """
    :arg hide_progress Hide progress bar
    :type hide_progress bool
    :type new_status str
    """
    if hide_progress:
      kwargs = {
        "begin_line": self._begin_line_character,
        "text": self._text,
        "fill_space": " " * (self._console_width - len(self._text) - len(os.linesep))
      }
      self.stdout.write("{begin_line}{text}{fill_space}".format(**kwargs))
    else:
      self.progress(int(self._max), new_status=new_status)

    self.stdout.write(os.linesep)

