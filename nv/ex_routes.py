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

from collections import OrderedDict

from NeoVintageous.nv.ex.tokens import TokenCommand
from NeoVintageous.nv.ex.tokens import TokenEof


# TODO [bug] (all commands) ":command" followed by character that is not "!"  shouldn't be # valid e.g. the ":close" command should run when !:closex". There are a # bunch of commands that have this bug.  # noqa: E501


# TODO Fix broken :abbreviate scanner
def _ex_route_abbreviate(state):
    command = TokenCommand('abbreviate')
    params = {'short': None, 'full': None}

    state.expect(' ')
    state.skip(' ')
    state.ignore()

    if state.consume() == state.EOF:
        return None, [command, TokenEof()]

    state.backup()

    m = state.match(r'(?P<short>.+?)(?: +(?P<full>.+))?$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_browse(state):
    command = TokenCommand('browse')
    # TODO [review] "cmd" param looks unused.
    params = {'cmd': None}

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<cmd>.*)$')

    params.update(m.groupdict())
    if params['cmd']:
        raise NotImplementedError('parameter not implemented')

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_buffers(state):
    command = TokenCommand('buffers')

    try:
        state.expect_eof()
    except ValueError:
        # TODO Use a special domain exception for exceptions raised in scans.
        raise Exception("E488: Trailing characters")

    return None, [command, TokenEof()]


def _ex_route_cd(state):
    command = TokenCommand('cd')

    # TODO [refactor] Should params should used keys compatible with **kwargs? (review other commands too) # noqa: E501
    params = {'path': None, '-': None}
    bang = False

    c = state.consume()
    if c == state.EOF:
        command.params = params
        command.forced = bang

        return None, [command, TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        command.params = params
        command.forced = bang

        return None, [command, TokenEof()]

    if c == '-':
        raise NotImplementedError('parameter not implemented')

    state.backup()
    m = state.match(r'(?P<path>.+?)\s*$')
    params.update(m.groupdict())

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_cdd(state):
    command = TokenCommand('cdd')

    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_close(state):
    command = TokenCommand('close')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_copy(state):
    command = TokenCommand('copy')
    command.addressable = True

    params = {'address': None}
    m = state.expect_match(r'\s*(?P<address>.+?)\s*$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_cquit(state):
    command = TokenCommand('cquit')

    state.expect_eof()

    return None, [command, TokenEof()]


def _ex_route_delete(state):
    command = TokenCommand('delete')
    command.addressable = True

    params = {'register': '"', 'count': None}

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    state.backup()
    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<register>[a-zA-Z0-9"])(?:\s+(?P<count>\d+))?\s*$')

    params.update(m.groupdict())
    if params['count']:
        raise NotImplementedError('parameter not implemented')

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_double_ampersand(state):
    command = TokenCommand('&&', target='ex_double_ampersand')
    command.addressable = True

    params = {'flags': [], 'count': ''}

    m = state.match(r'\s*([cgr])*\s*(\d*)\s*$')

    params['flags'] = list(m.group(1)) if m.group(1) else []
    params['count'] = m.group(2) or ''

    state.expect_eof()

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_edit(state):
    command = TokenCommand('edit')
    # TODO [refactor] Should params should used keys compatible with **kwargs? (review other commands too) # noqa: E501
    params = {
        '++': None,
        'cmd': None,
        'file_name': None,
        'count': None,
    }

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    plus_plus_translations = {
        'ff': 'fileformat',
        'bin': 'binary',
        'enc': 'fileencoding',
        'nobin': 'nobinary'
    }

    while True:
        c = state.consume()

        if c == state.EOF:
            command.params = params
            command.forced = bang

            return None, [command, TokenEof()]

        if c == '+':
            k = state.consume()
            if k == '+':
                state.ignore()
                # TODO: expect_match should work with emit()
                # https://vimhelp.appspot.com/editing.txt.html#[++opt]
                m = state.expect_match(
                    r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
                    lambda: Exception("E474: Invalid argument"))

                name = m.group(0)
                params['++'] = plus_plus_translations.get(name, name)

                state.ignore()

                raise NotImplementedError('param not implemented')
                continue

            state.backup()
            state.ignore()
            state.expect_match(r'.+$')

            params['cmd'] = state.emit()

            raise NotImplementedError('param not implemented')
            continue

        if c != ' ':
            state.match(r'.*')
            params['file_name'] = state.emit().strip()

            state.skip(' ')
            state.ignore()
            continue

        if c == '#':
            state.ignore()
            m = state.expect_match(r'\d+')
            params['count'] = m.group(0)

            raise NotImplementedError('param not implemented')
            continue

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_exit(state):
    command = TokenCommand('exit')
    command.addressable = True

    # TODO [review] file_name param looks unused by the ex_exit
    params = {'file_name': ''}

    bang = state.consume()

    if bang == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    bang = bang == '!'
    if not bang:
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
            command.params = params
            command.forced = bang

            return None, [command, TokenEof()]

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

        if c != ' ':
            state.match(r'.*')
            params['file_name'] = state.emit().strip()
            state.skip(' ')
            state.ignore()

    state.expect_eof()

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_file(state):
    command = TokenCommand('file')
    bang = state.consume()
    if bang == state.EOF:
        return None, [command, TokenEof()]

    bang = bang == '!'
    if not bang:
        raise Exception("E488: Trailing characters")

    state.expect_eof(on_error=lambda: Exception("E488: Trailing characters"))

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_global(state):
    command = TokenCommand('global')
    command.addressable = True
    params = {'pattern': None, 'cmd': None}

    c = state.consume()

    bang = c == '!'
    sep = c if not bang else state.consume()

    # TODO: we're probably missing legal separators.
    # TODO [refactor] and remove assertion
    assert c in '!:?/\\&$', 'bad separator'

    state.ignore()

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
    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_help(state):
    command = TokenCommand('help')
    match = state.expect_match(r'(?P<bang>!)?\s*(?P<subject>.+)?$').groupdict()
    params = {'subject': match['subject']}
    bang = bool(match['bang'])

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_let(state):
    command = TokenCommand('let')
    params = {'name': None, 'value': None}

    m = state.expect_match(
        r'(?P<name>.+?)\s*=\s*(?P<value>.+?)\s*$',
        on_error=lambda: Exception("E121: Undefined variable"))

    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_move(state):
    command = TokenCommand('move')
    command.addressable = True
    params = {'address': None}

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<address>.*$)')
    if m:
        address_command_line = m.group(0).strip() or '.'
        params['address'] = address_command_line

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_new(state):
    command = TokenCommand('new')
    # TODO [refactor] Should params should used keys compatible with **kwargs? (review other commands too) # noqa: E501
    params = {'++': None, 'cmd': None}

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == '+':
        state.expect('+')
        state.ignore()

        # TODO: expect_match should work with emit()
        # https://vimhelp.appspot.com/editing.txt.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: Exception("E474: Invalid argument"))

        name = m.group(0)

        plus_plus_translations = {
            'ff': 'fileformat',
            'bin': 'binary',
            'enc': 'fileencoding',
            'nobin': 'nobinary'
        }

        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()

        raise NotImplementedError(':new not fully implemented')

    m = state.match(r'.+$')
    if m:
        params['cmd'] = m.group(0).strip()
        raise NotImplementedError(':new not fully implemented')

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_nnoremap(state):
    command = TokenCommand('nnoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_noremap(state):
    command = TokenCommand('noremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_nunmap(state):
    command = TokenCommand('nunmap')
    params = {'keys': None}

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_only(state):
    command = TokenCommand('only')

    bang = state.consume()
    if bang == '!':
        state.ignore()
        state.expect_eof()

        command.forced = True

        return None, [command, TokenEof()]

    # TODO [refactor] and remove assertion
    assert bang == state.EOF, 'trailing characters'

    return None, [command, TokenEof()]


def _ex_route_onoremap(state):
    command = TokenCommand('onoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    return None, [command, TokenEof()]


def _ex_route_ounmap(state):
    command = TokenCommand('ounmap')
    params = {'keys': None}

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_print(state):
    command = TokenCommand('print')
    command.addressable = True
    command.cooperates_with_global = True

    # TODO [review] count param looks unused.
    params = {'count': '', 'flags': []}

    while True:
        c = state.consume()

        state.skip(' ')
        state.ignore()

        if c == state.EOF:
            command.params = params

            return None, [command, TokenEof()]

        if c.isdigit():
            state.match(r'\d*')
            params['count'] = state.emit()
            continue

        m = state.expect_match(r'[l#p]+')
        params['flags'] = list(m.group(0))
        state.ignore()
        state.expect_eof()
        break

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_pwd(state):
    command = TokenCommand('pwd')

    state.expect_eof()

    return None, [command, TokenEof()]


def _ex_route_qall(state):
    command = TokenCommand('qall')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_quit(state):
    command = TokenCommand('quit')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_read(state):
    command = TokenCommand('read')
    params = {
        'cmd': None,
        '++': [],
        'file_name': None,
    }

    state.skip(' ')
    state.ignore()

    c = state.consume()

    if c == '+':
        state.expect('+')
        state.ignore()
        # TODO: expect_match should work with emit()
        # https://vimhelp.appspot.com/editing.txt.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: Exception("E474: Invalid argument"))
        name = m.group(0)

        plus_plus_translations = {
            'ff': 'fileformat',
            'bin': 'binary',
            'enc': 'fileencoding',
            'nobin': 'nobinary',
        }

        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()
        raise NotImplementedError('++opt not implemented')

    elif c == '!':
        m = state.match(r'(?P<cmd>.+)')
        params.update(m.groupdict())

    else:
        state.backup()
        m = state.match(r'(?P<file_name>.+)$')
        params.update(m.groupdict())

    state.expect_eof()

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_registers(state):
    command = TokenCommand('registers')
    # TODO [review] "names" param looks unused by ex_registers
    params = {'names': []}

    state.skip(' ')
    state.ignore()

    while True:
        c = state.consume()
        if c == state.EOF:
            command.params = params

            return None, [command, TokenEof()]
        elif c.isalpha() or c.isdigit():
            params['names'].append(c)
        else:
            raise ValueError('wrong arguments')


def _ex_route_set(state):
    command = TokenCommand('set')
    params = {'option': None, 'value': None}

    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<option>.+?)(?:[:=](?P<value>.+?))?$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_setlocal(state):
    command = TokenCommand('setlocal')
    params = {'option': None, 'value': None}

    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<option>.+?)(?:[:=](?P<value>.+?))?$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_shell(state):
    command = TokenCommand('shell')
    state.expect_eof()

    return None, [command, TokenEof()]


def _ex_route_shell_out(state):
    command = TokenCommand('!', target='ex_shell_out')
    command.addressable = True
    params = {'cmd': None}

    m = state.expect_match(r'(?P<cmd>.+)$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_snoremap(state):
    command = TokenCommand('snoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_sunmap(state):
    command = TokenCommand('sunmap')
    params = {'keys': None}

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_split(state):
    command = TokenCommand('split')
    params = {'file': None}

    state.skip(' ')
    state.ignore()

    if state.consume() == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    state.backup()

    params['file'] = state.match(r'.+$').group(0).strip()

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_substitute(state):
    command = TokenCommand('substitute')
    command.addressable = True

    delim = state.consume()

    if delim == state.EOF:
        return None, [command, TokenEof()]

    state.backup()
    delim = state.consume()
    params = {
        "pattern": None,
        "replacement": None,
        "count": 1,
        "flags": [],
    }

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

    return None, [command, TokenEof()]


def _ex_route_tabfirst(state):
    command = TokenCommand('tabfirst')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_tablast(state):
    command = TokenCommand('tablast')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_tabnext(state):
    command = TokenCommand('tabnext')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_tabonly(state):
    command = TokenCommand('tabonly')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_tabprevious(state):
    command = TokenCommand('tabprevious')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_unabbreviate(state):
    command = TokenCommand('unabbreviate')
    params = {'lhs': None}

    m = state.expect_match(r'\s+(?P<lhs>.+?)\s*$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_unmap(state):
    command = TokenCommand('unmap')
    params = {'keys': None}

    # TODO [refactor] Some commands require certain arguments e.g "keys" is a
    # required argument for the unmap ex command. Currently the do_ex_command
    # (may have  been refactored into another name), passes params to the ex
    # commands, and None is valid argument, but in the case of this command
    # it's a required argument, so rather than the ex command deal with the
    # invalid argument, it should be dealt with a) either here, or b) by the
    # command runner.

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_unvsplit(state):
    command = TokenCommand('unvsplit')
    state.expect_eof()

    return None, [command, TokenEof()]


def _ex_route_vnoremap(state):
    command = TokenCommand('vnoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_vsplit(state):
    command = TokenCommand('vsplit')
    params = {'file': None}

    state.skip(' ')
    state.ignore()

    if state.consume() == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    state.backup()

    params['file'] = state.match(r'.+$').group(0).strip()

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_vunmap(state):
    command = TokenCommand('vunmap')
    params = {'keys': None}

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_wall(state):
    command = TokenCommand('wall')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_wq(state):
    command = TokenCommand('wq')
    # TODO [review] None of the prams looks used
    params = {
        '++': None,
        'file': None,
    }

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    bang = True if c == '!' else False
    if not bang:
        state.backup()

    c = state.consume()
    if c == '+':
        state.expect('+')
        state.ignore()

        # TODO: expect_match should work with emit()
        # https://vimhelp.appspot.com/editing.txt.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: Exception("E474: Invalid argument"))

        name = m.group(0)

        plus_plus_translations = {
            'ff': 'fileformat',
            'bin': 'binary',
            'enc': 'fileencoding',
            'nobin': 'nobinary',
        }

        params['++'] = plus_plus_translations.get(name, name)

        state.ignore()
        raise NotImplementedError('param not implemented')

    if c == state.EOF:
        command.params = params
        command.forced = bang

        return None, [command, TokenEof()]

    m = state.expect_match(r'.+$')
    params['file'] = m.group(0).strip()

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_wqall(state):
    command = TokenCommand('wqall')
    command.addressable = True
    params = {'++': ''}

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == '+':
        state.expect('+')
        state.ignore()
        # TODO: expect_match should work with emit()
        # https://vimhelp.appspot.com/editing.txt.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: Exception("E474: Invalid argument"))

        name = m.group(0)

        plus_plus_translations = {
            'ff': 'fileformat',
            'bin': 'binary',
            'enc': 'fileencoding',
            'nobin': 'nobinary'
        }

        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()

    state.expect_eof()

    command.params = params

    return None, [command, TokenEof()]


def _ex_route_write(state):
    command = TokenCommand('write')
    command.addressable = True
    # TODO [refactor] params should used keys compatible with **kwargs, see do_ex_command(). Review other scanners too. # noqa: E501
    params = {
        '++': '',
        'file_name': '',
        '>>': False,
        'cmd': '',
    }

    bang = state.consume()
    if bang == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

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
            # TODO: forced?
            command.params = params
            command.forced = bang

            return None, [command, TokenEof()]

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

    state.expect_eof()

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]


def _ex_route_yank(state):
    command = TokenCommand('yank')
    command.addressable = True

    params = {'register': '"', 'count': None}

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    state.backup()
    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<register>[a-zA-Z0-9"])(?:\s+(?P<count>\d+))?\s*$')

    params.update(m.groupdict())
    if params['count']:
        raise NotImplementedError('parameter not implemented')

    command.params = params

    return None, [command, TokenEof()]


# TODO: compile regexes. ??
ex_routes = OrderedDict()
ex_routes[r'!(?=.+)'] = _ex_route_shell_out
ex_routes[r'&&?'] = _ex_route_double_ampersand
ex_routes[r'ab(?:breviate)?'] = _ex_route_abbreviate
ex_routes[r'bro(?:wse)?'] = _ex_route_browse
ex_routes[r'clo(?:se)?'] = _ex_route_close
ex_routes[r'co(?:py)?'] = _ex_route_copy
ex_routes[r'cq(?:uit)?'] = _ex_route_cquit
ex_routes[r'd(?:elete)?'] = _ex_route_delete
ex_routes[r'exi(?:t)?'] = _ex_route_exit
ex_routes[r'(?:files|ls|buffers)!?'] = _ex_route_buffers
ex_routes[r'f(?:ile)?'] = _ex_route_file
ex_routes[r'g(?:lobal)?(?=[^ ])'] = _ex_route_global
ex_routes[r'h(?:elp)?'] = _ex_route_help
ex_routes[r'vs(?:plit)?'] = _ex_route_vsplit
ex_routes[r'x(?:it)?$'] = _ex_route_exit
ex_routes[r'^cd(?=[^d]|$)'] = _ex_route_cd
ex_routes[r'^cdd'] = _ex_route_cdd
ex_routes[r'e(?:dit)?(?= |$)?'] = _ex_route_edit
ex_routes[r'let\s'] = _ex_route_let
ex_routes[r'm(?:ove)?(?=[^a]|$)'] = _ex_route_move
ex_routes[r'no(?:remap)?'] = _ex_route_noremap
ex_routes[r'new'] = _ex_route_new
ex_routes[r'nn(?:oremap)?'] = _ex_route_nnoremap
ex_routes[r'nun(?:map)?'] = _ex_route_nunmap
ex_routes[r'ono(?:remap)?'] = _ex_route_onoremap
ex_routes[r'on(?:ly)?(?=!$|$)'] = _ex_route_only
ex_routes[r'ou(nmap)?'] = _ex_route_ounmap
ex_routes[r'p(?:rint)?$'] = _ex_route_print
ex_routes[r'pwd?$'] = _ex_route_pwd
ex_routes[r'q(?!a)(?:uit)?'] = _ex_route_quit
ex_routes[r'qa(?:ll)?'] = _ex_route_qall
ex_routes[r'r(?!eg)(?:ead)?'] = _ex_route_read
ex_routes[r'reg(?:isters)?(?=\s+[a-z0-9]+$|$)'] = _ex_route_registers
ex_routes[r's(?:ubstitute)?(?=[%&:/=]|$)'] = _ex_route_substitute
ex_routes[r'se(?:t)?(?=$|\s)'] = _ex_route_set
ex_routes[r'setl(?:ocal)?'] = _ex_route_setlocal
ex_routes[r'sh(?:ell)?'] = _ex_route_shell
ex_routes[r'snor(?:emap)?'] = _ex_route_snoremap
ex_routes[r'sp(?:lit)?'] = _ex_route_split
ex_routes[r'sunm(?:ap)?'] = _ex_route_sunmap
ex_routes[r'tabfir(?:st)?'] = _ex_route_tabfirst
ex_routes[r'tabl(?:ast)?'] = _ex_route_tablast
ex_routes[r'tabn(?:ext)?'] = _ex_route_tabnext
ex_routes[r'tabo(?:nly)?'] = _ex_route_tabonly
ex_routes[r'tabp(?:revious)?'] = _ex_route_tabprevious
ex_routes[r'tabr(?:ewind)?'] = _ex_route_tabfirst
ex_routes[r'una(?:bbreviate)?'] = _ex_route_unabbreviate
ex_routes[r'unm(?:ap)?'] = _ex_route_unmap
ex_routes[r'unvsplit$'] = _ex_route_unvsplit
ex_routes[r'vn(?:oremap)?'] = _ex_route_vnoremap
ex_routes[r'vu(?:nmap)?'] = _ex_route_vunmap
ex_routes[r'w(?:rite)?(?=(?:!?(?:\+\+|>>| |$)))'] = _ex_route_write
ex_routes[r'wqa(?:ll)?'] = _ex_route_wqall
ex_routes[r'xa(?:ll)?'] = _ex_route_wqall
ex_routes[r'wa(?:ll)?'] = _ex_route_wall
ex_routes[r'wq(?=[^a-zA-Z]|$)?'] = _ex_route_wq
ex_routes[r'y(?:ank)?'] = _ex_route_yank
