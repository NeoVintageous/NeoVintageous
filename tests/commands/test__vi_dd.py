import unittest

from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests import set_text
from NeoVintageous.tests import add_sel
from NeoVintageous.tests import get_sel
from NeoVintageous.tests import first_sel
from NeoVintageous.tests import ViewTest


class Test_vi_dd_InNormalMode(ViewTest):
    def testDeletesLastLine(self):
        self.write('abc\nabc\nabc')
        self.clear_sel()
        self.add_sel(self.R((2, 0), (2, 0)))

        self.view.run_command('_vi_dd', {'mode': modes.INTERNAL_NORMAL})

        expected = self.view.substr(self.R(0, self.view.size()))
        self.assertEqual(expected, 'abc\nabc')
