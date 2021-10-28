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


@unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
class Test_ex_global(unittest.FunctionalTestCase):

    def test_global_delete(self):
        self.eq('|fizz\nxyz\nbuzz\n', ':global/^x/d', 'fizz\n|buzz\n')
        self.eq('|fizz\nxyz\nbuzz\n', ':global/^x/delete', 'fizz\n|buzz\n')
        self.eq('|fizz\nxyz\nbuzz\n', ':g/^x/d', 'fizz\n|buzz\n')
        self.eq('|fizz\nxyz\nbuzz\n', ':g/^x/delete', 'fizz\n|buzz\n')
        self.eq('|fizz\nxyz\nbuzz\nfizz\nxyz\nbuzz\n', ':global/^x/d', 'fizz\nbuzz\nfizz\n|buzz\n')
        self.eq('|fizz\nxyz\nbuzz\n', ':global/^./d', '|')
        self.eq('|fizz\nxyz\nbuzz\n', ':global/^/d', '|')
        self.eq('|fizz\n\nbuzz\n', ':global/^$/d', 'fizz\n|buzz\n')
        self.eq('|fizz\n\nbuzz\nfizz\n\n\n\n\n\nbuzz\n', ':global/^$/d', 'fizz\nbuzz\nfizz\n|buzz\n')
        self.eq('|fizz\n\nbuzz\nfizz\n\n\n\n\n\nbuzz\n', ':%global/^$/d', 'fizz\nbuzz\nfizz\n|buzz\n')
        self.eq('|1\n2\n3\n4\n5\n6\n7\n8\n9\n0', ':3,6g/^/d', '1\n2\n|7\n8\n9\n0')
        self.eq('|1\nx2\n3\n4\nx5\n6\nx7\nx8\n9\n0', ':3,7g/^x/d', '1\nx2\n3\n4\n6\n|x8\n9\n0')

    def test_global_not_match_delete(self):
        self.eq('|fizz\nxyz\nbuzz\n', ':global!/^x/d', 'xyz\n|')
        self.eq('|fizz\nxyz\nbuzz\nfizz\nxyz\nbuzz\n', ':global!/^x/d', 'xyz\nxyz\n|')
