import sublime

from .lib.logger import get_logger
from .lib.state import init_state

# Load the commands

# TODO Refactor: there's gotta be a better way to organise commands; perhaps
#       just put all commands in one file?

from .lib.cmds.ex_commands import *  # noqa: F401, F403
from .lib.cmds.ex_main import *  # noqa: F401, F403
from .lib.cmds.ex_motions import *  # noqa: F401, F403

from .lib.cmds.support import _vi_add_to_jump_list  # noqa: F401
from .lib.cmds.support import _vi_adjust_carets  # noqa: F401
from .lib.cmds.support import _vi_question_mark_on_parser_done  # noqa: F401
from .lib.cmds.support import _vi_slash_on_parser_done  # noqa: F401
from .lib.cmds.support import NeovintageousExitFromCommandModeCommand  # noqa: F401
from .lib.cmds.support import NeovintageousOpenMyRcFileCommand  # noqa: F401
from .lib.cmds.support import NeovintageousReloadMyRcFileCommand  # noqa: F401
from .lib.cmds.support import NeovintageousResetCommand  # noqa: F401
from .lib.cmds.support import NeovintageousToggleUseCtrlKeysCommand  # noqa: F401
from .lib.cmds.support import Sequence  # noqa: F401

from .lib.cmds.actions import *  # noqa: F401, F403
from .lib.cmds.motions import *  # noqa: F401, F403

from .lib.extras.surround import nvim_surround_cs  # noqa: F401
from .lib.extras.surround import nvim_surround_ds  # noqa: F401
from .lib.extras.surround import nvim_surround_ys  # noqa: F401

# Load the events
# TODO Refactor: events listeners into one event listener, see .lib.events
from .lib.events import CmdlineContextProvider  # noqa: F401
from .lib.events import ExCompletionsProvider  # noqa: F401
from .lib.events import ExecuteModeLines  # noqa: F401
from .lib.events import HistoryIndexRestorer  # noqa: F401
from .lib.events import ViFocusRestorer  # noqa: F401
from .lib.events import ViMouseTracker  # noqa: F401
from .lib.events import VintageStateTracker  # noqa: F401


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
