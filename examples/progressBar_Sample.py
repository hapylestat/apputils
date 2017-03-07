# coding=utf-8
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

from apputils.console import ProgressBar, ProgressBarOptions, ProgressBarFormat, CharacterStyles
import time


def do_progress(p, hide=False):
  """
  :type p ProgressBar
  :type hide bool
  """
  p.start(4)

  for i in range(0, 10):
    p.progress_inc()
    time.sleep(1)

  p.stop(hide_progress=hide)


def do_status_progress(p, hide=False):
  """
  :type p ProgressBar
  :type hide bool
  """
  p.start(10)

  for i in range(1, 10):
    p.progress_inc(new_status="count %s" % i)
    time.sleep(0.5)

  p.stop(hide_progress=hide, new_status="done")


do_progress(ProgressBar("Infinite bar", 40, options=ProgressBarOptions(progress_format=ProgressBarFormat.PROGRESS_FORMAT_INFINITE_SIMPLE)))

do_progress(ProgressBar("Some progress", 60), True)

do_progress(ProgressBar("Short progress bar", 40, options=ProgressBarOptions(progress_format=ProgressBarFormat.PROGRESS_FORMAT_SHORT)))

do_progress(ProgressBar("Default progress bar", 60,
                        options=ProgressBarOptions(character_style=CharacterStyles.simple,
                                                   progress_format=ProgressBarFormat.PROGRESS_FORMAT_SIMPLE)))
do_status_progress(ProgressBar("Counting job", 20,
                               options=ProgressBarOptions(character_style=CharacterStyles.simple,
                                                          progress_format=ProgressBarFormat.PROGRESS_FORMAT_STATUS)))

do_status_progress(ProgressBar("", 20,
                               options=ProgressBarOptions(character_style=CharacterStyles.simple,
                                                          progress_format=ProgressBarFormat.PROGRESS_FORMAT_STATUS_SIMPLE)))

do_status_progress(ProgressBar("Counting job", 20,
                               options=ProgressBarOptions(character_style=CharacterStyles.graphic,
                                                          progress_format=ProgressBarFormat.PROGRESS_FORMAT_STATUS)), hide=True)

