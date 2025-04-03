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

from NeoVintageous.tests import unittest
from NeoVintageous.tests.text_object_targets import all_one_line_targets


class TestTextObjectSelection(unittest.FunctionalTestCase):

    def test_vaw(self):
        self.eq('x    fi|zz    xx', 'v_aw', 'x    |fizz    |xx')
        self.eq('x    |fizz    xx', 'v_aw', 'x    |fizz    |xx')
        self.eq('x  |  f|izz    xx', 'v_aw', 'x  |  fizz    |xx')
        self.eq('x    fi|zz    xx    yy    zz', 'v_3aw', 'x    |fizz    xx    yy    |zz')
        self.eq(' f|iz    b', 'v_aw', ' |fiz    |b')
        self.eq('fi|z| = x', 'v_aw', '|fiz |= x')

    def test_vaw_issue_748_01(self):
        self.eq(' fi|z    b', 'v_aw', ' |fiz    |b')

    def test_vaw_issue_748_02(self):
        self.eq('fi|z\nbuz x', 'v_aw', '|fiz|\nbuz x')

    def test_viw(self):
        self.eq('x    fi|zz    xx', 'v_iw', 'x    |fizz|    xx')
        self.eq('x  |  fizz    xx', 'v_iw', 'x|    |fizz    xx')
        self.eq('x    |fizz|    xx', 'v_iw', 'x    |fizz    |xx')
        self.eq('x|    fizz    xx', 'v_3iw', 'x|    fizz    |xx')
        self.eq('x    fi|zz    xx    yy    zz', 'v_3iw', 'x    |fizz    xx|    yy    zz')
        self.eq('x  .,|-;abc#"]  y', 'v_iw', 'x  |.,-;|abc#"]  y')
        self.eq('x  .,-;a|bc#"]  y', 'v_iw', 'x  .,-;|abc|#"]  y')
        self.eq(' f|iz|z b', 'v_iw', ' f|izz| b')
        self.eq(' f|iz| b', 'v_iw', ' f|iz |b')
        self.eq(' f|iz|    b', 'v_iw', ' f|iz    |b')
        self.eq(' |fiz| b', 'v_iw', ' |fiz |b')
        self.eq(' |fiz|    b', 'v_iw', ' |fiz    |b')
        self.eq(' |fiz|...b', 'v_iw', ' |fiz...|b')
        self.eq('fi|z| = x', 'v_iw', '|fiz| = x')
        self.eq('r_fi|z| = x', 'v_iw', '|fiz| = x')

    def test_viw_issue_748_04(self):
        self.eq('r_fiz...b|uz|z', 'v_iw', 'r_fiz...|buz|z')

    def test_viw_issue_748_05(self):
        self.eq('r_fiz...|buz|z', 'v_iw', 'r_fiz|...buz|z')

    def test_viw_issue_748_06(self):
        self.eq('r_fiz   |buz|z', 'v_iw', 'r_fiz|   buz|z')

    def test_vaW(self):
        self.eq('x    fi|zz    xx', 'v_aW', 'x    |fizz    |xx')
        self.eq('x    fi|zz    xx    yy    zz', 'v_3aW', 'x    |fizz    xx    yy    |zz')
        self.eq('.    |.,-   f.";   (x)    yy', 'v_aW', '.    |.,-   |f.";   (x)    yy')
        self.eq('.    .|,-   f.";   (x)    yy', 'v_aW', '.    |.,-   |f.";   (x)    yy')
        self.eq('.   |.,-   f.";   (x)    yy', 'v_3aW', '.   |.,-   f.";   (x)    |yy')
        self.eq('x   f|i|zz   y', 'v_aW', 'x   |fizz   |y')

    def test_viW(self):
        self.eq('x  |.,-;abc#"]  y', 'v_iW', 'x  |.,-;abc#"]|  y')
        self.eq('x  .,|-;abc#"]  y', 'v_iW', 'x  |.,-;abc#"]|  y')
        self.eq('x fi|z.z\\ b,u|zz x', 'v_iW', 'x fi|z.z\\ b,uzz| x')
        self.eq('fi|zz|', 'v_iW', 'fi|zz|')

    def test_vas(self):
        self.eq('x.  x  Fi|zz buzz.  y', 'v_as', 'x.  |x  Fizz buzz.|  y')

    def test_vis(self):
        self.eq('x.  x   Fi|zz buzz.yy.  xx', 'v_is', 'x.  |x   Fizz buzz.yy.|  xx')
        self.eq('x.  x  Fi|zz buzz.  y', 'v_is', 'x.  |x  Fizz buzz.|  y')
        self.eq('x.  a |b c.  y', 'v_is', 'x.  |a b c.|  y')
        self.eq('x?  a |b c?  y', 'v_is', 'x?  |a b c?|  y')
        self.eq('x!  a |b c!  y', 'v_is', 'x!  |a b c!|  y')
        self.eq('x.  (a |b c).  y', 'v_is', 'x.  |(a b c).|  y')
        self.eq('x.  [a |b c].  y', 'v_is', 'x.  |[a b c].|  y')
        self.eq('x.  "a |b c".  y', 'v_is', 'x.  |"a b c".|  y')
        self.eq('x.  (["a |b c"]).  y', 'v_is', 'x.  |(["a b c"]).|  y')
        self.eq('x.\n\na\b|b\nc.\n\nx', 'v_is', 'x.\n\n|a\bb\nc.|\n\nx')

    def test_vap(self):
        self.eq('1\n\n2\n|3\n4\n\n\n5', 'v_ap', '1\n\n|2\n3\n4\n\n\n|5')
        self.eq('1\n\n2\n|3\n4\n\n\n5\n6\n\n7', 'v_2ap', '1\n\n|2\n3\n4\n\n\n5\n6\n\n|7')
        self.eq('x\n\n|1\n\n2\n3\n4\n\n\n5\n6\n\n7', 'v_3ap', 'x\n\n|1\n\n2\n3\n4\n\n\n5\n6\n\n|7')

    def test_vip(self):
        self.eq('1\n\n2\n|3\n4\n\n\n5', 'v_ip', '1\n\n|2\n3\n4\n|\n\n5')
        self.eq('1\n\n2\n|3\n4\n\n\n5', 'v_2ip', '1\n\n|2\n3\n4\n\n\n|5')
        self.eq('1\n\n2\n|3\n4\n\n\n5\n6\n\n7', 'v_3ip', '1\n\n|2\n3\n4\n\n\n5\n6\n|\n7')

    def test_va__square_bracket__(self):
        for target in ('[', ']'):
            self.eq('x[fi|zz]x', 'v_a' + target, 'x|[fizz]|x')
            self.eq('x[\nfi|zz\n]x', 'v_a' + target, 'x|[\nfizz\n]|x')
            self.eq('x[\n\n  \n    fi|zz\n\n\n]x', 'v_a' + target, 'x|[\n\n  \n    fizz\n\n\n]|x')

    def test_vi__square_bracket__(self):
        for target in ('[', ']'):
            self.eq('[fi|zz]', 'v_i' + target, '[|fizz|]')
            self.eq('[fi|zz\nbuzz]', 'v_i' + target, '[|fizz\nbuzz|]')
            self.eq('[fi|zz\n    buzz]', 'v_i' + target, '[|fizz\n    buzz|]')
            self.eq('[\nfi|zz\n]', 'v_i' + target, '[\n|fizz\n|]')
            self.eq('[\n    fi|zz\n]', 'v_i' + target, '[\n|    fizz\n|]')
            self.eq('[\n    fi|zz\n    buzz\n]', 'v_i' + target, '[\n|    fizz\n    buzz\n|]')

    def test_yaB(self):
        for target in ('{', '}', 'B'):
            self.resetRegisters()
            self.eq('x{\nfi|zz\n}y', 'ya' + target, 'x|{\nfizz\n}y')
            self.assertLinewiseRegisters('"0', '{\nfizz\n}', '-1')
            self.eq('x({\nfi|zz\n})y', 'ya' + target, 'x(|{\nfizz\n})y')
            self.eq('x({  \n  fi|zz  \n  })y', 'ya' + target, 'x(|{  \n  fizz  \n  })y')

    def test_yi__one_line_targets(self):
        for t in all_one_line_targets:
            self.resetRegisters()
            self.eq('x{0}fi|zz{0}x'.format(t), 'yi' + t, 'x{0}|fizz{0}x'.format(t))
            self.assertRegisters('"0', 'fizz', '1-')

    def test_ya__one_line_targets(self):
        for t in all_one_line_targets:
            self.resetRegisters()
            self.eq('x{0}fi|zz{0}x'.format(t), 'ya' + t, 'x|{0}fizz{0}x'.format(t))
            self.assertRegisters('"0', '{0}fizz{0}'.format(t), '1-')

    def test_va__angle_bracket__(self):
        for target in ('<', '>'):
            self.eq('x<fi|zz>x', 'v_a' + target, 'x|<fizz>|x')
            self.eq('x<\nfi|zz\n>x', 'v_a' + target, 'x|<\nfizz\n>|x')
            self.eq('x<\n\n  \n    fi|zz\n\n\n>x', 'v_a' + target, 'x|<\n\n  \n    fizz\n\n\n>|x')

    def test_vi__angle_bracket__(self):
        for target in ('<', '>'):
            self.eq('<fi|zz>', 'v_i' + target, '<|fizz|>')
            self.eq('fi|zz', 'v_i' + target, 'fi|z|z')

    def test_vat(self):
        self.eq('x<p>a|bc</p>x', 'v_at', 'x|<p>abc</p>|x')
        self.eq('x<p><b>_</b>a|bc<i>_</i>e</p>x', 'v_at', 'x|<p><b>_</b>abc<i>_</i>e</p>|x')
        self.eq('x<p>fi|zz bu|zz</p>y', 'v_at', 'x|<p>fizz buzz</p>|y')
        self.eq('r_x<p>fi|zz bu|zz</p>y', 'v_at', 'x|<p>fizz buzz</p>|y')
        self.eq('x<div> |<p>fizz buzz</p>| </div>x', 'v_at', 'x|<div> <p>fizz buzz</p> </div>|x')
        self.eq('r_x<div> |<p>fizz buzz</p>| </div>x', 'v_at', 'x|<div> <p>fizz buzz</p> </div>|x')
        self.eq('abc<p>fizz|<i>fizz buzz</i>|buzz</p>abc', 'v_at', 'abc|<p>fizz<i>fizz buzz</i>buzz</p>|abc')
        self.eq('<tag>|<sub>hello world</sub>|</tag>', 'v_at', '|<tag><sub>hello world</sub></tag>|')
        self.eq('<tag>  |<sub>hello world</sub>|  </tag>', 'v_at', '|<tag>  <sub>hello world</sub>  </tag>|')
        self.eq('<tag>\n  |<sub>hello world</sub>|\n</tag>', 'v_at', '|<tag>\n  <sub>hello world</sub>\n</tag>|')
        self.eq('r_<tag>\n  |<sub>hello world</sub>|\n</tag>', 'v_at', '|<tag>\n  <sub>hello world</sub>\n</tag>|')
        self.eq('xx<tag>\n  |<sub>hello</sub>|\n</tag>xx', 'v_at', 'xx|<tag>\n  <sub>hello</sub>\n</tag>|xx')
        self.eq('<a>\n  |  <a>fizz</a>\n</a>', 'v_at', '<a>\n    |<a>fizz</a>|\n</a>')
        self.eq('<div>\n  |<h1>fizz</h1>\n</div>', 'v_at', '<div>\n  |<h1>fizz</h1>|\n</div>')
        self.eq('<div>\n|\n<h1>fizz</h1>\n</div>', 'v_at', '|<div>\n\n<h1>fizz</h1>\n</div>|')

    def test_vit(self):
        self.eq('x<p>a|bc</p>x', 'v_it', 'x<p>|abc|</p>x')
        self.eq('x<p>_<i>_</i>a|bc<i>_</i>d</p>x', 'v_it', 'x<p>|_<i>_</i>abc<i>_</i>d|</p>x')
        self.eq('fi|zz', 'v_it', 'fi|z|z')
        self.eq('fi<div>zz|buzz', 'v_it', 'fi<div>zz|b|uzz')
        self.eq('fi<d|iv>zzbuzz', 'v_it', 'fi<d|i|v>zzbuzz')
        self.eq('fi|zzbu</div>zz', 'v_it', 'fi|z|zbu</div>zz')
        self.eq('fizzbu</d|iv>zz', 'v_it', 'fizzbu</d|i|v>zz')
        self.eq('<a>\n\n<b><c>|fizz|</c></b>\n\n</a>', 'v_it', '<a>\n\n<b>|<c>fizz</c>|</b>\n\n</a>')
        self.eq('<a>\n\n<b>|<c>fizz</c>|</b>\n\n</a>', 'v_it', '<a>\n\n|<b><c>fizz</c></b>|\n\n</a>')
        self.eq('<a>\n\n\n|<b><c>fizz</c></b>|\n\n</a>', 'v_it', '<a>|\n\n\n<b><c>fizz</c></b>\n\n|</a>')
        self.eq('xx<a>|\n\n\n<b><c>fizz</c></b>\n|</a>xx', 'v_it', 'xx|<a>\n\n\n<b><c>fizz</c></b>\n</a>|xx')
        self.eq('<a>\n  |  <a>fizz</a>\n</a>', 'v_it', '<a>\n    <a>|fizz|</a>\n</a>')
        self.eq('<div>\n  |<h1>fizz</h1>\n</div>', 'v_it', '<div>\n  <h1>|fizz|</h1>\n</div>')
        self.eq('<div>\n  <h|1>fizz</h1>\n</div>', 'v_it', '<div>\n  <h1>|fizz|</h1>\n</div>')
        self.eq('<div>\n|\n<h1>fizz</h1>\n</div>', 'v_it', '<div>|\n\n<h1>fizz</h1>\n|</div>')
        self.eq('<div>|\n<h1>fizz</h1>\n</div>', 'v_it', '<div>|\n<h1>fizz</h1>\n|</div>')
        self.eq('<div>|\n  <h1>fizz</h1>\n</div>', 'v_it', '<div>|\n  <h1>fizz</h1>\n|</div>')
        self.eq('<div>  |  <h1>fizz</h1>  </div>', 'v_it', '<div>|    <h1>fizz</h1>  |</div>')

    def test_vi__brace__(self):
        for target in ('{', '}', 'B'):
            self.eq('{\na\n|b\nc\n}\n', 'v_i' + target, '{\n|a\nb\nc\n|}\n')
            self.eq('{\na\n|b\nc\n}\n', 'v_i' + target, '{\n|a\nb\nc\n|}\n')
            self.eq('{xx\na\n|b\nc\nxx}\n', 'v_i' + target, '{|xx\na\nb\nc\nxx|}\n')
            self.eq('{\na\n|b\nc\n   }\n', 'v_i' + target, '{\n|a\nb\nc\n|   }\n')
            self.eq('{\na\n|b\nc\n   } // ...\n', 'v_i' + target, '{\n|a\nb\nc\n|   } // ...\n')
            self.eq('({\na\n|b\nc\n   })\n', 'v_i' + target, '({\n|a\nb\nc\n|   })\n')

    def test_va__brace__(self):
        for target in ('{', '}', 'B'):
            self.eq('{\na\n|b\nc\n}\n', 'v_a' + target, '|{\na\nb\nc\n}|\n')
            self.eq('x{\na\n|b\nc\n}x\n', 'v_a' + target, 'x|{\na\nb\nc\n}|x\n')
            self.eq('x{  \n  a\n|b\nc\n  }  x\n', 'v_a' + target, 'x|{  \n  a\nb\nc\n  }|  x\n')
            self.eq('({\na\n|b\nc\n   })\n', 'v_a' + target, '(|{\na\nb\nc\n   }|)\n')

    def test_va__one_line_targets(self):
        for mark in all_one_line_targets:
            self.eq('f|iz|z', 'v_i.', 'f|iz|z')
            self.eq('f|iz{0}z'.format(mark), 'v_a' + mark, 'f|i|z{0}z'.format(mark))
            self.eq('x{0}fi|zz{0}x'.format(mark), 'v_a' + mark, 'x|{0}fizz{0}|x'.format(mark))
            self.eq('x{0}fi|zz bu|zz{0}x'.format(mark), 'v_a' + mark, 'x|{0}fizz buzz{0}|x'.format(mark))

    def test_vi__one_line_targets(self):
        for mark in all_one_line_targets:
            self.eq('f|iz|z', 'v_i' + mark, 'f|iz|z')
            self.eq('f|iz{0}z'.format(mark), 'v_i' + mark, 'f|i|z{0}z'.format(mark))
            self.eq('x{0}fi|zz{0}x'.format(mark), 'v_i' + mark, 'x{0}|fizz|{0}x'.format(mark))
            self.eq('x{0}fi|zz bu|zz{0}x'.format(mark), 'v_i' + mark, 'x{0}|fizz buzz|{0}x'.format(mark))
            self.eq('x{0}fi|zz  {0}x'.format(mark), 'v_i' + mark, 'x{0}|fizz  |{0}x'.format(mark))

    def test_issue_570(self):
        self.visual('<div>\n\n<tag><subtag>hello| |world</subtag></tag>\n\n</div>')
        self.feed('it')
        self.assertVisual('<div>\n\n<tag><subtag>|hello world|</subtag></tag>\n\n</div>')
        self.feed('it')
        self.assertVisual('<div>\n\n<tag>|<subtag>hello world</subtag>|</tag>\n\n</div>')
        self.feed('it')
        self.assertVisual('<div>\n\n|<tag><subtag>hello world</subtag></tag>|\n\n</div>')
        self.feed('it')
        self.assertVisual('<div>|\n\n<tag><subtag>hello world</subtag></tag>\n\n|</div>')
        self.feed('it')
        self.assertVisual('|<div>\n\n<tag><subtag>hello world</subtag></tag>\n\n</div>|')

    def test_issue_654(self):
        self.eq('<div>\n|    <h1>fizz</h1>\n</div>', 'v_it', '<div>\n    <h1>|fizz|</h1>\n</div>')
        self.eq('<div>\n  |  <h1>fizz</h1>\n</div>', 'v_it', '<div>\n    <h1>|fizz|</h1>\n</div>')

    def test_issue_161(self):
        self.eq(
            '<head>\n    <link rel=|"shortcut icon" href="favicon.png">\n</head>',
            'v_it',
            '<head>|\n    <link rel="shortcut icon" href="favicon.png">\n|</head>'
        )

        self.eq(
            '<head>\n    <link rel=|"shortcut icon" href="favicon.png">\n</head>',
            'v_at',
            '|<head>\n    <link rel="shortcut icon" href="favicon.png">\n</head>|'
        )
