from collections import namedtuple

from NeoVintageous.tests.utils import ViewTestCase


test_data = namedtuple('test_data', 'initial_text regions cmd_params expected msg')

TESTS = (
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 1}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 1}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 2}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 2}, 'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 3}, 'abc abc abc',         'should join 3 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\n    abc',                   [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 3}, 'abc abc abc',         'should join 3 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc\nabc\nabc',                 [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 5}, 'abc abc abc abc abc', 'should join 5 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\n    abc\n    abc\n    abc', [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 5}, 'abc abc abc abc abc', 'should join 5 lines'),  # noqa: E501, E241
    test_data('abc\n\n',                                 [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 3}, 'abc ',                'should join 3 lines and add one trailing space'),  # noqa: E501, E241
    test_data('\n\nabc',                                 [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 3}, 'abc',                 'should join 3 lines without adding any spaces'),  # noqa: E501, E241
    test_data('abc \n    abc  \n  abc',                  [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 3}, 'abc abc  abc',        'should join 3 lines with leading spaces removed but trailing spaces intact'),  # noqa: E501, E241
    test_data('   abc\nabc   ',                          [[(0, 0), (0, 0)]],                   {'mode': ViewTestCase.INTERNAL_NORMAL_MODE, 'count': 1}, '   abc abc   ',       'should join 2 lines with leading spaces of first line and trailing spaces of last line intact'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 0), (0, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 0), (0, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 0), (1, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 0), (1, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(1, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(1, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc\nabc',        'should join 2 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 0), (2, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc abc',         'should join 3 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 0), (2, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc abc',         'should join 3 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(2, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc abc',         'should join 3 lines'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(2, 1), (0, 0)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       'abc abc abc',         'should join 3 lines'),  # noqa: E501, E241
    test_data('abc\nabc\nabc',                           [[(0, 0), (1, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE, 'count': 3},           'abc abc\nabc',        'should join 2 lines - count shouldn\'t matter'),  # noqa: E501, E241
    test_data('abc\n    abc\nabc',                       [[(0, 0), (1, 1)]],                   {'mode': ViewTestCase.VISUAL_MODE, 'count': 3},           'abc abc\nabc',        'should join 2 lines - count shouldn\'t matter'),  # noqa: E501, E241
    test_data('   abc\nabc   ',                          [[(0, 0), (1, 5)]],                   {'mode': ViewTestCase.VISUAL_MODE},                       '   abc abc   ',       'should join 2 lines with leading spaces of first line and trailing spaces of last line intact'),  # noqa: E501, E241
    test_data('    abc\n\n\n',                           [[(0, 0), (3, 0)]],                   {'mode': ViewTestCase.VISUAL_LINE_MODE},                  '    abc \n',          'should join 4 lines'),  # noqa: E501, E241
    test_data('    abc  \n   abc\nabc',                  [[(0, 0), (0, 1)], [(1, 0), (1, 1)]], {'mode': ViewTestCase.VISUAL_BLOCK_MODE},                 '    abc  abc\nabc',   'should join 2 lines'),  # noqa: E501, E241
)


class Test__vi_big_j(ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.initial_text)
            self.select([self._R(*region) for region in data.regions])

            self.view.run_command('_vi_big_j', data.cmd_params)

            self.assertEqual(data.expected, self.content(), "[{0}] {1}".format(i, data.msg))
