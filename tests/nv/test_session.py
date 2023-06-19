# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

import json
import os
import tempfile

from NeoVintageous.nv import session
from NeoVintageous.tests import unittest


class TestSession(unittest.ViewTestCase):

    @unittest.mock_session()
    def test_session_on_close_view(self):
        self.assertIsNone(session.session_on_close(self.view))

    @unittest.mock_session()
    def test_session_on_close_silently_catches_key_errors(self):
        view = unittest.mock.Mock()
        view.id.return_value = -1
        self.assertIsNone(session.session_on_close(view))
        view.id.assert_called_once()

    @unittest.mock_session()
    def test_get_set_session_value(self):
        session.set_session_value('fizz', 'buzz')
        self.assertEqual('buzz', session.get_session_value('fizz'))

    @unittest.mock_session()
    def test_get__session_value_returns_default_when_does_not_exist(self):
        self.assertEqual(None, session.get_session_value('fizz'))

    @unittest.mock_session()
    def test_get_session_value_returns_default_param_value_when_does_not_exist(self):
        self.assertEqual('default', session.get_session_value('fizz', 'default'))

    @unittest.mock_session()
    def test_set_session_value_can_persist_session_in_older_builds(self):
        session.set_session_value('fizz', 'buzz', persist=True)
        if unittest.ST_VERSION >= 4081:
            self.assertSessionNotSaved()
        else:
            self.assertSessionSaved()

    @unittest.mock_session()
    @unittest.mock.patch('NeoVintageous.nv.session._get_session_file')
    def test_load_empty_object_session(self, get_session_file):
        get_session_file.return_value = self.fixturePath('session_is_empty_object.json')
        session.load_session()
        self.assertSession({})

    @unittest.mock_session()
    @unittest.mock.patch('NeoVintageous.nv.session._get_session_file')
    def test_load_empty_session(self, get_session_file):
        get_session_file.return_value = self.fixturePath('session_is_empty.json')
        session.load_session()
        self.assertSession({})

    @unittest.mock_session()
    @unittest.mock.patch('NeoVintageous.nv.session._get_session_file')
    def test_load_blank_session(self, get_session_file):
        get_session_file.return_value = self.fixturePath('session_is_blank.json')
        session.load_session()
        self.assertSession({})

    @unittest.mock_session()
    @unittest.mock.patch('NeoVintageous.nv.session._get_session_file')
    def test_load_session_does_not_exist_is_noop(self, get_session_file):
        get_session_file.return_value = self.fixturePath('session_does_not_exist.json')
        session.load_session()
        self.assertSession({})

    @unittest.mock_session()
    @unittest.mock.patch('NeoVintageous.nv.session._get_session_file')
    def test_load_session_basic(self, get_session_file):
        get_session_file.return_value = self.fixturePath('session_basic.json')
        session.load_session()
        self.assertSession({
            "history": {
                1: {
                    'num': 6,
                    'items': {
                        1: 's/fizz/buzz/',
                        2: 'ls',
                        6: 'help'
                    }
                },
                2: {'num': 0, "items": {}},
                3: {'num': 0, "items": {}},
                4: {'num': 0, "items": {}},
                5: {'num': 0, "items": {}},
            },
            "last_substitute_search_pattern": "fizz",
            "last_substitute_string": "buzz",
            "last_used_register_name": "w",
            "macros": {
                "w": [
                    [
                        "nv_vi_w",
                        {
                            "mode": "mode_normal",
                            "count": 1
                        }
                    ]
                ]
            },
        })

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {
        "foo": "bar",
        "history": {
            1: {
                'num': 6,
                'items': {
                    1: 's/fizz/buzz/',
                    2: 'ls',
                    6: 'help'
                }
            },
            2: {'num': 0, "items": {}},
            3: {'num': 0, "items": {}},
            4: {'num': 0, "items": {}},
            5: {'num': 0, "items": {}}
        },
        "last_substitute_search_pattern": "fizz",
        "last_substitute_string": "buzz",
        "last_used_register_name": "w",
        "macros": {
            "w": [
                [
                    "nv_vi_w",
                    {
                        "mode": "mode_normal",
                        "count": 1
                    }
                ]
            ]
        },
    }, clear=True)
    @unittest.mock.patch('NeoVintageous.nv.session._get_session_file')
    def test_save_session(self, get_session_file):
        self.maxDiff = None
        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = os.path.join(tmpdir, 'test.session')
            get_session_file.return_value = session_file
            session.save_session()

            with open(session_file, 'r', encoding='utf-8', errors='replace') as f:
                with open(self.fixturePath('session_basic.json'), 'r', encoding='utf-8') as s:
                    self.assertEqual(
                        sorted(json.loads(f.read())),
                        sorted(json.loads(s.read())))
