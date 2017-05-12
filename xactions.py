from functools import partial
import re

import sublime

from NeoVintageous.lib.logger import PluginLogger
from NeoVintageous.state import _init_vintageous
from NeoVintageous.lib.state import State
from NeoVintageous.vi import cmd_base
from NeoVintageous.vi import cmd_defs
from NeoVintageous.vi import mappings
from NeoVintageous.vi import search
from NeoVintageous.vi import units
from NeoVintageous.vi import utils
from NeoVintageous.vi.constants import regions_transformer_reversed
from NeoVintageous.vi.core import ViTextCommandBase
from NeoVintageous.vi.core import ViWindowCommandBase
from NeoVintageous.vi.keys import key_names
from NeoVintageous.vi.keys import KeySequenceTokenizer
from NeoVintageous.vi.keys import to_bare_command_name
from NeoVintageous.vi.mappings import Mappings
from NeoVintageous.vi.registers import REG_EXPRESSION
from NeoVintageous.vi.utils import first_sel
from NeoVintageous.vi.utils import gluing_undo_groups
from NeoVintageous.vi.utils import IrreversibleTextCommand
from NeoVintageous.vi.utils import is_view
from NeoVintageous.vi.utils import modes
from NeoVintageous.vi.utils import R
from NeoVintageous.vi.utils import regions_transformer
from NeoVintageous.vi.utils import resolve_insertion_point_at_b
from NeoVintageous.lib.sublime_ext import SublimeWindowAPI

_logger = PluginLogger(__name__)


class _vi_g_big_u(ViTextCommandBase):
    '''
    Command: gU
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).upper())
            # Reverse the resulting region so that _enter_normal_mode
            # collapses the selection as we want it.
            return R(s.b, s.a)

        if mode not in (modes.INTERNAL_NORMAL,
                        modes.VISUAL,
                        modes.VISUAL_LINE,
                        modes.VISUAL_BLOCK):
            raise ValueError('bad mode: ' + mode)

        if motion is None and mode == modes.INTERNAL_NORMAL:
            raise ValueError('motion data required')

        if mode == modes.INTERNAL_NORMAL:
            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if self.has_sel_changed():
                regions_transformer(self.view, f)
            else:
                utils.blink()
        else:
                regions_transformer(self.view, f)

        self.enter_normal_mode(mode)


class _vi_gu(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).lower())
            # reverse the resulting region so that _enter_normal_mode collapses the
            # selection as we want it.
            return R(s.b, s.a)

        if mode not in (modes.INTERNAL_NORMAL,
                        modes.VISUAL,
                        modes.VISUAL_LINE,
                        modes.VISUAL_BLOCK):
            raise ValueError('bad mode: ' + mode)

        if motion is None and mode == modes.INTERNAL_NORMAL:
            raise ValueError('motion data required')

        if mode == modes.INTERNAL_NORMAL:
            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if self.has_sel_changed():
                regions_transformer(self.view, f)
            else:
                utils.blink()
        else:
                regions_transformer(self.view, f)

        self.enter_normal_mode(mode)


class _vi_gq(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def wrap_command():
            hasWrapPlus = self.view.settings().get('WrapPlus.include_line_ending')
            if hasWrapPlus is None:
                return 'wrap_lines'
            else:
                return 'wrap_lines_plus'

        def reverse(view, s):
            return R(s.end(), s.begin())

        def shrink(view, s):
            if view.substr(s.b - 1) == '\n':
                return R(s.a, s.b - 1)
            return s

        wrap_lines = wrap_command()

        if mode in (modes.VISUAL, modes.VISUAL_LINE):
            # TODO: ST seems to always reformat whole paragraphs with
            #       'wrap_lines'.
            regions_transformer(self.view, shrink)
            regions_transformer(self.view, reverse)
            self.view.run_command(wrap_lines)
            self.enter_normal_mode(mode)
            return

        elif mode == modes.INTERNAL_NORMAL:
            if motion is None:
                raise ValueError('motion data required')

            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if self.has_sel_changed():
                self.save_sel()
                self.view.run_command(wrap_lines)
                self.view.sel().clear()
                self.view.sel().add_all(self.old_sel)
            else:
                utils.blink()

            self.enter_normal_mode(mode)

        else:
            raise ValueError('bad mode: ' + mode)


class _vi_u(ViWindowCommandBase):
    '''
    Undoes last change.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: surely must accept a mode?
    def run(self, count=1):
        for i in range(count):
            self._view.run_command('undo')

        if self._view.has_non_empty_selection_region():
            def reverse(view, s):
                return R(s.end(), s.begin())

            # TODO: xpos is misaligned after this.
            regions_transformer(self._view, reverse)
            # FIXME: why from modes.VISUAL?
            self.window.run_command('_enter_normal_mode', {
                    'mode': modes.VISUAL
                    })

        # If we yy, then u, we might end up with outlined regions if we
        # don't erase them here, because ST will restore them when undoing.
        self._view.erase_regions('vi_yy_target')


class _vi_ctrl_r(ViWindowCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1, mode=None):
        for i in range(count):
            self._view.run_command('redo')

        self.correct_xpos()

    # XXX: make this a global 'service'?
    # XXX: In fact, this may indicate that the redone command is at fault. For example, it seems
    # that de near EOL does not adjust xpos as it should. In summary: we need to revise commands
    # and probably remove this here.
    def correct_xpos(self):
        def f(view, s):
            if (view.substr(s.b) == '\n' and not view.line(s.b).empty()):
                return R(s.b - 1)
            return s

        regions_transformer(self._view, f)


class _vi_a(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None):
        def f(view, s):
            if view.substr(s.b) != '\n' and s.b < view.size():
                return R(s.b + 1)
            return s

        state = State(self.view)
        # Abort if the *actual* mode is insert mode. This prevents
        # _vi_a from adding spaces between text fragments when used with a
        # count, as in 5aFOO. In that case, we only need to run 'a' the first
        # time, not for every iteration.
        if state.mode == modes.INSERT:
            return

        if mode is None:
            raise ValueError('mode required')
        # TODO: We should probably not define the keys for these modes
        # in the first place.
        elif mode != modes.INTERNAL_NORMAL:
            return

        regions_transformer(self.view, f)
        # TODO(guillermooo): derive this class from ViTextCommandBase ???
        self.view.window().run_command('_enter_insert_mode', {'mode': mode,
            'count': state.normal_insert_count})


class _vi_c(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _can_yank = True
    _populates_small_delete_register = True

    def run(self, edit, count=1, mode=None, motion=None, register=None):
        def compact(view, s):
            if view.substr(s).strip():
                if s.b > s.a:
                    pt = utils.previous_non_white_space_char(
                            view, s.b - 1, white_space=' \t\n')
                    return R(s.a, pt + 1)
                pt = utils.previous_non_white_space_char(
                        view, s.a - 1, white_space=' \t\n')
                return R(pt + 1, s.b)
            return s

        if mode is None:
            raise ValueError('mode required')

        if (mode == modes.INTERNAL_NORMAL) and (motion is None):
            raise ValueError('motion required')

        self.save_sel()

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])

            # Vim ignores trailing white space for c. XXX Always?
            if mode == modes.INTERNAL_NORMAL:
                regions_transformer(self.view, compact)

            if not self.has_sel_changed():
                self.enter_insert_mode(mode)
                return

            # If we ci' and the target is an empty pair of quotes, we should
            # not delete anything.
            # FIXME: This will not work well with multiple selections.
            if all(s.empty() for s in self.view.sel()):
                self.enter_insert_mode(mode)
                return

        self.state.registers.yank(self, register)

        self.view.run_command('right_delete')

        self.enter_insert_mode(mode)


class _enter_normal_mode(ViTextCommandBase):
    """
    The equivalent of pressing the Esc key in Vim.

    @mode
      The mode we're coming from, which should still be the current mode.

    @from_init
      Whether _enter_normal_mode has been called from _init_vintageous. This
      is important to know in order to not hide output panels when the user
      is only navigating files or clicking around, not pressing Esc.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, from_init=False):
        state = self.state

        self.view.window().run_command('hide_auto_complete')
        self.view.window().run_command('hide_overlay')

        if ((not from_init and (mode == modes.NORMAL) and not state.sequence) or
             not is_view(self.view)):
            # When _enter_normal_mode is requested from _init_vintageous, we
            # should not hide output panels; hide them only if the user
            # pressed Esc and we're not cancelling partial state data, or if a
            # panel has the focus.
            # XXX: We are assuming that state.sequence will always be empty
            #      when we do the check above. Is that so?
            # XXX: The 'not is_view(self.view)' check above seems to be
            #      redundant, since those views should be ignored by
            #      NeoVintageous altogether.
            if len(self.view.sel()) < 2:
                # don't hide panel if multiple cursors
                # if not from_init and getattr(self.view, 'settings') is None:
                if not from_init:
                    self.view.window().run_command('hide_panel', {'cancel': True})

        self.view.settings().set('command_mode', True)
        self.view.settings().set('inverse_caret_state', True)

        # Exit replace mode.
        self.view.set_overwrite_status(False)

        state.enter_normal_mode()
        # XXX: st bug? if we don't do this, selections won't be redrawn
        self.view.run_command('_enter_normal_mode_impl', {'mode': mode})

        if state.glue_until_normal_mode and not state.processing_notation:
            if self.view.is_dirty():
                self.view.window().run_command('glue_marked_undo_groups')
                # We're exiting from insert mode or replace mode. Capture
                # the last native command as repeat data.
                state.repeat_data = ('native', self.view.command_history(0)[:2], mode, None)
                # Required here so that the macro gets recorded.
                state.glue_until_normal_mode = False
                state.add_macro_step(*self.view.command_history(0)[:2])
                state.add_macro_step('_enter_normal_mode', {'mode': mode,
                                     'from_init': from_init})
            else:
                state.add_macro_step('_enter_normal_mode', {'mode': mode,
                                     'from_init': from_init})
                self.view.window().run_command('unmark_undo_groups_for_gluing')
                state.glue_until_normal_mode = False

        if mode == modes.INSERT and int(state.normal_insert_count) > 1:
            state.enter_insert_mode()
            # TODO: Calculate size the view has grown by and place the caret
            # after the newly inserted text.
            sels = list(self.view.sel())
            self.view.sel().clear()
            new_sels = [R(s.b + 1) if self.view.substr(s.b) != '\n'
                                                else s
                                                for s in sels]
            self.view.sel().add_all(new_sels)
            times = int(state.normal_insert_count) - 1
            state.normal_insert_count = '1'
            self.view.window().run_command('_vi_dot', {
                                'count': times,
                                'mode': mode,
                                'repeat_data': state.repeat_data,
                                })
            self.view.sel().clear()
            self.view.sel().add_all(new_sels)

        state.update_xpos(force=True)
        sublime.status_message('')


class _enter_normal_mode_impl(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None):
        def f(view, s):
            _logger.info(
                '[_enter_normal_mode_impl] entering normal mode from {0}'
                .format(mode))
            if mode == modes.INSERT:
                if view.line(s.b).a != s.b:
                    return R(s.b - 1)

                return R(s.b)

            if mode == modes.INTERNAL_NORMAL:
                return R(s.b)

            if mode == modes.VISUAL:
                if s.a < s.b:
                    pt = s.b - 1
                    if view.line(pt).empty():
                        return R(pt)
                    if view.substr(pt) == '\n':
                        pt -= 1
                    return R(pt)
                return R(s.b)

            if mode in (modes.VISUAL_LINE, modes.VISUAL_BLOCK):
                # save selections for gv
                # But only if there are non-empty sels. We might be in visual
                # mode and not have non-empty sels because we've just existed
                # from an action.
                if self.view.has_non_empty_selection_region():
                    self.view.add_regions('visual_sel', list(self.view.sel()))

                if s.a < s.b:
                    pt = s.b - 1
                    if (view.substr(pt) == '\n') and not view.line(pt).empty():
                        pt -= 1
                    return R(pt)
                else:
                    return R(s.b)

            if mode == modes.SELECT:
                return R(s.begin())

            return R(s.b)

        if mode == modes.UNKNOWN:
            return

        if (len(self.view.sel()) > 1) and (mode == modes.NORMAL):
            sel = self.view.sel()[0]
            self.view.sel().clear()
            self.view.sel().add(sel)

        regions_transformer(self.view, f)

        self.view.erase_regions('vi_search')
        self.view.run_command('_vi_adjust_carets', {'mode': mode})


class _enter_select_mode(ViWindowCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, mode=None, count=1):
        self.state.enter_select_mode()

        view = self.window.active_view()

        # If there are no visual selections, do some work work for the user.
        if not view.has_non_empty_selection_region():
            self.window.run_command('find_under_expand')

        state = State(view)
        state.display_status()


class _enter_insert_mode(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        self.view.settings().set('inverse_caret_state', False)
        self.view.settings().set('command_mode', False)

        self.state.enter_insert_mode()
        self.state.normal_insert_count = str(count)
        self.state.display_status()


class _enter_visual_mode(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None):
        state = self.state

        # TODO(guillermooo): If all selections are non-zero-length, we may be
        # looking at a pseudo-visual selection, like the ones that are
        # created pressing Alt+Enter when using ST's built-in search dialog.
        # What shall we really do in that case?
        # XXX: In response to the above, we would probably already be in
        # visual mode, but we should double-check that.
        if state.mode == modes.VISUAL:
            self.view.run_command('_enter_normal_mode', {'mode': mode})
            return

        self.view.run_command('_enter_visual_mode_impl', {'mode': mode})

        if any(s.empty() for s in self.view.sel()):
            return

        # Sometimes we'll call this command without the global state knowing
        # its metadata. For example, when shift-clicking with the mouse to
        # create visual selections. Always update xpos to cover this case.
        state.update_xpos(force=True)
        state.enter_visual_mode()
        state.display_status()


class _enter_visual_mode_impl(ViTextCommandBase):
    """
    Transforms the view's selections. We don't do this inside the
    EnterVisualMode window command because ST seems to neglect to repaint the
    selections. (bug?)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None):
        def f(view, s):
            if mode == modes.VISUAL_LINE:
                return R(s.a, s.b)
            else:
                if s.empty() and (s.b == self.view.size()):
                    utils.blink()
                    return s

                # Extending from s.a to s.b because we may be looking at
                # selections with len>0. For example, if it's been created
                # using the mouse. Normally, though, the selection will be
                # empty when we reach here.
                end = s.b
                # Only extend .b by 1 if we're looking at empty sels.
                if not view.has_non_empty_selection_region():
                    end += 1
                return R(s.a, end)

        regions_transformer(self.view, f)


class _enter_visual_line_mode(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None):

        state = self.state
        if state.mode == modes.VISUAL_LINE:
            self.view.run_command('_enter_normal_mode', {'mode': mode})
            return

        # FIXME: 'V' from normal mode sets mode to internal normal.
        if mode in (modes.NORMAL, modes.INTERNAL_NORMAL):
            # Abort if we are at EOF -- no newline char to hold on to.
            if any(s.b == self.view.size() for s in self.view.sel()):
                utils.blink()
                return

        self.view.run_command('_enter_visual_line_mode_impl', {'mode': mode})
        state.enter_visual_line_mode()
        state.display_status()


class _enter_visual_line_mode_impl(ViTextCommandBase):
    """
    Transforms the view's selections.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None):
        def f(view, s):
            if mode == modes.VISUAL:
                if s.a < s.b:
                    if view.substr(s.b - 1) != '\n':
                        return R(view.line(s.a).a,
                                              view.full_line(s.b - 1).b)
                    else:
                        return R(view.line(s.a).a, s.b)
                else:
                    if view.substr(s.a - 1) != '\n':
                        return R(view.full_line(s.a - 1).b,
                                              view.line(s.b).a)
                    else:
                        return R(s.a, view.line(s.b).a)
            else:
                return view.full_line(s.b)

        regions_transformer(self.view, f)


class _enter_replace_mode(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit):
        def f(view, s):
            return R(s.b)

        state = self.state
        state.settings.view['command_mode'] = False
        state.settings.view['inverse_caret_state'] = False
        state.view.set_overwrite_status(True)
        state.enter_replace_mode()
        regions_transformer(self.view, f)
        state.display_status()
        state.reset()


# TODO: Remove this command once we don't need it any longer.
class ToggleMode(ViWindowCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        value = self.window.active_view().settings().get('command_mode')
        self.window.active_view().settings().set('command_mode', not value)
        self.window.active_view().settings().set('inverse_caret_state', not value)
        print("command_mode status:", not value)

        state = self.state
        if not self.window.active_view().settings().get('command_mode'):
            state.mode = modes.INSERT
        sublime.status_message('command mode status: %s' % (not value))


class ProcessNotation(ViWindowCommandBase):
    """
    Runs sequences of keys representing Vim commands.

    For example: fngU5l

    @keys
        Key sequence to be run.
    @repeat_count
        Count to be applied when repeating through the '.' command.
    @check_user_mappings
        Whether user mappings should be consulted to expand key sequences.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, keys, repeat_count=None, check_user_mappings=True):
        state = self.state
        _logger.info("[ProcessNotation] seq received: {0} mode: {1}"
                                                    .format(keys, state.mode))
        initial_mode = state.mode
        # Disable interactive prompts. For example, to supress interactive
        # input collection in /foo<CR>.
        state.non_interactive = True

        # First, run any motions coming before the first action. We don't keep
        # these in the undo stack, but they will still be repeated via '.'.
        # This ensures that undoing will leave the caret where the  first
        # editing action started. For example, 'lldl' would skip 'll' in the
        # undo history, but store the full sequence for '.' to use.
        leading_motions = ''
        for key in KeySequenceTokenizer(keys).iter_tokenize():
            self.window.run_command('press_key', {
                                'key': key,
                                'do_eval': False,
                                'repeat_count': repeat_count,
                                'check_user_mappings': check_user_mappings
                                })
            if state.action:
                # The last key press has caused an action to be primed. That
                # means there are no more leading motions. Break out of here.
                _logger.info('[ProcessNotation] first action found in {0}'
                                                      .format(state.sequence))
                state.reset_command_data()
                if state.mode == modes.OPERATOR_PENDING:
                    state.mode = modes.NORMAL
                break

            elif state.runnable():
                # Run any primed motion.
                leading_motions += state.sequence
                state.eval()
                state.reset_command_data()

            else:
                # XXX: When do we reach here?
                state.eval()

        if state.must_collect_input:
            # State is requesting more input, so this is the last command in
            # the sequence and it needs more input.
            self.collect_input()
            return

        # Strip the already run commands.
        if leading_motions:
            if ((len(leading_motions) == len(keys)) and (not state.must_collect_input)):
                state.non_interactive = False
                return

            _logger.info('[ProcessNotation] original seq/leading motions: {0}/{1}'
                                               .format(keys, leading_motions))
            keys = keys[len(leading_motions):]
            _logger.info('[ProcessNotation] seq stripped to {0}'.format(keys))

        if not (state.motion and not state.action):
            with gluing_undo_groups(self.window.active_view(), state):
                try:
                    for key in KeySequenceTokenizer(keys).iter_tokenize():
                        if key.lower() == key_names.ESC:
                            # XXX: We should pass a mode here?
                            self.window.run_command('_enter_normal_mode')
                            continue

                        elif state.mode not in (modes.INSERT, modes.REPLACE):
                            self.window.run_command('press_key', {
                                    'key': key,
                                    'repeat_count': repeat_count,
                                    'check_user_mappings': check_user_mappings
                                    })
                        else:
                            self.window.run_command('insert', {
                                'characters': utils.translate_char(key)
                            })
                    if not state.must_collect_input:
                        return
                finally:
                    state.non_interactive = False
                    # Ensure we set the full command for '.' to use, but don't
                    # store '.' alone.
                    if (leading_motions + keys) not in ('.', 'u', '<C-r>'):
                            state.repeat_data = (
                                        'vi', (leading_motions + keys),
                                        initial_mode, None)

        # We'll reach this point if we have a command that requests input
        # whose input parser isn't satistied. For example, `/foo`. Note that
        # `/foo<CR>`, on the contrary, would have satisfied the parser.
        _logger.info('[ProcessNotation] unsatisfied parser: {0} {1}'
                                          .format(state.action, state.motion))
        if (state.action and state.motion):
            # We have a parser an a motion that can collect data. Collect data
            # interactively.
            motion_data = state.motion.translate(state) or None

            if motion_data is None:
                utils.blink()
                state.reset_command_data()
                return

            motion_data['motion_args']['default'] = state.motion._inp
            self.window.run_command(motion_data['motion'],
                                    motion_data['motion_args'])
            return

        self.collect_input()

    def collect_input(self):
        try:
            command = None
            if self.state.motion and self.state.action:
                if self.state.motion.accept_input:
                    command = self.state.motion
                else:
                    command = self.state.action
            else:
                command = self.state.action or self.state.motion

            parser_def = command.input_parser
            _logger.info('[ProcessNotation] last attemp to collect input: {0}'
                                                  .format(parser_def.command))
            if parser_def.interactive_command:
                self.window.run_command(parser_def.interactive_command,
                                        {parser_def.input_param: command._inp}
                                       )
        except IndexError:
            _logger.info('[NeoVintageous] could not find a command to collect'
                           'more user input')
            utils.blink()
        finally:
            self.state.non_interactive = False


class PressKey(ViWindowCommandBase):
    """
    Core command. It interacts with the global state each time a key is
    pressed.

    @key
        Key pressed.
    @repeat_count
        Count to be used when repeating through the '.' command.
    @do_eval
        Whether to evaluate the global state when it's in a runnable
        state. Most of the time, the default value of `True` should be
        used. Set to `False` when you want to manually control
        the global state's evaluation. For example, this is what the
        PressKey command does.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, key, repeat_count=None, do_eval=True, check_user_mappings=True):
        _logger.info("[PressKey] pressed: {0}".format(key))

        state = self.state

        # If the user has made selections with the mouse, we may be in an
        # inconsistent state. Try to remedy that.
        if (state.view.has_non_empty_selection_region() and
            state.mode not in (modes.VISUAL,
                               modes.VISUAL_LINE,
                               modes.VISUAL_BLOCK,
                               modes.SELECT)):
                _init_vintageous(state.view)

        if key.lower() == '<esc>':
            self.window.run_command('_enter_normal_mode', {'mode': state.mode})
            state.reset_command_data()
            return

        state.sequence += key
        state.display_status()

        if state.must_capture_register_name:
            state.register = key
            state.partial_sequence = ''
            return

        # if capturing input, we shall not pass this point
        if state.must_collect_input:
            state.process_user_input2(key)
            if state.runnable():
                _logger.info('[PressKey] state holds a complete command.')
                if do_eval:
                    _logger.info('[PressKey] evaluating complete command')
                    state.eval()
                    state.reset_command_data()
            return

        if repeat_count:
            state.action_count = str(repeat_count)

        if self.handle_counts(key, repeat_count):
            return

        state.partial_sequence += key
        _logger.info("[PressKey] sequence {0}".format(state.sequence))
        _logger.info("[PressKey] partial sequence {0}".format(state.partial_sequence))

        # key_mappings = KeyMappings(self.window.active_view())
        key_mappings = Mappings(state)
        if check_user_mappings and key_mappings.incomplete_user_mapping():
            _logger.info("[PressKey] incomplete user mapping: {0}".format(state.partial_sequence))
            # for example, we may have typed 'aa' and there's an 'aaa' mapping.
            # we need to keep collecting input.
            return

        _logger.info('[PressKey] getting cmd for seq/partial seq in (mode): {0}/{1} ({2})'.format(state.sequence,
                                                                                                    state.partial_sequence,
                                                                                                    state.mode))
        command = key_mappings.resolve(check_user_mappings=check_user_mappings)

        if isinstance(command, cmd_defs.ViOpenRegister):
            _logger.info('[PressKey] requesting register name')
            state.must_capture_register_name = True
            return

        # XXX: This doesn't seem to be correct. If we are in OPERATOR_PENDING mode, we should
        # most probably not have to wipe the state.
        if isinstance(command, mappings.Mapping):
            if do_eval:
                new_keys = command.mapping
                if state.mode == modes.OPERATOR_PENDING:
                    command_name = command.mapping
                    new_keys = state.sequence[:-len(state.partial_sequence)] + command.mapping
                reg = state.register
                acount = state.action_count
                mcount = state.motion_count
                state.reset_command_data()
                state.register = reg
                state.motion_count = mcount
                state.action_count = acount
                state.mode = modes.NORMAL
                _logger.info('[PressKey] running user mapping {0} via process_notation starting in mode {1}'.format(new_keys, state.mode))
                self.window.run_command('process_notation', {'keys': new_keys, 'check_user_mappings': False})
            return

        if isinstance(command, cmd_defs.ViOpenNameSpace):
            # Keep collecing input to complete the sequence. For example, we
            # may have typed 'g'.
            _logger.info("[PressKey] opening namespace: {0}".format(state.partial_sequence))
            return

        elif isinstance(command, cmd_base.ViMissingCommandDef):
            bare_seq = to_bare_command_name(state.sequence)

            if state.mode == modes.OPERATOR_PENDING:
                # We might be looking at a command like 'dd'. The first 'd' is
                # mapped for normal mode, but the second is missing in
                # operator pending mode, so we get a missing command. Try to
                # build the full command now.
                #
                # Exclude user mappings, since they've already been given a
                # chance to evaluate.
                command = key_mappings.resolve(sequence=bare_seq,
                                                   mode=modes.NORMAL,
                                                   check_user_mappings=False)
            else:
                command = key_mappings.resolve(sequence=bare_seq)

            if isinstance(command, cmd_base.ViMissingCommandDef):
                _logger.info('[PressKey] unmapped sequence: {0}'.format(state.sequence))
                utils.blink()
                state.mode = modes.NORMAL
                state.reset_command_data()
                return

        if (state.mode == modes.OPERATOR_PENDING and
            isinstance(command, cmd_defs.ViOperatorDef)):
                # TODO: This may be unreachable code by now. ???
                # we're expecting a motion, but we could still get an action.
                # For example, dd, g~g~ or g~~
                # remove counts
                action_seq = to_bare_command_name(state.sequence)
                _logger.info('[PressKey] action seq: {0}'.format(action_seq))
                command = key_mappings.resolve(sequence=action_seq, mode=modes.NORMAL)
                # TODO: Make _missing a command.
                if isinstance(command, cmd_base.ViMissingCommandDef):
                    _logger.info("[PressKey] unmapped sequence: {0}".format(state.sequence))
                    state.reset_command_data()
                    return

                if not command['motion_required']:
                    state.mode = modes.NORMAL

        state.set_command(command)

        _logger.info("[PressKey] '{0}' mapped to '{1}'".format(state.partial_sequence, command))

        if state.mode == modes.OPERATOR_PENDING:
            state.reset_partial_sequence()

        if do_eval:
            state.eval()

    def handle_counts(self, key, repeat_count):
        """
        Returns `True` if the processing of the current key needs to stop.
        """
        state = State(self.window.active_view())
        if not state.action and key.isdigit():
            if not repeat_count and (key != '0' or state.action_count):
                _logger.info('[PressKey] action count digit: {0}'.format(key))
                state.action_count += key
                return True

        if (state.action and (state.mode == modes.OPERATOR_PENDING) and
            key.isdigit()):
                if not repeat_count and (key != '0' or state.motion_count):
                    _logger.info('[PressKey] motion count digit: {0}'.format(key))
                    state.motion_count += key
                    return True


class _vi_dot(ViWindowCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, mode=None, count=None, repeat_data=None):
        state = self.state
        state.reset_command_data()

        if state.mode == modes.INTERNAL_NORMAL:
            state.mode = modes.NORMAL

        if repeat_data is None:
            _logger.info('[_vi_dot] nothing to repeat')
            return

        # TODO: Find out if the user actually meant '1'.
        if count and count == 1:
            count = None

        type_, seq_or_cmd, old_mode, visual_data = repeat_data
        _logger.info(
            '[_vi_dot] type: {0} seq or cmd: {1} old mode: {2}'
            .format(type_, seq_or_cmd, old_mode))

        if visual_data and (mode != modes.VISUAL):
            state.restore_visual_data(visual_data)
        elif not visual_data and (mode == modes.VISUAL):
            # Can't repeat normal mode commands in visual mode.
            utils.blink()
            return
        elif mode not in (modes.VISUAL, modes.VISUAL_LINE, modes.NORMAL,
                          modes.INTERNAL_NORMAL, modes.INSERT):
            utils.blink()
            return

        if type_ == 'vi':
            self.window.run_command('process_notation', {'keys': seq_or_cmd,
                                                   'repeat_count': count})
        elif type_ == 'native':
            sels = list(self.window.active_view().sel())
            # FIXME: We're not repeating as we should. It's the motion that
            # should receive this count.
            for i in range(count or 1):
                self.window.run_command(*seq_or_cmd)
            # FIXME: What happens in visual mode?
            self.window.active_view().sel().clear()
            self.window.active_view().sel().add_all(sels)
        else:
            raise ValueError('bad repeat data')

        self.window.run_command('_enter_normal_mode', {'mode': mode})
        state.repeat_data = repeat_data
        state.update_xpos()


class _vi_dd(ViTextCommandBase):

    _can_yank = True
    _yanks_linewise = True
    _populates_small_delete_register = False
    _synthetize_new_line_at_eof = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, register='"'):
        def do_motion(view, s):
            if mode != modes.INTERNAL_NORMAL:
                return s

            return units.lines(view, s, count)

        def do_action(view, s):
            if mode != modes.INTERNAL_NORMAL:
                return s

            view.erase(edit, s)
            pt = utils.next_non_white_space_char(view, view.line(s.a).a,
                white_space=' \t')
            return R(pt)

        def set_sel():
            old = [s.a for s in list(self.view.sel())]
            self.view.sel().clear()
            new = [utils.next_non_white_space_char(self.view, pt) for pt in old]
            self.view.sel().add_all([R(pt) for pt in new])

        regions_transformer(self.view, do_motion)
        self.state.registers.yank(self, register, operation='delete')
        self.view.run_command('right_delete')
        set_sel()
        # TODO(guillermooo): deleting last line leaves the caret at \n


class _vi_cc(ViTextCommandBase):

    _can_yank = True
    _yanks_linewise = True
    _populates_small_delete_register = False
    _synthetize_new_line_at_eof = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, register='"'):
        def motion(view, s):
            if mode != modes.INTERNAL_NORMAL:
                return s

            if view.line(s.b).empty():
                return s

            return units.inner_lines(view, s, count)

        regions_transformer(self.view, motion)
        self.state.registers.yank(self, register)
        if not all(s.empty() for s in self.view.sel()):
            self.view.run_command('right_delete')
        self.enter_insert_mode(mode)
        self.set_xpos(self.state)


class _vi_visual_o(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            # FIXME: In Vim, o doesn't work in modes.VISUAL_LINE, but ST can't move the caret while
            # in modes.VISUAL_LINE, so we enable this for convenience. Change when/if ST can move
            # the caret while in modes.VISUAL_LINE.
            if mode in (modes.VISUAL, modes.VISUAL_LINE):
                return R(s.b, s.a)
            return s

        regions_transformer(self.view, f)
        self.view.show(self.view.sel()[0].b, False)


# TODO: is this really a text command?
class _vi_yy(ViTextCommandBase):

    _can_yank = True
    _synthetize_new_line_at_eof = True
    _yanks_linewise = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):
            if count > 1:
                row, col = self.view.rowcol(s.b)
                end = view.text_point(row + count - 1, 0)
                return R(view.line(s.a).a, view.full_line(end).b)

            if view.line(s.b).empty():
                return R(s.b, min(view.size(), s.b + 1))
            return view.full_line(s.b)

        def restore():
            self.view.sel().clear()
            self.view.sel().add_all(list(self.old_sel))

        if mode != modes.INTERNAL_NORMAL:
            utils.blink()
            raise ValueError('wrong mode')

        self.save_sel()
        regions_transformer(self.view, select)

        state = self.state
        self.outline_target()
        state.registers.yank(self, register)
        restore()
        self.enter_normal_mode(mode)


class _vi_y(ViTextCommandBase):

    _can_yank = True
    _populates_small_delete_register = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        def f(view, s):
            return R(s.end(), s.begin())

        if mode == modes.INTERNAL_NORMAL:
            if motion is None:
                raise ValueError('bad args')
            self.view.run_command(motion['motion'], motion['motion_args'])
            self.outline_target()

        elif mode not in (modes.VISUAL, modes.VISUAL_LINE, modes.VISUAL_BLOCK):
            return

        state = self.state
        state.registers.yank(self, register)
        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_d(ViTextCommandBase):

    _can_yank = True
    _populates_small_delete_register = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        def reverse(view, s):
            return R(s.end(), s.begin())

        if mode not in (modes.INTERNAL_NORMAL, modes.VISUAL,
                        modes.VISUAL_LINE):
            raise ValueError('wrong mode')

        if mode == modes.INTERNAL_NORMAL and not motion:
            raise ValueError('missing motion')

        if motion:
            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            # The motion has failed, so abort.
            if not self.has_sel_changed():
                utils.blink()
                self.enter_normal_mode(mode)
                return

            # If the target's an empty pair of quotes, don't delete.
            # FIXME: This won't work well with multiple sels.
            if all(s.empty() for s in self.view.sel()):
                self.enter_normal_mode(mode)
                return

        state = self.state
        state.registers.yank(self, register, operation='delete')

        self.view.run_command('left_delete')
        self.view.run_command('_vi_adjust_carets')

        self.enter_normal_mode(mode)

        # XXX: abstract this out for all types of selections.
        def advance_to_text_start(view, s):
            pt = utils.next_non_white_space_char(self.view, s.b)
            return R(pt)

        if mode == modes.INTERNAL_NORMAL:
            regions_transformer(self.view, advance_to_text_start)


class _vi_big_a(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == modes.VISUAL_BLOCK:
                if self.view.substr(s.b - 1) == '\n':
                    return R(s.end() - 1)
                return R(s.end())

            elif mode == modes.VISUAL:
                pt = s.b
                if self.view.substr(s.b - 1) == '\n':
                    pt -= 1
                if s.a > s.b:
                    pt = view.line(s.a).a
                return R(pt)

            elif mode == modes.VISUAL_LINE:
                if s.a < s.b:
                    if s.b < view.size():
                        return R(s.end() - 1)
                    return R(s.end())
                return R(s.begin())

            elif mode != modes.INTERNAL_NORMAL:
                return s

            if s.b == view.size():
                return s

            hard_eol = self.view.line(s.b).end()
            return R(hard_eol, hard_eol)

        if mode == modes.SELECT:
            self.view.window().run_command('find_all_under')
            return

        regions_transformer(self.view, f)

        self.enter_insert_mode(mode)


class _vi_big_i(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None):
        def f(view, s):
            if mode == modes.VISUAL_BLOCK:
                return R(s.begin())
            elif mode == modes.VISUAL:
                pt = view.line(s.a).a
                if s.a > s.b:
                    pt = s.b
                return R(pt)
            elif mode == modes.VISUAL_LINE:
                line = view.line(s.a)
                pt = utils.next_non_white_space_char(view, line.a)
                return R(pt)
            elif mode != modes.INTERNAL_NORMAL:
                return s
            line = view.line(s.b)
            pt = utils.next_non_white_space_char(view, line.a)
            return R(pt, pt)

        regions_transformer(self.view, f)

        self.enter_insert_mode(mode)


class _vi_m(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, character=None):
        state = self.state
        state.marks.add(character, self.view)

        # TODO: What if we are in visual mode?
        self.enter_normal_mode(mode)


class _vi_quote(ViTextCommandBase):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, character=None, count=1):
        def f(view, s):
            if mode == modes.VISUAL:
                if s.a <= s.b:
                    if address.b < s.b:
                        return R(s.a + 1, address.b)
                    else:
                        return R(s.a, address.b)
                else:
                    return R(s.a + 1, address.b)

            elif mode == modes.NORMAL:
                return address

            elif mode == modes.INTERNAL_NORMAL:
                if s.a < address.a:
                    return R(view.full_line(s.b).a,
                                          view.line(address.b).b)
                return R(view.full_line(s.b).b,
                                      view.line(address.b).a)

            return s

        state = self.state
        address = state.marks.get_as_encoded_address(character)

        if address is None:
            return

        if isinstance(address, str):
            if not address.startswith('<command'):
                self.view.window().open_file(address, sublime.ENCODED_POSITION)
            else:
                # We get a command in this form: <command _vi_double_quote>
                self.view.run_command(address.split(' ')[1][:-1])
            return

        regions_transformer(self.view, f)

        if not self.view.visible_region().intersects(address):
            self.view.show_at_center(address)


class _vi_backtick(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None, character=None):
        def f(view, s):
            if mode == modes.VISUAL:
                if s.a <= s.b:
                    if address.b < s.b:
                        return R(s.a + 1, address.b)
                    else:
                        return R(s.a, address.b)
                else:
                    return R(s.a + 1, address.b)
            elif mode == modes.NORMAL:
                return address
            elif mode == modes.INTERNAL_NORMAL:
                return R(s.a, address.b)

            return s

        state = self.state
        address = state.marks.get_as_encoded_address(character, exact=True)

        if address is None:
            return

        if isinstance(address, str):
            if not address.startswith('<command'):
                self.view.window().open_file(address, sublime.ENCODED_POSITION)
            return

        # This is a motion in a composite command.
        regions_transformer(self.view, f)


class _vi_quote_quote(IrreversibleTextCommand):
    next_command = 'jump_back'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        current = _vi_quote_quote.next_command
        self.view.window().run_command(current)
        _vi_quote_quote.next_command = ('jump_forward' if (current ==
                                                            'jump_back')
                                                       else 'jump_back')


class _vi_big_d(ViTextCommandBase):

    _can_yank = True
    _synthetize_new_line_at_eof = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        eol = view.line(s.b).b
                        return R(s.b, eol)
                    return s
            return s

        self.save_sel()
        regions_transformer(self.view, f)

        state = self.state
        state.registers.yank(self)

        self.view.run_command('left_delete')

        self.enter_normal_mode(mode)


class _vi_big_c(ViTextCommandBase):

    _can_yank = True
    _synthetize_new_line_at_eof = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        eol = view.line(s.b).b
                        return R(s.b, eol)
                    return s
            return s

        self.save_sel()
        regions_transformer(self.view, f)

        state = self.state
        state.registers.yank(self)

        empty = [s for s in list(self.view.sel()) if s.empty()]
        self.view.add_regions('vi_empty_sels', empty)
        for r in empty:
            self.view.sel().subtract(r)

        self.view.run_command('right_delete')

        self.view.sel().add_all(self.view.get_regions('vi_empty_sels'))
        self.view.erase_regions('vi_empty_sels')

        self.enter_insert_mode(mode)


class _vi_big_s_action(ViTextCommandBase):

    _can_yank = True
    _synthetize_new_line_at_eof = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, register=None):
        def sel_line(view, s):
            if mode == modes.INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        eol = view.line(s.b).b
                        begin = view.line(s.b).a
                        begin = utils.next_non_white_space_char(view, begin, white_space=' \t')
                        return R(begin, eol)
                    return s
            return s

        regions_transformer(self.view, sel_line)

        state = self.state
        state.registers.yank(self, register)

        empty = [s for s in list(self.view.sel()) if s.empty()]
        self.view.add_regions('vi_empty_sels', empty)
        for r in empty:
            self.view.sel().subtract(r)

        self.view.run_command('right_delete')

        self.view.sel().add_all(self.view.get_regions('vi_empty_sels'))
        self.view.erase_regions('vi_empty_sels')
        self.view.run_command('reindent', {'force_indent': False})

        self.enter_insert_mode(mode)


class _vi_s(ViTextCommandBase):
    """
    Implementation of Vim's 's' action.
    """
    # Yank config data.
    _can_yank = True
    _populates_small_delete_register = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):
            if mode == modes.INTERNAL_NORMAL:
                if view.line(s.b).empty():
                    return R(s.b)
                return R(s.b, s.b + count)
            return R(s.begin(), s.end())

        if mode not in (modes.VISUAL,
                        modes.VISUAL_LINE,
                        modes.VISUAL_BLOCK,
                        modes.INTERNAL_NORMAL):
            # error?
            utils.blink()
            self.enter_normal_mode(mode)

        self.save_sel()

        regions_transformer(self.view, select)

        if not self.has_sel_changed() and mode == modes.INTERNAL_NORMAL:
            self.enter_insert_mode(mode)
            return

        state = self.state
        state.registers.yank(self, register)
        self.view.run_command('right_delete')

        self.enter_insert_mode(mode)


class _vi_x(ViTextCommandBase):

    """
    Implementation of Vim's x action.
    """
    _can_yank = True
    _populates_small_delete_register = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def line_end(self, pt):
        return self.view.line(pt).end()

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):
            nonlocal abort
            if mode == modes.INTERNAL_NORMAL:
                eol = utils.get_eol(view, s.b)
                return R(s.b, min(s.b + count, eol))
            if s.size() == 1:
                b = s.b - 1 if s.a < s.b else s.b
            return s

        if mode not in (modes.VISUAL,
                        modes.VISUAL_LINE,
                        modes.VISUAL_BLOCK,
                        modes.INTERNAL_NORMAL):
            # error?
            utils.blink()
            self.enter_normal_mode(mode)

        if mode == modes.INTERNAL_NORMAL:
            if all(self.view.line(s.b).empty() for s in self.view.sel()):
                utils.blink()
                return

        abort = False

        regions_transformer(self.view, select)

        if not abort:
            self.state.registers.yank(self, register)
            self.view.run_command('right_delete')
        self.enter_normal_mode(mode)


class _vi_r(ViTextCommandBase):

    _can_yank = True
    _synthetize_new_line_at_eof = True
    _populates_small_delete_register = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_replacement_text(self, char, r):
        frags = self.view.split_by_newlines(r)
        new_frags = []
        for fr in frags:
            new_frags.append(char * len(fr))
        return '\n'.join(new_frags)

    def run(self, edit, mode=None, count=1, register=None, char=None):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                pt = s.b + count
                text = self.make_replacement_text(char, R(s.a, pt))
                view.replace(edit, R(s.a, pt), text)

                if char == '\n':
                    return R(s.b + 1)
                else:
                    return R(s.b)

            if mode in (modes.VISUAL, modes.VISUAL_LINE, modes.VISUAL_BLOCK):
                ends_in_newline = (view.substr(s.end() - 1) == '\n')
                text = self.make_replacement_text(char, s)
                if ends_in_newline:
                    text += '\n'

                view.replace(edit, s, text)

                if char == '\n':
                    return R(s.begin() + 1)
                else:
                    return R(s.begin())

        if char is None:
            raise ValueError('bad parameters')
        char = utils.translate_char(char)

        self.state.registers.yank(self, register)
        regions_transformer(self.view, f)

        self.enter_normal_mode(mode)


class _vi_less_than_less_than(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=None):
        def motion(view, s):
            if mode != modes.INTERNAL_NORMAL:
                return s

            if count <= 1:
                return s

            a = utils.get_bol(view, s.a)
            pt = view.text_point(utils.row_at(view, a) + (count - 1), 0)
            return R(a, utils.get_eol(view, pt))

        def action(view, s):
            bol = utils.get_bol(view, s.begin())
            pt = utils.next_non_white_space_char(view, bol, white_space='\t ')
            return R(pt)

        regions_transformer(self.view, motion)
        self.view.run_command('unindent')
        regions_transformer(self.view, action)


class _vi_equal_equal(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            return R(s.begin())

        def select(view):
            s0 = utils.first_sel(self.view)
            end_row = utils.row_at(view, s0.b) + (count - 1)
            view.sel().clear()
            view.sel().add(R(s0.begin(), view.text_point(end_row, 1)))

        if count > 1:
            select(self.view)

        self.view.run_command('reindent', {'force_indent': False})
        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_greater_than_greater_than(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            bol = utils.get_bol(view, s.begin())
            pt = utils.next_non_white_space_char(view, bol, white_space='\t ')
            return R(pt)

        def select(view):
            s0 = utils.first_sel(view)
            end_row = utils.row_at(view, s0.b) + (count - 1)
            utils.replace_sel(view, R(s0.begin(), view.text_point(end_row, 1)))

        if count > 1:
            select(self.view)

        self.view.run_command('indent')
        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_greater_than(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return R(s.begin())

        def indent_from_begin(view, s, level=1):
            block = '\t' if not translate else ' ' * size
            self.view.insert(edit, s.begin(), block * level)
            return R(s.begin() + 1)

        if mode == modes.VISUAL_BLOCK:
            translate = self.view.settings().get('translate_tabs_to_spaces')
            size = self.view.settings().get('tab_size')
            indent = partial(indent_from_begin, level=count)

            regions_transformer_reversed(self.view, indent)
            regions_transformer(self.view, f)

            # Restore only the first sel.
            utils.replace_sel(self.view, utils.first_sel(self.view))
            self.enter_normal_mode(mode)
            return

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (modes.VISUAL, modes.VISUAL_LINE):
            utils.blink()
            return

        for i in range(count):
            self.view.run_command('indent')

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_less_than(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return R(s.begin())

        # Note: Vim does not unindent in visual block mode.

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (modes.VISUAL, modes.VISUAL_LINE):
            utils.blink()
            return

        for i in range(count):
            self.view.run_command('unindent')

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_equal(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return R(s.begin())

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (modes.VISUAL, modes.VISUAL_LINE):
            utils.blink()
            return

        self.view.run_command('reindent', {'force_indent': False})

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_big_o(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None):
        if mode == modes.INTERNAL_NORMAL:
            self.view.run_command('run_macro_file', {'file': 'res://Packages/Default/Add Line Before.sublime-macro'})

        self.enter_insert_mode(mode)


class _vi_o(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None):
        if mode == modes.INTERNAL_NORMAL:
            self.view.run_command('run_macro_file', {'file': 'res://Packages/Default/Add Line.sublime-macro'})

        self.enter_insert_mode(mode)


class _vi_big_x(ViTextCommandBase):

    _can_yank = True
    _populates_small_delete_register = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def line_start(self, pt):
        return self.view.line(pt).begin()

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):
            nonlocal abort
            if mode == modes.INTERNAL_NORMAL:
                if view.line(s.b).empty():
                    abort = True
                return R(s.b, max(s.b - count,
                                               self.line_start(s.b)))
            elif mode == modes.VISUAL:
                if s.a < s.b:
                    if view.line(s.b - 1).empty() and s.size() == 1:
                        abort = True
                    return R(view.full_line(s.b - 1).b,
                                          view.line(s.a).a)

                if view.line(s.b).empty() and s.size() == 1:
                    abort = True
                return R(view.line(s.b).a,
                                      view.full_line(s.a - 1).b)
            return R(s.begin(), s.end())

        abort = False

        regions_transformer(self.view, select)

        state = self.state
        state.registers.yank(self, register)

        if not abort:
            self.view.run_command('left_delete')

        self.enter_normal_mode(mode)


class _vi_big_p(ViTextCommandBase):
    _can_yank = True
    _synthetize_new_line_at_eof = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, register=None, count=1, mode=None):
        state = self.state

        if state.mode == modes.VISUAL:
            prev_text = state.registers.get_selected_text(self)

        if register:
            fragments = state.registers[register]
        else:
            # TODO: There should be a simpler way of getting the unnamed
            # register's content.
            fragments = state.registers['"']

        if state.mode == modes.VISUAL:
            # Populate registers with the text we're about to paste.
            state.registers['"'] = prev_text

        # TODO: Enable pasting to multiple selections.
        sel = list(self.view.sel())[0]
        text_block, linewise = self.merge(fragments)

        if mode == modes.INTERNAL_NORMAL:
            if not linewise:
                self.view.insert(edit, sel.a, text_block)
                self.view.sel().clear()
                pt = sel.a + len(text_block) - 1
                self.view.sel().add(R(pt))
            else:
                pt = self.view.line(sel.a).a
                self.view.insert(edit, pt, text_block)
                self.view.sel().clear()
                row = utils.row_at(self.view, pt)
                pt = self.view.text_point(row, 0)
                self.view.sel().add(R(pt))

        elif mode == modes.VISUAL:
            if not linewise:
                self.view.replace(edit, sel, text_block)
            else:
                pt = sel.a
                if text_block[0] != '\n':
                    text_block = '\n' + text_block
                self.view.replace(edit, sel, text_block)
                self.view.sel().clear()
                row = utils.row_at(self.view, pt + len(text_block))
                pt = self.view.text_point(row - 1, 0)
                self.view.sel().add(R(pt))
        else:
            return

        self.enter_normal_mode(mode=mode)

    def merge(self, fragments):
        """Merges a list of strings.

        Returns a block of text and a bool indicating whether it's a linewise
        block.
        """
        block = ''.join(fragments)
        if '\n' in fragments[0]:
            if block[-1] != '\n':
                return (block + '\n'), True
            return block, True
        return block, False


class _vi_p(ViTextCommandBase):

    _can_yank = True
    _synthetize_new_line_at_eof = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, register=None, count=1, mode=None):
        state = self.state
        register = register or '"'
        fragments = state.registers[register]
        if not fragments:
            print("NeoVintageous: Nothing in register \".")
            return

        if state.mode == modes.VISUAL:
            prev_text = state.registers.get_selected_text(self)
            state.registers['"'] = prev_text

        sels = list(self.view.sel())
        # If we have the same number of pastes and selections, map 1:1. Otherwise paste paste[0]
        # to all target selections.
        if len(sels) == len(fragments):
            sel_to_frag_mapped = zip(sels, fragments)
        else:
            sel_to_frag_mapped = zip(sels, [fragments[0],] * len(sels))

        # FIXME: Fix this mess. Separate linewise from charwise pasting.
        pasting_linewise = True
        offset = 0
        paste_locations = []
        for selection, fragment in reversed(list(sel_to_frag_mapped)):
            fragment = self.prepare_fragment(fragment)
            if fragment.startswith('\n'):
                # Pasting linewise...
                # If pasting at EOL or BOL, make sure we paste before the newline character.
                if (utils.is_at_eol(self.view, selection) or
                    utils.is_at_bol(self.view, selection)):
                    l = self.paste_all(edit, selection,
                                       self.view.line(selection.b).b,
                                       fragment,
                                       count)
                    paste_locations.append(l)
                else:
                    l = self.paste_all(edit, selection,
                                   self.view.line(selection.b - 1).b,
                                   fragment,
                                   count)
                    paste_locations.append(l)
            else:
                pasting_linewise = False
                # Pasting charwise...
                # If pasting at EOL, make sure we don't paste after the newline character.
                if self.view.substr(selection.b) == '\n':
                    l = self.paste_all(edit, selection, selection.b + offset,
                                   fragment, count)
                    paste_locations.append(l)
                else:
                    l = self.paste_all(edit, selection, selection.b + offset + 1,
                                   fragment, count)
                    paste_locations.append(l)
                offset += len(fragment) * count

        if pasting_linewise:
            self.reset_carets_linewise(paste_locations)
        else:
            self.reset_carets_charwise(paste_locations, len(fragment))

        self.enter_normal_mode(mode)

    def reset_carets_charwise(self, pts, paste_len):
        # FIXME: Won't work for multiple jagged pastes...
        b_pts = [s.b for s in list(self.view.sel())]
        if len(b_pts) > 1:
            self.view.sel().clear()
            self.view.sel().add_all([R(ploc + paste_len - 1,
                                                    ploc + paste_len - 1)
                                    for ploc in pts])
        else:
            self.view.sel().clear()
            self.view.sel().add(R(pts[0] + paste_len - 1,
                                               pts[0] + paste_len - 1))

    def reset_carets_linewise(self, pts):
        self.view.sel().clear()

        if self.state.mode == modes.VISUAL_LINE:
            self.view.sel().add_all([R(loc) for loc in pts])
            return

        pts = [utils.next_non_white_space_char(self.view, pt + 1)
                    for pt in pts]

        self.view.sel().add_all([R(pt) for pt in pts])

    def prepare_fragment(self, text):
        if text.endswith('\n') and text != '\n':
            text = '\n' + text[0:-1]
        return text

    # TODO: Improve this signature.
    def paste_all(self, edit, sel, at, text, count):
        state = self.state

        if state.mode not in (modes.VISUAL, modes.VISUAL_LINE):
            # TODO: generate string first, then insert?
            # Make sure we can paste at EOF.
            at = at if at <= self.view.size() else self.view.size()
            for x in range(count):
                self.view.insert(edit, at, text)
            return at

        else:
            if text.startswith('\n'):
                text = text * count
                if not text.endswith('\n'):
                    text = text + '\n'
            else:
                text = text * count

            if state.mode == modes.VISUAL_LINE:
                if text.startswith('\n'):
                    text = text[1:]

            self.view.replace(edit, sel, text)
            return sel.begin()


class _vi_ga(ViWindowCommandBase):

    """
    http://vimdoc.sourceforge.net/htmldoc/various.html#ga
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):

        def character_to_notation(character):
            """
            Convert a character to a key notation.
            Uses vim key notation.
            http://vimdoc.sourceforge.net/htmldoc/intro.html#key-notation
            """

            character_notation_map = {
                "\0": "Nul",
                " ": "Space",
                "\t": "Tab",
                "\n": "NL"
            }

            if character in character_notation_map:
                character = character_notation_map[character]

            return "<" + character + ">"

        view = self.window.active_view()

        for region in view.sel():

            c_str = view.substr(region.begin())
            c_ord = ord(c_str)
            c_hex = hex(c_ord)
            c_oct = oct(c_ord)
            c_not = character_to_notation(c_str)

            msg_template = "%7s %3s,  Hex %4s,  Octal %5s"

            return sublime.status_message(msg_template % (c_not, c_ord, c_hex, c_oct))


class _vi_gt(ViWindowCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1, mode=None):
        self.window.run_command('tab_control', {'command': 'next'})
        self.window.run_command('_enter_normal_mode', {'mode': mode})


class _vi_g_big_t(ViWindowCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1, mode=None):
        self.window.run_command('tab_control', {'command': 'prev'})
        self.window.run_command('_enter_normal_mode', {'mode': mode})


# TODO <C-]> should learn visual mode
# TODO <C-]> should learn to count
class _vi_ctrl_right_square_bracket(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/tagsrch.html#CTRL-]
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.window.run_command('goto_definition')


class _vi_ctrl_w_b(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#ctrl-w_b
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).move_group_focus_to_bottom_right()


class _vi_ctrl_w_big_h(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#ctrl-w_h
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).move_current_view_to_far_left()


class _vi_ctrl_w_big_j(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#ctrl-w_j
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).move_current_view_to_very_bottom()


class _vi_ctrl_w_big_k(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#ctrl-w_k
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).move_current_view_to_very_top()


class _vi_ctrl_w_big_l(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_L
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).move_current_view_to_far_right()


class _vi_ctrl_w_c(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_c
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).close_current_view()


class _vi_ctrl_w_equal(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_=
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).resize_groups_almost_equally()


class _vi_ctrl_w_greater_than(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_>
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).increase_current_group_width_by_n(count)


class _vi_ctrl_w_h(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_h
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).move_group_focus_to_nth_left_of_current_one(count)


class _vi_ctrl_w_j(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_j
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).move_group_focus_to_nth_below_current_one(count)


class _vi_ctrl_w_k(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_k
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).move_group_focus_to_nth_above_current_one(count)


class _vi_ctrl_w_l(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_l
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).move_group_focus_to_nth_right_of_current_one(count)


class _vi_ctrl_w_less_than(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_<
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).decrease_current_group_width_by_n(count)


class _vi_ctrl_w_minus(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_-
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).decrease_current_group_height_by_n(count)


class _vi_ctrl_w_n(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_n
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).split_with_new_file(count)


class _vi_ctrl_w_o(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_o
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).close_all_other_views()


class _vi_ctrl_w_pipe(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_bar
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=None):
        SublimeWindowAPI(self.window).set_current_group_width_to_n(count)


class _vi_ctrl_w_plus(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_+
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).increase_current_group_height_by_n(count)


class _vi_ctrl_w_q(IrreversibleTextCommand):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_q
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.view.window()).quit_current_view()


class _vi_ctrl_w_s(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_s
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=None):
        SublimeWindowAPI(self.window).split_current_view_in_two(count)


class _vi_ctrl_w_t(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_t
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        SublimeWindowAPI(self.window).move_group_focus_to_top_left()


class _vi_ctrl_w_underscore(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W__
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=None):
        SublimeWindowAPI(self.window).set_current_group_height_to_n(count)


class _vi_ctrl_w_v(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_v
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1, mode=None):
        SublimeWindowAPI(self.window).split_current_view_in_two_vertically(count)


class _vi_ctrl_w_x(ViWindowCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/windows.html#CTRL-W_x
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1):
        SublimeWindowAPI(self.window).exchange_current_view_with_view_in_next_or_previous_group(count)


# TODO: z<CR> != zt
class _vi_z_enter(IrreversibleTextCommand):
    '''
    Command: z<cr>

    http://vimdoc.sourceforge.net/htmldoc/scroll.html#z<CR>
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1, mode=None):

        # TODO if count is given should be the same as CTRL-W__

        pt = resolve_insertion_point_at_b(first_sel(self.view))
        home_line = self.view.line(pt)

        taget_pt = self.view.text_to_layout(home_line.begin())
        self.view.set_viewport_position(taget_pt)


class _vi_z_minus(IrreversibleTextCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1, mode=None):
        layout_coord = self.view.text_to_layout(first_sel(self.view).b)
        viewport_extent = self.view.viewport_extent()
        new_pos = (0.0, layout_coord[1] - viewport_extent[1])

        self.view.set_viewport_position(new_pos)


class _vi_zz(IrreversibleTextCommand):

    def __init__(self, view):
        IrreversibleTextCommand.__init__(self, view)

    def run(self, count=1, mode=None):
        first_sel = self.view.sel()[0]
        current_position = self.view.text_to_layout(first_sel.b)
        viewport_dim = self.view.viewport_extent()
        new_pos = (0.0, current_position[1] - viewport_dim[1] / 2)

        self.view.set_viewport_position(new_pos)


class _vi_modify_numbers(ViTextCommandBase):
    """
    Base class for Ctrl-x and Ctrl-a.
    """
    DIGIT_PAT = re.compile('(\D+?)?(-)?(\d+)(\D+)?')
    NUM_PAT = re.compile('\d')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_editable_data(self, pt):
        sign = -1 if (self.view.substr(pt - 1) == '-') else 1
        end = pt
        while self.view.substr(end).isdigit():
            end += 1
        return (sign, int(self.view.substr(R(pt, end))),
                R(end, self.view.line(pt).b))

    def find_next_num(self, regions):
        # Modify selections that are inside a number already.
        for i, r in enumerate(regions):
            a = r.b
            if self.view.substr(r.b).isdigit():
                while self.view.substr(a).isdigit():
                    a -= 1
                regions[i] = R(a)

        lines = [self.view.substr(R(r.b, self.view.line(r.b).b)) for r in regions]
        matches = [_vi_modify_numbers.NUM_PAT.search(text) for text in lines]
        if all(matches):
            return [(reg.b + ma.start()) for (reg, ma) in zip(regions, matches)]
        return []

    def run(self, edit, count=1, mode=None, subtract=False):
        if mode != modes.INTERNAL_NORMAL:
            return

        # TODO: Deal with octal, hex notations.
        # TODO: Improve detection of numbers.
        regs = list(self.view.sel())

        pts = self.find_next_num(regs)
        if not pts:
            utils.blink()
            return

        count = count if not subtract else -count
        end_sels = []
        for pt in reversed(pts):
            sign, num, tail = self.get_editable_data(pt)

            num_as_text = str((sign * num) + count)
            new_text = num_as_text + self.view.substr(tail)

            offset = 0
            if sign == -1:
                offset = -1
                self.view.replace(edit, R(pt - 1, tail.b), new_text)
            else:
                self.view.replace(edit, R(pt, tail.b), new_text)

            rowcol = self.view.rowcol(pt + len(num_as_text) - 1 + offset)
            end_sels.append(rowcol)

        self.view.sel().clear()
        for (row, col) in end_sels:
            self.view.sel().add(R(self.view.text_point(row, col)))


class _vi_select_big_j(IrreversibleTextCommand):
    """
    Active in select mode. Clears multiple selections and returns to normal
    mode. Should be more convenient than having to reach for Esc.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, mode=None, count=1):
        s = self.view.sel()[0]
        self.view.sel().clear()
        self.view.sel().add(s)
        self.view.run_command('_enter_normal_mode', {'mode': mode})


class _vi_big_j(ViTextCommandBase):
    WHITE_SPACE = ' \t'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, separator=' ', count=1):

        # jsodc_join is better when joining comments
        # self.view.run_command('jsdocs_join')
        # return

        sels = self.view.sel()
        s = R(sels[0].a, sels[-1].b)
        if mode == modes.INTERNAL_NORMAL:
            end_pos = self.view.line(s.b).b
            start = end = s.b
            if count > 2:
                end = self.view.text_point(utils.row_at(self.view, s.b) + (count - 1), 0)
                end = self.view.line(end).b
            else:
                # Join current line and the next.
                end = self.view.text_point(utils.row_at(self.view, s.b) + 1, 0)
                end = self.view.line(end).b
        elif mode in [modes.VISUAL, modes.VISUAL_LINE, modes.VISUAL_BLOCK]:
            if s.a < s.b:
                end_pos = self.view.line(s.a).b
                start = s.a
                if utils.row_at(self.view, s.b - 1) == utils.row_at(self.view, s.a):
                    end = self.view.text_point(utils.row_at(self.view, s.a) + 1, 0)
                else:
                    end = self.view.text_point(utils.row_at(self.view, s.b - 1), 0)
                end = self.view.line(end).b
            else:
                end_pos = self.view.line(s.b).b
                start = s.b
                if utils.row_at(self.view, s.b) == utils.row_at(self.view, s.a - 1):
                    end = self.view.text_point(utils.row_at(self.view, s.a - 1) + 1, 0)
                else:
                    end = self.view.text_point(utils.row_at(self.view, s.a - 1), 0)
                end = self.view.line(end).b
        else:
            return s

        text_to_join = self.view.substr(R(start, end))
        lines = text_to_join.split('\n')

        if separator:
            # J
            joined_text = lines[0]
            for line in lines[1:]:
                line = line.lstrip()
                if joined_text and joined_text[-1] not in self.WHITE_SPACE:
                    line = ' ' + line
                joined_text += line
        else:
            # gJ
            joined_text = ''.join(lines)

        self.view.replace(edit, R(start, end), joined_text)
        sels.clear()
        sels.add(R(end_pos))


class _vi_gv(IrreversibleTextCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, mode=None, count=None):
        sels = self.view.get_regions('visual_sel')
        if not sels:
            return

        self.view.window().run_command('_enter_visual_mode', {'mode': mode})
        self.view.sel().clear()
        self.view.sel().add_all(sels)


class _vi_ctrl_e(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        # TODO: Implement this motion properly; don't use built-in commands.
        # We're using an action because we don't care too much right now and we don't want the
        # motion to utils.blink every time we issue it (it does because the selections don't change and
        # NeoVintageous rightfully thinks it has failed.)
        if mode == modes.VISUAL_LINE:
            return
        extend = True if mode == modes.VISUAL else False
        self.view.run_command('scroll_lines', {'amount': -1, 'extend': extend})


class _vi_ctrl_y(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        # TODO: Implement this motion properly; don't use built-in commands.
        # We're using an action because we don't care too much right now and we don't want the
        # motion to utils.blink every time we issue it (it does because the selections don't change and
        # NeoVintageous rightfully thinks it has failed.)
        if mode == modes.VISUAL_LINE:
            return
        extend = True if mode == modes.VISUAL else False
        self.view.run_command('scroll_lines', {'amount': 1, 'extend': extend})


class _vi_ctrl_r_equal(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, insert=False, next_mode=None):
        def on_done(s):
            state = State(self.view)
            try:
                rv = [str(eval(s, None, None)),]
                if not insert:
                    state.registers[REG_EXPRESSION] = rv
                else:
                    self.view.run_command('insert_snippet', {'contents': str(rv[0])})
                    state.reset()
            except:
                sublime.status_message("NeoVintageous: Invalid expression.")
                on_cancel()

        def on_cancel():
            state = State(self.view)
            state.reset()

        self.view.window().show_input_panel('', '', on_done, None, on_cancel)


class _vi_q(IrreversibleTextCommand):
    _register_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, name=None, mode=None, count=1):
        state = State(self.view)

        if state.is_recording:
            State.macro_registers[_vi_q._register_name] = list(State.macro_steps)
            state.stop_recording()
            _vi_q._register_name = None
            return

        # TODO(guillermooo): What happens when we change views?
        state.start_recording()
        _vi_q._register_name = name


class _vi_at(IrreversibleTextCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, name=None, mode=None, count=1):
        # TODO(guillermooo): Do we need to glue all these edits?
        cmds = State.macro_steps
        if name != '@':
            try:
                cmds = State.macro_registers[name]
                State.macro_steps = cmds
            except ValueError as e:
                print('NeoVintageous: error: %s' % e)
                return

        state = State(self.view)
        for cmd, args in cmds:
            # TODO(guillermooo): Is this robust enough?
            if 'xpos' in args:
                state.update_xpos(force=True)
                args['xpos'] = State(self.view).xpos
            elif args.get('motion') and 'xpos' in args.get('motion'):
                state.update_xpos(force=True)
                motion = args.get('motion')
                motion['motion_args']['xpos'] = State(self.view).xpos
                args['motion'] = motion
            self.view.run_command(cmd, args)


class _enter_visual_block_mode(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None):
        def f(view, s):
            return R(s.b, s.b + 1)

        if mode in (modes.VISUAL_LINE,):
            return

        if mode == modes.VISUAL_BLOCK:
            self.enter_normal_mode(mode)
            return

        if mode == modes.VISUAL:
            first = utils.first_sel(self.view)

            if self.view.line(first.end() - 1).empty():
                self.enter_normal_mode(mode)
                utils.blink()
                return

            self.view.sel().clear()
            lhs_edge = self.view.rowcol(first.b)[1]
            regs = self.view.split_by_newlines(first)

            offset_a, offset_b = self.view.rowcol(first.a)[1], self.view.rowcol(first.b)[1]
            min_offset_x = min(offset_a, offset_b)
            max_offset_x = max(offset_a, offset_b)

            new_regs = []
            for r in regs:
                if r.empty():
                    break
                row, _ = self.view.rowcol(r.end() - 1)
                a = self.view.text_point(row, min_offset_x)
                eol = self.view.rowcol(self.view.line(r.end() - 1).b)[1]
                b = self.view.text_point(row, min(max_offset_x, eol))

                if first.a <= first.b:
                    if offset_b < offset_a:
                        new_r = R(a - 1, b + 1, eol)
                    else:
                        new_r = R(a, b, eol)
                elif offset_b < offset_a:
                    new_r = R(a, b, eol)
                else:
                    new_r = R(a - 1, b + 1, eol)

                new_regs.append(new_r)

            if not new_regs:
                new_regs.append(first)

            self.view.sel().add_all(new_regs)
            state = State(self.view)
            state.enter_visual_block_mode()
            return

        # Handling multiple visual blocks seems quite hard, so ensure we only
        # have one.
        first = list(self.view.sel())[0]
        self.view.sel().clear()
        self.view.sel().add(first)

        state = State(self.view)
        state.enter_visual_block_mode()

        if not self.view.has_non_empty_selection_region():
            regions_transformer(self.view, f)


class _vi_select_j(ViWindowCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, count=1, mode=None):
        if mode != modes.SELECT:
            raise ValueError('wrong mode')

        for i in range(count):
            self.window.run_command('find_under_expand')


class _vi_tilde(ViTextCommandBase):
    """
    Implemented as if 'notildeopt' was `True`.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None, motion=None):
        def select(view, s):
            if mode == modes.VISUAL:
                return R(s.end(), s.begin())
            return R(s.begin(), s.end() + count)

        def after(view, s):
            return R(s.begin())

        regions_transformer(self.view, select)
        self.view.run_command('swap_case')

        if mode in (modes.VISUAL, modes.VISUAL_LINE, modes.VISUAL_BLOCK):
            regions_transformer(self.view, after)

        self.enter_normal_mode(mode)


class _vi_g_tilde(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None, motion=None):
        def f(view, s):
            return R(s.end(), s.begin())

        if motion:
            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if not self.has_sel_changed():
                utils.blink()
                self.enter_normal_mode(mode)
                return

        self.view.run_command('swap_case')

        if motion:
            regions_transformer(self.view, f)

        self.enter_normal_mode(mode)


class _vi_visual_u(ViTextCommandBase):
    """
    'u' action in visual modes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).lower())

        def after(view, s):
            return R(s.begin())

        regions_transformer(self.view, after)

        self.enter_normal_mode(mode)


class _vi_visual_big_u(ViTextCommandBase):
    """
    'U' action in visual modes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).upper())

        def after(view, s):
            return R(s.begin())

        regions_transformer(self.view, after)

        self.enter_normal_mode(mode)


class _vi_g_tilde_g_tilde(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, count=1, mode=None):
        def select(view, s):
            l = view.line(s.b)
            return R(l.end(), l.begin())

        if mode != modes.INTERNAL_NORMAL:
            raise ValueError('wrong mode')

        regions_transformer(self.view, select)
        self.view.run_command('swap_case')
        # Ensure we leave the sel .b end where we want it.
        regions_transformer(self.view, select)

        self.enter_normal_mode(mode)


class _vi_g_big_u_big_u(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def select(view, s):
            return units.lines(view, s, count)

        def to_upper(view, s):
            view.replace(edit, s, view.substr(s).upper())
            return R(s.a)

        regions_transformer(self.view, select)
        regions_transformer(self.view, to_upper)
        self.enter_normal_mode(mode)


class _vi_guu(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def select(view, s):
            l = view.line(s.b)
            return R(l.end(), l.begin())

        def to_lower(view, s):
            view.replace(edit, s, view.substr(s).lower())
            return s

        regions_transformer(self.view, select)
        regions_transformer(self.view, to_lower)
        self.enter_normal_mode(mode)


class _vi_g_big_h(ViWindowCommandBase):
    """
    Non-standard command.

    After a search has been performed via '/' or '?', selects all matches and
    enters select mode.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, mode=None, count=1):
        view = self.window.active_view()

        regs = view.get_regions('vi_search')
        if regs:
            view.sel().add_all(view.get_regions('vi_search'))

            self.state.enter_select_mode()
            self.state.display_status()
            return

        utils.blink()
        sublime.status_message('NeoVintageous: No available search matches')
        self.state.reset_command_data()


class _vi_ctrl_x_ctrl_l(ViTextCommandBase):
    """
    http://vimdoc.sourceforge.net/htmldoc/insert.html#i_CTRL-X_CTRL-L
    """
    MAX_MATCHES = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_matches(self, prefix, end):
        escaped = re.escape(prefix)
        matches = []
        while end > 0:
            match = search.reverse_search(self.view,
                                          r'^\s*{0}'.format(escaped),
                                          0, end, flags=0)
            if (match is None) or (len(matches) == self.MAX_MATCHES):
                break
            line = self.view.line(match.begin())
            end = line.begin()
            text = self.view.substr(line).lstrip()
            if text not in matches:
                matches.append(text)
        return matches

    def run(self, edit, mode=None, register='"'):
        # TODO: Must exit to insert mode. As we're using a quick panel, the
        #       mode is being reset in _init_vintageous.
        assert mode == modes.INSERT, 'bad mode'

        if (len(self.view.sel()) > 1 or not self.view.sel()[0].empty()):
            utils.blink()
            return

        s = self.view.sel()[0]
        line_begin = self.view.text_point(utils.row_at(self.view, s.b), 0)
        prefix = self.view.substr(R(line_begin, s.b)).lstrip()
        self._matches = self.find_matches(prefix, end=self.view.line(s.b).a)
        if self._matches:
            self.show_matches(self._matches)
            state = State(self.view)
            state.reset_during_init = False
            state.reset_command_data()
            return
        utils.blink()

    def show_matches(self, items):
        self.view.window().show_quick_panel(items, self.replace,
                                            sublime.MONOSPACE_FONT)

    def replace(self, s):
        self.view.run_command('__replace_line',
                              {'with_what': self._matches[s]})
        del self.__dict__['_matches']
        pt = self.view.sel()[0].b
        self.view.sel().clear()
        self.view.sel().add(R(pt))


class __replace_line(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, with_what):
        b = self.view.line(self.view.sel()[0].b).a
        pt = utils.next_non_white_space_char(self.view, b, white_space=' \t')
        self.view.replace(edit, R(pt, self.view.line(pt).b),
                          with_what)


class _vi_gc(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return R(s.begin())

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (modes.VISUAL, modes.VISUAL_LINE):
            utils.blink()
            return

        self.view.run_command('toggle_comment', {'block': False})

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_g_big_c(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return R(s.begin())

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (modes.VISUAL, modes.VISUAL_LINE):
            utils.blink()
            return

        self.view.run_command('toggle_comment', {'block': True})

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_gcc_action(ViTextCommandBase):

    _can_yank = True
    _synthetize_new_line_at_eof = True
    _yanks_linewise = False
    _populates_small_delete_register = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                view.run_command('toggle_comment')
                if utils.row_at(self.view, s.a) != utils.row_at(self.view, self.view.size()):
                    pt = utils.next_non_white_space_char(view, s.a, white_space=' \t')
                else:
                    pt = utils.next_non_white_space_char(view,
                                                         self.view.line(s.a).a,
                                                         white_space=' \t')

                return R(pt, pt)
            return s

        self.view.run_command('_vi_gcc_motion', {'mode': mode, 'count': count})

        state = self.state
        state.registers.yank(self)

        row = [self.view.rowcol(s.begin())[0] for s in self.view.sel()][0]
        regions_transformer_reversed(self.view, f)
        self.view.sel().clear()
        self.view.sel().add(R(self.view.text_point(row, 0)))


class _vi_gcc_motion(ViTextCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == modes.INTERNAL_NORMAL:
                end = view.text_point(utils.row_at(self.view, s.b) + (count - 1), 0)
                begin = view.line(s.b).a
                if ((utils.row_at(self.view, end) == utils.row_at(self.view, view.size())) and
                    (view.substr(begin - 1) == '\n')):
                        begin -= 1

                return R(begin, view.full_line(end).b)

            return s

        regions_transformer(self.view, f)
