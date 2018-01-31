# DEPRECATED These tests can be removed when the functional tests are merged.
from NeoVintageous.tests import unittest


class Test_ys(unittest.ViewTestCase):

    def dataProvider(self):
        return (
            ('"', 'dog "cat" turkey'),
            ('2', 'dog 2cat2 turkey'),
            ('(', 'dog ( cat ) turkey'),
            (')', 'dog (cat) turkey'),
            ('[', 'dog [ cat ] turkey'),
            (']', 'dog [cat] turkey'),
            ('{', 'dog { cat } turkey'),
            ('}', 'dog {cat} turkey'),
            ('<foo>', 'dog <foo>cat</foo> turkey'),
        )

    def test_all_visual_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            self.write('dog cat turkey')
            self.select((4, 7))
            self.state.mode = unittest.VISUAL

            surround_with, expected = data

            self.view.run_command('_nv_surround_ys', {
                'mode': unittest.VISUAL,
                'surround_with': surround_with
            })

            self.assertContent(expected, 'failed at {0}'.format(i))

    # TODO These tests can be removed because they have been ported to the functional test suite
    def test_all_internal_normal_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            self.write('dog cat turkey')
            self.select(4)
            self.state.mode = unittest.INTERNAL_NORMAL

            motion = {}
            motion['motion'] = '_vi_e'
            motion['motion_args'] = {'mode': unittest.INTERNAL_NORMAL, 'count': 1}

            surround_with, expected = data

            self.view.run_command('_nv_surround_ys', {
                'mode': unittest.INTERNAL_NORMAL,
                'surround_with': surround_with,
                'motion': motion
            })

            self.assertContent(expected, 'failed at {0}'.format(i))


# TODO These tests can be removed because they have been ported to the functional test suite
class Test_cs(unittest.ViewTestCase):

    def dataProvider(self):
        return (
            (')"', 'dog "cat" turkey'),
            (')\'', 'dog \'cat\' turkey'),
            (')2', 'dog 2cat2 turkey'),
            (')(', 'dog ( cat ) turkey'),
            (')[', 'dog [ cat ] turkey'),
            (')]', 'dog [cat] turkey'),
            ('){', 'dog { cat } turkey'),
            (')}', 'dog {cat} turkey'),
            (')>', 'dog <cat> turkey'),
        )

    def test_all_internal_normal_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            self.write('dog (cat) turkey')
            self.select(5)
            self.state.mode = unittest.INTERNAL_NORMAL

            replace_what, expected = data
            self.view.run_command('_nv_surround', {
                'action': 'cs',
                'mode': unittest.INTERNAL_NORMAL,
                'target': replace_what[0],
                'replacement': replace_what[1]
            })

            self.assertContent(expected, 'failed at {0}'.format(i))


# TODO These tests can be removed because they have been ported to the functional test suite
class Test_ds(unittest.ViewTestCase):

    def dataProvider(self):
        return (
            ('dog (cat) turkey', '(', 'dog cat turkey'),
            ('dog (cat) turkey', ')', 'dog cat turkey'),
            ('dog (cat) turkey', 'b', 'dog cat turkey'),
            ('dog ( cat ) turkey', '(', 'dog cat turkey'),
            ('dog ( cat ) turkey', ')', 'dog  cat  turkey'),
            ('dog ( cat ) turkey', 'b', 'dog  cat  turkey'),
            ('dog {cat} turkey', '{', 'dog cat turkey'),
            ('dog {cat} turkey', '}', 'dog cat turkey'),
            ('dog {cat} turkey', 'B', 'dog cat turkey'),
            ('dog [cat] turkey', '[', 'dog cat turkey'),
            ('dog [cat] turkey', ']', 'dog cat turkey'),
            ('dog [cat] turkey', 'r', 'dog cat turkey'),
            ('dog <cat> turkey', '<', 'dog cat turkey'),
            ('dog <cat> turkey', '>', 'dog cat turkey'),
            ('dog <cat> turkey', 'a', 'dog cat turkey'),
            ('dog <i>cat</i> turkey', 't', 'dog cat turkey'),
        )

    def test_all_internal_normal_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            text, target, expected = data
            self.write(text)
            self.select(7)
            self.state.mode = unittest.INTERNAL_NORMAL

            self.view.run_command('_nv_surround', {
                'action': 'ds',
                'mode': unittest.INTERNAL_NORMAL,
                'target': target
            })

            self.assertContent(expected, 'failed at {0}'.format(i))


class Test_big_s(unittest.ViewTestCase):

    def dataProvider(self):
        return (
            ('dog cat turkey', [[(0, 0), (0, 3)], [(0, 8), (0, 14)]], '"', '"dog" cat "turkey"'),
            ('dog cat turkey', [[(0, 3), (0, 0)]], '"', '"dog" cat turkey'),
        )

    def test_big_s_visual_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            text, regions, surround_with, expected = data
            self.write(text)
            self.select([self._R(*region) for region in regions])

            self.view.run_command('_nv_surround_ys', {
                'mode': unittest.VISUAL,
                'surround_with': surround_with
            })

            self.assertContent(expected, 'failed at {0}'.format(i))
