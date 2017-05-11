import sublime

from .lib.logger import get_logger
from .lib.state import init_state

# Load all the commands
from .lib.cmds.ex_motions import _vi_cmd_line_a # noqa TODO command appears to be unused
from .lib.cmds.ex_motions import _vi_cmd_line_k # noqa TODO command appears to be unused
from .lib.cmds.jumplist import _vi_add_to_jump_list # noqa
from .lib.cmds.modelines import ExecuteSublimeTextModeLinesCommand # noqa
from .lib.cmds.support import NeovintageousToggleUseCtrlKeysCommand # noqa
from .lib.cmds.support import NeovintageousOpenMyRcFileCommand # noqa
from .lib.cmds.support import NeovintageousResetCommand # noqa
from .lib.cmds.support import NeovintageousExitFromCommandModeCommand # noqa
from .lib.cmds.support import NeovintageousReloadMyRcFileCommand # noqa
from .lib.extras.surround import nvim_surround_cs # noqa
from .lib.extras.surround import nvim_surround_ds # noqa
from .lib.extras.surround import nvim_surround_ys # noqa


_logger = get_logger(__name__)


def _ensure_other_vimlike_packages_are_disabled():
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
    _logger.debug('{}.{}'.format(__name__, 'plugin_loaded()'))
    try:
        from package_control import events
        if events.install('NeoVintageous'):
            _ensure_other_vimlike_packages_are_disabled()
    except ImportError:
        print('NeoVintageous: could not import Package Control')

    view = sublime.active_window().active_view()
    init_state(view, new_session=True)


def plugin_unloaded():
    _logger.debug('{}.{}'.format(__name__, 'plugin_unloaded() DONE'))
    view = sublime.active_window().active_view()
    try:
        view.settings().set('command_mode', False)
        view.settings().set('inverse_caret_state', False)
    except AttributeError:
        _logger.warning('could not access sublime.active_window().active_view().settings while unloading')
    _logger.debug('{}.{}'.format(__name__, 'plugin_unloaded() DONE'))
