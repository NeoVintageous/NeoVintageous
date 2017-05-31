from NeoVintageous.tests.utils import ViewTestCase


class Test_ys(ViewTestCase):

    def dataProvider(self):
        return (
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

    def test_all_visual_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            self.write('dog cat turkey')
            self.selectRegion(4, 7)
            self.state.mode = self.modes.VISUAL

            surround_with, expected = data

            self.view.run_command('nvim_surround_ys', {
                'mode': self.modes.VISUAL,
                'surround_with': surround_with
            })

            self.assertContent(expected, 'failed at {0}'.format(i))

    def test_all_internal_normal_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            self.write('dog cat turkey')
            self.select(4)
            self.state.mode = self.modes.INTERNAL_NORMAL

            motion = {}
            motion['motion'] = '_vi_e'
            motion['motion_args'] = {'mode': self.modes.INTERNAL_NORMAL, 'count': 1}

            surround_with, expected = data

            self.view.run_command('nvim_surround_ys', {
                'mode': self.modes.INTERNAL_NORMAL,
                'surround_with': surround_with,
                'motion': motion
            })

            self.assertContent(expected, 'failed at {0}'.format(i))


class Test_cs(ViewTestCase):

    def dataProvider(self):
        return (
            ('("', 'dog "cat" turkey'),
            ('(2', 'dog 2cat2 turkey'),
            ('([', 'dog [cat] turkey'),
            ('(]', 'dog [ cat ] turkey'),
            ('({', 'dog {cat} turkey'),
            ('(}', 'dog { cat } turkey'),
        )

    def test_all_internal_normal_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            self.write('dog (cat) turkey')
            self.select(5)
            self.state.mode = self.modes.INTERNAL_NORMAL

            replace_what, expected = data
            self.view.run_command('nvim_surround_cs', {
                'mode': self.modes.INTERNAL_NORMAL,
                'replace_what': replace_what
            })

            self.assertContent(expected, 'failed at {0}'.format(i))


class Test_ds(ViewTestCase):

    def dataProvider(self):
        return (
            ('dog (cat) turkey', '(', 'dog cat turkey'),
            ('dog ( cat ) turkey', '(', 'dog  cat  turkey'),
            ('dog [cat] turkey', '[', 'dog cat turkey'),
            ('dog {cat} turkey', '{', 'dog cat turkey'),
            # ('dog <foo>cat</foo> turkey', '<foo>', 'dog cat turkey'),
        )

    def test_all_internal_normal_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            text, replace_what, expected = data
            self.write(text)
            self.select(5)
            self.state.mode = self.modes.INTERNAL_NORMAL

            self.view.run_command('nvim_surround_ds', {
                'mode': self.modes.INTERNAL_NORMAL,
                'replace_what': replace_what
            })

            self.assertContent(expected, 'failed at {0}'.format(i))


class Test_big_s(ViewTestCase):

    def dataProvider(self):
        return (
            ('dog cat turkey', [[(0, 0), (0, 3)], [(0, 8), (0, 14)]], '"', '"dog" cat "turkey"'),
            ('dog cat turkey', [[(0, 3), (0, 0)]], '"', '"dog" cat turkey'),
        )

    def test_big_s_visual_mode(self):
        for (i, data) in enumerate(self.dataProvider()):
            text, regions, surround_with, expected = data
            self.write(text)
            self.selectMultiple([self.R(*region) for region in regions])

            self.view.run_command('nvim_surround_ys', {
                'mode': self.modes.VISUAL,
                'surround_with': surround_with
            })

            self.assertContent(expected, 'failed at {0}'.format(i))
