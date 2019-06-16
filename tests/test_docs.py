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

import os
import unittest

from sublime import load_resource


class TestDocs(unittest.TestCase):

    def test_doc_encoding(self):

        # Some vim docs are Windows-1252 encoded and load_resource() has issues
        # loading them. I don't know if this is a bug in Vim or Sublime or if
        # those docs are intentionally set to that encoding. Either way,
        # `load_resource()` fails with decode errors like "utf-8' codec can't
        # decode byte 0xe1 in position 21672: invalid continuation byte".
        #
        # So all docs included by Neovintageous must be utf-8. This test ensures
        # that all docs can be loaded via `load_resourse()`

        docs_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'res/doc')

        for f in os.listdir(docs_path):
            if f.endswith('.txt'):
                resource = 'Packages/NeoVintageous/res/doc/%s' % f

                exception = None

                try:
                    load_resource(resource)
                except Exception as e:
                    exception = e

                if exception:
                    self.fail('failed to load resource \'%s\': %s' % (resource, exception))
