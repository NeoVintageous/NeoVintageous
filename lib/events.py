# TODO Refactor: event listeners into on event listener for more control over event priorities, cleaner code and improve perforamance

import threading

import sublime
import sublime_plugin

from NeoVintageous.lib.ex import command_names
from NeoVintageous.lib.ex.completions import wants_fs_completions
from NeoVintageous.lib.ex.completions import wants_setting_completions
from NeoVintageous.lib.modelines import modelines
from NeoVintageous.lib.state import init_state
from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi import settings
from NeoVintageous.lib.vi.utils import modes


_COMPLETIONS = sorted([x[0] for x in command_names])


class CmdlineContextProvider(sublime_plugin.EventListener):
    """Provide contexts for the cmdline input panel."""

    def on_query_context(self, view, key, operator, operand, match_all):
        if view.score_selector(0, 'text.excmdline') == 0:
            return

        if key == 'vi_cmdline_at_fs_completion':
            value = wants_fs_completions(view.substr(view.line(0)))
            value = value and view.sel()[0].b == view.size()
            if operator == sublime.OP_EQUAL:
                if operand is True:
                    return value
                elif operand is False:
                    return not value

        if key == 'vi_cmdline_at_setting_completion':
            value = wants_setting_completions(view.substr(view.line(0)))
            value = value and view.sel()[0].b == view.size()
            if operator == sublime.OP_EQUAL:
                if operand is True:
                    return value
                elif operand is False:
                    return not value


class ExCompletionsProvider(sublime_plugin.EventListener):

    _CACHED_COMPLETIONS = []
    _CACHED_COMPLETION_PREFIXES = []

    def on_query_completions(self, view, prefix, locations):
        if view.score_selector(0, 'text.excmdline') == 0:
            return []

        if len(prefix) + 1 != view.size():
            return []

        if prefix and prefix in self._CACHED_COMPLETION_PREFIXES:
            return self._CACHED_COMPLETIONS

        compls = [x for x in _COMPLETIONS if x.startswith(prefix) and x != prefix]
        self._CACHED_COMPLETION_PREFIXES = [prefix] + compls
        # S3 can only handle lists, not iterables.
        self._CACHED_COMPLETIONS = list(zip([prefix] + compls, compls + [prefix]))

        return self._CACHED_COMPLETIONS


class ExecuteModeLines(sublime_plugin.EventListener):
    """
    This event listener provides a feature similar to vim modelines.

    Modelines set options local to the view by declaring them in the source
    code file itself.

        Example:

        # sublime: gutter false
        # sublime: translate_tab_to_spaces true
        # sublime: rulers [80, 120]
        # sublime: tab_size 4

    The top as well as the bottom of the buffer is scanned for modelines.
    _MAX_LINES_TO_CHECK * _LINE_LENGTH defines the size of the regions to be
    scanned.
    """

    def on_load(self, view):
        modelines(view)

    def on_post_save(self, view):
        modelines(view)


class VintageStateTracker(sublime_plugin.EventListener):

    def on_post_save(self, view):
        # Ensure the carets are within valid bounds. For instance, this is a
        # concern when `trim_trailing_white_space_on_save` is set to true.
        state = State(view)
        view.run_command('_vi_adjust_carets', {'mode': state.mode})

    def on_query_context(self, view, key, operator, operand, match_all):
        return State(view).context.check(key, operator, operand, match_all)

    def on_close(self, view):
        settings.destroy(view)


class ViMouseTracker(sublime_plugin.EventListener):

    def on_text_command(self, view, command, args):
        if command == 'drag_select':
            state = State(view)

            if state.mode in (modes.VISUAL, modes.VISUAL_LINE, modes.VISUAL_BLOCK):
                if (args.get('extend') or (args.get('by') == 'words') or args.get('additive')):
                    return
                elif not args.get('extend'):
                    return ('sequence', {
                        'commands': [
                            ['drag_select', args],
                            ['_enter_normal_mode', {'mode': state.mode}]
                        ]
                    })

            elif state.mode == modes.NORMAL:
                # TODO(guillermooo): Dragging the mouse does not seem to
                # fire a different event than simply clicking. This makes it
                # hard to update the xpos.
                if args.get('extend') or (args.get('by') == 'words'):
                    return ('sequence', {
                        'commands': [
                            ['drag_select', args],
                            ['_enter_visual_mode', {'mode': state.mode}]
                        ]
                    })


class ViFocusRestorer(sublime_plugin.EventListener):

    def __init__(self):
        self.timer = None

    def action(self):
        self.timer = None

    def on_activated(self, view):
        if self.timer:
            self.timer.cancel()
            # Switching to a different view; enter normal mode.
            init_state(view)
        else:
            # Switching back from another application. Ignore.
            pass

    def on_deactivated(self, view):
        self.timer = threading.Timer(0.25, self.action)
        self.timer.start()


# TODO This listener should be unnecessary
class HistoryIndexRestorer(sublime_plugin.EventListener):

    def on_deactivated(self, view):
        # Because views load asynchronously, do not restore history index
        # .on_activated(), but here instead. Otherwise, the .score_selector()
        # call won't yield the desired results.
        if view.score_selector(0, 'text.excmdline') > 0:
            view.run_command('clear_cmdline_history_index')
