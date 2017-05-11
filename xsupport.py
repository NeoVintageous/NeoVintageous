import sublime
import sublime_plugin

from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi import cmd_defs
from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi.utils import regions_transformer


class _vi_slash_on_parser_done(sublime_plugin.WindowCommand):

    def run(self, key=None):
        state = State(self.window.active_view())
        state.motion = cmd_defs.ViSearchForwardImpl()
        state.last_buffer_search = (state.motion._inp or state.last_buffer_search)


class _vi_question_mark_on_parser_done(sublime_plugin.WindowCommand):

    def run(self, key=None):
        state = State(self.window.active_view())
        state.motion = cmd_defs.ViSearchBackwardImpl()
        state.last_buffer_search = (state.motion._inp or state.last_buffer_search)


class _vi_adjust_carets(sublime_plugin.TextCommand):

    def run(self, edit, mode=None):
        def f(view, s):
            if mode in (modes.NORMAL, modes.INTERNAL_NORMAL):
                if ((view.substr(s.b) == '\n' or s.b == view.size()) and not view.line(s.b).empty()):
                    return sublime.Region(s.b - 1)
            return s

        regions_transformer(self.view, f)


class Sequence(sublime_plugin.TextCommand):
    """Required so that mark_undo_groups_for_gluing and friends work."""

    def run(self, edit, commands):
        for cmd, args in commands:
            self.view.run_command(cmd, args)
