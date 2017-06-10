import unittest

from NeoVintageous.lib.rcfile import _parse_line


class TestRcfile(unittest.TestCase):

    def test_parse_return_none(self):
        self.assertEquals((None, None), _parse_line(''))
        self.assertEquals((None, None), _parse_line('"'))
        self.assertEquals((None, None), _parse_line('foobar'))
        self.assertEquals((None, None), _parse_line('" foobar'))
        self.assertEquals((None, None), _parse_line('":let mapleader=,'))
        self.assertEquals((None, None), _parse_line('":map x zy'))
        self.assertEquals((None, None), _parse_line('zap x zy'))

    def test_parse_returns_command_and_arguments(self):
        self.assertEquals(('ex_let', {'command_line': 'let mapleader=,'}), _parse_line(':let mapleader=,'))
        self.assertEquals(('ex_map', {'command_line': 'map x yz'}), _parse_line(':map x yz'))
        self.assertEquals(('ex_nmap', {'command_line': 'nmap x yz'}), _parse_line(':nmap x yz'))
        self.assertEquals(('ex_vmap', {'command_line': 'vmap x yz'}), _parse_line(':vmap x yz'))
        self.assertEquals(('ex_omap', {'command_line': 'omap x yz'}), _parse_line(':omap x yz'))

    def test_parse_line_strips_trailing_whitespace(self):
        self.assertEquals(('ex_let', {'command_line': 'let mapleader=,'}), _parse_line(':let mapleader=,    '))
        self.assertEquals(('ex_map', {'command_line': 'map x yz'}), _parse_line(':map x yz  '))

    def test_parse_line_colon_prefix_is_optional(self):
        self.assertEquals(('ex_let', {'command_line': 'let mapleader=,'}), _parse_line('let mapleader=,'))
        self.assertEquals(('ex_map', {'command_line': 'map x yz'}), _parse_line('map x yz'))
        self.assertEquals(('ex_nmap', {'command_line': 'nmap x yz'}), _parse_line('nmap x yz'))
        self.assertEquals(('ex_vmap', {'command_line': 'vmap x yz'}), _parse_line('vmap x yz'))
        self.assertEquals(('ex_omap', {'command_line': 'omap x yz'}), _parse_line('omap x yz'))
