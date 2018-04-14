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

import glob
import os
import re


_completion_types = [
    (re.compile(r'^(?P<cmd>:\s*cd!?)\s+(?P<path>.*)$'), True),
    (re.compile(r'^(?P<cmd>:\s*w(?:rite)?!?)\s+(?P<path>.*)$'), True),
    (re.compile(r'^(?P<cmd>:\s*e(?:dit)?!?)\s+(?P<path>.*)$'), False),
    (re.compile(r'^(?P<cmd>:\s*t(?:abedit)?!?)\s+(?P<path>.*)$'), False),
    (re.compile(r'^(?P<cmd>:\s*t(?:abe)?!?)\s+(?P<path>.*)$'), False),
    (re.compile(r'^(?P<cmd>:\s*vs(?:plit)?!?)\s+(?P<path>.*)$'), False),
]

_completion_settings = [
    (re.compile(r'^(?P<cmd>:\s*setl(?:ocal)?\??)\s+(?P<setting>.*)$'), None),
    (re.compile(r'^(?P<cmd>:\s*se(?:t)?\??)\s+(?P<setting>.*)$'), None),
]


def iter_paths(prefix=None, from_dir=None, only_dirs=False):
    if prefix:
        start_at = os.path.expandvars(os.path.expanduser(prefix))
        # TODO: implement env var completion.
        if not prefix.startswith(('%', '$', '~')):
            start_at = os.path.join(from_dir, prefix)
            start_at = os.path.expandvars(os.path.expanduser(start_at))

        prefix_split = os.path.split(prefix)
        prefix_len = len(prefix_split[1])
        if ('/' in prefix and not prefix_split[0]):
            prefix_len = 0

        for path in glob.iglob(start_at + '*'):
            if not only_dirs or os.path.isdir(path):
                suffix = ('/' if os.path.isdir(path) else '')
                item = os.path.split(path)[1]
                yield prefix + (item + suffix)[prefix_len:]
    else:
        prefix = from_dir
        start_at = os.path.expandvars(os.path.expanduser(prefix))
        for path in glob.iglob(start_at + '*'):
            if not only_dirs or os.path.isdir(path):
                yield path[len(start_at):] + ('' if not os.path.isdir(path) else '/')


def parse_for_fs(text):
    found = None
    for (pattern, only_dirs) in _completion_types:
        found = pattern.search(text)
        if found:
            return found.groupdict()['cmd'], found.groupdict()['path'], only_dirs

    return (None, None, None)


def wants_fs_completions(text):
    return parse_for_fs(text)[0] is not None


def parse_for_setting(text):
    found = None
    for (pattern, _) in _completion_settings:
        found = pattern.search(text)
        if found:
            return found.groupdict()['cmd'], found.groupdict().get('setting'), None

    return (None, None, None)


def wants_setting_completions(text):
    return parse_for_setting(text)[0] is not None
