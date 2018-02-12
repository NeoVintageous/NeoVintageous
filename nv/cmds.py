import os
import re

from sublime import CLASS_WORD_START
from sublime import Region
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand

from NeoVintageous.nv import rc
from NeoVintageous.nv.ex.completions import iter_paths
from NeoVintageous.nv.ex.completions import parse
from NeoVintageous.nv.ex.completions import parse_for_setting
from NeoVintageous.nv.ex.parser.parser import parse_command_line
from NeoVintageous.nv.ex.parser.scanner_command_goto import TokenCommandGoto
from NeoVintageous.nv.history import history_get
from NeoVintageous.nv.history import history_get_type
from NeoVintageous.nv.history import history_len
from NeoVintageous.nv.history import history_update
from NeoVintageous.nv.mappings import Mapping
from NeoVintageous.nv.mappings import mappings_is_incomplete
from NeoVintageous.nv.mappings import mappings_resolve
from NeoVintageous.nv.state import init_state
from NeoVintageous.nv.state import State
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.ui import ui_blink
from NeoVintageous.nv.ui import ui_cmdline_prompt
from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef
from NeoVintageous.nv.vi.cmd_defs import ViOpenNameSpace
from NeoVintageous.nv.vi.cmd_defs import ViOpenRegister
from NeoVintageous.nv.vi.cmd_defs import ViOperatorDef
from NeoVintageous.nv.vi.cmd_defs import ViSearchBackwardImpl
from NeoVintageous.nv.vi.cmd_defs import ViSearchForwardImpl
from NeoVintageous.nv.vi.core import ViWindowCommandBase
from NeoVintageous.nv.vi.keys import key_names
from NeoVintageous.nv.vi.keys import KeySequenceTokenizer
from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vi.settings import iter_settings
from NeoVintageous.nv.vi.utils import gluing_undo_groups
from NeoVintageous.nv.vi.utils import regions_transformer
from NeoVintageous.nv.vi.utils import translate_char
from NeoVintageous.nv.vim import console_message
from NeoVintageous.nv.vim import get_logger
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import message
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import REPLACE
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import status_message
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE


__all__ = [
    '_nv_cmdline_handle_key',
    '_nv_feed_key',
    '_nv_fix_st_eol_caret',
    '_nv_goto_help',
    '_vi_question_mark_on_parser_done',
    '_vi_slash_on_parser_done',
    'FsCompletion',
    'NeovintageousOpenMyRcFileCommand',
    'NeovintageousReloadMyRcFileCommand',
    'NeovintageousToggleSideBarCommand',
    'ProcessNotation',
    'Sequence',
    'TabControlCommand',
    'ViColonInput',
    'ViSettingCompletion',
    'WriteFsCompletion'
]


_log = get_logger(__name__)


class _nv_cmdline_handle_key(TextCommand):

    LAST_HISTORY_ITEM_INDEX = None

    def run(self, edit, key):
        if self.view.size() == 0:
            raise RuntimeError('expected a non-empty command-line')

        if self.view.size() == 1 and key not in ('<up>', '<C-n>', '<down>', '<C-p>', '<C-c>', '<C-[>'):
            return

        if key in ('<up>', '<C-p>'):
            # Recall older command-line from history, whose beginning matches
            # the current command-line.
            self._next_history(edit, backwards=True)

        elif key in ('<down>', '<C-n>'):
            # Recall more recent command-line from history, whose beginning
            # matches the current command-line.
            self._next_history(edit, backwards=False)

        elif key in ('<C-b>', '<home>'):
            # Cursor to beginning of command-line.
            self.view.sel().clear()
            self.view.sel().add(1)

        elif key in ('<C-c>', '<C-[>'):
            # Quit command-line without executing.
            self.view.window().run_command('hide_panel', {'cancel': True})

        elif key in ('<C-e>', '<end>'):
            # Cursor to end of command-line.
            self.view.sel().clear()
            self.view.sel().add(self.view.size())

        elif key == '<C-h>':
            # Delete the character in front of the cursor.
            pt_end = self.view.sel()[0].b
            pt_begin = pt_end - 1
            self.view.erase(edit, Region(pt_begin, pt_end))

        elif key == '<C-u>':
            # Remove all characters between the cursor position and the
            # beginning of the line.
            self.view.erase(edit, Region(1, self.view.sel()[0].end()))

        elif key == '<C-w>':
            # Delete the |word| before the cursor.
            word_region = self.view.word(self.view.sel()[0].begin())
            word_region = self.view.expand_by_class(self.view.sel()[0].begin(), CLASS_WORD_START)
            word_start_pt = word_region.begin()
            caret_end_pt = self.view.sel()[0].end()
            word_part_region = Region(max(word_start_pt, 1), caret_end_pt)
            self.view.erase(edit, word_part_region)
        else:
            raise NotImplementedError('unknown key')

    def _next_history(self, edit, backwards):
        if self.view.size() == 0:
            raise RuntimeError('expected a non-empty command-line')

        firstc = self.view.substr(0)
        if not history_get_type(firstc):
            raise RuntimeError('expected a valid command-line')

        if _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX is None:
            _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX = -1 if backwards else 0
        else:
            _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX += -1 if backwards else 1

        count = history_len(firstc)
        if count == 0:
            _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX = None

            return ui_bell()

        if abs(_nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX) > count:
            _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX = -count

            return ui_bell()

        if _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX >= 0:
            _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX = 0

            if self.view.size() > 1:
                return self.view.erase(edit, Region(1, self.view.size()))
            else:
                return ui_bell()

        if self.view.size() > 1:
            self.view.erase(edit, Region(1, self.view.size()))

        item = history_get(firstc, _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX)
        if item:
            self.view.insert(edit, 1, item)

    @staticmethod
    def reset_last_history_index():  # type: () -> None
        _nv_cmdline_handle_key.LAST_HISTORY_ITEM_INDEX = None


class _nv_fix_st_eol_caret(TextCommand):

    # Tries to workaround some of the Sublime Text issues where the cursor caret
    # is positioned, off-by-one, at the end of line i.e. the caret positions
    # itself at >>>eol| |<<< instead of >>>eo|l|<<<. In some cases, the cursor
    # positions itself at >>>eol| |<<<, and then a second later,  moves to the
    # correct position >>>eo|l|<<< e.g. a left mouse click after the end of a
    # line. Some of these issues can't be worked-around e.g. the mouse click
    # issue described above.

    def run(self, edit, mode=None):
        def f(view, s):
            if mode in (NORMAL, INTERNAL_NORMAL):
                if ((view.substr(s.b) == '\n' or s.b == view.size()) and not view.line(s.b).empty()):
                    return Region(s.b - 1)

            return s

        regions_transformer(self.view, f)


class _nv_goto_help(WindowCommand):
    def run(self):
        view = self.window.active_view()
        pt = view.sel()[0]
        # scope_name() needs to striped due to a bug in ST:
        # See https://github.com/SublimeTextIssues/Core/issues/657.
        scope = view.scope_name(pt.b).rstrip()

        # TODO Fix jumptags scopes (rename them to less generic scopes)
        jumptag_scopes = [
            'text.neovintageous.help string.neovintageous',
            'text.neovintageous.help support.constant.neovintageous'
        ]

        if scope not in jumptag_scopes:
            return

        subject = view.substr(view.extract_scope(pt.b))

        if len(subject) < 3:
            return message('E149: Sorry, no help for %s' % subject)

        match = re.match('^\'[a-z_]+\'|\\|[^\\s\\|]+\\|$', subject)
        if match:
            subject = subject.strip('|')
            # TODO Refactor ex_help code into a reusable middle layer so that
            # this command doesn't have to call the ex command.
            self.window.run_command('ex_help', {'command_line': 'help ' + subject})
        else:
            return message('E149: Sorry, no help for %s' % subject)


class _nv_feed_key(ViWindowCommandBase):

    # Interact with the global state each time a key is pressed.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, key, repeat_count=None, do_eval=True, check_user_mappings=True):
        # Args:
        #   key (str): Key pressed.
        #   repeat_count (int): Count to be used when repeating through the '.' command.
        #   do_eval (bool): Whether to evaluate the global state when it's in a
        #       runnable state. Most of the time, the default value of `True` should
        #       be used. Set to `False` when you want to manually control the global
        #       state's evaluation. For example, this is what the _nv_feed_key
        #       command does.
        #   check_user_mappings (bool):
        # type: (str, int, bool, bool) -> None
        _log.info('key evt: %s repeat_count=%s do_eval=%s check_user_mappings=%s', key, repeat_count, do_eval, check_user_mappings)  # noqa: E501
        state = self.state

        # If the user has made selections with the mouse, we may be in an
        # inconsistent state. Try to remedy that.
        if (state.view.has_non_empty_selection_region() and
            state.mode not in (VISUAL,
                               VISUAL_LINE,
                               VISUAL_BLOCK,
                               SELECT)):
                init_state(state.view)

        if key.lower() == '<esc>':
            self.window.run_command('_enter_normal_mode', {'mode': state.mode})
            state.reset_command_data()

            return

        state.sequence += key
        state.display_status()

        if state.must_capture_register_name:
            _log.debug('capturing register name...')
            state.register = key
            state.partial_sequence = ''

            return

        if state.must_collect_input:
            _log.debug('collecting input...')
            state.process_input(key)
            if state.runnable():
                _log.debug('state is runnable')
                if do_eval:
                    _log.debug('evaluating state...')
                    state.eval()
                    state.reset_command_data()

            return

        if repeat_count:
            state.action_count = str(repeat_count)

        if self._handle_count(state, key, repeat_count):
            _log.debug('handled count')

            return

        state.partial_sequence += key

        if check_user_mappings and mappings_is_incomplete(state.mode, state.partial_sequence):
            _log.debug('found incomplete mapping')

            return

        command = mappings_resolve(state, check_user_mappings=check_user_mappings)

        if isinstance(command, ViOpenRegister):
            _log.debug('opening register...')
            state.must_capture_register_name = True

            return

        # XXX: This doesn't seem to be correct. If we are in OPERATOR_PENDING mode, we should
        # most probably not have to wipe the state.
        if isinstance(command, Mapping):
            _log.debug('found user mapping...')

            if do_eval:
                _log.debug('evaluating user mapping...')

                new_keys = command.mapping
                if state.mode == OPERATOR_PENDING:
                    new_keys = state.sequence[:-len(state.partial_sequence)] + command.mapping
                reg = state.register
                acount = state.action_count
                mcount = state.motion_count
                state.reset_command_data()
                state.register = reg
                state.motion_count = mcount
                state.action_count = acount

                _log.info('user mapping %s -> %s', key, new_keys)

                # Support for basic Command-line mode mappings:
                #
                # `:Command<CR>` maps to Sublime Text command (starts with uppercase letter).
                # `:command<CR>` maps to Command-line mode command.

                if ':' in new_keys:
                    match = re.match('^\\:(?P<cmd_line_command>[a-zA-Z][a-zA-Z_]*)\\<CR\\>', new_keys)
                    if match:
                        cmd_line_command = match.group('cmd_line_command')
                        if cmd_line_command[0].isupper():
                            # run regular sublime text command
                            def _coerce_to_snakecase(string):
                                string = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', string)
                                string = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', string)
                                string = string.replace("-", "_")

                                return string.lower()

                            command = _coerce_to_snakecase(cmd_line_command)
                            command_args = {}
                        else:
                            command = 'vi_colon_input'
                            command_args = {'cmd_line': ':' + cmd_line_command}

                        _log.info('run command -> %s %s', command, command_args)

                        return self.window.run_command(command, command_args)

                    if ':' == new_keys:
                        return self.window.run_command('vi_colon_input')

                    return console_message('invalid command line mapping %s -> %s (only `:[a-zA-Z][a-zA-Z_]*<CR>` is supported)' % (command.head, command.mapping))  # noqa: E501

                self.window.run_command('process_notation', {'keys': new_keys, 'check_user_mappings': False})

            return

        if isinstance(command, ViOpenNameSpace):
            # Keep collecting input to complete the sequence. For example, we
            # may have typed 'g'
            _log.info('opening namespace')

            return

        elif isinstance(command, ViMissingCommandDef):
            _log.info('found missing command...')

            bare_seq = to_bare_command_name(state.sequence)
            if state.mode == OPERATOR_PENDING:
                # We might be looking at a command like 'dd'. The first 'd' is
                # mapped for normal mode, but the second is missing in
                # operator pending mode, so we get a missing command. Try to
                # build the full command now.
                #
                # Exclude user mappings, since they've already been given a
                # chance to evaluate.
                command = mappings_resolve(state, sequence=bare_seq, mode=NORMAL, check_user_mappings=False)
            else:
                command = mappings_resolve(state, sequence=bare_seq)

            if isinstance(command, ViMissingCommandDef):
                _log.debug('unmapped sequence %s', state.sequence)
                state.mode = NORMAL
                state.reset_command_data()

                return ui_blink()

        if (state.mode == OPERATOR_PENDING and isinstance(command, ViOperatorDef)):
            _log.info('found operator pending...')
            # TODO: This may be unreachable code by now. ???
            # we're expecting a motion, but we could still get an action.
            # For example, dd, g~g~ or g~~
            # remove counts
            action_seq = to_bare_command_name(state.sequence)
            _log.debug('action sequence %s', action_seq)
            command = mappings_resolve(state, sequence=action_seq, mode=NORMAL)
            # TODO: Make _missing a command.
            if isinstance(command, ViMissingCommandDef):
                _log.debug('unmapped sequence %s', state.sequence)
                state.reset_command_data()
                return

            if not command['motion_required']:
                state.mode = NORMAL

        state.set_command(command)

        if state.mode == OPERATOR_PENDING:
            state.reset_partial_sequence()

        if do_eval:
            _log.info('evaluating state...')
            state.eval()

    def _handle_count(self, state, key, repeat_count):
        """Return True if the processing of the current key needs to stop."""
        if not state.action and key.isdigit():
            if not repeat_count and (key != '0' or state.action_count):
                _log.debug('action count digit %s', key)
                state.action_count += key
                return True

        if (state.action and (state.mode == OPERATOR_PENDING) and key.isdigit()):
            if not repeat_count and (key != '0' or state.motion_count):
                _log.debug('motion count digit %s', key)
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
        _log.debug('process notation keys \'%s\', mode \'%s\'', keys, state.mode)
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
            self.window.run_command('_nv_feed_key', {
                'key': key,
                'do_eval': False,
                'repeat_count': repeat_count,
                'check_user_mappings': check_user_mappings
            })
            if state.action:
                # The last key press has caused an action to be primed. That
                # means there are no more leading motions. Break out of here.
                _log.debug('[process_notation] first action found in \'%s\'', state.sequence)
                state.reset_command_data()
                if state.mode == OPERATOR_PENDING:
                    state.mode = NORMAL

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

            _log.debug('[process_notation] original seq/leading motions: %s/%s', keys, leading_motions)
            keys = keys[len(leading_motions):]
            _log.debug('[process_notation] seq stripped to \'%s\'', keys)

        if not (state.motion and not state.action):
            with gluing_undo_groups(self.window.active_view(), state):
                try:
                    for key in KeySequenceTokenizer(keys).iter_tokenize():
                        if key.lower() == key_names.ESC:
                            # XXX: We should pass a mode here?
                            self.window.run_command('_enter_normal_mode')
                            continue

                        elif state.mode not in (INSERT, REPLACE):
                            self.window.run_command('_nv_feed_key', {
                                'key': key,
                                'repeat_count': repeat_count,
                                'check_user_mappings': check_user_mappings
                            })
                        else:
                            self.window.run_command('insert', {
                                'characters': translate_char(key)
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
        _log.debug('[process_notation] unsatisfied parser action=\'%s\', motion=\'%s\'', state.action, state.motion)
        if (state.action and state.motion):
            # We have a parser an a motion that can collect data. Collect data
            # interactively.
            motion_data = state.motion.translate(state) or None

            if motion_data is None:
                state.reset_command_data()

                return ui_blink()

            motion_data['motion_args']['default'] = state.motion._inp

            self.window.run_command(motion_data['motion'], motion_data['motion_args'])

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
            if parser_def.interactive_command:

                self.window.run_command(
                    parser_def.interactive_command,
                    {parser_def.input_param: command._inp}
                )
        except IndexError:
            _log.debug('[process_notation] could not find a command to collect more user input')
            ui_blink()
        finally:
            self.state.non_interactive = False


class ViColonInput(WindowCommand):
    interactive_call = True

    def is_enabled(self):
        return bool(self.window.active_view())

    def adjust_initial_text(self, text):
        state = State(self.window.active_view())
        if state.mode in (VISUAL, VISUAL_LINE):
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

        ui_cmdline_prompt(
            self.window,
            initial_text=self.adjust_initial_text(initial_text),
            on_done=self.on_done,
            on_change=self.on_change,
            on_cancel=self.on_cancel)

        state = State(self.window.active_view())
        state.reset_during_init = False

    def on_change(self, s):
        if s == '':
            return self._force_cancel()

        if len(s) <= 1:
            return

        if s[0] != ':':
            return self._force_cancel()

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
        if len(cmd_line) <= 1:
            return

        if cmd_line[0] != ':':
            return

        if ViColonInput.interactive_call:
            history_update(cmd_line)

        _nv_cmdline_handle_key.reset_last_history_index()

        try:
            parsed = parse_command_line(cmd_line[1:])
            if not parsed.command:
                parsed.command = TokenCommandGoto()

            cmd = parsed.command.target_command
            args = {'command_line': cmd_line[1:]}

            _log.debug('run command %s %s', cmd, args)
            self.window.run_command(cmd, args)
        except Exception as e:
            message('{} ({})'.format(str(e), cmd_line))
            _log.exception('{}'.format(cmd_line))

    def _force_cancel(self):
        self.on_cancel()
        self.window.run_command('hide_panel', {'cancel': True})

    def on_cancel(self):
        _nv_cmdline_handle_key.reset_last_history_index()


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
    def invalidate():  # type: () -> None
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
    def invalidate():  # type: () -> None
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


class NeovintageousOpenMyRcFileCommand(WindowCommand):
    """A command that opens the the user runtime configuration file."""

    def run(self):
        rc.open(self.window)


class NeovintageousReloadMyRcFileCommand(WindowCommand):
    """A command that reloads the user runtime configuration file."""

    def run(self):
        rc.reload()

        status_message('rc file reloaded')


class NeovintageousToggleSideBarCommand(WindowCommand):

    def run(self, **kwargs):
        self.window.run_command('toggle_side_bar')

        # is_sidebar_visible() api requires >= 3115.
        if self.window.is_sidebar_visible():
            self.window.run_command('focus_side_bar')
        else:
            self.window.focus_group(self.window.active_group())


class _vi_slash_on_parser_done(WindowCommand):

    def run(self, key=None):
        state = State(self.window.active_view())
        state.motion = ViSearchForwardImpl()
        state.last_buffer_search = (state.motion._inp or state.last_buffer_search)


class _vi_question_mark_on_parser_done(WindowCommand):

    def run(self, key=None):
        state = State(self.window.active_view())
        state.motion = ViSearchBackwardImpl()
        state.last_buffer_search = (state.motion._inp or state.last_buffer_search)


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
                return message("E445: Other window contains changes")

            for view in group:
                if view.id() == self._view.id():
                    continue
                self.window.focus_view(view)
                self.window.run_command('ex_quit', {
                    'command_line': quit_command_line})

            self.window.focus_view(self._view)

        else:
            return message('unknown tab control command')
