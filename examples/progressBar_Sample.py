# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# Copyright (c) 2015 Reishin <hapy.lestat@gmail.com>

from appcore.console import ProgressBar, ProgressBarOptions, ProgressBarFormat
import time


def do_progress(p, hide=False):
  """
  :type p ProgressBar
  :type hide bool
  """
  p.start(10)

  for i in range(1, 10):
    p.progress_inc()
    time.sleep(0.3)

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


do_progress(ProgressBar("Some progress", 60), True)

do_progress(ProgressBar("Short progress bar", 40, options=ProgressBarOptions(progress_format=ProgressBarFormat.PROGRESS_FORMAT_SHORT)))

do_progress(ProgressBar("Default progress bar", 60,
                        options=ProgressBarOptions(fill_char="#",
                                                   blank_char="-",
                                                   progress_format=ProgressBarFormat.PROGRESS_FORMAT_SIMPLE)))
do_status_progress(ProgressBar("Counting job", 20,
                               options=ProgressBarOptions(fill_char="#",
                                                          blank_char="-",
                                                          progress_format=ProgressBarFormat.PROGRESS_FORMAT_STATUS)))

do_status_progress(ProgressBar("", 20,
                               options=ProgressBarOptions(fill_char="#",
                                                          blank_char="-",
                                                          progress_format=ProgressBarFormat.PROGRESS_FORMAT_STATUS_SIMPLE)))




