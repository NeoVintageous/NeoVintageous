import os

import sublime
from sublime import Region
from sublime_plugin import WindowCommand
from sublime_plugin import TextCommand

from Default.history_list import get_jump_history

from NeoVintageous.lib import nvim
from NeoVintageous.lib import rcfile
from NeoVintageous.lib.ex.completions import iter_paths
from NeoVintageous.lib.ex.completions import parse
from NeoVintageous.lib.ex.completions import parse_for_setting
from NeoVintageous.lib.ex.parser.parser import parse_command_line
from NeoVintageous.lib.ex.parser.scanner_command_goto import TokenCommandGoto
from NeoVintageous.lib.state import init_state
from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi import cmd_base
from NeoVintageous.lib.vi import cmd_defs
from NeoVintageous.lib.vi import mappings
from NeoVintageous.lib.vi import utils
from NeoVintageous.lib.vi.core import ViWindowCommandBase
from NeoVintageous.lib.vi.keys import key_names
from NeoVintageous.lib.vi.keys import KeySequenceTokenizer
from NeoVintageous.lib.vi.keys import to_bare_command_name
from NeoVintageous.lib.vi.mappings import Mappings
from NeoVintageous.lib.vi.settings import iter_settings
from NeoVintageous.lib.vi.sublime import show_ipanel
from NeoVintageous.lib.vi.utils import gluing_undo_groups
from NeoVintageous.lib.vi.utils import mark_as_widget
from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi.utils import regions_transformer


__all__ = [
    '_vi_add_to_jump_list',
    '_vi_adjust_carets',
    '_vi_question_mark_on_parser_done',
    '_vi_slash_on_parser_done',
    'ClearCmdlineHistoryIndex',
    'CycleCmdlineHistory',
    'FsCompletion',
    'NeovintageousOpenMyRcFileCommand',
    'NeovintageousReloadMyRcFileCommand',
    'NeovintageousToggleUseCtrlKeysCommand',
    'PressKey',
    'ProcessNotation',
    'Sequence',
    'TabControlCommand',
    'ViColonInput',
    'ViColonRepeatLast',
    'ViSettingCompletion',
    'WriteFsCompletion'
]


_logger = nvim.get_logger(__name__)


_EX_HISTORY_MAX_LENGTH = 20
_EX_HISTORY = {
    'cmdline': [],
    'searches': []
}


def _update_command_line_history(slot_name, item):
    if len(_EX_HISTORY[slot_name]) >= _EX_HISTORY_MAX_LENGTH:
        _EX_HISTORY[slot_name] = _EX_HISTORY[slot_name][1:]

    if item in _EX_HISTORY[slot_name]:
        _EX_HISTORY[slot_name].pop(_EX_HISTORY[slot_name].index(item))

    _EX_HISTORY[slot_name].append(item)


class PressKey(ViWindowCommandBase):
    """
    Interact with the global state each time a key is pressed.

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
        _logger.debug('[press_key] \'%s\', repeat_count=%s, do_eval=%s, check_user_mappings=%s', key, repeat_count, do_eval, check_user_mappings)  # noqa: E501
        state = self.state

        # If the user has made selections with the mouse, we may be in an
        # inconsistent state. Try to remedy that.
        if (state.view.has_non_empty_selection_region() and
            state.mode not in (modes.VISUAL,
                               modes.VISUAL_LINE,
                               modes.VISUAL_BLOCK,
                               modes.SELECT)):
                init_state(state.view)

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
                _logger.debug('[press_key] state holds a complete command')
                if do_eval:
                    _logger.debug('[press_key] evaluate complete command')
                    state.eval()
                    state.reset_command_data()
            return

        if repeat_count:
            state.action_count = str(repeat_count)

        if self.handle_counts(key, repeat_count):
            return

        state.partial_sequence += key

        _logger.debug('[press_key] sequence=\'%s\', partial=\'%s\'', state.sequence, state.partial_sequence)

        key_mappings = Mappings(state)
        if check_user_mappings and key_mappings.incomplete_user_mapping():
            _logger.debug('[press_key] incomplete user mapping: \'%s\'', state.partial_sequence)
            # e.g. we may have typed 'aa' and there's an 'aaa' mapping, so we need to keep collecting input.
            return

        _logger.debug('[press_key] get cmd for seq/partial seq in (mode): %s/%s (%s)', state.sequence, state.partial_sequence, state.mode)  # noqa: E501

        command = key_mappings.resolve(check_user_mappings=check_user_mappings)

        if isinstance(command, cmd_defs.ViOpenRegister):
            _logger.debug('[press_key] request register name')
            state.must_capture_register_name = True
            return

        # XXX: This doesn't seem to be correct. If we are in OPERATOR_PENDING mode, we should
        # most probably not have to wipe the state.
        if isinstance(command, mappings.Mapping):
            if do_eval:
                new_keys = command.mapping
                if state.mode == modes.OPERATOR_PENDING:
                    command_name = command.mapping  # FIXME # noqa: F841
                    new_keys = state.sequence[:-len(state.partial_sequence)] + command.mapping
                reg = state.register
                acount = state.action_count
                mcount = state.motion_count
                state.reset_command_data()
                state.register = reg
                state.motion_count = mcount
                state.action_count = acount
                state.mode = modes.NORMAL
                _logger.debug('[press_key] running user mapping \'%s\' via process_notation starting in mode \'%s\'', new_keys, state.mode)  # noqa: E501
                self.window.run_command('process_notation', {'keys': new_keys, 'check_user_mappings': False})
            return

        if isinstance(command, cmd_defs.ViOpenNameSpace):
            # Keep collecting input to complete the sequence. For example, we may have typed 'g'
            _logger.debug('[press_key] opening namespace \'%s\'', state.partial_sequence)
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
                _logger.debug('[press_key] unmapped sequence \'%s\'', state.sequence)
                utils.blink()
                state.mode = modes.NORMAL
                state.reset_command_data()
                return

        if (state.mode == modes.OPERATOR_PENDING and isinstance(command, cmd_defs.ViOperatorDef)):
            # TODO: This may be unreachable code by now. ???
            # we're expecting a motion, but we could still get an action.
            # For example, dd, g~g~ or g~~
            # remove counts
            action_seq = to_bare_command_name(state.sequence)
            _logger.debug('[press_key] action seq \'%s\'', action_seq)
            command = key_mappings.resolve(sequence=action_seq, mode=modes.NORMAL)
            # TODO: Make _missing a command.
            if isinstance(command, cmd_base.ViMissingCommandDef):
                _logger.debug('[press_key] unmapped sequence \'%s\'', state.sequence)
                state.reset_command_data()
                return

            if not command['motion_required']:
                state.mode = modes.NORMAL

        state.set_command(command)

        _logger.debug('[press_key] \'%s\' mapped to \'%s\'', state.partial_sequence, command)

        if state.mode == modes.OPERATOR_PENDING:
            state.reset_partial_sequence()

        if do_eval:
            state.eval()

    def handle_counts(self, key, repeat_count):
        """Return `True` if the processing of the current key needs to stop."""
        state = State(self.window.active_view())
        if not state.action and key.isdigit():
            if not repeat_count and (key != '0' or state.action_count):
                _logger.debug('[press_key] action count digit \'%s\'', key)
                state.action_count += key
                return True

        if (state.action and (state.mode == modes.OPERATOR_PENDING) and key.isdigit()):
            if not repeat_count and (key != '0' or state.motion_count):
                _logger.debug('[press_key] motion count digit \'%s\'', key)
                state.motion_count += key
                return True


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
        _logger.debug('[process_notation] run keys \'%s\', mode \'%s\'', keys, state.mode)
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
                _logger.debug('[process_notation] first action found in \'%s\'', state.sequence)
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

        # Strip the already run commands
        if leading_motions:
            if ((len(leading_motions) == len(keys)) and (not state.must_collect_input)):
                state.non_interactive = False
                return

            _logger.debug('[process_notation] original seq/leading motions: %s/%s', keys, leading_motions)
            keys = keys[len(leading_motions):]
            _logger.debug('[process_notation] seq stripped to \'%s\'', keys)

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
                            state.repeat_data = ('vi', (leading_motions + keys), initial_mode, None)

        # We'll reach this point if we have a command that requests input
        # whose input parser isn't satistied. For example, `/foo`. Note that
        # `/foo<CR>`, on the contrary, would have satisfied the parser.
        _logger.debug('[process_notation] unsatisfied parser action=\'%s\', motion=\'%s\'', state.action, state.motion)
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
            _logger.debug('[process_notation] last attemp to collect input \'%s\'', parser_def.command)

            if parser_def.interactive_command:
                self.window.run_command(
                    parser_def.interactive_command,
                    {parser_def.input_param: command._inp}
                )
        except IndexError:
            _logger.debug('[process_notation] could not find a command to collect more user input')
            utils.blink()
        finally:
            self.state.non_interactive = False


class ViColonInput(WindowCommand):
    # Indicates whether the user issued the call.
    interactive_call = True

    def is_enabled(self):
        return bool(self.window.active_view())

    def __init__(self, window):
        WindowCommand.__init__(self, window)

    def adjust_initial_text(self, text):
        state = State(self.window.active_view())
        if state.mode in (modes.VISUAL, modes.VISUAL_LINE):
            text = ":'<,'>" + text[1:]

        return text

    def run(self, initial_text=':', cmd_line=''):
        if cmd_line:
            # The caller has provided a command, to we're not in interactive
            # mode -- just run the command.
            ViColonInput.interactive_call = False
            self.on_done(cmd_line)
            return
        else:
            ViColonInput.interactive_call = True

        FsCompletion.invalidate()

        v = mark_as_widget(
            show_ipanel(
                self.window,
                initial_text=self.adjust_initial_text(initial_text),
                on_done=self.on_done,
                on_change=self.on_change
            )
        )

        v.set_syntax_file('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        v.settings().set('gutter', False)
        v.settings().set('rulers', [])
        v.settings().set('auto_match_enabled', False)

        state = State(self.window.active_view())
        state.reset_during_init = False

    def on_change(self, s):
        if ViColonInput.interactive_call:
            cmd, prefix, only_dirs = parse(s)
            if cmd:
                FsCompletion.prefix = prefix
                FsCompletion.is_stale = True
            cmd, prefix, _ = parse_for_setting(s)
            if cmd:
                ViSettingCompletion.prefix = prefix
                ViSettingCompletion.is_stale = True

            if not cmd:
                return

        ViColonInput.interactive_call = True

    def on_done(self, cmd_line):
        if ViColonInput.interactive_call:
            _update_command_line_history('cmdline', cmd_line)

        try:
            parsed_new = parse_command_line(cmd_line[1:])

            if not parsed_new.command:
                parsed_new.command = TokenCommandGoto()

            self.window.run_command(parsed_new.command.target_command, {'command_line': cmd_line[1:]})
        except nvim.Error as ve:
            nvim.exception_message(ve)
        except Exception as e:
            nvim.not_implemented_message(str(e) + ' ' + "(%s)" % cmd_line)


class ViColonRepeatLast(WindowCommand):
    def is_enabled(self):
        return ((len(self.window.views()) > 0) and (len(_EX_HISTORY['cmdline']) > 0))

    def run(self):
        self.window.run_command('vi_colon_input', {'cmd_line': _EX_HISTORY['cmdline'][-1]})


class CycleCmdlineHistory(TextCommand):
    HISTORY_INDEX = None

    def run(self, edit, backwards=False):
        if not _EX_HISTORY['cmdline']:
            return

        if CycleCmdlineHistory.HISTORY_INDEX is None:
            CycleCmdlineHistory.HISTORY_INDEX = -1 if backwards else 0
        else:
            CycleCmdlineHistory.HISTORY_INDEX += -1 if backwards else 1

        if (
            CycleCmdlineHistory.HISTORY_INDEX == len(_EX_HISTORY['cmdline']) or
            CycleCmdlineHistory.HISTORY_INDEX < -len(_EX_HISTORY['cmdline'])
        ):
            CycleCmdlineHistory.HISTORY_INDEX = -1 if backwards else 0

        self.view.erase(edit, Region(0, self.view.size()))
        self.view.insert(edit, 0, _EX_HISTORY['cmdline'][CycleCmdlineHistory.HISTORY_INDEX])


class ClearCmdlineHistoryIndex(TextCommand):
    def run(self, edit):
        CycleCmdlineHistory.HISTORY_INDEX = None


class WriteFsCompletion(TextCommand):
    def run(self, edit, cmd, completion):
        if self.view.score_selector(0, 'text.excmdline') == 0:
            return

        ViColonInput.interactive_call = False

        self.view.sel().clear()
        self.view.replace(edit, Region(0, self.view.size()), cmd + ' ' + completion)
        self.view.sel().add(Region(self.view.size()))


class FsCompletion(TextCommand):
    # Last user-provided path string.
    prefix = ''
    frozen_dir = ''
    is_stale = False
    items = None

    @staticmethod
    def invalidate():
        FsCompletion.prefix = ''
        FsCompletion.frozen_dir = ''
        FsCompletion.is_stale = True
        FsCompletion.items = None

    def run(self, edit):
        if self.view.score_selector(0, 'text.excmdline') == 0:
            return

        state = State(self.view)
        FsCompletion.frozen_dir = (FsCompletion.frozen_dir or
                                   (state.settings.vi['_cmdline_cd'] + '/'))

        cmd, prefix, only_dirs = parse(self.view.substr(self.view.line(0)))
        if not cmd:
            return

        if not (FsCompletion.prefix or FsCompletion.items) and prefix:
            FsCompletion.prefix = prefix
            FsCompletion.is_stale = True

        if prefix == '..':
            FsCompletion.prefix = '../'
            self.view.run_command('write_fs_completion', {
                'cmd': cmd,
                'completion': '../'
            })

        if prefix == '~':
            path = os.path.expanduser(prefix) + '/'
            FsCompletion.prefix = path
            self.view.run_command('write_fs_completion', {
                'cmd': cmd,
                'completion': path
            })

            return

        if (not FsCompletion.items) or FsCompletion.is_stale:
            FsCompletion.items = iter_paths(from_dir=FsCompletion.frozen_dir,
                                            prefix=FsCompletion.prefix,
                                            only_dirs=only_dirs)
            FsCompletion.is_stale = False

        try:
            self.view.run_command('write_fs_completion', {
                'cmd': cmd,
                'completion': next(FsCompletion.items)
            })
        except StopIteration:
            FsCompletion.items = iter_paths(prefix=FsCompletion.prefix,
                                            from_dir=FsCompletion.frozen_dir,
                                            only_dirs=only_dirs)

            self.view.run_command('write_fs_completion', {
                'cmd': cmd,
                'completion': FsCompletion.prefix
            })


class ViSettingCompletion(TextCommand):
    # Last user-provided path string.
    prefix = ''
    is_stale = False
    items = None

    @staticmethod
    def invalidate():
        ViSettingCompletion.prefix = ''
        ViSettingCompletion.is_stale = True
        ViSettingCompletion.items = None

    def run(self, edit):
        if self.view.score_selector(0, 'text.excmdline') == 0:
            return

        cmd, prefix, _ = parse_for_setting(self.view.substr(self.view.line(0)))
        if not cmd:
            return

        if (ViSettingCompletion.prefix is None) and prefix:
            ViSettingCompletion.prefix = prefix
            ViSettingCompletion.is_stale = True
        elif ViSettingCompletion.prefix is None:
            ViSettingCompletion.items = iter_settings('')
            ViSettingCompletion.is_stale = False

        if not ViSettingCompletion.items or ViSettingCompletion.is_stale:
            ViSettingCompletion.items = iter_settings(ViSettingCompletion.prefix)
            ViSettingCompletion.is_stale = False

        try:
            self.view.run_command('write_fs_completion', {
                'cmd': cmd,
                'completion': next(ViSettingCompletion.items)
            })
        except StopIteration:
            try:
                ViSettingCompletion.items = iter_settings(ViSettingCompletion.prefix)
                self.view.run_command('write_fs_completion', {
                    'cmd': cmd,
                    'completion': next(ViSettingCompletion.items)
                })
            except StopIteration:
                return


class _vi_add_to_jump_list(WindowCommand):
    def run(self):
        get_jump_history(self.window.id()).push_selection(self.window.active_view())


# DEPRECATED
class NeovintageousToggleUseCtrlKeysCommand(WindowCommand):

    def run(self):
        settings = sublime.load_settings('Preferences.sublime-settings')
        use_ctrl_keys = not settings.get('vintageous_use_ctrl_keys')

        settings.set('vintageous_use_ctrl_keys', use_ctrl_keys)
        sublime.save_settings('Preferences.sublime-settings')

        status = 'enabled' if use_ctrl_keys else 'disabled'

        nvim.status_message('ctrl keys have been {}'.format(status))


class NeovintageousOpenMyRcFileCommand(WindowCommand):
    """A command that opens the the user runtime configuration file."""

    def run(self):
        rcfile.open(self.window)


class NeovintageousReloadMyRcFileCommand(WindowCommand):
    """A command that reloads the user runtime configuration file."""

    def run(self):
        rcfile.reload()

        nvim.status_message('rc file reloaded')


class _vi_slash_on_parser_done(WindowCommand):

    def run(self, key=None):
        state = State(self.window.active_view())
        state.motion = cmd_defs.ViSearchForwardImpl()
        state.last_buffer_search = (state.motion._inp or state.last_buffer_search)


class _vi_question_mark_on_parser_done(WindowCommand):

    def run(self, key=None):
        state = State(self.window.active_view())
        state.motion = cmd_defs.ViSearchBackwardImpl()
        state.last_buffer_search = (state.motion._inp or state.last_buffer_search)


class _vi_adjust_carets(TextCommand):

    def run(self, edit, mode=None):
        def f(view, s):
            if mode in (modes.NORMAL, modes.INTERNAL_NORMAL):
                if ((view.substr(s.b) == '\n' or s.b == view.size()) and not view.line(s.b).empty()):
                    return Region(s.b - 1)
            return s

        regions_transformer(self.view, f)


class Sequence(TextCommand):
    """Required so that mark_undo_groups_for_gluing and friends work."""

    def run(self, edit, commands):
        for cmd, args in commands:
            self.view.run_command(cmd, args)


class TabControlCommand(ViWindowCommandBase):

    def run(self, command, file_name=None, forced=False, index=None):
        view_count = len(self.window.views_in_group(self.window.active_group()))
        (group_index, view_index) = self.window.get_view_index(self._view)

        if command == 'open':
            if not file_name:  # TODO: file completion
                self.window.run_command('show_overlay', {
                    'overlay': 'goto',
                    'show_files': True,
                })
            else:
                cur_dir = os.path.dirname(self._view.file_name())
                self.window.open_file(os.path.join(cur_dir, file_name))

        elif command == 'next':
            self.window.run_command('select_by_index', {
                'index': (view_index + 1) % view_count})

        elif command == 'prev':
            self.window.run_command('select_by_index', {
                'index': (view_index + view_count - 1) % view_count})

        elif command == "last":
            self.window.run_command('select_by_index', {'index': view_count - 1})

        elif command == "first":
            self.window.run_command('select_by_index', {'index': 0})

        elif command == 'goto':
            self.window.run_command('select_by_index', {'index': index - 1})

        elif command == 'only':
            quit_command_line = 'quit' + '' if not forced else '!'

            group = self.window.views_in_group(group_index)
            if any(view.is_dirty() for view in group):
                nvim.exception_message(nvim.Error(nvim.E_OTHER_BUFFER_HAS_CHANGES))
                return

            for view in group:
                if view.id() == self._view.id():
                    continue
                self.window.focus_view(view)
                self.window.run_command('ex_quit', {
                    'command_line': quit_command_line})

            self.window.focus_view(self._view)

        else:
            nvim.console_message('unknown tab control command')
            nvim.status_message('unknown tab control command')
