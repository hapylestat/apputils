# coding=utf-8
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

from apputils.console import ProgressBar, ProgressBarOptions, ProgressBarFormat, CharacterStyles
import time


def do_status_progress(p, hide=False):
  """
  :type p ProgressBar
  :type hide bool
  """
  p.start(10)

  for i in range(1, 60):
    p.progress_inc(new_status="count %s" % i)
    time.sleep(0.1)

  p.stop(hide_progress=hide, new_status="done")


test_suites = [
  ("Infinite bar", 40, ProgressBarOptions(progress_format=ProgressBarFormat.PROGRESS_FORMAT_INFINITE_SIMPLE, character_style=CharacterStyles.graphic3), False),
  ("Some progress", 60, ProgressBarOptions(), True),
  ("Short progress bar", 40, ProgressBarOptions(progress_format=ProgressBarFormat.PROGRESS_FORMAT_SHORT), False),
  ("Default progress bar", 60, ProgressBarOptions(character_style=CharacterStyles.simple, progress_format=ProgressBarFormat.PROGRESS_FORMAT_SIMPLE), False),
  ("Counting job", 20, ProgressBarOptions(character_style=CharacterStyles.graphic1, progress_format=ProgressBarFormat.PROGRESS_FORMAT_SIMPLE_BORDERLESS), False),
  ("", 20, ProgressBarOptions(character_style=CharacterStyles.simple, progress_format=ProgressBarFormat.PROGRESS_FORMAT_STATUS_SIMPLE), False),
  ("Counting job", 20, ProgressBarOptions(character_style=CharacterStyles.graphic, progress_format=ProgressBarFormat.PROGRESS_FORMAT_STATUS), True)
]


for suite in test_suites:
  do_status_progress(ProgressBar(suite[0], suite[1], options=suite[2]), hide=suite[3])
