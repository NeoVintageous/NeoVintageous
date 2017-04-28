import os

import sublime
import sublime_plugin

from NeoVintageous.lib.state import init_state
# from NeoVintageous.lib.state import State
# from NeoVintageous.lib.vi import settings
# from NeoVintageous.lib.vi import cmd_defs
from NeoVintageous.lib.vi.dot_file import DotFile
# from NeoVintageous.lib.vi.utils import modes
# from NeoVintageous.lib.vi.utils import regions_transformer


class NeovintageousToggleUseCtrlKeysCommand(sublime_plugin.WindowCommand):

    """
    A command that toggle the 'vintageous_use_ctrl_keys' setting.
    """

    def run(self):
        settings = sublime.load_settings('Preferences.sublime-settings')
        use_ctrl_keys = not settings.get('vintageous_use_ctrl_keys')

        settings.set('vintageous_use_ctrl_keys', use_ctrl_keys)
        sublime.save_settings('Preferences.sublime-settings')

        status = 'enabled' if use_ctrl_keys else 'disabled'
        sublime.status_message("NeoVintageous: 'use ctrl keys' setting {}".format(status))


class NeovintageousOpenMyRcFileCommand(sublime_plugin.WindowCommand):

    """
    A command that opens the the user .vintageousrc file.
    """

    def run(self):
        file = os.path.join(sublime.packages_path(), 'User', '.vintageousrc')

        if not os.path.exists(file):
            with open(file, 'w'):
                pass

        self.window.open_file(file)


class NeovintageousResetCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        view.settings().erase('vintage')
        init_state(view)

        DotFile.from_user().run()

        sublime.status_message("NeoVintageous: reset complete")


class NeovintageousExitFromCommandModeCommand(sublime_plugin.WindowCommand):

    """
    A sort of a panic button.
    """

    def run(self):
        v = self.window.active_view()
        v.settings().erase('vintage')

        # XXX: What happens exactly when the user presses Esc again now? Which
        #      mode are we in?

        v.settings().set('command_mode', False)
        v.settings().set('inverse_caret_state', False)

        sublime.status_message("NeoVintageous: exited from command mode")


# TODO command seems to be unused
class NeovintageousReloadSettingsCommand(sublime_plugin.WindowCommand):

    def run(self):
        DotFile.from_user().run()

        sublime.status_message("NeoVintageous: settings reloaded")
