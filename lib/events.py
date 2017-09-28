from threading import Timer

from sublime import OP_EQUAL
from sublime import OP_NOT_EQUAL
from sublime_plugin import EventListener

from NeoVintageous.lib.ex import command_names
from NeoVintageous.lib.ex.completions import wants_fs_completions
from NeoVintageous.lib.ex.completions import wants_setting_completions
from NeoVintageous.lib.modeline import modeline
from NeoVintageous.lib.state import init_state
from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi import settings
from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi.utils import is_view


_NORMAL_INSERT_MODE = modes.NORMAL_INSERT
_VISUAL_BLOCK_MODE = modes.VISUAL_BLOCK
_SELECT_MODE = modes.SELECT
_VISUAL_LINE_MODE = modes.VISUAL_LINE
_INSERT_MODE = modes.INSERT
_VISUAL_MODE = modes.VISUAL
_NORMAL_MODE = modes.NORMAL
_COMPLETIONS = sorted([x[0] for x in command_names])


class _Context(object):

    def __init__(self, view):
        self.view = view

    def create_state(self):
        return State(self.view)

    def vi_is_view(self, key, operator, operand, match_all):
        return self._check(is_view(self.create_state().view), operator, operand, match_all)

    def vi_command_mode_aware(self, key, operator, operand, match_all):
        in_command_mode = self.create_state().view.settings().get('command_mode')
        vi_is_view = self.vi_is_view(key, operator, operand, match_all)

        return self._check(in_command_mode and vi_is_view, operator, operand, match_all)

    def vi_insert_mode_aware(self, key, operator, operand, match_all):
        in_command_mode = self.create_state().view.settings().get('command_mode')
        vi_is_view = self.vi_is_view(key, operator, operand, match_all)

        return self._check(not in_command_mode and vi_is_view, operator, operand, match_all)

    def vi_use_ctrl_keys(self, key, operator, operand, match_all):
        return self._check(self.create_state().settings.view['vintageous_use_ctrl_keys'], operator, operand, match_all)

    def vi_is_cmdline(self, key, operator, operand, match_all):
        return self._check(
            self.create_state().view.score_selector(0, 'text.excmdline') != 0, operator, operand, match_all
        )

    def vi_cmdline_at_fs_completion(self, key, operator, operand, match_all):
        if self.view.score_selector(0, 'text.excmdline') != 0:
            value = wants_fs_completions(self.view.substr(self.view.line(0)))
            value = value and self.view.sel()[0].b == self.view.size()
            if operator == OP_EQUAL:
                if operand is True:
                    return value
                elif operand is False:
                    return not value

        # TODO queries should default to False because they can handle the
        # request. The tests are passing because None is falsy, see
        # https://stackoverflow.com/questions/35038519/python-unittest-successfully-asserts-none-is-false
        # All the tests should be revised to use assertIs(False|True... to fix
        # the edge case bugs.

    def vi_cmdline_at_setting_completion(self, key, operator, operand, match_all):
        if self.view.score_selector(0, 'text.excmdline') != 0:
            value = wants_setting_completions(self.view.substr(self.view.line(0)))
            value = value and self.view.sel()[0].b == self.view.size()
            if operator == OP_EQUAL:
                if operand is True:
                    return value
                elif operand is False:
                    return not value

    def vi_enable_cmdline_mode(self, key, operator, operand, match_all):
        return self._check(
            self.create_state().settings.view['vintageous_enable_cmdline_mode'], operator, operand, match_all
        )

    def vi_mode_normal_insert(self, key, operator, operand, match_all):
        return self._check(self.create_state().mode == _NORMAL_INSERT_MODE, operator, operand, match_all)

    def vi_mode_visual_block(self, key, operator, operand, match_all):
        return self._check(self.create_state().mode == _VISUAL_BLOCK_MODE, operator, operand, match_all)

    def vi_mode_select(self, key, operator, operand, match_all):
        return self._check(self.create_state().mode == _SELECT_MODE, operator, operand, match_all)

    def vi_mode_visual_line(self, key, operator, operand, match_all):
        return self._check(self.create_state().mode == _VISUAL_LINE_MODE, operator, operand, match_all)

    def vi_mode_insert(self, key, operator, operand, match_all):
        return self._check(self.create_state().mode == _INSERT_MODE, operator, operand, match_all)

    def vi_mode_visual(self, key, operator, operand, match_all):
        return self._check(self.create_state().mode == _VISUAL_MODE, operator, operand, match_all)

    def vi_mode_normal(self, key, operator, operand, match_all):
        return self._check(self.create_state().mode == _NORMAL_MODE, operator, operand, match_all)

    def vi_mode_normal_or_visual(self, key, operator, operand, match_all):
        # XXX: This context is used to disable some keys for VISUALLINE.
        # However, this is hiding some problems in visual transformers that might not be dealing
        # correctly with VISUALLINE.
        normal = self.vi_mode_normal(key, operator, operand, match_all)
        visual = self.vi_mode_visual(key, operator, operand, match_all)
        visual = visual or self.vi_mode_visual_block(key, operator, operand, match_all)

        return self._check((normal or visual), operator, operand, match_all)

    def vi_mode_normal_or_any_visual(self, key, operator, operand, match_all):
        normal_or_visual = self.vi_mode_normal_or_visual(key, operator, operand, match_all)
        visual_line = self.vi_mode_visual_line(key, operator, operand, match_all)

        return self._check((normal_or_visual or visual_line), operator, operand, match_all)

    def query(self, key, operator, operand, match_all):
        # Called when determining to trigger a key binding with the given
        # context key.
        #
        # If the plugin knows how to respond to the context, it should return
        # either True of False.
        #
        # If the context is unknown, should return None.
        #
        # operator is one of:
        #
        #     sublime.OP_EQUAL: Is the value of the context equal to the
        #                       operand?
        #
        #     sublime.OP_NOT_EQUAL: Is the value of the context not equal to
        #                           the operand?
        #
        #     sublime.OP_REGEX_MATCH: Does the value of the context match the
        #                             regex given in operand?
        #
        #     sublime.OP_NOT_REGEX_MATCH: Does the value of the context not
        #                                 match the regex given in operand?
        #
        #     sublime.OP_REGEX_CONTAINS: Does the value of the context contain
        #                                a substring matching the regex given
        #                                in operand?
        #
        #     sublime.OP_NOT_REGEX_CONTAINS: Does the value of the context not
        #                                    contain a substring matching the
        #                                    regex given in operand?
        #
        # match_all should be used if the context relates to the selections:
        # does every selection have to match (match_all == True), or is at least
        # one matching enough then (match_all == False).
        func = getattr(self, key, None)
        if func:
            return func(key, operator, operand, match_all)
        else:
            return None

    def _check(self, value, operator, operand, match_all):
        if operator == OP_EQUAL:
            if operand is True:
                return value
            elif operand is False:
                return not value
        elif operator is OP_NOT_EQUAL:
            if operand is True:
                return not value
            elif operand is False:
                return value


# TODO Refactor XXX; cleanup, optimise (especially the on_query_context() and the on_text_command() events)
class NeoVintageousEvents(EventListener):

    _CACHED_COMPLETIONS = []
    _CACHED_COMPLETION_PREFIXES = []

    def __init__(self):
        self._on_deactivate_callback_timer = None

    def on_query_context(self, view, key, operator, operand, match_all):
        return _Context(view).query(key, operator, operand, match_all)

    def on_query_completions(self, view, prefix, locations):
        if view.score_selector(0, 'text.excmdline') == 0:
            return []

        if len(prefix) + 1 != view.size():
            return []

        if prefix and prefix in self._CACHED_COMPLETION_PREFIXES:
            return self._CACHED_COMPLETIONS

        compls = [x for x in _COMPLETIONS if x.startswith(prefix) and x != prefix]
        self._CACHED_COMPLETION_PREFIXES = [prefix] + compls
        self._CACHED_COMPLETIONS = list(zip([prefix] + compls, compls + [prefix]))

        return self._CACHED_COMPLETIONS

    def on_text_command(self, view, command, args):
        if command == 'drag_select':
            state = State(view)

            if state.mode in (_VISUAL_MODE, _VISUAL_LINE_MODE, _VISUAL_BLOCK_MODE):
                if (args.get('extend') or (args.get('by') == 'words') or args.get('additive')):
                    return
                elif not args.get('extend'):
                    return ('sequence', {
                        'commands': [
                            ['drag_select', args],
                            ['_enter_normal_mode', {'mode': state.mode}]
                        ]
                    })

            elif state.mode == _NORMAL_MODE:
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

    def on_load(self, view):
        modeline(view)

    def on_post_save(self, view):
        modeline(view)

        # Ensure the carets are within valid bounds. For instance, this is a
        # concern when 'trim_trailing_white_space_on_save' is set to true.
        view.run_command('_vi_adjust_carets', {'mode': State(view).mode})

    def on_close(self, view):
        settings.destroy(view)

    def on_activated(self, view):
        if self._on_deactivate_callback_timer:
            # Switching to a different view; enter normal mode
            init_state(view)
            self._on_deactivate_callback_timer.cancel()
        else:  # Switching back from another application; Ignore
            pass

    def _on_deactivate_callback(self):
        self._on_deactivate_callback_timer = None

    def on_deactivated(self, view):

        # TODO Review clearing the cmdline history, does it need to be an event?
        # Because views load asynchronously, do not restore history index
        # .on_activated(), but here instead. Otherwise, the .score_selector()
        # call won't yield the desired results.
        if view.score_selector(0, 'text.excmdline') > 0:
            view.run_command('clear_cmdline_history_index')

        self._on_deactivate_callback_timer = Timer(0.25, self._on_deactivate_callback)
        self._on_deactivate_callback_timer.start()
