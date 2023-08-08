# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from NeoVintageous.nv.listener import register
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.shell import read
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import REPLACE


__all__ = []  # type: list


class IMSwitcher():

    saved_im = ''

    def run(self, view, new_mode: str) -> None:
        if not _is_enabled(view):
            return

        try:
            if new_mode in (INSERT, REPLACE):
                self.resume(view)
            else:
                self.switch_to_default(view)
        except Exception as e:
            print('NeoVintageous: Error switching imput method:\n', e)

    def resume(self, view) -> None:
        if self.saved_im and self.saved_im != _get_default_im(view):
            _switch_to(view, self.saved_im)

    def switch_to_default(self, view) -> None:
        saved_im = _execute(view, _get_obtain_im_cmd(view)).strip()
        if saved_im:
            self.saved_im = saved_im

        default_im = _get_default_im(view)
        if default_im != self.saved_im:
            _switch_to(view, default_im)


def _switch_to(view, im: str) -> None:
    _execute(view, _get_switch_im_cmd(view, im))


def _execute(view, command: str) -> str:
    return read(view, command)


def _is_enabled(view) -> bool:
    return get_setting(view, 'auto_switch_input_method')


def _get_default_im(view) -> str:
    return get_setting(view, 'auto_switch_input_method_default')


def _get_obtain_im_cmd(view) -> str:
    return get_setting(view, 'auto_switch_input_method_get_cmd')


def _get_switch_im_cmd(view, im: str) -> str:
    cmd = get_setting(view, 'auto_switch_input_method_set_cmd')
    cmd = cmd.replace('{im}', im)

    return cmd


class Listener():

    def __init__(self, switcher: IMSwitcher):
        self.switcher = switcher

    def on_insert_enter(self, view, prev_mode: str) -> None:
        self.switcher.run(view, INSERT)

    def on_insert_leave(self, view, new_mode: str) -> None:
        self.switcher.run(view, new_mode)


register(
    __package__,
    Listener(
        IMSwitcher()
    )
)
