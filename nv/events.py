from sublime import OP_EQUAL
from sublime import OP_NOT_EQUAL
from sublime_plugin import EventListener

from NeoVintageous.nv.ex import command_names
from NeoVintageous.nv.ex.completions import wants_fs_completions
from NeoVintageous.nv.ex.completions import wants_setting_completions
from NeoVintageous.nv.modeline import do_modeline
from NeoVintageous.nv.state import init_state
from NeoVintageous.nv.state import State
from NeoVintageous.nv.vi import settings
from NeoVintageous.nv.vi.utils import is_view
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE


_COMPLETIONS = sorted([x[0] for x in command_names])


class _Context:

    def __init__(self, view):
        self.view = view

    # TODO [refactor] Simplify the call to _check() by inlining/containing the logic.
    # TODO This is a dependency for creating custom keymaps see :h
    # neovintageous. However, we should create a generic "mode" context e.g.
    # psuedo code: is context neovintageous_mode equal to visual. Also see other
    # mode aware context methods.
    def vi_command_mode_aware(self, key, operator, operand, match_all):
        _is_command_mode = self.view.settings().get('command_mode')
        _is_view = is_view(self.view)

        return self._check((_is_command_mode and _is_view), operator, operand, match_all)

    # TODO [refactor] Simplify the call to _check() by inlining/containing the logic.
    # TODO This is a dependency for creating custom keymaps see :h
    # neovintageous. However, we should create a generic "mode" context e.g.
    # psuedo code: is context neovintageous_mode equal to visual. Also see other
    # mode aware context methods.
    def vi_insert_mode_aware(self, key, operator, operand, match_all):
        _is_command_mode = self.view.settings().get('command_mode')
        _is_view = is_view(self.view)

        return self._check((not _is_command_mode and _is_view), operator, operand, match_all)

    # TODO [refactor] Some completion keymaps depend on the "text.excmdline" so
    # remove this and use built-in scope selector context in the keymap
    # definition.
    def vi_is_cmdline(self, key, operator, operand, match_all):
        return self._check((self.view.score_selector(0, 'text.excmdline') != 0), operator, operand, match_all)

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

    def query(self, key, operator, operand, match_all):
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

    # TODO Refactor, cleanup and optimise on_query_context()
    def on_query_context(self, view, key, operator, operand, match_all):
        # Called when determining to trigger a key binding with the given
        # context key. If the plugin knows how to respond to the context, it
        # should return either True of False. If the context is unknown, it
        # should return None.
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

    # TODO Refactor, cleanup and optimise on_text_command()
    def on_text_command(self, view, command, args):
        if command == 'drag_select':
            state = State(view)
            mode = state.mode

            if mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
                if (args.get('extend') or (args.get('by') == 'words') or args.get('additive')):
                    return
                elif args.get('by') == 'lines':
                    return ('_nv_run_cmds', {'commands': [
                        ['drag_select', args],
                        ['_enter_visual_line_mode', {'mode': state.mode}]
                    ]})
                elif not args.get('extend'):
                    return ('_nv_run_cmds', {'commands': [
                        ['drag_select', args],
                        ['_enter_normal_mode', {'mode': mode}]
                    ]})

            elif mode == NORMAL:
                # TODO Dragging the mouse does not seem to fire a different
                # event than simply clicking. This makes it hard to update the
                # xpos.
                # See https://github.com/SublimeTextIssues/Core/issues/2117.
                if args.get('extend') or (args.get('by') == 'words'):
                    return ('_nv_run_cmds', {'commands': [
                        ['drag_select', args],
                        ['_enter_visual_mode', {'mode': mode}]
                    ]})

    def on_post_text_command(self, view, command, args):
        # This fixes issues where the xpos is not updated after a mouse click
        # moves the cursor position. These issues look like they could be
        # compounded by Sublime Text issues (see on_post_save() and the
        # _nv_fix_st_eol_caret command). The xpos only needs to be
        # updated on single mouse click.
        # See https://github.com/SublimeTextIssues/Core/issues/2117.
        if command == 'drag_select':
            if set(args) == {'event'}:
                if set(args['event']) == {'x', 'y', 'button'}:
                    if args['event']['button'] == 1:
                        state = State(view)
                        state.update_xpos(force=True)

    def on_load(self, view):
        if view.settings().get('vintageous_modeline', False):
            do_modeline(view)

    def on_post_save(self, view):
        if view.settings().get('vintageous_modeline', False):
            do_modeline(view)

        # Ensure the carets are within valid bounds. For instance, this is a
        # concern when 'trim_trailing_white_space_on_save' is set to true.
        view.run_command('_nv_fix_st_eol_caret', {'mode': State(view).mode})

    def on_close(self, view):
        settings.destroy(view)

    def on_activated(self, view):

        # Clear any visual selections in the view we are leaving. This mirrors
        # Vim behaviour. We can't put this functionality in the
        # view.on_deactivate() event, because that event is triggered when the
        # user right button clicks the view with the mouse, and we don't want
        # visual selections to be cleared on mouse right button clicks.
        window = view.window()
        if window:
            active_group = window.active_group()
            for group in range(window.num_groups()):
                if group != active_group:
                    other_view = window.active_view_in_group(group)
                    if other_view and other_view != view:
                        sel = other_view.sel()
                        if len(sel) > 0:
                            sels_begin_at_pt = sel[0].begin()
                            sel.clear()
                            sel.add(sels_begin_at_pt)

        # Initialise view state.
        init_state(view)
