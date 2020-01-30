# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from NeoVintageous.nv.session import set_session_value

# TODO Implement 'history' option so that the number of history entries
# remembered can be configured.
_MAX_ITEMS = 10000


_HIST_DEFAULT = -2
_HIST_INVALID = -1
_HIST_CMD = 1
_HIST_SEARCH = 2
_HIST_EXPR = 3
_HIST_INPUT = 4
_HIST_DEBUG = 5


_CHAR2TYPE = {
    ':': _HIST_CMD,
    '=': _HIST_EXPR,
    '@': _HIST_INPUT,
    '>': _HIST_DEBUG,
    '/': _HIST_SEARCH,
    '?': _HIST_SEARCH
}


_NAME2TYPE = {
    'cmd': _HIST_CMD,
    'search': _HIST_SEARCH,
    'expr': _HIST_EXPR,
    'input': _HIST_INPUT,
    'debug': _HIST_DEBUG
}


_storage = {
    _HIST_CMD: {
        'num': 0,
        'items': {}
    },
    _HIST_SEARCH: {
        'num': 0,
        'items': {}
    },
    _HIST_EXPR: {
        'num': 0,
        'items': {}
    },
    _HIST_INPUT: {
        'num': 0,
        'items': {}
    },
    _HIST_DEBUG: {
        'num': 0,
        'items': {}
    }
}  # type: dict


def _char2type(char: str) -> int:
    try:
        return _CHAR2TYPE[char]
    except KeyError:
        return _HIST_INVALID


def _name2type(name: str) -> int:
    try:
        return _NAME2TYPE[name]
    except KeyError:
        return _HIST_INVALID


def history_get_type(history: str) -> int:
    # Convert history name to its _HIST_ equivalent.
    #
    # Returns:
    #   int: Any of the _HIST constants, including _HIST_INVALID.
    if history in _CHAR2TYPE:
        return _CHAR2TYPE[history]

    if history in _NAME2TYPE:
        return _NAME2TYPE[history]

    return _HIST_INVALID


def history_update(item: str) -> None:
    firstc = item[0]
    histtype = _char2type(firstc)
    if histtype != _HIST_INVALID:
        if len(item) > 1:
            item = item[1:]
            history_add(firstc, item)


def history_add(history: str, item: str) -> int:
    # Add an string {item} to the history {history}, which can be one of:
    #
    #   "cmd"     or ":"         command line history
    #   "search"  or "/"  or "?" search pattern history
    #   "expr"    or "="         typed expression history
    #   "input"   or "@"         input line history
    #   "debug"   or ">"         debug command history
    #
    # If item already exists in the history, it will be shifted to become the
    # newest entry.
    #
    # The result is a Number: 1 if the operation was successful, otherwise 0 is
    # returned.
    #
    # Args:
    #   :history (str): See |hist-names| for the possible values of history.
    #   :item (str):
    #
    # Returns:
    #   int: 1 for a successful operation, otherwise 0
    if _MAX_ITEMS == 0:
        return 0

    history_type = history_get_type(history)

    pending_deletes = [k for k, v in _storage[history_type]['items'].items() if v == item]
    for pending_delete in pending_deletes:
        del _storage[history_type]['items'][pending_delete]

    _storage[history_type]['num'] += 1
    _storage[history_type]['items'][_storage[history_type]['num']] = item

    if len(_storage[history_type]['items']) > _MAX_ITEMS:
        del _storage[history_type]['items'][min(_storage[history_type]['items'].keys())]

    # TODO Refactor history _storage to use session store directly i.e. remove the need for the _storage variable.
    set_session_value('history', _storage, persist=True)

    return 1


def history_clear() -> None:
    for key in _storage:
        _storage[key] = {'num': 0, 'items': {}}


def history_del(history: str, item=None) -> int:
    # Delete an item from a history.
    #
    # Clear history, i.e. delete all its entries. See |hist-names| for the
    # possible values of history.
    #
    # If item evaluates to an int, it will be interpreted as an index, see
    # |history-indexing|. The respective entry will be removed if it exists.
    #
    # Args:
    #   :history (str): See |hist-names| for the possible values of history.
    #   :item (str):
    #
    # Returns:
    #   int: 1 for a successful operation, otherwise 0

    history_type = history_get_type(history)
    if history_type == _HIST_INVALID:
        return 0

    if item is None:
        _storage[history_type]['num'] = 0
        _storage[history_type]['items'] = {}
        ret = 1
    else:
        if isinstance(item, int):
            try:
                if item >= 0:
                    del _storage[history_type]['items'][item]
                    ret = 1
                else:
                    keys = sorted(_storage[history_type]['items'].keys())
                    key_index = keys[item]
                    del _storage[history_type]['items'][key_index]
                    ret = 1
            except (KeyError, IndexError):
                ret = 0
        else:
            raise NotImplementedError('history_del(history, item) where item is regular expression')

    return ret


def history_get(history: str, index: int = -1) -> str:
    # Get the item history from a history.
    #
    # The result is a str, the entry with int index from history. See
    # |hist-names| for the possible values of history, and |history-indexing|
    # for index. If there is no such entry, an empty str is returned. When
    # index is omitted, the most recent item from the history is used.
    #
    # Args:
    #   :history (str): See |hist-names| for the possible values of history.
    #   :index (int):
    #
    # Returns:
    #   str:
    history_type = history_get_type(history)
    if history_type == _HIST_INVALID:
        return ''

    try:
        # A positive int represents the absolute index of an entry.
        if index >= 0:
            ret = _storage[history_type]['items'][index]
        else:
            keys = sorted(_storage[history_type]['items'].keys())
            key_index = keys[index]
            ret = _storage[history_type]['items'][key_index]

    except Exception:
        ret = ''

    return ret


def history_len(history: str) -> int:
    return len(_storage[history_get_type(history)]['items'])


def history_nr(history: str) -> int:
    # Get highest index of a history.
    #
    # Args:
    #   :history (str): See |hist-names| for the possible values of history.
    #
    # Returns:
    #   int: -1 if no current entries or if an error occurred, otherwise the int
    #       of the current entry in history.
    history_type = history_get_type(history)
    if history_type == _HIST_INVALID:
        return -1

    items = _storage[history_type]['items'].keys()
    if len(items) > 0:
        num = max(items)
    else:
        num = -1

    return num


def history(name: str) -> str:
    # Args:
    #   :name (str): See |hist-names| for the possible values of name.
    #
    # Returns:
    #   str:

    # TODO use 'history' option (default=50)
    # TODO if 'history' option is 0 then print message "'history' option is zero"

    if name == 'all':
        history_types = sorted([_HIST_CMD, _HIST_EXPR, _HIST_INPUT, _HIST_DEBUG, _HIST_SEARCH])
    else:
        history_type = history_get_type(name)
        if history_type == _HIST_INVALID:
            return ''

        history_types = [history_type]

    buf = []

    type2name = {
        _HIST_CMD: 'cmd',
        _HIST_SEARCH: 'search',
        _HIST_EXPR: 'expr',
        _HIST_INPUT: 'input',
        _HIST_DEBUG: 'debug'
    }

    for history_type in history_types:
        name = type2name[history_type]
        contents = _storage[history_type]['items']
        count = len(contents)

        # TODO initial padding should be size of max history width
        buf.append('%6s  %s history' % ('#', name))
        for i, number in enumerate(sorted(contents, reverse=False), start=1):
            if i == count:
                buf.append('>%5d  %s' % (number, contents[number]))
            else:
                buf.append('%6d  %s' % (number, contents[number]))

    return '\n'.join(buf)
