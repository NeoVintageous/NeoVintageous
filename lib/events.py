# TODO Refactor XXX; cleanup, optimise (especially the on_query_context() and the on_text_command() events)

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


class NeoVintageousEvents(sublime_plugin.EventListener):

    _CACHED_COMPLETIONS = []
    _CACHED_COMPLETION_PREFIXES = []

    # XXX: Refactored from ViFocusRestorer
    def __init__(self):
        self.timer = None

    # XXX: Refactored from CmdlineContextProvider and VintageStateTrackers
    def on_query_context(self, view, key, operator, operand, match_all):

        # XXX: Refactored from CmdlineContextProviders
        if key == 'vi_cmdline_at_fs_completion':
            if view.score_selector(0, 'text.excmdline') != 0:
                value = wants_fs_completions(view.substr(view.line(0)))
                value = value and view.sel()[0].b == view.size()
                if operator == sublime.OP_EQUAL:
                    if operand is True:
                        return value
                    elif operand is False:
                        return not value

        # XXX: Refactored from CmdlineContextProviders
        if key == 'vi_cmdline_at_setting_completion':
            if view.score_selector(0, 'text.excmdline') != 0:
                value = wants_setting_completions(view.substr(view.line(0)))
                value = value and view.sel()[0].b == view.size()
                if operator == sublime.OP_EQUAL:
                    if operand is True:
                        return value
                    elif operand is False:
                        return not value

        # XXX: Refactored from VintageStateTrackers
        return State(view).context.check(key, operator, operand, match_all)

    # XXX: Refactored from ExCompletionsProvider
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

    # XXX: Refactored from ViMouseTracker
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

    # XXX: Refactored from ExecuteModeLines
    def on_load(self, view):
        modelines(view)

    # XXX: Refactored from ExecuteModeLines and VintageStateTrackers
    def on_post_save(self, view):

        # XXX: Refactored from ExecuteModeLines
        modelines(view)

        # XXX: Refactored from VintageStateTracker
        # Ensure the carets are within valid bounds. For instance, this is a
        # concern when `trim_trailing_white_space_on_save` is set to true.
        state = State(view)
        view.run_command('_vi_adjust_carets', {'mode': state.mode})

    # XXX: Refactored from VintageStateTrackers
    def on_close(self, view):
        settings.destroy(view)

    # XXX: Refactored from ViFocusRestorer
    def action(self):
        self.timer = None

    # XXX: Refactored from ViFocusRestorer
    def on_activated(self, view):
        if self.timer:
            self.timer.cancel()
            # Switching to a different view; enter normal mode.
            init_state(view)
        else:
            # Switching back from another application. Ignore.
            pass

    # XXX: Refactored from ViFocusRestorer and HistoryIndexRestorers
    def on_deactivated(self, view):

        # TODO Review clearing the cmdline history, does it need to be an event?
        # XXX: Refactored from HistoryIndexRestorer
        # Because views load asynchronously, do not restore history index
        # .on_activated(), but here instead. Otherwise, the .score_selector()
        # call won't yield the desired results.
        if view.score_selector(0, 'text.excmdline') > 0:
            view.run_command('clear_cmdline_history_index')

        # XXX: Refactored from ViFocusRestorer
        self.timer = threading.Timer(0.25, self.action)
        self.timer.start()
