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


class TestSurroundDocumentationExamples(unittest.FunctionalTestCase):

    def test_documentation_examples(self):
        # See the usage examples at https://github.com/tpope/vim-surround.

        self.normal('"Hello| world!"')
        self.feed('cs"\'')
        self.assertNormal("|'Hello world!'")

        # Now press `cs'<q>` to change it to <q>Hello world!</q>.
        self.feed("cs'<q>")
        self.assertNormal('|<q>Hello world!</q>')

        # To go full circle, press `cst"` to get "Hello world!".
        self.feed('cst"')
        self.assertNormal('|"Hello world!"')

        # To remove the delimiters entirely, press `ds"`.
        self.feed('ds"')
        self.assertNormal('|Hello world!')

        # Now with the cursor on "Hello", press `ysiw]` (`iw` is a text object).
        self.feed('ysiw]')
        self.assertNormal('|[Hello] world!')

        # Let's make that braces and add some space (use `}` instead of `{` for no space): `cs]{`
        self.select(1)  # TODO This should work without havng to use select() i.e. if cursor is at point on target.
        self.feed('cs]{')
        self.assertNormal('|{ Hello } world!')

        # Now wrap the entire line in parentheses with `yssb` or `yss)`.
        self.feed('yss)')
        self.assertNormal('|({ Hello } world!)')

        # Revert to the original text: `ds{ds)`
        self.select(1)
        self.feed('ds{')
        self.assertNormal('(|Hello world!)')
        self.feed('ds)')
        self.assertNormal('|Hello world!')

        # TODO Implement ysiw<em>
        # Emphasize hello: `ysiw<em>`
        #     <em>Hello</em> world!

        # TODO Implement S
        # Finally, let's try out visual mode. Press a capital V (for linewise
        # visual mode) followed by `S<p class="important">`.
        #     <p class="important">
        #       <em>Hello</em> world!
        #     </p>
