from NeoVintageous.lib.nvim import get_logger
from NeoVintageous.lib.vi.cmd_base import CMD_TYPE_USER
from NeoVintageous.lib.vi.keys import KeySequenceTokenizer
from NeoVintageous.lib.vi.keys import seq_to_command
from NeoVintageous.lib.vi.keys import to_bare_command_name
from NeoVintageous.lib.vi.utils import INSERT_MODE
from NeoVintageous.lib.vi.utils import NORMAL_MODE
from NeoVintageous.lib.vi.utils import OPERATOR_PENDING_MODE
from NeoVintageous.lib.vi.utils import SELECT_MODE
from NeoVintageous.lib.vi.utils import VISUAL_BLOCK_MODE
from NeoVintageous.lib.vi.utils import VISUAL_LINE_MODE
from NeoVintageous.lib.vi.utils import VISUAL_MODE
from NeoVintageous.lib.vi.variables import expand_keys


_log = get_logger(__name__)


# Currently not used anywhere else so marked as private (underscore prefix). If
# needed they can be refactored and made available to other modules. Add a
# prefix of something like "MAPPING_STATUS_" if making these public.
_STATUS_INCOMPLETE = 1
_STATUS_COMPLETE = 2


_mappings = {
    INSERT_MODE: {},
    NORMAL_MODE: {},
    OPERATOR_PENDING_MODE: {},
    SELECT_MODE: {},
    VISUAL_BLOCK_MODE: {},
    VISUAL_LINE_MODE: {},
    VISUAL_MODE: {}
}  # type: dict


class Mapping:

    def __init__(self, head, mapping, tail, status):
        self.mapping = mapping
        self.head = head
        self.tail = tail
        self.status = status

    @property
    def sequence(self):
        try:
            return self.head + self.tail
        except TypeError:
            raise ValueError('no mapping found')


# TODO [review] See about refactoring the Mappings class into a functional api.
class Mappings:

    def __init__(self, state):
        self.state = state

    def _get_mapped_seqs(self, mode):
        # type: (str) -> list
        return sorted(_mappings[mode])

    def _find_partial_match(self, mode, seq):
        # type: (str, str) -> list
        return [x for x in self._get_mapped_seqs(mode) if x.startswith(seq)]

    # TODO [review] Should thiis really accept empty string i.e. if seq='' then this all sequences for the mode are returned? # noqa
    def _find_full_match(self, mode, seq):
        # type: (str, str) -> tuple
        #
        # Returns:
        #   tuple: (None, None) if not found.
        #
        # Raises:
        #   IndexError: If has partial sequences, but not a full match.
        #
        # TODO [refactor] There doesn't look there is a need to use partials.
        partials = self._find_partial_match(mode, seq)

        try:

            # FIXME Possibly related to #46. We're not returning the view's
            # current mode. The command implementing > will incorrectly get mode
            # VISUAL when issued from VISUAL_BLOCK_MODE e.g with `:vmap > >gv`.
            # See https://github.com/NeoVintageous/NeoVintageous/issues/46.

            name = [x for x in partials if x == seq][0]

            return (name, _mappings[mode][name])
        except IndexError:
            return (None, None)

    def expand(self, seq):
        pass

    def expand_first(self, seq):
        head = ''

        keys, mapped_to = self._find_full_match(self.state.mode, seq)
        if keys:
            return Mapping(seq, mapped_to['name'], seq[len(keys):], _STATUS_COMPLETE)

        for key in KeySequenceTokenizer(seq).iter_tokenize():
            head += key
            keys, mapped_to = self._find_full_match(self.state.mode, head)
            if keys:
                return Mapping(head, mapped_to['name'], seq[len(head):], _STATUS_COMPLETE)
            else:
                break

        if self._find_partial_match(self.state.mode, seq):
            return Mapping(seq, '', '', _STATUS_INCOMPLETE)

    # XXX: Provisional. Get rid of this as soon as possible.
    def _can_be_long_user_mapping(self, key):
        full_match = self._find_full_match(self.state.mode, key)
        partial_matches = self._find_partial_match(self.state.mode, key)
        if partial_matches:
            return (True, full_match[0])

        return (False, True)

    # XXX: Provisional. Get rid of this as soon as possible.
    # e.g. we may have typed 'aa' and there's an 'aaa' mapping, so we need to keep collecting input.
    # TODO [refactor] To always return a boolean,
    def incomplete_user_mapping(self):
        (maybe_mapping, complete) = self._can_be_long_user_mapping(self.state.partial_sequence)
        if maybe_mapping and not complete:
            return True

    def resolve(self, sequence=None, mode=None, check_user_mappings=True):
        # Look at the current global state and return the command mapped to the available sequence.
        #
        # Args:
        #   sequence (str): The command sequence. If a sequence is passed, it is
        #       used instead of the global state's. This is necessary for some
        #       commands that aren't name spaces but act as them (for example,
        #       ys from the surround plugin).
        #   mode (str): If different than None, it will be used instead of the
        #       global state's. This is necessary when we are in operator
        #       pending mode and we receive a new action. By combining the
        #       existing action's name with name of the action just received we
        #       could find a new action.
        #   check_user_mappings (bool):
        #
        # Returns:
        #   Mapping:
        #   ViMissingCommandDef: If not found.

        # We usually need to look at the partial sequence, but some commands do
        # weird things, like ys, which isn't a namespace but behaves as such
        # sometimes.
        seq = to_bare_command_name(sequence or self.state.partial_sequence)

        # TODO: Use same structure as in mappings (nested dict).
        command = None
        if check_user_mappings:
            # TODO: We should be able to force a mode here too as, below.
            command = self.expand_first(seq)

        if not command:
            command = seq_to_command(self.state, seq, mode=mode)

        _log.debug('resolved %s -> %s -> %s', sequence, seq, command)

        return command

    def add(self, mode, new, target):
        # type: (str, str, str) -> None
        #
        # Raises:
        #   KeyError: If mode does not exist.
        _mappings[mode][expand_keys(new)] = {
            'name': target,
            'type': CMD_TYPE_USER}

    def remove(self, mode, new):
        # type: (str, str) -> None
        #
        # Raises:
        #   KeyError: If mapping not found.
        try:
            del _mappings[mode][expand_keys(new)]
        except KeyError:
            raise KeyError('mapping not found')

    def clear(self):
        # type: () -> None
        for k in _mappings:
            _mappings[k] = {}
