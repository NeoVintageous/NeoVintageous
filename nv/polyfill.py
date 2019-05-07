# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.


# *sigh* Sublime has no API to set the status for a Window:
# https://github.com/SublimeTextIssues/Core/issues/627
def set_window_status(window, key, value):
    for view in window.views():
        view.set_status(key, value)


# See set_window_status()
def erase_window_status(window, key):
    for view in window.views():
        view.erase_status(key)
