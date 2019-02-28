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

import sublime_plugin

from NeoVintageous.nv.state import State


class ViCommandMixin:

    @property
    def state(self):
        return State(self.view)

    def save_sel(self):
        self.old_sel = tuple(self.view.sel())

    def _is_equal_to_old_sel(self, new_sel):
        try:
            return (tuple((s.a, s.b) for s in self.old_sel) == tuple((s.a, s.b) for s in tuple(self.view.sel())))
        except AttributeError:
            raise AttributeError('have you forgotten to call .save_sel()?')

    def has_sel_changed(self):
        return not self._is_equal_to_old_sel(self.view.sel())


class IrreversibleTextCommand(sublime_plugin.TextCommand):

    # Base class. The undo stack will ignore commands derived from this class.
    # This is useful to prevent global state management commands from shadowing
    # commands performing edits to the buffer, which are the important ones to
    # keep in the undo history.

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)

    def run_(self, edit_token, args):

        # We discard the edit_token because we don't want an
        # IrreversibleTextCommand to be added to the undo stack, but Sublime
        # Text seems to still require us to begin..end the token. If we removed
        # those calls, the caret would blink while motion keys were pressed,
        # because --apparently-- we'd have an unclosed edit object around.

        args = self.filter_args(args)
        if args:
            edit = self.view.begin_edit(edit_token, self.name(), args)
            try:
                return self.run(**args)
            finally:
                self.view.end_edit(edit)
        else:
            edit = self.view.begin_edit(edit_token, self.name())
            try:
                return self.run()
            finally:
                self.view.end_edit(edit)

    def run(self, **kwargs):
        pass


# DEPRECATED
# TODO Remove this command
class ViTextCommandBase(sublime_plugin.TextCommand, ViCommandMixin):
    pass


# DEPRECATED
# TODO Remove this command or refactor it just to allow commands to bypass the undo stack
class ViMotionCommand(IrreversibleTextCommand, ViTextCommandBase):
    # Motion should bypass the undo stack.
    # Due to MRO in Python subclasses, IrreversibleTextCommand must come first so
    # that the modified .run_() method is found first.
    pass


# DEPRECATED
# TODO Remove this command
class ViWindowCommandBase(sublime_plugin.WindowCommand, ViCommandMixin):

    @property
    def view(self):
        return self.window.active_view()
