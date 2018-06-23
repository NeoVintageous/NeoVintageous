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

from sublime import set_timeout
import sublime_plugin

from NeoVintageous.nv.state import State
from NeoVintageous.nv.ui import ui_region_flags
from NeoVintageous.nv.vi.utils import IrreversibleTextCommand
from NeoVintageous.nv.vim import console_message


class ViCommandMixin(object):

    @property
    def _view(self):
        view = None
        try:
            view = self.view
        except AttributeError:
            try:
                view = self.window.active_view()
            except AttributeError:
                raise AttributeError(
                    'ViCommandMixin must be used with a TextCommand or a WindowCommand class')
        return view

    @property
    def _window(self):
        window = None
        try:
            window = self.window
        except AttributeError:
            try:
                window = self.view.window()
            except AttributeError:
                raise AttributeError(
                    'ViCommandMixin must be used with a TextCommand or a WindowCommand class')
        return window

    @property
    def state(self):
        return State(self._view)

    def save_sel(self):
        self.old_sel = tuple(self._view.sel())

    def is_equal_to_old_sel(self, new_sel):
        try:
            return (tuple((s.a, s.b) for s in self.old_sel) ==
                    tuple((s.a, s.b) for s in tuple(self._view.sel())))
        except AttributeError:
            raise AttributeError('have you forgotten to call .save_sel()?')

    def has_sel_changed(self):
        return not self.is_equal_to_old_sel(self._view.sel())

    def enter_normal_mode(self, mode):
        # Args:
        #   mode (str): The current mode
        self._window.run_command('_enter_normal_mode', {'mode': mode})

    def enter_insert_mode(self, mode):
        # Args:
        #   mode (str): The current mode
        self._window.run_command('_enter_insert_mode', {'mode': mode})

    def set_xpos(self, state):
        try:
            xpos = self._view.rowcol(self._view.sel()[0].b)[1]
        except Exception as e:
            console_message(str(e))
            raise ValueError('could not set xpos')

        state.xpos = xpos

    def outline_target(self):
        view = self._view
        _get = view.settings().get

        if not _get('highlightedyank'):
            return

        view.add_regions(
            'highlightedyank',
            list(view.sel()),
            scope='string highlightedyank',
            flags=ui_region_flags(_get('highlightedyank_style'))
        )

        set_timeout(
            lambda: view.erase_regions('highlightedyank'),
            _get('highlightedyank_duration')
        )


# TODO [refactor] Move to commands module
class ViTextCommandBase(sublime_plugin.TextCommand, ViCommandMixin):
    """
    Base class form motion and action commands.

    Not all commands need to derive from this base class, but it's
    recommended they do if there isn't any good reason they shouldn't.
    """

    # Yank config data is controlled through class attributes:
    _can_yank = False
    _synthetize_new_line_at_eof = False
    _yanks_linewise = False
    _populates_small_delete_register = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# TODO [refactor] Move to commands module
# Due to MRO in Python subclasses, IrreversibleTextCommand must come first so
# that the modified .run_() method is found first.
class ViMotionCommand(IrreversibleTextCommand, ViTextCommandBase):
    """Motion should bypass the undo stack."""

    pass


# DEPRECATED TODO REMOVE
# TODO [refactor] Move to commands module
class ViWindowCommandBase(sublime_plugin.WindowCommand, ViCommandMixin):
    """
    Base class form some window commands.

    Not all window commands need to derive from this base class, but it's
    recommended they do if there isn't any good reason they shouldn't.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
