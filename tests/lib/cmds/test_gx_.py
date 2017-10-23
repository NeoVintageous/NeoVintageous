import re

from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.cmds.vi_actions import _vi_gx as command

URL_REGEX = re.compile(command.URL_REGEX)


class gx(ViewTestCase):

    def assertMatch(self, expected, text):
        r = re.match(URL_REGEX, text)
        self.assertIsNotNone(r)
        self.assertEqual(expected, r.group('url'))

    def test_invalid(self):
        self.assertEqual(None, re.match(URL_REGEX, ''))
        self.assertEqual(None, re.match(URL_REGEX, 'http'))
        self.assertEqual(None, re.match(URL_REGEX, 'http://.com'))

    def test_x(self):
        self.assertMatch('http://example.com', 'http://example.com')
        self.assertMatch('https://example.com', 'https://example.com')

        self.assertMatch('http://EXAMPLE.COM', 'http://EXAMPLE.COM _xxx_')
        self.assertMatch('http://www.example.com', 'http://www.example.com _xxx_')
        self.assertMatch('http://sub.example.com', 'http://sub.example.com _xxx_')
        self.assertMatch('http://sub.sub.example.com', 'http://sub.sub.example.com _xxx_')

        self.assertMatch('http://example.com/x/y', 'http://example.com/x/y _xxx_')
        self.assertMatch('http://example.com/x/y.html', 'http://example.com/x/y.html _xxx_')
        self.assertMatch('http://example.com/x/y.html#x', 'http://example.com/x/y.html#x _xxx_')
        self.assertMatch('http://example.com/x/y.html#x-y', 'http://example.com/x/y.html#x-y _xxx_')
        self.assertMatch('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')
        self.assertMatch('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')
