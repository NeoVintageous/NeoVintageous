import sublime

from NeoVintageous.lib.logger import PluginLogger
from NeoVintageous.vi.dot_file import DotFile
from NeoVintageous.vi.utils import is_ignored
from NeoVintageous.vi.utils import is_ignored_but_command_mode
from NeoVintageous.vi.utils import is_view
from NeoVintageous.vi.utils import modes
from NeoVintageous.lib.state import State


_logger = PluginLogger(__name__)


def _init_vintageous(view, new_session=False):
    """
    Initializes global data. Runs at startup and every time a view gets
    activated, loaded, etc.

    @new_session
      Whether we're starting up Sublime Text. If so, volatile data must be
      wiped.
    """

    _logger.debug("running init for view %d", view.id())

    if not is_view(view):
        # Abort if we got a widget, panel...
        _logger.info(
            '[_init_vintageous] ignoring view: {0}'.format(
                view.name() or view.file_name() or '<???>'))
        try:
            # XXX: All this seems to be necessary here.
            if not is_ignored_but_command_mode(view):
                view.settings().set('command_mode', False)
                view.settings().set('inverse_caret_state', False)
            view.settings().erase('vintage')
            if is_ignored(view):
                # Someone has intentionally disabled NeoVintageous, so let the user know.
                sublime.status_message(
                    'NeoVintageous: Vim emulation disabled for the current view')
        except AttributeError:
            _logger.info(
                '[_init_vintageous] probably received the console view')
        except Exception:
            _logger.error('[_init_vintageous] error initializing view')
        finally:
            return

    state = State(view)

    if not state.reset_during_init:
        # Probably exiting from an input panel, like when using '/'. Don't
        # reset the global state, as it may contain data needed to complete
        # the command that's being built.
        state.reset_during_init = True
        return

    # Non-standard user setting.
    reset = state.settings.view['vintageous_reset_mode_when_switching_tabs']
    # XXX: If the view was already in normal mode, we still need to run the
    # init code. I believe this is due to Sublime Text (intentionally) not
    # serializing the inverted caret state and the command_mode setting when
    # first loading a file.
    # If the mode is unknown, it might be a new file. Let normal mode setup
    # continue.
    if not reset and (state.mode not in (modes.NORMAL, modes.UNKNOWN)):
        return

    # If we have no selections, add one.
    if len(state.view.sel()) == 0:
        state.view.sel().add(sublime.Region(0))

    state.logger.info('[_init_vintageous] running init')

    if state.mode in (modes.VISUAL, modes.VISUAL_LINE):
        # TODO: Don't we need to pass a mode here?
        view.window().run_command('_enter_normal_mode', {'from_init': True})

    elif state.mode in (modes.INSERT, modes.REPLACE):
        # TODO: Don't we need to pass a mode here?
        view.window().run_command('_enter_normal_mode', {'from_init': True})

    elif (view.has_non_empty_selection_region() and
          state.mode != modes.VISUAL):
            # Runs, for example, when we've performed a search via ST3 search
            # panel and we've pressed 'Find All'. In this case, we want to
            # ensure a consistent state for multiple selections.
            # TODO: We could end up with multiple selections in other ways
            #       that bypass _init_vintageous.
            state.mode = modes.VISUAL

    else:
        # This may be run when we're coming from cmdline mode.
        pseudo_visual = view.has_non_empty_selection_region()
        mode = modes.VISUAL if pseudo_visual else state.mode
        # TODO: Maybe the above should be handled by State?
        state.enter_normal_mode()
        view.window().run_command('_enter_normal_mode', {'mode': mode,
                                                         'from_init': True})

    state.reset_command_data()
    if new_session:
        state.reset_volatile_data()

        # Load settings.
        DotFile.from_user().run()


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
    _init_vintageous(view, new_session=True)


def plugin_unloaded():
    view = sublime.active_window().active_view()
    try:
        view.settings().set('command_mode', False)
        view.settings().set('inverse_caret_state', False)
    except AttributeError:
        _logger.warn(
            'could not access sublime.active_window().active_view().settings '
            ' while unloading')
