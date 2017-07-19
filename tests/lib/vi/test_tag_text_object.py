from collections import namedtuple

from sublime import Region

from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.text_objects import previous_begin_tag
from NeoVintageous.lib.vi.text_objects import find_containing_tag
from NeoVintageous.lib.vi.text_objects import next_end_tag
from NeoVintageous.lib.vi.text_objects import get_region_end
from NeoVintageous.lib.vi.text_objects import next_unbalanced_tag


test_data = namedtuple('test_data', 'content args expected msg')


TESTS_SEARCH_TAG_FORWARD = (
    test_data(content='<a>foo', args={'start': 0}, expected=(Region(0, 3), 'a', False), msg='find tag'),
    test_data(content='<a>foo', args={'start': 1}, expected=(None, None, None), msg="don't find tag"),
    test_data(content='<a>foo</a>', args={'start': 1}, expected=(Region(6, 10), 'a', True), msg='find other tag'),
    test_data(content='<a hey="ho">foo', args={'start': 0}, expected=(Region(0, 12), 'a', False), msg='find tag with attributes'),  # FIXME # noqa: E501
)

TESTS_SEARCH_TAG_BACKWARD = (
    test_data(content='<a>foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 6}, expected=(Region(0, 3), 'a', True), msg='find tag'),  # FIXME # noqa: E501
    test_data(content='<a>foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 0}, expected=(None, None, None), msg="don't find tag"),  # FIXME # noqa: E501
    test_data(content='</a>foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 6}, expected=(Region(0, 4), 'a', False), msg='find a closing tag'),  # FIXME # noqa: E501
    test_data(content='<a>foo</a>', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 5}, expected=(Region(0, 3), 'a', True), msg='find other tag'),  # FIXME # noqa: E501
    test_data(content='<a hey="ho">foo', args={'pattern': r'</?(a) *?.*?>', 'start': 0, 'end': 14}, expected=(Region(0, 12), 'a', True), msg='find tag with attributes'),  # FIXME # noqa: E501
)

TESTS_NEXT_UNBALANCED_END_TAG = (
    test_data(content='<p>foo <p>bar</p> baz</p>', args={'search': next_end_tag, 'search_args': {'start': 3}, 'restart_at': get_region_end}, expected=(Region(21, 25), 'p'), msg='find end tag skipping nested'),  # FIXME # noqa: E501
)

TESTS_CONTAINING_TAG = (
    test_data(content='<a>foo</a>', args={'start': 4}, expected=(Region(0, 3), Region(6, 10), 'a'), msg='find tag'),
    test_data(content='<div>foo</div>', args={'start': 5}, expected=(Region(0, 5), Region(8, 14), 'div'), msg='find long tag'),  # FIXME # noqa: E501
    test_data(content='<div class="foo">foo</div>', args={'start': 17}, expected=(Region(0, 17), Region(20, 26), 'div'), msg='find tag with attributes'),  # FIXME # noqa: E501
    test_data(content='<div>foo</div>', args={'start': 2}, expected=(Region(0, 5), Region(8, 14), 'div'), msg='find tag from within start tag'),  # FIXME # noqa: E501
    test_data(content='<div>foo</div>', args={'start': 13}, expected=(Region(0, 5), Region(8, 14), 'div'), msg='find tag from within end tag'),  # FIXME # noqa: E501
    test_data(content='<div>foo <p>bar</p></div>', args={'start': 12}, expected=(Region(9, 12), Region(15, 19), 'p'), msg='find nested tag from inside'),  # FIXME # noqa: E501
)


class Test_next_unbalanced_end_tag(ViewTestCase):

    def test_next_unbalanced_end_tag(self):
        self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        for (i, data) in enumerate(TESTS_NEXT_UNBALANCED_END_TAG):
            self.write(data.content)
            actual = next_unbalanced_tag(self.view, **data.args)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)


class Test_TagSearch(ViewTestCase):

    def test_next_end_tag(self):
        self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        for (i, data) in enumerate(TESTS_SEARCH_TAG_FORWARD):
            self.write(data.content)
            actual = next_end_tag(self.view, **data.args)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)

    def test_previous_begin_tag(self):
        self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        for (i, data) in enumerate(TESTS_SEARCH_TAG_BACKWARD):
            self.write(data.content)
            actual = previous_begin_tag(self.view, **data.args)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)


class Test_FindContainingTag(ViewTestCase):

    def test_find_containing_tag(self):
        self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        for (i, data) in enumerate(TESTS_CONTAINING_TAG):
            self.write(data.content)
            actual = find_containing_tag(self.view, **data.args)

            msg = "failed at test index {0}: {1}".format(i, data.msg)
            self.assertEqual(data.expected, actual, msg)
