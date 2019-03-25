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

from NeoVintageous.tests import unittest


class Test_p(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('vintageous_use_sys_clipboard', False)
        self.resetRegisters()

    def test_p(self):
        self.register('"', 'one')
        self.eq('|xy', 'p', 'xon|ey')

    # TODO How paste works depends on how the register was created (not just the
    # contents of the register e.g. just because the register has newlines
    # doesn't mean that it should be pasted linewise).
    #
    # Maybe have a "get-for-paste" register content retrival method that  will
    # return the content with the appropriate prefix/suffix newlines  already
    # added, then the paste commands can just insert it.
    #
    # def test_p_newlines(self):
    #     self.register('"', 'x\n')
    #     self.eq('|ab', 'p', 'a|x\nb')
