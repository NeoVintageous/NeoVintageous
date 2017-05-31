import os

import sublime
import sublime_plugin

from Default.history_list import get_jump_history

from NeoVintageous.lib import nvim
from NeoVintageous.lib.state import init_state
from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi import cmd_defs
from NeoVintageous.lib.vi.dot_file import DotFile
from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi.utils import regions_transformer


__all__ = [
    '_vi_add_to_jump_list',
    '_vi_adjust_carets',
    '_vi_question_mark_on_parser_done',
    '_vi_slash_on_parser_done',
    'NeovintageousExitFromCommandModeCommand',
    'NeovintageousOpenMyRcFileCommand',
    'NeovintageousReloadMyRcFileCommand',
    'NeovintageousResetCommand',
    'NeovintageousToggleUseCtrlKeysCommand',
    'Sequence'
]


class _vi_add_to_jump_list(sublime_plugin.WindowCommand):
    def run(self):
        get_jump_history(self.window.id()).push_selection(self.window.active_view())
        hl = get_jump_history(self.window.id())


class NeovintageousToggleUseCtrlKeysCommand(sublime_plugin.WindowCommand):
    """A command that toggle the 'vintageous_use_ctrl_keys' setting."""

    def run(self):
        settings = sublime.load_settings('Preferences.sublime-settings')
        use_ctrl_keys = not settings.get('vintageous_use_ctrl_keys')

        settings.set('vintageous_use_ctrl_keys', use_ctrl_keys)
        sublime.save_settings('Preferences.sublime-settings')

        status = 'enabled' if use_ctrl_keys else 'disabled'

        nvim.status_message('ctrl keys have been {}'.format(status))


class NeovintageousOpenMyRcFileCommand(sublime_plugin.WindowCommand):
    """A command that opens the the user runtime configuration file."""

    def run(self):
        file = os.path.join(sublime.packages_path(), 'User', '.vintageousrc')

        if not os.path.exists(file):
            with open(file, 'w'):
                pass

        self.window.open_file(file)


class NeovintageousReloadMyRcFileCommand(sublime_plugin.WindowCommand):
    """A command that reloads the user runtime configuration file."""

    def run(self):
        DotFile.from_user().run()

        nvim.status_message('rc file reloaded')


class NeovintageousResetCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        view.settings().erase('vintage')
        init_state(view)

        DotFile.from_user().run()

        nvim.status_message('reset complete')


class NeovintageousExitFromCommandModeCommand(sublime_plugin.WindowCommand):
    """A sort of a panic button."""

    def run(self):
        v = self.window.active_view()
        v.settings().erase('vintage')

        # XXX: What happens exactly when the user presses Esc again now? Which
        #      mode are we in?

        v.settings().set('command_mode', False)
        v.settings().set('inverse_caret_state', False)

        nvim.status_message('exited from command mode')


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
