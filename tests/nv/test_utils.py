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

from NeoVintageous.nv.utils import extract_file_name


class TestExtractFileName(unittest.ViewTestCase):

    def test_extract_file_name(self):
        tests = {
            '|': None,
            'REA|DME.md': 'README.md',
            ' REA|DME.md ': 'README.md',
            '\nREA|DME.md\n': 'README.md',
            'path/to/REA|DME.md': 'path/to/README.md',
            ' pat|h/to/README.md ': 'path/to/README.md',
            '\npath|/to/README.md\n': 'path/to/README.md',
        }

        for text, file_name in tests.items():
            self.normal(text)
            self.assertEqual(extract_file_name(self.view), file_name)
