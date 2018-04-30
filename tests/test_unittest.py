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

from sublime import Region
from sublime import Settings

from NeoVintageous.tests import unittest


class TestViewTestCase(unittest.ViewTestCase):

    def test_content(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.assertEqual('hello world', self.content())

    def test_region(self):
        self.assertEqual(self.Region(3), Region(3))
        self.assertEqual(self.Region(3, 5), Region(3, 5))

    def test_select(self):
        self.view.run_command('insert', {'characters': 'another brick in the wall'})

        # Int.
        self.select(3)
        self.assertEqual([Region(3)], list(self.view.sel()))
        self.select(5)
        self.assertEqual([Region(5)], list(self.view.sel()))

        # Tuple.
        self.select((3, 5))
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select((7, 11))
        self.assertEqual([Region(7, 11)], list(self.view.sel()))

        # Region.
        self.select(Region(3, 5))
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select(Region(7, 11))
        self.assertEqual([Region(7, 11)], list(self.view.sel()))

        # Ints.
        self.select([3])
        self.assertEqual([Region(3)], list(self.view.sel()))
        self.select([5, 7])
        self.assertEqual([Region(5), Region(7)], list(self.view.sel()))

        # Tuples.
        self.select([(3, 5)])
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select([(7, 11), (13, 17)])
        self.assertEqual([Region(7, 11), Region(13, 17)], list(self.view.sel()))

        # Regions.
        self.select([Region(3, 5)])
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select([Region(7, 11), Region(13, 17)])
        self.assertEqual([Region(7, 11), Region(13, 17)], list(self.view.sel()))

        # Misc.
        self.select([3, (11, 13), Region(5, 7)])
        self.assertEqual([Region(3), Region(5, 7), Region(11, 13)], list(self.view.sel()))

    def test_settings(self):
        self.assertIsInstance(self.settings(), Settings)

    def test_write(self):
        self.write('Hello world!')
        self.assertEqual('Hello world!', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(12)], list(self.view.sel()))

    def test_assert_content(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertContent('hello world')

        with self.assertRaises(AssertionError):
            self.assertContent('foobar')

    def test_assert_content_regex(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertContentRegex('hello world', 'foo msg')

        with self.assertRaises(AssertionError, msg='foo msg'):
            self.assertContentRegex('foobar', 'foo msg')

    def test_assert_region(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertRegion(1, Region(1))
        self.assertRegion((1, 1), Region(1))
        self.assertRegion((3, 5), Region(3, 5))
        self.assertRegion(Region(3, 5), Region(3, 5))
        self.assertRegion('hello', Region(0, 5))
        self.assertRegion('o wor', Region(4, 9))

    def test_assert_selection(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()

        self.view.sel().add(3)
        self.assertSelection(3)
        self.assertSelection((3, 3))
        self.assertSelection(Region(3, 3))
        self.assertSelection([Region(3, 3)])
        with self.assertRaises(AssertionError):
            self.assertSelection(10)
        with self.assertRaises(AssertionError):
            self.assertSelection((10, 10))
        with self.assertRaises(AssertionError):
            self.assertSelection(Region(10, 10))
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(10, 10)])
        with self.assertRaises(AssertionError):
            self.assertSelection(20)
        with self.assertRaises(AssertionError):
            self.assertSelection([])

        self.view.sel().add(11)
        self.assertSelection([Region(3, 3), Region(11, 11)])
        with self.assertRaises(AssertionError):
            self.assertSelection(3)
        with self.assertRaises(AssertionError):
            self.assertSelection(11)
        with self.assertRaises(AssertionError):
            self.assertSelection((3, 11))
        with self.assertRaises(AssertionError):
            self.assertSelection(Region(3, 11))
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(4, 4), Region(11, 11)])

        self.view.sel().add(Region(5, 7))
        self.assertSelection([Region(3, 3), Region(5, 7), Region(11, 11)])
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(3, 3), Region(11, 11)])

        self.view.sel().clear()
        self.assertSelection([])
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(3, 3), Region(5, 7), Region(11, 11)])

        self.view.sel().add(Region(3, 7))
        self.assertSelection((3, 7))
        self.assertSelection(Region(3, 7))
        self.assertSelection([Region(3, 7)])
        self.assertSelection([Region(3, 7)])
        with self.assertRaises(AssertionError):
            self.assertSelection([])
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(2, 7)])

    def test_assert_selection_count(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.view.sel().clear()
        self.assertSelectionCount(0)

        self.view.sel().add(0)
        self.assertSelectionCount(1)

        self.view.sel().add(3)
        self.view.sel().add(5)
        self.assertSelectionCount(3)
        with self.assertRaises(AssertionError):
            self.assertSelectionCount(1)

        self.view.sel().clear()
        self.assertSelectionCount(0)
        with self.assertRaises(AssertionError):
            self.assertSelectionCount(1)

        self.view.sel().add(7)
        self.assertSelectionCount(1)
        with self.assertRaises(AssertionError):
            self.assertSelectionCount(0)

    def test_assert_size(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertSize(11)

        with self.assertRaises(AssertionError):
            self.assertSize(5)

        with self.assertRaises(AssertionError):
            self.assertSize(12)
