import sublime

from .lib.logger import PluginLogger
from .lib.state import init_state

# Load all the commands
from .lib.commands.jumplist import _vi_add_to_jump_list # noqa
from .lib.commands.modelines import ExecuteSublimeTextModeLinesCommand # noqa

from .lib.commands.support import NeovintageousToggleUseCtrlKeysCommand # noqa
from .lib.commands.support import NeovintageousOpenMyRcFileCommand # noqa
from .lib.commands.support import NeovintageousResetCommand # noqa
from .lib.commands.support import NeovintageousExitFromCommandModeCommand # noqa

# TODO command seems to be unused
from .lib.commands.support import NeovintageousReloadSettingsCommand # noqa


_logger = PluginLogger(__name__)


def ensure_other_vimlike_packages_are_disabled():
    settings = sublime.load_settings('Preferences.sublime-settings')
    ignored_packages = settings.get('ignored_packages', [])

    save_settings = False
    if 'Vintage' not in ignored_packages:
        ignored_packages.append('Vintage')
        save_settings = True

    if 'Vintageous' not in ignored_packages:
        ignored_packages.append('Vintageous')
        save_settings = True

    if 'Six' not in ignored_packages:
        ignored_packages.append('Six')
        save_settings = True

    if save_settings:
        ignored_packages.sort()
        settings.set('ignored_packages', ignored_packages)
        sublime.save_settings('Preferences.sublime-settings')


def plugin_loaded():
    try:
        from package_control import events
        if events.install('NeoVintageous'):
            ensure_other_vimlike_packages_are_disabled()
    except ImportError:
        print('NeoVintageous: could not import Package Control')

    view = sublime.active_window().active_view()
    init_state(view, new_session=True)


def plugin_unloaded():
    view = sublime.active_window().active_view()
    try:
        view.settings().set('command_mode', False)
        view.settings().set('inverse_caret_state', False)
    except AttributeError:
        _logger.warn(
            'could not access sublime.active_window().active_view().settings '
            ' while unloading')
