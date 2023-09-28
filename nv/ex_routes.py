# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from collections import OrderedDict
from string import ascii_letters
import re

from NeoVintageous.nv.ex.tokens import TokenCommand


def _create_route(state, name: str, forcable: bool = False, **kwargs) -> TokenCommand:
    command = TokenCommand(name, **kwargs)

    if forcable and state.match('!'):
        command.forced = True

    return command


def _create_word_route(state, name: str, word: str, forcable: bool = False, **kwargs) -> TokenCommand:
    command = _create_route(state, name, forcable, **kwargs)
    command.params.update(
        state.expect_match('\\s*(?P<' + word + '>.+)\\s*$').groupdict()
    )

    return command


def _create_count_param_route(state, name: str, param: str = 'count', forcable: bool = False, **kwargs) -> TokenCommand:
    command = _create_route(state, name, forcable, **kwargs)

    match = state.match('\\s*(?P<' + param + '>[1-9][0-9]*)')
    if match:
        command.params[param] = int(match.group(param))

    return command


def _create_map_route(state, name: str) -> TokenCommand:
    command = TokenCommand(name)

    return _resolve(state, command, r'\s*(?P<lhs>.+?)\s+(?P<rhs>.+?)\s*$')


def _create_file_route(state, name: str) -> TokenCommand:
    command = _create_route(state, name)

    return _resolve(state, command, '\\s+(?P<file>.+)')


def _resolve(state, command: TokenCommand, pattern: str) -> TokenCommand:
    m = state.match(pattern)
    if m:
        command.params.update(m.groupdict())

    return command


def _ex_route_ascii(state) -> TokenCommand:
    return _create_route(state, 'ascii')


def _ex_route_bfirst(state) -> TokenCommand:
    return _create_route(state, 'bfirst')


def _ex_route_blast(state) -> TokenCommand:
    return _create_route(state, 'blast')


def _ex_route_bnext(state) -> TokenCommand:
    return _create_count_param_route(state, 'bnext', param='N')


def _ex_route_bprevious(state) -> TokenCommand:
    return _create_count_param_route(state, 'bprevious', param='N')


def _ex_route_browse(state) -> TokenCommand:
    return _create_route(state, 'browse')


def _ex_route_buffer(state) -> TokenCommand:
    command = _create_route(state, 'buffer', forcable=True)

    return _resolve(state, command, '\\s*(?P<index>[0-9]+)\\s*$')


def _ex_route_buffers(state) -> TokenCommand:
    return _create_route(state, 'buffers')


def _ex_route_cd(state) -> TokenCommand:
    command = _create_route(state, 'cd', forcable=True)

    state.skip(' ')
    state.ignore()

    if state.match('-'):
        raise NotImplementedError('parameter not implemented')

    m = state.match(r'(?P<path>.+?)\s*$')
    if m:
        command.params.update(m.groupdict())

    return command


def _ex_route_close(state) -> TokenCommand:
    return _create_route(state, 'close', forcable=True)


def _ex_route_copy(state) -> TokenCommand:
    command = _create_route(state, 'copy', addressable=True)

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<address>.+$)')
    if m:
        command.params.update(m.groupdict())

    return command


def _ex_route_cquit(state) -> TokenCommand:
    return _create_route(state, 'cquit')


def _ex_route_delete(state) -> TokenCommand:
    command = TokenCommand('delete')
    command.cooperates_with_global = True
    command.addressable = True

    params = {'register': '"', 'count': None}

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return command

    state.backup()
    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<register>[a-zA-Z0-9"])(?:\s+(?P<count>\d+))?\s*$')

    params.update(m.groupdict())
    if params['count']:
        raise NotImplementedError('parameter not implemented')

    command.params = params

    return command


def _ex_route_double_ampersand(state) -> TokenCommand:
    command = TokenCommand('&&', target='double_ampersand')
    command.addressable = True

    params = {'flags': [], 'count': ''}

    m = state.match(r'\s*([cgr])*\s*(\d*)\s*$')

    params['flags'] = list(m.group(1)) if m.group(1) else []
    params['count'] = m.group(2) or ''

    state.expect_eof()

    command.params = params

    return command


def _ex_route_edit(state) -> TokenCommand:
    command = TokenCommand('edit')

    params = {
        'file_name': None
    }

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return command

    bang = c == '!'
    if not bang:
        state.backup()

    while True:
        c = state.consume()
        if c == state.EOF:
            command.params = params
            command.forced = bang

            return command

        if c in ('+', '#'):
            raise NotImplementedError('parameter not implemented')

        if c != ' ':
            state.match(r'.*')
            params['file_name'] = state.emit().strip()

            state.skip(' ')
            state.ignore()


def _ex_route_file(state) -> TokenCommand:
    return _create_route(state, 'file')


def _ex_route_global(state) -> TokenCommand:
    command = _create_route(state, 'global', forcable=True, addressable=True)

    sep = state.consume()
    if sep in tuple('\\"|' + ascii_letters):
        raise ValueError('bad separator')

    state.ignore()

    params = {}

    while True:
        c = state.consume()

        if c == state.EOF:
            raise ValueError('unexpected EOF in: ' + state.source)

        if c == sep:
            state.backup()

            params['pattern'] = state.emit()

            state.consume()
            state.ignore()
            break

    cmd = state.match(r'.*$').group(0).strip()
    if cmd:
        params['cmd'] = cmd

    command.params = params

    return command


def _ex_route_help(state) -> TokenCommand:
    command = TokenCommand('help')
    match = state.expect_match(r'(?P<bang>!)?\s*(?P<subject>.+)?$').groupdict()
    params = {'subject': match['subject']}
    bang = bool(match['bang'])

    command.params = params
    command.forced = bang

    return command


def _ex_route_inoremap(state) -> TokenCommand:
    return _create_map_route(state, 'inoremap')


def _ex_route_history(state) -> TokenCommand:
    command = _create_route(state, 'history')

    return _resolve(state, command, r'\s*(?P<name>.+)')


def _ex_route_let(state) -> TokenCommand:
    command = TokenCommand('let')
    params = {'name': None, 'value': None}

    m = state.expect_match(
        r'(?P<name>.+?)\s*=\s*(?P<value>.+?)\s*$',
        on_error=lambda: Exception("E121: Undefined variable"))

    params.update(m.groupdict())

    command.params = params

    return command


def _ex_route_marks(state) -> TokenCommand:
    return _create_route(state, 'marks')


def _ex_route_delmarks(state) -> TokenCommand:
    command = _create_route(state, 'delmarks', forcable=True)
    command = _resolve(state, command, '\\s+(?P<marks>.+)')

    return command


def _ex_route_move(state) -> TokenCommand:
    command = _create_route(state, 'move', addressable=True)

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<address>.+$)')
    if m:
        command.params.update(m.groupdict())

    return command


def _ex_route_new(state) -> TokenCommand:
    return _create_file_route(state, 'new')


def _ex_route_nnoremap(state) -> TokenCommand:
    return _create_map_route(state, 'nnoremap')


def _ex_route_nohlsearch(state) -> TokenCommand:
    return _create_route(state, 'nohlsearch')


def _ex_route_noremap(state) -> TokenCommand:
    return _create_map_route(state, 'noremap')


def _ex_route_nunmap(state) -> TokenCommand:
    return _create_word_route(state, 'nunmap', 'lhs')


def _ex_route_only(state) -> TokenCommand:
    return _create_route(state, 'only', forcable=True)


def _ex_route_onoremap(state) -> TokenCommand:
    return _create_map_route(state, 'onoremap')


def _ex_route_ounmap(state) -> TokenCommand:
    return _create_word_route(state, 'ounmap', 'lhs')


def _ex_route_print(state) -> TokenCommand:
    command = TokenCommand('print')
    command.addressable = True
    command.cooperates_with_global = True

    while True:
        c = state.consume()

        state.skip(' ')
        state.ignore()

        if c == state.EOF:
            break

        c = state.consume()
        if c.isdigit():
            state.match(r'\d*')
            command.params['count'] = state.emit()
            continue

        state.backup()

        m = state.expect_match(r'[l#p]+')
        command.params['flags'] = list(m.group(0))
        state.ignore()
        state.expect_eof()
        break

    return command


def _ex_route_pwd(state) -> TokenCommand:
    return _create_route(state, 'pwd')


def _ex_route_qall(state) -> TokenCommand:
    return _create_route(state, 'qall', forcable=True)


def _ex_route_quit(state) -> TokenCommand:
    return _create_route(state, 'quit', forcable=True)


def _ex_route_read(state) -> TokenCommand:
    command = TokenCommand('read', addressable=True)

    state.skip(' ')
    state.ignore()

    c = state.consume()

    if c == '+':
        raise NotImplementedError('parameter not implemented')

    elif c == '!':
        m = state.match(r'(?P<cmd>.+)')
        command.params.update(m.groupdict())

    else:
        state.backup()
        m = state.match(r'(?P<file_name>.+)$')
        command.params.update(m.groupdict())

    state.expect_eof()

    return command


def _ex_route_registers(state) -> TokenCommand:
    return _create_route(state, 'registers')


def _ex_route_set(state) -> TokenCommand:
    command = TokenCommand('set')
    command.params.update(
        state.expect_match(r'\s*(?P<option>.+?)\s*(?:=\s*(?P<value>.*))?$').groupdict()
    )

    return command


def _ex_route_setlocal(state) -> TokenCommand:
    command = TokenCommand('setlocal')
    command.params.update(
        state.expect_match(r'\s*(?P<option>.+?)\s*(?:=\s*(?P<value>.*))?$').groupdict()
    )

    return command


def _ex_route_shell(state) -> TokenCommand:
    return _create_route(state, 'shell')


def _ex_route_silent(state) -> TokenCommand:
    return _create_word_route(state, 'silent', 'command', forcable=True)


def _ex_route_shell_out(state) -> TokenCommand:
    command = TokenCommand('!', target='shell_out')
    command.addressable = True
    params = {'cmd': None}

    m = state.expect_match(r'(?P<cmd>.+)$')
    params.update(m.groupdict())

    command.params = params

    return command


def _ex_route_snoremap(state) -> TokenCommand:
    return _create_map_route(state, 'snoremap')


def _ex_route_sunmap(state) -> TokenCommand:
    return _create_word_route(state, 'sunmap', 'lhs')


def _ex_route_sort(state) -> TokenCommand:
    command = _create_route(state, 'sort', forcable=True, addressable=True)

    return _resolve(state, command, r'\s*(?P<options>[iu]+)')


def _ex_route_spellgood(state) -> TokenCommand:
    return _create_word_route(state, 'spellgood', 'word')


def _ex_route_spellundo(state) -> TokenCommand:
    return _create_word_route(state, 'spellundo', 'word')


def _ex_route_split(state) -> TokenCommand:
    return _create_file_route(state, 'split')


def _ex_route_substitute(state) -> TokenCommand:
    command = TokenCommand('substitute')
    command.addressable = True

    delim = state.consume()

    if delim == state.EOF:
        return command

    state.backup()
    delim = state.consume()
    params = {
        "pattern": None,
        "replacement": None,
        "count": 1,
        "flags": [],
    }  # type: dict

    while True:
        c = state.consume()

        if c == delim:
            state.start += 1
            state.backup()
            params['pattern'] = state.emit()
            state.consume()
            break

        if c == state.EOF:
            raise ValueError("bad command: {0}".format(state.source))

    while True:
        c = state.consume()
        if c == delim:
            state.start += 1
            state.backup()
            params['replacement'] = state.emit()
            state.consume()
            state.ignore()
            break

        if c == state.EOF:
            state.start += 1
            params['replacement'] = state.emit()
            state.consume()
            state.ignore()
            break

    if state.match(r'\s*[&cegiInp#lr]+'):
        params['flags'] = list(state.emit().strip())
        if '&' in params['flags'] and params['flags'][0] != '&':
            raise ValueError("bad command: {}".format(state.source))

    if state.peek(' '):
        state.skip(' ')
        state.ignore()
        if state.match(r'\d+'):
            params['count'] = int(state.emit())

    state.skip(' ')
    state.ignore()
    state.expect_eof()

    command.params = params

    return command


def _ex_route_tabclose(state) -> TokenCommand:
    return _create_route(state, 'tabclose')


def _ex_route_tabfirst(state) -> TokenCommand:
    return _create_route(state, 'tabfirst')


def _ex_route_tablast(state) -> TokenCommand:
    return _create_route(state, 'tablast')


def _ex_route_tabnext(state) -> TokenCommand:
    return _create_count_param_route(state, 'tabnext')


def _ex_route_tabnew(state) -> TokenCommand:
    return _create_route(state, 'tabnew')


def _ex_route_tabonly(state) -> TokenCommand:
    return _create_route(state, 'tabonly')


def _ex_route_tabprevious(state) -> TokenCommand:
    return _create_count_param_route(state, 'tabprevious')


def _ex_route_unmap(state) -> TokenCommand:
    return _create_word_route(state, 'unmap', 'lhs')


def _ex_route_vnew(state) -> TokenCommand:
    return _create_file_route(state, 'vnew')


def _ex_route_vnoremap(state) -> TokenCommand:
    return _create_map_route(state, 'vnoremap')


def _ex_route_vsplit(state) -> TokenCommand:
    return _create_file_route(state, 'vsplit')


def _ex_route_vunmap(state) -> TokenCommand:
    return _create_word_route(state, 'vunmap', 'lhs')


def _ex_route_wall(state) -> TokenCommand:
    return _create_route(state, 'wall', forcable=True)


def _ex_route_wq(state) -> TokenCommand:
    return _create_route(state, 'wq', forcable=True)


def _ex_route_wqall(state) -> TokenCommand:
    return _create_route(state, 'wqall', forcable=True, addressable=True)


def _ex_route_write(state) -> TokenCommand:
    command = TokenCommand('write')
    command.addressable = True

    params = {
        '++': '',
        'file_name': '',
        '>>': False,
        'cmd': '',
    }

    bang = state.consume()
    if bang == state.EOF:
        command.params = params

        return command

    if bang != '!':
        bang = False
        state.backup()

    state.skip(' ')
    state.ignore()

    plus_plus_translations = {
        'ff': 'fileformat',
        'bin': 'binary',
        'enc': 'fileencoding',
        'nobin': 'nobinary'
    }

    while True:
        c = state.consume()
        if c == state.EOF:
            break

        if c == '+':
            state.expect('+')
            state.ignore()
            # TODO: expect_match should work with emit()
            # https://vimhelp.appspot.com/editing.txt.html#[++opt]
            m = state.expect_match(
                r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
                lambda: Exception("E474: Invalid argument"))

            name = m.group(0)
            params['++'] = plus_plus_translations.get(name, name)
            state.ignore()
            continue

        if c == '>':
            state.expect('>')
            state.ignore()
            params['>>'] = True
            state.match(r'.*$')
            params['file_name'] = state.emit().strip()
            continue

        if c == '!':
            state.ignore()
            state.match(r'.*$')
            params['cmd'] = state.emit()
            continue

        if c != ' ':
            state.match(r'.*')
            params['file_name'] = state.emit().strip()
            state.skip(' ')
            state.ignore()

    command.params = params
    command.forced = bang == '!'

    return command


def _ex_route_xnoremap(state) -> TokenCommand:
    return _create_map_route(state, 'xnoremap')


def _ex_route_xunmap(state) -> TokenCommand:
    return _create_word_route(state, 'xunmap', 'lhs')


def _ex_route_yank(state) -> TokenCommand:
    command = TokenCommand('yank')
    command.addressable = True

    params = {'register': '"', 'count': None}

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return command

    state.backup()
    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<register>[a-zA-Z0-9"])(?:\s+(?P<count>\d+))?\s*$')

    params.update(m.groupdict())
    if params['count']:
        raise NotImplementedError('parameter not implemented')

    command.params = params

    return command


ex_routes = OrderedDict()
ex_completions = []


def _add_ex_route(pattern: str, function, completions=None) -> None:
    ex_routes[re.compile(pattern)] = function

    if completions:
        if isinstance(completions, str):
            ex_completions.append(completions)
        else:
            for completion in completions:
                ex_completions.append(completion)


# Note that the order of the routes is important.
_add_ex_route(r'!(?=.+)', _ex_route_shell_out)
_add_ex_route(r'&&?', _ex_route_double_ampersand)
_add_ex_route(r'(?:files|ls|buffers)!?', _ex_route_buffers, ['files', 'ls', 'buffers'])
_add_ex_route(r'as(?:cii)?', _ex_route_ascii, 'ascii')
_add_ex_route(r'bf(?:irst)?', _ex_route_bfirst, 'bfirst')
_add_ex_route(r'bl(?:ast)?', _ex_route_blast, 'blast')
_add_ex_route(r'bn(?:ext)?', _ex_route_bnext, 'bnext')
_add_ex_route(r'bN(?:ext)?', _ex_route_bprevious, 'bNext')  # alias of :bprevious
_add_ex_route(r'bp(?:revious)?', _ex_route_bprevious, 'bprevious')
_add_ex_route(r'bro(?:wse)?', _ex_route_browse, 'browse')
_add_ex_route(r'br(?:ewind)?', _ex_route_bfirst, 'brewind')
_add_ex_route(r'b(?:uffer)?', _ex_route_buffer, 'buffer')
_add_ex_route(r'cd', _ex_route_cd, 'cd')
_add_ex_route(r'clo(?:se)?', _ex_route_close, 'close')
_add_ex_route(r'co(?:py)?', _ex_route_copy, 'copy')
_add_ex_route(r'cq(?:uit)?', _ex_route_cquit, 'cquit')
_add_ex_route(r'delm(?:arks)?', _ex_route_delmarks, 'delmarks')
_add_ex_route(r'd(?:elete)?', _ex_route_delete, 'delete')
_add_ex_route(r'exi(?:t)?', _ex_route_wq, 'exit')
_add_ex_route(r'e(?:dit)?(?= |$)?', _ex_route_edit, 'edit')
_add_ex_route(r'f(?:ile)?', _ex_route_file, 'file')
_add_ex_route(r'g(?:lobal)?', _ex_route_global, 'global')
_add_ex_route(r'his(?:tory)?', _ex_route_history, 'history')
_add_ex_route(r'h(?:elp)?', _ex_route_help, 'help')
_add_ex_route(r'ino(?:remap)?', _ex_route_inoremap, 'inoremap')
_add_ex_route(r'let\s', _ex_route_let, 'let')
_add_ex_route(r'marks', _ex_route_marks, 'marks')
_add_ex_route(r'm(?:ove)?(?=[^a]|$)', _ex_route_move, 'move')
_add_ex_route(r'new', _ex_route_new, 'new')
_add_ex_route(r'nn(?:oremap)?', _ex_route_nnoremap, 'nnoremap')
_add_ex_route(r'noh(?:lsearch)?', _ex_route_nohlsearch, 'nohlsearch')
_add_ex_route(r'no(?:remap)?', _ex_route_noremap, 'noremap')
_add_ex_route(r'nun(?:map)?', _ex_route_nunmap, 'nunmap')
_add_ex_route(r'ono(?:remap)?', _ex_route_onoremap, 'onoremap')
_add_ex_route(r'on(?:ly)?', _ex_route_only, 'only')
_add_ex_route(r'ou(?:nmap)?', _ex_route_ounmap, 'ounmap')
_add_ex_route(r'pw(?:d)?', _ex_route_pwd, 'pwd')
_add_ex_route(r'p(?:rint)?', _ex_route_print, 'print')
_add_ex_route(r'qa(?:ll)?', _ex_route_qall, 'qall')
_add_ex_route(r'quita(?:ll)?', _ex_route_qall, 'quitall')
_add_ex_route(r'q(?!a)(?:uit)?', _ex_route_quit, 'quit')
_add_ex_route(r'reg(?:isters)?', _ex_route_registers, 'registers')
_add_ex_route(r'r(?!eg)(?:ead)?', _ex_route_read, 'read')
_add_ex_route(r'setl(?:ocal)?', _ex_route_setlocal, 'setlocal')
_add_ex_route(r'se(?:t)?', _ex_route_set, 'set')
_add_ex_route(r's(?:ubstitute)?(?=[%&:/=]|$)', _ex_route_substitute, 'substitute')
_add_ex_route(r'sh(?:ell)?', _ex_route_shell, 'shell')
_add_ex_route(r'sil(?:ent)?', _ex_route_silent, 'silent')
_add_ex_route(r'snor(?:emap)?', _ex_route_snoremap, 'snoremap')
_add_ex_route(r'sor(?:t)?', _ex_route_sort, 'sort')
_add_ex_route(r'spellu(?:ndo)?', _ex_route_spellundo, 'spellundo')
_add_ex_route(r'spe(?:llgood)?', _ex_route_spellgood, 'spellgood')
_add_ex_route(r'sp(?:lit)?', _ex_route_split, 'split')
_add_ex_route(r'sunm(?:ap)?', _ex_route_sunmap, 'sunmap')
_add_ex_route(r'tabc(?:lose)?', _ex_route_tabclose, 'tabclose')
_add_ex_route(r'tabfir(?:st)?', _ex_route_tabfirst, 'tabfirst')
_add_ex_route(r'tabl(?:ast)?', _ex_route_tablast, 'tablast')
_add_ex_route(r'tab(?:new|e(?:dit)?)', _ex_route_tabnew, ['tabnew', 'tabedit'])
_add_ex_route(r'tabn(?:ext)?', _ex_route_tabnext, 'tabnext')
_add_ex_route(r'tabN(?:ext)?', _ex_route_tabprevious, 'tabNext')
_add_ex_route(r'tabo(?:nly)?', _ex_route_tabonly, 'tabonly')
_add_ex_route(r'tabp(?:revious)?', _ex_route_tabprevious, 'tabprevious')
_add_ex_route(r'tabr(?:ewind)?', _ex_route_tabfirst, 'tabrewind')
_add_ex_route(r'unm(?:ap)?', _ex_route_unmap, 'unmap')
_add_ex_route(r'vne(?:w)?', _ex_route_vnew, 'vnew')
_add_ex_route(r'vn(?:oremap)?', _ex_route_vnoremap, 'vnoremap')
_add_ex_route(r'vs(?:plit)?', _ex_route_vsplit, 'vsplit')
_add_ex_route(r'vu(?:nmap)?', _ex_route_vunmap, 'vunmap')
_add_ex_route(r'w(?:rite)?(?=(?:!?(?:\+\+|>>| |$)))', _ex_route_write, 'write')
_add_ex_route(r'wa(?:ll)?', _ex_route_wall, 'wall')
_add_ex_route(r'wqa(?:ll)?', _ex_route_wqall, 'wqall')
_add_ex_route(r'wq(?=[^a-zA-Z]|$)?', _ex_route_wq, 'wq')
_add_ex_route(r'xa(?:ll)?', _ex_route_wqall, 'xall')
_add_ex_route(r'xn(?:oremap)?', _ex_route_xnoremap, 'xnoremap')
_add_ex_route(r'xu(?:nmap)?', _ex_route_xunmap, 'xunmap')
_add_ex_route(r'x(?:it)?', _ex_route_wq, 'xit')
_add_ex_route(r'y(?:ank)?', _ex_route_yank, 'yank')
