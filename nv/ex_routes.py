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
def scan_cmd_abbreviate(state):
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


def scan_cmd_browse(state):
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


# TODO [refactor] Rename target from ex_prompt_select_open_file to buffers
def scan_cmd_buffers(state):
    command = TokenCommand('buffers', target='ex_prompt_select_open_file')

    try:
        state.expect_eof()
    except ValueError:
        # TODO Use a special domain exception for exceptions raised in scans.
        raise Exception("E488: Trailing characters")

    return None, [command, TokenEof()]


def scan_cmd_cd(state):
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


def scan_cmd_cdd(state):
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


def scan_cmd_close(state):
    command = TokenCommand('close')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_copy(state):
    command = TokenCommand('copy')
    command.addressable = True

    params = {'address': None}
    m = state.expect_match(r'\s*(?P<address>.+?)\s*$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_cquit(state):
    command = TokenCommand('cquit')

    state.expect_eof()

    return None, [command, TokenEof()]


def scan_cmd_delete(state):
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


def scan_cmd_double_ampersand(state):
    command = TokenCommand('&&', target='ex_double_ampersand')
    command.addressable = True

    params = {'flags': [], 'count': ''}

    m = state.match(r'\s*([cgr])*\s*(\d*)\s*$')

    params['flags'] = list(m.group(1)) if m.group(1) else []
    params['count'] = m.group(2) or ''

    state.expect_eof()

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_edit(state):
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


def scan_cmd_exit(state):
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


def scan_cmd_file(state):
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


def scan_cmd_global(state):
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


def scan_cmd_help(state):
    command = TokenCommand('help')
    match = state.expect_match(r'(?P<bang>!)?\s*(?P<subject>.+)?$').groupdict()
    params = {'subject': match['subject']}
    bang = bool(match['bang'])

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_let(state):
    command = TokenCommand('let')
    params = {'name': None, 'value': None}

    m = state.expect_match(
        r'(?P<name>.+?)\s*=\s*(?P<value>.+?)\s*$',
        on_error=lambda: Exception("E121: Undefined variable"))

    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_move(state):
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


def scan_cmd_new(state):
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


def scan_cmd_nnoremap(state):
    command = TokenCommand('nnoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_noremap(state):
    command = TokenCommand('noremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_nunmap(state):
    command = TokenCommand('nunmap')
    params = {'keys': None}

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_only(state):
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


def scan_cmd_onoremap(state):
    command = TokenCommand('onoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    return None, [command, TokenEof()]


def scan_cmd_ounmap(state):
    command = TokenCommand('ounmap')
    params = {'keys': None}

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_print(state):
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


def scan_cmd_pwd(state):
    command = TokenCommand('pwd')

    state.expect_eof()

    return None, [command, TokenEof()]


def scan_cmd_qall(state):
    command = TokenCommand('qall')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_quit(state):
    command = TokenCommand('quit')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_read(state):
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


def scan_cmd_registers(state):
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


def scan_cmd_set(state):
    command = TokenCommand('set')
    params = {'option': None, 'value': None}

    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<option>.+?)(?:[:=](?P<value>.+?))?$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_setlocal(state):
    command = TokenCommand('setlocal')
    params = {'option': None, 'value': None}

    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<option>.+?)(?:[:=](?P<value>.+?))?$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_shell(state):
    command = TokenCommand('shell')
    state.expect_eof()

    return None, [command, TokenEof()]


def scan_cmd_shell_out(state):
    command = TokenCommand('!', target='ex_shell_out')
    command.addressable = True
    params = {'cmd': None}

    m = state.expect_match(r'(?P<cmd>.+)$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_snoremap(state):
    command = TokenCommand('snoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_split(state):
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


def scan_cmd_substitute(state):
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


def scan_cmd_tabfirst(state):
    command = TokenCommand('tabfirst')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_tablast(state):
    command = TokenCommand('tablast')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_tabnext(state):
    command = TokenCommand('tabnext')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_tabonly(state):
    command = TokenCommand('tabonly')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_tabprevious(state):
    command = TokenCommand('tabprevious')
    c = state.consume()
    if c == state.EOF:
        return None, [command, TokenEof()]

    bang = c == '!'

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_unabbreviate(state):
    command = TokenCommand('unabbreviate')
    params = {'lhs': None}

    m = state.expect_match(r'\s+(?P<lhs>.+?)\s*$')
    params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_unmap(state):
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


def scan_cmd_unvsplit(state):
    command = TokenCommand('unvsplit')
    state.expect_eof()

    return None, [command, TokenEof()]


def scan_cmd_vnoremap(state):
    command = TokenCommand('vnoremap')
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_vsplit(state):
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


def scan_cmd_vunmap(state):
    command = TokenCommand('vunmap')
    params = {'keys': None}

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]


def scan_cmd_wall(state):
    command = TokenCommand('wall')
    bang = state.consume() == '!'

    state.expect_eof()

    command.forced = bang

    return None, [command, TokenEof()]


def scan_cmd_wq(state):
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


def scan_cmd_wqall(state):
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


def scan_cmd_write(state):
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


def scan_cmd_yank(state):
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
command_routes = OrderedDict()
command_routes[r'!(?=.+)'] = scan_cmd_shell_out
command_routes[r'&&?'] = scan_cmd_double_ampersand
command_routes[r'ab(?:breviate)?'] = scan_cmd_abbreviate
command_routes[r'bro(?:wse)?'] = scan_cmd_browse
command_routes[r'clo(?:se)?'] = scan_cmd_close
command_routes[r'co(?:py)?'] = scan_cmd_copy
command_routes[r'cq(?:uit)?'] = scan_cmd_cquit
command_routes[r'd(?:elete)?'] = scan_cmd_delete
command_routes[r'exi(?:t)?'] = scan_cmd_exit
command_routes[r'f(?:ile)?'] = scan_cmd_file
command_routes[r'g(?:lobal)?(?=[^ ])'] = scan_cmd_global
command_routes[r'h(?:elp)?'] = scan_cmd_help
command_routes[r'(?:ls|files|buffers)!?'] = scan_cmd_buffers
command_routes[r'vs(?:plit)?'] = scan_cmd_vsplit
command_routes[r'x(?:it)?$'] = scan_cmd_exit
command_routes[r'^cd(?=[^d]|$)'] = scan_cmd_cd
command_routes[r'^cdd'] = scan_cmd_cdd
command_routes[r'e(?:dit)?(?= |$)?'] = scan_cmd_edit
command_routes[r'let\s'] = scan_cmd_let
command_routes[r'm(?:ove)?(?=[^a]|$)'] = scan_cmd_move
command_routes[r'no(?:remap)'] = scan_cmd_noremap
command_routes[r'new'] = scan_cmd_new
command_routes[r'nn(?:oremap)?'] = scan_cmd_nnoremap
command_routes[r'nun(?:map)?'] = scan_cmd_nunmap
command_routes[r'ono(?:remap)?'] = scan_cmd_onoremap
command_routes[r'on(?:ly)?(?=!$|$)'] = scan_cmd_only
command_routes[r'ounm(?:ap)?'] = scan_cmd_ounmap
command_routes[r'p(?:rint)?$'] = scan_cmd_print
command_routes[r'pwd?$'] = scan_cmd_pwd
command_routes[r'q(?!a)(?:uit)?'] = scan_cmd_quit
command_routes[r'qa(?:ll)?'] = scan_cmd_qall
command_routes[r'r(?!eg)(?:ead)?'] = scan_cmd_read
command_routes[r'reg(?:isters)?(?=\s+[a-z0-9]+$|$)'] = scan_cmd_registers
command_routes[r's(?:ubstitute)?(?=[%&:/=]|$)'] = scan_cmd_substitute
command_routes[r'se(?:t)?(?=$|\s)'] = scan_cmd_set
command_routes[r'setl(?:ocal)?'] = scan_cmd_setlocal
command_routes[r'sh(?:ell)?'] = scan_cmd_shell
command_routes[r'snor(?:emap)?'] = scan_cmd_snoremap
command_routes[r'sp(?:lit)?'] = scan_cmd_split
command_routes[r'tabfir(?:st)?'] = scan_cmd_tabfirst
command_routes[r'tabl(?:ast)?'] = scan_cmd_tablast
command_routes[r'tabn(?:ext)?'] = scan_cmd_tabnext
command_routes[r'tabo(?:nly)?'] = scan_cmd_tabonly
command_routes[r'tabp(?:revious)?'] = scan_cmd_tabprevious
command_routes[r'tabr(?:ewind)?'] = scan_cmd_tabfirst
command_routes[r'una(?:bbreviate)?'] = scan_cmd_unabbreviate
command_routes[r'unm(?:ap)?'] = scan_cmd_unmap
command_routes[r'unvsplit$'] = scan_cmd_unvsplit
command_routes[r'vn(?:oremap)?'] = scan_cmd_vnoremap
command_routes[r'vu(?:nmap)?'] = scan_cmd_vunmap
command_routes[r'w(?:rite)?(?=(?:!?(?:\+\+|>>| |$)))'] = scan_cmd_write
command_routes[r'wqa(?:ll)?'] = scan_cmd_wqall
command_routes[r'xa(?:ll)?'] = scan_cmd_wqall
command_routes[r'wa(?:ll)?'] = scan_cmd_wall
command_routes[r'wq(?=[^a-zA-Z]|$)?'] = scan_cmd_wq
command_routes[r'y(?:ank)?'] = scan_cmd_yank
