import sublime

from Vintageous.tests import ViewTest
from Vintageous.state import State
from Vintageous.vi.utils import modes


TESTS_YS = (
    ('"', 'dog "cat" turkey'),
    ('2', 'dog 2cat2 turkey'),
    ('(', 'dog (cat) turkey'),
    (')', 'dog ( cat ) turkey'),
    ('[', 'dog [cat] turkey'),
    (']', 'dog [ cat ] turkey'),
    ('{', 'dog {cat} turkey'),
    ('}', 'dog { cat } turkey'),
    ('<foo>', 'dog <foo>cat</foo> turkey'),
)


class Test_ys(ViewTest):
    def testAll_VisualMode(self):
        for (i, data) in enumerate(TESTS_YS):

            self.write('dog cat turkey')
            self.clear_sel()
            self.add_sel(self.R((0, 4), (0, 7)))
            self.state.mode = modes.VISUAL

            surround_with, expected = data
            self.view.run_command('_vi_plug_ys', {'mode': modes.VISUAL,
                                                  'surround_with': surround_with})

            actual = self.get_all_text()
            self.assertEqual(actual, expected, 'failed at {0}'.format(i))

            self.erase_all()

    def testAll_InternalNormalMode(self):
        for (i, data) in enumerate(TESTS_YS):

            self.write('dog cat turkey')
            self.clear_sel()
            self.add_sel(self.R(4))
            self.state.mode = modes.INTERNAL_NORMAL

            motion = {}
            motion['motion'] = '_vi_e'
            motion['motion_args'] = {'mode': modes.INTERNAL_NORMAL, 'count': 1}

            surround_with, expected = data
            self.view.run_command('_vi_plug_ys', {'mode': modes.INTERNAL_NORMAL,
                                                  'surround_with': surround_with,
                                                  'motion': motion})

            actual = self.get_all_text()
            self.assertEqual(actual, expected, 'failed at {0}'.format(i))

            self.erase_all()


TESTS_CS = (
    ('("', 'dog "cat" turkey'),
    ('(2', 'dog 2cat2 turkey'),
    ('([', 'dog [cat] turkey'),
    ('(]', 'dog [ cat ] turkey'),
    ('({', 'dog {cat} turkey'),
    ('(}', 'dog { cat } turkey'),
)


class Test_cs(ViewTest):
    def testAll_InternalNormalMode(self):
        for (i, data) in enumerate(TESTS_CS):

            self.write('dog (cat) turkey')
            self.clear_sel()
            self.add_sel(self.R(5))
            self.state.mode = modes.INTERNAL_NORMAL

            replace_what, expected = data
            self.view.run_command('_vi_plug_cs', {'mode': modes.INTERNAL_NORMAL,
                                                   'replace_what': replace_what})

            actual = self.get_all_text()
            self.assertEqual(actual, expected, 'failed at {0}'.format(i))

            self.erase_all()


TESTS_DS = (
    ('dog (cat) turkey', '(', 'dog cat turkey'),
    ('dog ( cat ) turkey', '(', 'dog  cat  turkey'),
    ('dog [cat] turkey', '[', 'dog cat turkey'),
    ('dog {cat} turkey', '{', 'dog cat turkey'),
    # ('dog <foo>cat</foo> turkey', '<foo>', 'dog cat turkey'),
)


class Test_cs(ViewTest):
    def testAll_InternalNormalMode(self):
        for (i, data) in enumerate(TESTS_DS):

            text, replace_what, expected = data
            self.write(text)
            self.clear_sel()
            self.add_sel(self.R(5))
            self.state.mode = modes.INTERNAL_NORMAL

            self.view.run_command('_vi_plug_ds', {'mode': modes.INTERNAL_NORMAL,
                                                  'replace_what': replace_what})

            actual = self.get_all_text()
            self.assertEqual(actual, expected, 'failed at {0}'.format(i))

            self.erase_all()


TESTS_BIG_S = (
    ('dog cat turkey',  [[(0, 0), (0, 3)], [(0, 8), (0, 14)]], '"', '"dog" cat "turkey"'),
    ('dog cat turkey',  [[(0, 3), (0, 0)]], '"', '"dog" cat turkey'),
)


class Test_big_s(ViewTest):
    def testBigS_VisualMode(self):
        for (i, data) in enumerate(TESTS_BIG_S):

            text, regions, surround_with, expected = data
            self.write(text)
            self.clear_sel()
            for region in regions:
                self.add_sel(self.R(*region))

            self.view.run_command('_vi_plug_ys', {'mode': modes.VISUAL,
                                                  'surround_with': surround_with})

            actual = self.get_all_text()
            self.assertEqual(actual, expected, 'failed at {0}'.format(i))

            self.erase_all()
