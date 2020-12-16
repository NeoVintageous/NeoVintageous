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

from sublime import Region

from NeoVintageous.nv.options import get_option_completions
from NeoVintageous.nv.polyfill import view_to_region
from NeoVintageous.nv.polyfill import view_to_str
from NeoVintageous.nv.settings import get_cmdline_cwd
from NeoVintageous.nv.vim import is_ex_mode


_completion_types = [
    (re.compile(r'^(?P<cmd>:\s*cd!?)\s+(?P<path>.*)$'), True),
    (re.compile(r'^(?P<cmd>:\s*w(?:rite)?!?)\s+(?P<path>.*)$'), True),
    (re.compile(r'^(?P<cmd>:\s*e(?:dit)?!?)\s+(?P<path>.*)$'), False),
    (re.compile(r'^(?P<cmd>:\s*t(?:abedit)?!?)\s+(?P<path>.*)$'), False),
    (re.compile(r'^(?P<cmd>:\s*t(?:abe)?!?)\s+(?P<path>.*)$'), False),
    (re.compile(r'^(?P<cmd>:\s*(?:sp(?:lit)?|vs(?:plit)?)!?)\s+(?P<path>.*)$'), False),
]

_completion_settings = (
    re.compile(r'^(?P<cmd>:\s*setl(?:ocal)?\??)\s+(?P<setting>.*)$'),
    re.compile(r'^(?P<cmd>:\s*se(?:t)?\??)\s+(?P<setting>.*)$'),
)


def _iter_paths(prefix=None, from_dir=None, only_dirs: bool = False):
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

        for path in sorted(glob.iglob(start_at + '*')):
            if not only_dirs or os.path.isdir(path):
                suffix = ('/' if os.path.isdir(path) else '')
                item = os.path.split(path)[1]
                yield prefix + (item + suffix)[prefix_len:]
    else:
        prefix = from_dir
        start_at = os.path.expandvars(os.path.expanduser(prefix))
        for path in sorted(glob.iglob(start_at + '*')):
            if not only_dirs or os.path.isdir(path):
                yield path[len(start_at):] + ('' if not os.path.isdir(path) else '/')


def _parse_cmdline_for_fs(text: str) -> tuple:
    found = None
    for (pattern, only_dirs) in _completion_types:
        found = pattern.search(text)
        if found:
            return found.groupdict()['cmd'], found.groupdict()['path'], only_dirs

    return (None, None, None)


def _wants_fs_completions(text: str) -> bool:
    return _parse_cmdline_for_fs(text)[0] is not None


def _parse_cmdline_for_setting(text: str) -> tuple:
    found = None
    for pattern in _completion_settings:
        found = pattern.search(text)
        if found:
            return found.groupdict()['cmd'], found.groupdict().get('setting')

    return (None, None)


def _wants_setting_completions(text: str) -> bool:
    return _parse_cmdline_for_setting(text)[0] is not None


def _is_fs_completion(view) -> bool:
    return _wants_fs_completions(view.substr(view.line(0))) and view.sel()[0].b == view.size()


def _is_setting_completion(view) -> bool:
    return _wants_setting_completions(view.substr(view.line(0))) and view.sel()[0].b == view.size()


def _write_to_ex_cmdline(view, edit, cmd: str, completion: str) -> None:
    # Mark the window to ignore updates during view changes. For example, when
    # changes may trigger an input panel on_change() event, which could then
    # trigger a prefix update. See: on_change_cmdline_completion_prefix().
    view.window().settings().set('_nv_ignore_next_on_change', True)
    view.sel().clear()
    view.replace(edit, view_to_region(view), cmd + ' ' + completion)
    view.sel().add(Region(view.size()))


class _SettingCompletion():
    # Last user-provided path string.
    prefix = None
    is_stale = False
    items = None

    def __init__(self, view):
        self.view = view

    @staticmethod
    def reset() -> None:
        _SettingCompletion.prefix = None
        _SettingCompletion.is_stale = True
        _SettingCompletion.items = None

    def run(self, edit):
        cmd, prefix = _parse_cmdline_for_setting(self.view.substr(self.view.line(0)))
        if cmd:
            self._update(edit, cmd, prefix)

    def _update(self, edit, cmd: str, prefix: str) -> None:
        if (_SettingCompletion.prefix is None) and prefix:
            _SettingCompletion.prefix = prefix
            _SettingCompletion.is_stale = True
        elif _SettingCompletion.prefix is None:
            _SettingCompletion.prefix = ''
            _SettingCompletion.items = get_option_completions()
            _SettingCompletion.is_stale = False

        if not _SettingCompletion.items or _SettingCompletion.is_stale:
            _SettingCompletion.items = get_option_completions(_SettingCompletion.prefix)
            _SettingCompletion.is_stale = False

        try:
            _write_to_ex_cmdline(self.view, edit, cmd, next(_SettingCompletion.items))
        except StopIteration:
            try:
                _SettingCompletion.items = get_option_completions(_SettingCompletion.prefix)
                _write_to_ex_cmdline(self.view, edit, cmd, next(_SettingCompletion.items))
            except StopIteration:
                pass


class _FsCompletion():
    # Last user-provided path string.
    prefix = ''
    frozen_dir = ''
    is_stale = False
    items = None

    def __init__(self, view):
        self.view = view

    @staticmethod
    def reset() -> None:
        _FsCompletion.prefix = ''
        _FsCompletion.frozen_dir = ''
        _FsCompletion.is_stale = True
        _FsCompletion.items = None

    def run(self, edit):
        _FsCompletion.frozen_dir = (_FsCompletion.frozen_dir or (get_cmdline_cwd() + '/'))

        cmd, prefix, only_dirs = _parse_cmdline_for_fs(self.view.substr(self.view.line(0)))
        if cmd:
            self._update(edit, cmd, prefix, only_dirs)

    def _update(self, edit, cmd: str, prefix: str, only_dirs: bool) -> None:
        if not (_FsCompletion.prefix or _FsCompletion.items) and prefix:
            _FsCompletion.prefix = prefix
            _FsCompletion.is_stale = True

        if prefix == '..':
            _FsCompletion.prefix = '../'
            _write_to_ex_cmdline(self.view, edit, cmd, '../')

            return

        if prefix == '~':
            path = os.path.expanduser(prefix) + '/'
            _FsCompletion.prefix = path
            _write_to_ex_cmdline(self.view, edit, cmd, path)

            return

        if (not _FsCompletion.items) or _FsCompletion.is_stale:
            _FsCompletion.items = _iter_paths(
                from_dir=_FsCompletion.frozen_dir,
                prefix=_FsCompletion.prefix,
                only_dirs=only_dirs
            )
            _FsCompletion.is_stale = False

        try:
            _write_to_ex_cmdline(self.view, edit, cmd, next(_FsCompletion.items))
        except StopIteration:
            _FsCompletion.items = _iter_paths(
                prefix=_FsCompletion.prefix,
                from_dir=_FsCompletion.frozen_dir,
                only_dirs=only_dirs
            )

            _write_to_ex_cmdline(self.view, edit, cmd, _FsCompletion.prefix)


def on_change_cmdline_completion_prefix(window, cmdline: str) -> None:
    if window.settings().get('_nv_ignore_next_on_change'):
        window.settings().erase('_nv_ignore_next_on_change')

        return

    cmd, prefix, only_dirs = _parse_cmdline_for_fs(cmdline)
    if cmd:
        _FsCompletion.prefix = prefix
        _FsCompletion.is_stale = True

        return

    cmd, prefix = _parse_cmdline_for_setting(cmdline)
    if cmd:
        _SettingCompletion.prefix = prefix
        _SettingCompletion.is_stale = True

        return


def reset_cmdline_completion_state() -> None:
    _SettingCompletion.reset()
    _FsCompletion.reset()


_CMDLINE_COMPLETIONS = [
    'bNext', 'bfirst', 'blast', 'bnext', 'bprevious', 'brewind', 'browse',
    'buffer', 'buffers', 'cd', 'close', 'copy', 'cquit', 'delete', 'edit',
    'exit', 'file', 'files', 'global', 'help', 'history', 'inoremap', 'let',
    'ls', 'move', 'new', 'nnoremap', 'nohlsearch', 'noremap', 'nunmap', 'only',
    'onoremap', 'ounmap', 'print', 'pwd', 'qall', 'quit', 'read', 'registers',
    'set', 'setlocal', 'shell', 'silent', 'snoremap', 'sort', 'spellgood',
    'spellundo', 'split', 'substitute', 'sunmap', 'tabNext', 'tabclose',
    'tabfirst', 'tablast', 'tabnext', 'tabonly', 'tabprevious', 'tabrewind',
    'unmap', 'unvsplit', 'vnoremap', 'vsplit', 'vunmap', 'wall', 'wq', 'wqall',
    'write', 'xall', 'xit', 'yank'
]

# Keeps track of current completion completion.
_current_cmdline_completions = []  # type: list


def insert_best_cmdline_completion(view, edit, forward: bool = True) -> None:
    if is_ex_mode(view):
        if _is_setting_completion(view):
            _SettingCompletion(view).run(edit)
        elif _is_fs_completion(view):
            _FsCompletion(view).run(edit)
        else:
            cmdline = view_to_str(view)
            if len(cmdline) < 1:
                return

            prefix = cmdline[1:]

            if prefix not in _current_cmdline_completions:
                prefix_completions = [x for x in _CMDLINE_COMPLETIONS if x.startswith(prefix) and x != prefix]
                if prefix_completions:
                    _current_cmdline_completions[:] = [prefix] + prefix_completions

            try:
                prefix_index = _current_cmdline_completions.index(prefix)
            except ValueError:
                view.window().settings().set('_nv_ignore_next_on_change', True)
                view.insert(edit, view.size(), "\t")
                _current_cmdline_completions.clear()
                return

            next_index = prefix_index + 1 if forward else prefix_index - 1

            if forward:
                idx = next_index if len(_current_cmdline_completions) > next_index else 0
            else:
                idx = next_index if next_index >= 0 else len(_current_cmdline_completions) - 1

            completion = _current_cmdline_completions[idx]

            view.window().settings().set('_nv_ignore_next_on_change', True)
            view.sel().clear()
            view.replace(edit, Region(1, view.size()), completion)
            view.sel().add(Region(view.size()))
