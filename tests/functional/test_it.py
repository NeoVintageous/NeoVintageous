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


class Test_it(unittest.FunctionalTestCase):

    def test_v_it(self):
        self.eq('x<p>a|bc</p>x', 'v_it', 'x<p>|abc|</p>x')
        self.eq('x<p>_<i>_</i>a|bc<i>_</i>d</p>x', 'v_it', 'x<p>|_<i>_</i>abc<i>_</i>d|</p>x')

    def test_161(self):
        self.vFixture('<head>\n    <link rel=|"shortcut icon" href="favicon.png">\n</head>')
        self.feed('v_it')
        self.expectsV('<head>|\n    <link rel="shortcut icon" href="favicon.png">\n|</head>')
