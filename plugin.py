import sublime

from .lib import nvim
from .lib.state import init_state

# Load the commands
# TODO Review: Perhaps just put all commands, except extras, in one file lib/commands.py?
from .lib.commands import *  # noqa: F401, F403
from .lib.cmds.ex_actions import *  # noqa: F401, F403
from .lib.cmds.ex_motions import *  # noqa: F401, F403
from .lib.cmds.vi_actions import *  # noqa: F401, F403
from .lib.cmds.vi_motions import *  # noqa: F401, F403
from .lib.extras.surround import *  # noqa: F401, F403
from .lib.extras.unimpaired import *  # noqa: F401, F403
from .lib.extras.abolish import *  # noqa: F401, F403

# Load the events
from .lib.events import NeoVintageousEvents  # noqa: F401


_logger = nvim.get_logger(__name__)


def _ensure_other_vimlike_packages_are_disabled():
    settings = sublime.load_settings('Preferences.sublime-settings')
    ignored_packages = settings.get('ignored_packages', [])

    settings_need_saving = False

    if 'Vintage' not in ignored_packages:
        ignored_packages.append('Vintage')
        settings_need_saving = True

    if 'Vintageous' not in ignored_packages:
        ignored_packages.append('Vintageous')
        settings_need_saving = True

    if 'Six' not in ignored_packages:
        ignored_packages.append('Six')
        settings_need_saving = True

    if settings_need_saving:
        ignored_packages.sort()
        settings.set('ignored_packages', ignored_packages)
        sublime.save_settings('Preferences.sublime-settings')
        # TODO Should the user be prompted with dialog about needing to restart ST?


def plugin_loaded():
    _logger.debug('init')

    # Tests fail for OSX on Travis if we try to disable existing
    # vim emulator plugins on load. Things work fine on Linux
    # and Windows (on Travis and I've also manually tested on
    # both Windows and Linix) so this might be an issue only
    # on Travis. TODO needs investigating
    if sublime.platform() == 'osx':
        try:
            from package_control import events
            if events.install('NeoVintageous'):
                _ensure_other_vimlike_packages_are_disabled()
        except ImportError:
            nvim.console_message('could not import Package Control')
    else:
        _ensure_other_vimlike_packages_are_disabled()

    # TODO Should the CHANGELOG be opened on upgrade?
    # TODO Should the user be prompted with dialog about needing to restart ST on upgrade?

    init_state(sublime.active_window().active_view(), new_session=True)

    _logger.debug('done')


def plugin_unloaded():
    view = sublime.active_window().active_view()
    if view:
        view.settings().set('command_mode', False)
        view.settings().set('inverse_caret_state', False)
