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


class TestIndentObject(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('tab_size', 2)

    def test_vii_and_viI(self):
        for seq in ('ii', 'iI'):
            self.eq('x\nxx\nif\n  fi|zz\nend\nxx\nx', 'v_' + seq, 'x\nxx\nif\n|  fizz\n|end\nxx\nx')
            self.eq('x\nxx\nif\n  fi|zz\n  buzz\nend\nxx\nx', 'v_' + seq, 'x\nxx\nif\n|  fizz\n  buzz\n|end\nxx\nx')
            self.eq('x\nxx\n  |if\n    fizz\n  then\nxx\nx', 'v_' + seq, 'x\nxx\n|  if\n    fizz\n  then\n|xx\nx')
            self.eq('x\nxx\nif\n\n|\n\n  fizz\nend\nxx\nx', 'v_' + seq, 'x\nxx\nif\n\n\n\n|  fizz\n|end\nxx\nx')
            self.eq('x\nxx\nif\n  fi|zz\n\n\nend\nxx\nx', 'v_' + seq, 'x\nxx\nif\n|  fizz\n|\n\nend\nxx\nx')
            self.eq('x\nxx\n\n\nif\n  fi|zz\n\n\n\nend\nxx\nx', 'v_' + seq, 'x\nxx\n\n\nif\n|  fizz\n|\n\n\nend\nxx\nx')
            self.eq('x\nxx\n\nfi|zz\n\nxx\nx', 'v_' + seq, 'x\nxx\n\n|fizz\n|\nxx\nx')
            self.eq('x\nxx\n\nfi|zz\nbuzz\n\nxx\nx', 'v_' + seq, 'x\nxx\n\n|fizz\nbuzz\n|\nxx\nx')
            self.eq('x\nxx\nfi|zz\nbuzz\nxx', 'v_' + seq, '|x\nxx\nfizz\nbuzz\nxx|')
            self.eq('x\nxx\nfi|zz\nbuzz\nxx\n', 'v_' + seq, '|x\nxx\nfizz\nbuzz\nxx\n|')
            self.eq('x\nxx\n\n fi|zz\n\nxx\nx', 'v_' + seq, 'x\nxx\n\n| fizz\n|\nxx\nx')
            self.eq('x\nxx\n    fizz\n\n | buz|z\nxx\nx', 'v_' + seq, 'x\nxx\n|    fizz\n\n  buzz\n|xx\nx')
            self.eq('x\nxx\n\nfizz\n\n|\n\nbuzz\n\nx', 'v_' + seq, 'x\nxx\n\n|fizz\n\n\n|\nbuzz\n\nx')
            self.eq('x\nxx\n\nfizz\n\n|\nbuzz\n\nx', 'v_' + seq, 'x\nxx\n\n|fizz\n\n\n|buzz\n\nx')
            self.eq('x\nxx\n\nfizz\n|\n\n\nbuzz\n\nx', 'v_' + seq, 'x\nxx\n\n|fizz\n\n|\n\nbuzz\n\nx')
            self.eq('x\nxx\n\nfizz\n|\n\nbuzz\n\nx', 'v_' + seq, 'x\nxx\n\n|fizz\n\n|\nbuzz\n\nx')
            self.eq('x\nxx\n\nfizz\n|\nbuzz\n\nx', 'v_' + seq, 'x\nxx\n\n|fizz\n\n|buzz\n\nx')
            self.eq('x\nxx\n\n    fizz\n\n\n|\n\n  buzz\n\nxx\nx', 'v_' + seq, 'x\nxx\n\n|    fizz\n|\n\n\n\n  buzz\n\nxx\nx')  # noqa: E501
            self.eq('x\nxx\n\n  fizz\n\n\n|\n\n    buzz\n\nxx\nx', 'v_' + seq, 'x\nxx\n\n  fizz\n\n\n\n\n|    buzz\n|\nxx\nx')  # noqa: E501

    def test_vai(self):
        self.eq('1\n222\nif\n  fi|zz\nend\nxx\nx', 'v_ai', '1\n222\n|if\n  fizz\n|end\nxx\nx')
        self.eq('1\n222\nif\n  fi|zz\n  buzz\nend\nxx\nx', 'v_ai', '1\n222\n|if\n  fizz\n  buzz\n|end\nxx\nx')
        self.eq('x\nxx\n  |if\n    fizz\n  then\nxx\nx', 'v_ai', 'x\n|xx\n  if\n    fizz\n  then\n|xx\nx')
        self.eq('x\nxx\nif\n\n|\n\n  fizz\nend\nxx\nx', 'v_ai', 'x\nxx\n|if\n\n\n\n  fizz\n|end\nxx\nx')
        self.eq('x\nxx\nif\n  \n\n  |  \n  fizz\nend\nxx\nx', 'v_ai', 'x\nxx\n|if\n  \n\n    \n  fizz\n|end\nxx\nx')
        self.eq('x\nxx\n\n\nif\n  fi|zz\n\n  \nend\nxx\nx', 'v_ai', 'x\nxx\n\n\n|if\n  fizz\n\n  \n|end\nxx\nx')
        self.eq('x\nxx\n\nfi|zz\n\nxx\nx', 'v_ai', 'x\nxx\n|\nfizz\n|\nxx\nx')
        self.eq('x\nxx\n\n\nfi|zz\n\nxx\nx', 'v_ai', 'x\nxx\n\n|\nfizz\n|\nxx\nx')
        self.eq('x\nxx\n\n\n\nfi|zz\n\nxx\nx', 'v_ai', 'x\nxx\n\n\n|\nfizz\n|\nxx\nx')
        self.eq('x\nxx\n\nfi|zz\nbuzz\n\nxx\nx', 'v_ai', 'x\nxx\n|\nfizz\nbuzz\n|\nxx\nx')
        self.eq('x\nxx\n\n\nfi|zz\nbuzz\n\nxx\nx', 'v_ai', 'x\nxx\n\n|\nfizz\nbuzz\n|\nxx\nx')
        self.eq('x\nxx\n\n\n\nfi|zz\nbuzz\n\nxx\nx', 'v_ai', 'x\nxx\n\n\n|\nfizz\nbuzz\n|\nxx\nx')
        self.eq('x\nxx\nfi|zz\nbuzz\nxx', 'v_ai', '|x\nxx\nfizz\nbuzz\nxx|')
        self.eq('x\nxx\nfi|zz\nbuzz\nxx\n', 'v_ai', '|x\nxx\nfizz\nbuzz\nxx\n|')
        self.eq('1\nif\n  fi|zz\n\n\n\nend\nx', 'v_ai', '1\n|if\n  fizz\n\n\n\n|end\nx')
        self.eq('1\n  if\n    fi|zz\n\n\n\n  end\nx', 'v_ai', '1\n|  if\n    fizz\n\n\n\n|  end\nx')
        self.eq('1\n  if\n\n\n\n    fi|zz\n\n\n\n  end\nxx\nx', 'v_ai', '1\n|  if\n\n\n\n    fizz\n\n\n\n|  end\nxx\nx')
        self.eq('1\n  if\n\n\n\n    fi|zz\n\n\n\n  end\n  xx\n  x', 'v_ai', '1\n|  if\n\n\n\n    fizz\n\n\n\n|  end\n  xx\n  x')  # noqa: E501
        self.eq('1\n  xx\n  if\n\n\n\n    fi|zz\n\n\n\n  end\n  xx\n  x', 'v_ai', '1\n  xx\n|  if\n\n\n\n    fizz\n\n\n\n|  end\n  xx\n  x')  # noqa: E501
        self.eq('1\nxx\n\n\nfi|zz\nbuzz\n\nxx\nx', 'v_ai', '1\nxx\n\n|\nfizz\nbuzz\n|\nxx\nx')

    def test_vaI(self):
        self.eq('1\n222\nif\n  fi|zz\nend\nxx\nx', 'v_aI', '1\n222\n|if\n  fizz\nend\n|xx\nx')
        self.eq('x\nxx\nif\n\n|\n\n  fizz\nend\nxx\nx', 'v_aI', 'x\nxx\n|if\n\n\n\n  fizz\nend\n|xx\nx')
        self.eq('x\nxx\n\n\nif\n  fi|zz\n\n  \nend\nxx\nx', 'v_aI', 'x\nxx\n\n\n|if\n  fizz\n\n  \nend\n|xx\nx')
        self.eq('x\nxx\n\n\nif\n  fi|zz\n\n  \nend\n\n\nxx\nx', 'v_aI', 'x\nxx\n\n\n|if\n  fizz\n\n  \nend\n|\n\nxx\nx')
        self.eq('x\nxx\n\nfi|zz\n\nxx\nx', 'v_aI', 'x\nxx\n|\nfizz\n\n|xx\nx')
        self.eq('x\nxx\n\n\n\nfi|zz\n\n\n\n\nxx\nx', 'v_aI', 'x\nxx\n\n\n|\nfizz\n\n|\n\n\nxx\nx')
        self.eq('x\nxx\n\n\n\nfi|zz\nbuzz\n\n\n\n\nxx\nx', 'v_aI', 'x\nxx\n\n\n|\nfizz\nbuzz\n\n|\n\n\nxx\nx')
        self.eq('x\nxx\nfi|zz\nbuzz\nxx', 'v_aI', '|x\nxx\nfizz\nbuzz\nxx|')
        self.eq('x\nxx\nfi|zz\nbuzz\nxx\n', 'v_aI', '|x\nxx\nfizz\nbuzz\nxx\n|')
        self.eq('1\n  if\n\n\n\n    fi|zz\n\n\n\n  end\nxx\nx', 'v_aI', '1\n|  if\n\n\n\n    fizz\n\n\n\n  end\n|xx\nx')
        self.eq('1\n  if\n\n\n\n    fi|zz\n\n\n\n  end\n  xx\n  x', 'v_aI', '1\n|  if\n\n\n\n    fizz\n\n\n\n  end\n|  xx\n  x')  # noqa: E501
        self.eq('1\n  xx\n  if\n\n\n\n    fi|zz\n\n\n\n  end\n  xx\n  x', 'v_aI', '1\n  xx\n|  if\n\n\n\n    fizz\n\n\n\n  end\n|  xx\n  x')  # noqa: E501

    def test_viix(self):
        self.eq('a\n\nfi|zz\n\nb', 'v_ii', 'a\n\n|fizz\n|\nb')
        self.eq('a\n\nfi|zz\nbuzz\n\nb', 'v_ii', 'a\n\n|fizz\nbuzz\n|\nb')
        self.eq('a\n\n  fi|zz\n\nb', 'v_ii', 'a\n\n|  fizz\n|\nb')
        self.eq('a\n\n  fi|zz\n  buzz\n\nb', 'v_ii', 'a\n\n|  fizz\n  buzz\n|\nb')
        self.eq('a\n\n  x\n\n  fi|zz\n  buzz\n\n  y\n\nb', 'v_ii', 'a\n\n|  x\n\n  fizz\n  buzz\n\n  y\n|\nb')
        self.eq('x\n  1|11\n  222\n\ny', 'v_ii', 'x\n|  111\n  222\n|\ny')
        self.eq('x\n  1|11\n\n  222\ny', 'v_ii', 'x\n|  111\n\n  222\n|y')
        self.eq('x\n  1|11\n  222\n\n  333\n  444\n\ny', 'v_ii', 'x\n|  111\n  222\n\n  333\n  444\n|\ny')
        self.eq('x\n  1|11\n    222\ny\n', 'v_ii', 'x\n|  111\n    222\n|y\n')
        self.eq('x\n  1|11\n    222\n      333\ny\n', 'v_ii', 'x\n|  111\n    222\n      333\n|y\n')
        self.eq('x\n  111\n|    222\n      333\ny\n', 'v_ii', 'x\n  111\n|    222\n      333\n|y\n')
        self.eq('x\n  111\n    222\n   |   333\ny\n', 'v_ii', 'x\n  111\n    222\n|      333\n|y\n')
        self.eq('x\n  |111\n    222\n      333\n  111\ny\n', 'v_ii', 'x\n|  111\n    222\n      333\n  111\n|y\n')
        self.eq('x\n  |111\n    222\n      333\n\n  111\ny\n', 'v_ii', 'x\n|  111\n    222\n      333\n\n  111\n|y\n')
        self.eq('x\n  |111\n    222\n      333\n\n\n  111\ny\n', 'v_ii', 'x\n|  111\n    222\n      333\n\n\n  111\n|y\n')  # noqa: E501
