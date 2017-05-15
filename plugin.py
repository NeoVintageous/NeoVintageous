import sublime

from .lib.logger import get_logger
from .lib.state import init_state

# Load the commands
# TODO Review: Perhaps just put all commands, except extras, in one file lib/commands.py?
from .lib.cmds.ex import *  # noqa: F401, F403
from .lib.cmds.ex_main import *  # noqa: F401, F403
from .lib.cmds.ex_motions import *  # noqa: F401, F403
from .lib.cmds.actions import *  # noqa: F401, F403
from .lib.cmds.motions import *  # noqa: F401, F403
from .lib.cmds.support import *  # noqa: F401, F403
from .lib.extras.surround import *  # noqa: F401, F403

# Load the events
from .lib.events import NeoVintageousEvents  # noqa: F401


_logger = get_logger(__name__)


def _ensure_other_vimlike_packages_are_disabled():
    settings = sublime.load_settings('Preferences.sublime-settings')
    ignored_packages = settings.get('ignored_packages', [])

    do_save = False

    if 'Vintage' not in ignored_packages:
        ignored_packages.append('Vintage')
        do_save = True

    if 'Vintageous' not in ignored_packages:
        ignored_packages.append('Vintageous')
        do_save = True

    if 'Six' not in ignored_packages:
        ignored_packages.append('Six')
        do_save = True

    if do_save:
        ignored_packages.sort()
        settings.set('ignored_packages', ignored_packages)
        sublime.save_settings('Preferences.sublime-settings')


def plugin_loaded():
    _logger.debug('%s.plugin_loaded()', __name__)

    try:
        from package_control import events
        if events.install('NeoVintageous'):
            _ensure_other_vimlike_packages_are_disabled()
    except ImportError:
        print('NeoVintageous: could not import Package Control')

    init_state(sublime.active_window().active_view(), new_session=True)

    _logger.debug('%s.plugin_loaded() done.', __name__)


def plugin_unloaded():
    _logger.debug('%s.plugin_unloaded()', __name__)

    view = sublime.active_window().active_view()
    if view:
        view.settings().set('command_mode', False)
        view.settings().set('inverse_caret_state', False)

    _logger.debug('%s.plugin_unloaded() done.', __name__)
