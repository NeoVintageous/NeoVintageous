import unittest

from NeoVintageous.lib.vi.dot_file import DotFile


class TestDotFile(unittest.TestCase):

    def test_parse(self):
        dot_file = DotFile(None)

        self.assertEquals((None, None), dot_file.parse('foobar'))
        self.assertEquals((None, None), dot_file.parse('" foobar'))
        self.assertEquals((None, None), dot_file.parse('":let mapleader=,'))
        self.assertEquals((None, None), dot_file.parse('":map x zy'))

        self.assertEquals(('ex_let', {'command_line': 'let mapleader=,'}),
            dot_file.parse(':let mapleader=,'))

        self.assertEquals(('ex_map', {'command_line': 'map x yz'}),
            dot_file.parse(':map x yz'))

        self.assertEquals(('ex_nmap', {'command_line': 'nmap x yz'}),
            dot_file.parse(':nmap x yz'))

        self.assertEquals(('ex_vmap', {'command_line': 'vmap x yz'}),
            dot_file.parse(':vmap x yz'))

        self.assertEquals(('ex_omap', {'command_line': 'omap x yz'}),
            dot_file.parse(':omap x yz'))

