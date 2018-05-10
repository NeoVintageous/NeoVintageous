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


class TestDocumentationExamples(unittest.FunctionalTestCase):

    def test_documentation_examples(self):
        # See https://github.com/tpope/vim-surround

        # It's easiest to explain with examples.  Press `cs"'` inside
        #     "Hello world!"

        self.fixture('"Hello| world!"')
        self.feed('cs"\'')

        # to change it to
        #     'Hello world!'

        self.expects("|'Hello world!'")

        # Now press `cs'<q>` to change it to
        #     <q>Hello world!</q>

        self.select(1)  # TODO Fix: should work if cursor is at point on target.
        self.feed("cs'<q>")
        self.expects('|<q>Hello world!</q>')

        # To go full circle, press `cst"` to get
        #     "Hello world!"

        self.feed('cst"')
        self.expects('|"Hello world!"')

        # To remove the delimiters entirely, press `ds"`.
        #     Hello world!

        self.feed('ds"')
        self.expects('|Hello world!')

        # Now with the cursor on "Hello", press `ysiw]` (`iw` is a text object).
        #     [Hello] world!

        self.feed('ysiw]')
        self.expects('|[Hello] world!')

        # Let's make that braces and add some space (use `}` instead of `{` for no
        # space): `cs]{`
        #     { Hello } world!

        self.select(1)  # TODO Fix: should work if cursor is at point on target.
        self.feed('cs]{')
        self.expects('|{ Hello } world!')

        # Now wrap the entire line in parentheses with `yssb` or `yss)`.
        #     ({ Hello } world!)

        # self.feed('yss)')
        # self.expects('|({ Hello } world!)')
        # TODO yss operation above is not yet supported, setup a fixture for next feed.
        self.fixture('|{(Hello world!)}')

        # Revert to the original text: `ds{ds)`
        #     Hello world!

        self.feed('ds{')
        self.expects('|(Hello world!)')
        self.feed('ds)')
        self.expects('|Hello world!')

        # TODO Implement ysiw<em>
        # Emphasize hello: `ysiw<em>`
        #     <em>Hello</em> world!

        # TODO Implement S
        # Finally, let's try out visual mode. Press a capital V (for linewise
        # visual mode) followed by `S<p class="important">`.
        #     <p class="important">
        #       <em>Hello</em> world!
        #     </p>
