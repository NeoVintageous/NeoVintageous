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

SEQ = dict()

# ToDo: simplify config keymap and have S-a everywhere instead of A to be consistent with S-f1
  # but need to retain the old A and <M-A> notation since user configs use it, so not worth it
# ToDo: add a Shifted function instead of Upper to also work with 9→( and [→{
_sep = ' '
_mod2vim = {"⇧":"", "⎈":"C-", "⇧⎈":"C-", "⎇":"M-", "":""}
symbolSubs = {
  'up'      	: ['▲'],
  'down'    	: ['▼'],
  'left'    	: ['◀'],
  'right'   	: ['▶'],
  'pagedown'	: ['⇟'],
  'pageup'  	: ['⇞'],
  'bs'      	: ['␈'],
  'cr'      	: ['⏎'],
  'space'   	: ['␠'],
}
_letters = { # space-separated lists of keycaps
  "function"  	: {"keycaps":"1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "mods":[
    {"mLbl"   	: None ,"varLbl":"F"   ,"preVal":"<","valLbl":"f"  ,"posVal":">"},
    {"mLbl"   	: "⇧" ,"varLbl":"F"   ,"preVal":"<","valLbl":"S-f" ,"posVal":">"},
    #         	   ↑↓ requires manual "S-" since special keys don't get Capitalized
    {"mLbl"   	: "⇧⎈","varLbl":"F"  ,"preVal":"<","valLbl":"S-f" ,"posVal":">"},
    {"mLbl"   	: "⎈" ,"varLbl":"F"   ,"preVal":"<","valLbl":"f"  ,"posVal":">"},
    ]}        	,
  "number"    	: {"keycaps":"1 2 3 4 5 6 7 8 9 0","mods":[
    {"mLbl"   	: None,"preVal":"" ,"posVal":""},
    {"mLbl"   	: "⎈","preVal":"<","posVal":">"},
    ]}        	,
  "unimpaired"	: {"keycaps":"q w e r t y u i o p a s d f g h j k l z x c v b n m","mods":[
    {"mLbl"   	: None,"preVar":"[","preVal":"","valLbl":"[" ,"posVal":""},
    # {"mLbl" 	: "⎈","preVar":"["   ,"preVal":"","valLbl":"["  ,"posVal":""},
    {"mLbl"   	: "⇧","preVar":"["   ,"preVal":"","valLbl":"["  ,"posVal":""},
    {"mLbl"   	: None,"preVar":"]","preVal":"","valLbl":"]" ,"posVal":""},
    # {"mLbl" 	: "⎈","preVar":"]"   ,"preVal":"","valLbl":"]"  ,"posVal":""},
    {"mLbl"   	: "⇧","preVar":"]"   ,"preVal":"","valLbl":"]"  ,"posVal":""},
    ]}        	,
  "keypad"    	: {"keycaps":"1 2 3 4 5 6 7 8 9 0","mods":[
    {"mLbl"   	: None,"varLbl":"🔢","preVal":"<","valLbl":"k" ,"posVal":">"},
    ]}        	,
  "qwerty"    	: {"keycaps":"q w e r t y u i o p", "mods":[
    {"mLbl"   	: None , "preVal":"" ,"posVal":""},
    {"mLbl"   	: "⇧" , "preVal":"" ,"posVal":""},
    {"mLbl"   	:  "⎈", "preVal":"<","posVal":">"},
    {"mLbl"   	: "⇧⎈", "preVal":"<","posVal":">"},
    ]}        	,
  "asdf"      	: {"keycaps":"a s d f g h j k l", "mods":[
    {"mLbl"   	: None , "preVal":"" ,"posVal":""},
    {"mLbl"   	: "⇧" , "preVal":"" ,"posVal":""},
    {"mLbl"   	:  "⎈", "preVal":"<","posVal":">"},
    {"mLbl"   	: "⇧⎈", "preVal":"<","posVal":">"},
    ]}        	,
  "zxcv"      	: {"keycaps":"z x c v b n m", "mods":[
    {"mLbl"   	: None , "preVal":"" ,"posVal":""},
    {"mLbl"   	: "⇧" , "preVal":"" ,"posVal":""},
    {"mLbl"   	:  "⎈", "preVal":"<","posVal":">"},
    {"mLbl"   	: "⇧⎈", "preVal":"<","posVal":">"},
    ]}        	,
  "sub_a"     	: {"keycaps":"q w e r t y u i o p a s d f g h j k l z x c v b n m","mods":[
    {"mLbl"   	: None,"preVar":"a","preVal":"","preVal":"a"},
    {"mLbl"   	: "⇧","preVar":"a","preVal":"","preVal":"a"},
    ]}        	,
  "sub_c"     	: {"keycaps":"q w e r t y u i o p a s d f g h j k l z x c v b n m","mods":[
    {"mLbl"   	: None,"preVar":"c","preVal":"","preVal":"c"},
    {"mLbl"   	: "⇧","preVar":"c","preVal":"","preVal":"c"},
    ]}        	,
  "sub_d"     	: {"keycaps":"q w e r t y u i o p a s d f g h j k l z x c v b n m","mods":[
    {"mLbl"   	: None,"preVar":"d","preVal":"","preVal":"d"},
    {"mLbl"   	: "⇧","preVar":"d","preVal":"","preVal":"d"},
    ]}        	,
  "sub_g"     	: {"keycaps":"q w e r t y u i o p a s d f g h j k l z x c v b n m","mods":[
    {"mLbl"   	: None,"preVar":"g","preVal":"","preVal":"g"},
    {"mLbl"   	: "⇧","preVar":"g","preVal":"","preVal":"g"},
    ]}        	,
  "sub_y"     	: {"keycaps":"q w e r t y u i o p a s d f g h j k l z x c v b n m","mods":[
    {"mLbl"   	: None,"preVar":"y","preVal":"","preVal":"y"},
    {"mLbl"   	: "⇧","preVar":"y","preVal":"","preVal":"y"},
    ]}        	,
  "sub_z"     	: {"keycaps":"q w e r t y u i o p a s d f g h j k l z x c v b n m","mods":[
    {"mLbl"   	: None,"preVar":"z","preVal":"","preVal":"z"},
    {"mLbl"   	: "⇧","preVar":"z","preVal":"","preVal":"z"},
    ]}        	,
  "symbol"    	: {"keycaps":list(symbolSubs.keys()),"mods":[
    {"mLbl"   	: None ,"varLbl":""   ,"preVal":"<","valLbl":""  ,"posVal":">"},
    {"mLbl"   	: "⇧" ,"varLbl":""   ,"preVal":"<","valLbl":"S-" ,"posVal":">"},
    #         	   ↑↓ requires manual "S-" since special keys don't get Capitalized
    {"mLbl"   	: "⇧⎈","varLbl":""  ,"preVal":"<","valLbl":"S-" ,"posVal":">"},
    {"mLbl"   	: "⎈" ,"varLbl":""   ,"preVal":"<","valLbl":""  ,"posVal":">"},
    {"mLbl"   	: "⎇" ,"varLbl":""   ,"preVal":"<","valLbl":""  ,"posVal":">"},
    ]}
}

for lbl, row in _letters.items():
  keycaps	= row["keycaps"].split(_sep) if (type(row["keycaps"]) == str) else row["keycaps"]
  mods   	= row["mods"]
  for mod in mods:
    modVar	= mod["mLbl"] if mod["mLbl"] else ''
    modVal	= _mod2vim[modVar]
    preVar	= mod["preVar"] if "preVar" in mod else ""
    varLbl	= mod["varLbl"] if "varLbl" in mod else ""
    preVal	= mod["preVal"] if "preVal" in mod else ""
    valLbl	= mod["valLbl"] if "valLbl" in mod else ""
    posVal	= mod["posVal"] if "posVal" in mod else ""
    for key in keycaps:
      if key in symbolSubs:
        key_var	= symbolSubs[key][0]
        key_vim	= key
      else:
        key_var	= key
        key_vim	= key.upper() if "⇧" in modVar else key
      var      	= preVar + modVar + varLbl + key_var
      val      	= preVal + modVal + valLbl + key_vim  + posVal
      ### TODO add translation from user config
      SEQ[var]   = [val]

# ↓ SEQ dictionary ('quotes' omitted)
# lbl     list of allowed vim values
#   F1	: [<f1>]
# ⇧F1 	: [<S-f1>]
# ⎈F1 	: [<C-f1>]
#⇧⎈F1 	: [<C-S-f1>],
#   1 	: [1]
# 🔢1  	: [<k1>]
#   q 	: [q]
# ⇧q  	: [Q]
#  ⎈a 	: [<C-a>]
# ⇧⎈p 	: [<C-P>]

# Manual bindings
# Keypad
SEQ['🔢/']	= ['<kdivide>']
SEQ['🔢=']	= ['<kenter>']
SEQ['🔢-']	= ['<kminus>']
SEQ['🔢*']	= ['<kmultiply>']
SEQ['🔢.']	= ['<kperiod>']
SEQ['🔢+']	= ['<kplus>']

# Unimpaired
SEQ['⎈['] 	= ['<C-[>']
SEQ['[']  	= ['[']
SEQ['[␠'] 	= ['[<space>']
SEQ['[⇧[']	= ['[{']
SEQ['[⇧9']	= ['[(']
SEQ[']']  	= [']']
SEQ[']⇧]']	= [']}']
SEQ[']⇧0']	= ['])']
SEQ[']␠'] 	= [']<space>']

# subMode
SEQ['g⇧-'] 		= ['g_']
SEQ['⇧z⇧q']	= ['ZQ']
SEQ['⇧z⇧z']	= ['ZZ']

# other
SEQ['⇧[']	= ['{']
SEQ['⇧9']	= ['(']

Z_LEFT = ['z<left>']
G_DOWN = ['g<down>']
G_UP = ['g<up>']
Z_RIGHT = ['z<right>']
CTRL_W_DOWN = ['<C-w><down>']
CTRL_W_RIGHT = ['<C-w><right>']
CTRL_SHIFT_ENTER = ['<C-S-cr>']
CTRL_W_LEFT = ['<C-w><left>']
CTRL_W_UP = ['<C-w><up>']

CTRL_ALT_P = ['<C-M-p>']
CTRL_BIG_B = ['<C-B>']
CTRL_BIG_F = ['<C-F>']
CTRL_BIG_P = ['<C-P>']
CTRL_DOT = ['<C-.>']
CTRL_HAT = ['<C-^>']
CTRL_HOME = ['<C-home>']
CTRL_K_CTRL_B = ['<C-k><C-b>']
CTRL_RIGHT_SQUARE_BRACKET = ['<C-]>']
CTRL_R_EQUAL = ['<C-r>=']
CTRL_SHIFT_DOT = ['<C-S-.>']
CTRL_W_B = ['<C-w>b']
CTRL_W_BACKSPACE = ['<C-w><bs>']
CTRL_W_BAR = ['<C-w><bar>']
CTRL_W_BIG_H = ['<C-w>H']
CTRL_W_BIG_J = ['<C-w>J']
CTRL_W_BIG_K = ['<C-w>K']
CTRL_W_BIG_L = ['<C-w>L']
CTRL_W_BIG_S = ['<C-w>S']
CTRL_W_BIG_W = ['<C-w>W']
CTRL_W_C = ['<C-w>c']
CTRL_W_CTRL_B = ['<C-w><C-b>']
CTRL_W_CTRL_H = ['<C-w><C-h>']
CTRL_W_CTRL_J = ['<C-w><C-j>']
CTRL_W_CTRL_K = ['<C-w><C-k>']
CTRL_W_CTRL_L = ['<C-w><C-l>']
CTRL_W_CTRL_N = ['<C-w><C-n>']
CTRL_W_CTRL_O = ['<C-w><C-o>']
CTRL_W_CTRL_Q = ['<C-w><C-q>']
CTRL_W_CTRL_RIGHT_SQUARE_BRACKET = ['<C-w><C-]>']
CTRL_W_CTRL_S = ['<C-w><C-s>']
CTRL_W_CTRL_T = ['<C-w><C-t>']
CTRL_W_CTRL_UNDERSCORE = ['<C-w><C-_>']
CTRL_W_CTRL_V = ['<C-w><C-v>']
CTRL_W_CTRL_X = ['<C-w><C-x>']
CTRL_W_EQUAL = ['<C-w>=']
CTRL_W_GREATER_THAN = ['<C-w>>']
CTRL_W_H = ['<C-w>h']
CTRL_W_J = ['<C-w>j']
CTRL_W_K = ['<C-w>k']
CTRL_W_L = ['<C-w>l']
CTRL_W_LESS_THAN = ['<C-w><lt>']
CTRL_W_MINUS = ['<C-w>-']
CTRL_W_N = ['<C-w>n']
CTRL_W_O = ['<C-w>o']
CTRL_W_PLUS = ['<C-w>+']
CTRL_W_Q = ['<C-w>q']
CTRL_W_RIGHT_SQUARE_BRACKET = ['<C-w>]']
CTRL_W_S = ['<C-w>s']
CTRL_W_T = ['<C-w>t']
CTRL_W_UNDERSCORE = ['<C-w>_']
CTRL_W_V = ['<C-w>v']
CTRL_W_X = ['<C-w>x']
CTRL_X_CTRL_L = ['<C-x><C-l>']
CTRL_Y = ['<C-y>']


ALT_N = ['<M-n>']
AMPERSAND = ['&']
AT = ['@']
BACKSLASH = ['<bslash>']
BACKSPACE = ['<bs>']
BACKTICK = ['`']
BAR = ['<bar>']
COLON = [':']
COMMA = [',']
COMMAND_BIG_B = ['<D-B>']
COMMAND_BIG_F = ['<D-F>']
COMMAND_BIG_P = ['<D-P>']
COMMAND_P = ['<D-p>']
DEL = ['<del>']
DOLLAR = ['$']
DOT = ['.']
DOUBLE_QUOTE = ['"']
END = ['<end>']
ENTER = ['<cr>']
EQUAL = ['=']
EQUAL_EQUAL = ['==']
ESC = ['<esc>']
GCC = ['gcc']
GQGQ = ['gqgq']
GQQ = ['gqq']
GREATER_THAN = ['>']
GREATER_THAN_GREATER_THAN = ['>>']
GUGU = ['gugu']
GUU = ['guu']
G_BIG_U_BIG_U = ['gUU']
G_BIG_U_G_BIG_U = ['gUgU']
G_TILDE = ['g~']
G_TILDE_G_TILDE = ['g~g~']
G_TILDE_TILDE = ['g~~']
HAT = ['^']
HOME = ['<home>']
INSERT = ['<insert>']
LEADER = ['<leader>']
LESS_THAN = ['<lt>']
LESS_THAN_LESS_THAN = ['<lt><lt>']
MINUS = ['-']
OCTOTHORP = ['#']
PERCENT = ['%']
PLUS = ['+']
QUESTION_MARK = ['?']
QUOTE = ["'"]
QUOTE_QUOTE = ["''"]
RIGHT_BRACE = ['}']
RIGHT_PAREN = [')']
SEMICOLON = [';']
SHIFT_ENTER = ['<S-cr>']
SLASH = ['/']
SPACE = ['<space>']
STAR = ['*']
TAB = ['<tab>']
TILDE = ['~']
UNDERSCORE = ['_']
YSS = ['yss']
ZERO = ['0']
ZUG = ['zug']
Z_DOT = ['z.']
Z_ENTER = ['z<cr>']
Z_EQUAL = ['z=']
Z_MINUS = ['z-']
