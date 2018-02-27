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

from collections import OrderedDict

from .cmd_abbreviate import scan_cmd_abbreviate
from .cmd_browse import scan_cmd_browse
from .cmd_buffers import scan_cmd_buffers
from .cmd_cd import scan_cmd_cd
from .cmd_cdd import scan_cmd_cdd
from .cmd_close import scan_cmd_close
from .cmd_copy import scan_cmd_copy
from .cmd_cquit import scan_cmd_cquit
from .cmd_delete import scan_cmd_delete
from .cmd_double_ampersand import scan_cmd_double_ampersand
from .cmd_edit import scan_cmd_edit
from .cmd_exit import scan_cmd_exit
from .cmd_file import scan_cmd_file
from .cmd_global import scan_cmd_global
from .cmd_help import scan_cmd_help
from .cmd_let import scan_cmd_let
from .cmd_move import scan_cmd_move
from .cmd_new import scan_cmd_new
from .cmd_nnoremap import scan_cmd_nnoremap
from .cmd_noremap import scan_cmd_noremap
from .cmd_nunmap import scan_cmd_nunmap
from .cmd_only import scan_cmd_only
from .cmd_onoremap import scan_cmd_onoremap
from .cmd_ounmap import scan_cmd_ounmap
from .cmd_print import scan_cmd_print
from .cmd_pwd import scan_cmd_pwd
from .cmd_qall import scan_cmd_qall
from .cmd_quit import scan_cmd_quit
from .cmd_read import scan_cmd_read
from .cmd_registers import scan_cmd_registers
from .cmd_set import scan_cmd_set
from .cmd_setlocal import scan_cmd_setlocal
from .cmd_shell import scan_cmd_shell
from .cmd_shell_out import scan_cmd_shell_out
from .cmd_snoremap import scan_cmd_snoremap
from .cmd_split import scan_cmd_split
from .cmd_substitute import scan_cmd_substitute
from .cmd_tabfirst import scan_cmd_tabfirst
from .cmd_tablast import scan_cmd_tablast
from .cmd_tabnext import scan_cmd_tabnext
from .cmd_tabonly import scan_cmd_tabonly
from .cmd_tabprevious import scan_cmd_tabprevious
from .cmd_unabbreviate import scan_cmd_unabbreviate
from .cmd_unmap import scan_cmd_unmap
from .cmd_unvsplit import scan_cmd_unvsplit
from .cmd_vnoremap import scan_cmd_vnoremap
from .cmd_vsplit import scan_cmd_vsplit
from .cmd_vunmap import scan_cmd_vunmap
from .cmd_wall import scan_cmd_wall
from .cmd_wq import scan_cmd_wq
from .cmd_wqall import scan_cmd_wqall
from .cmd_write import scan_cmd_write
from .cmd_yank import scan_cmd_yank


# TODO: compile regexes. ??
routes = OrderedDict()
routes[r'!(?=.+)'] = scan_cmd_shell_out
routes[r'&&?'] = scan_cmd_double_ampersand
routes[r'ab(?:breviate)?'] = scan_cmd_abbreviate
routes[r'bro(?:wse)?'] = scan_cmd_browse
routes[r'clo(?:se)?'] = scan_cmd_close
routes[r'co(?:py)?'] = scan_cmd_copy
routes[r'cq(?:uit)?'] = scan_cmd_cquit
routes[r'd(?:elete)?'] = scan_cmd_delete
routes[r'exi(?:t)?'] = scan_cmd_exit
routes[r'f(?:ile)?'] = scan_cmd_file
routes[r'g(?:lobal)?(?=[^ ])'] = scan_cmd_global
routes[r'h(?:elp)?'] = scan_cmd_help
routes[r'(?:ls|files|buffers)!?'] = scan_cmd_buffers
routes[r'vs(?:plit)?'] = scan_cmd_vsplit
routes[r'x(?:it)?$'] = scan_cmd_exit
routes[r'^cd(?=[^d]|$)'] = scan_cmd_cd
routes[r'^cdd'] = scan_cmd_cdd
routes[r'e(?:dit)?(?= |$)?'] = scan_cmd_edit
routes[r'let\s'] = scan_cmd_let
routes[r'm(?:ove)?(?=[^a]|$)'] = scan_cmd_move
routes[r'no(?:remap)'] = scan_cmd_noremap
routes[r'new'] = scan_cmd_new
routes[r'nn(?:oremap)?'] = scan_cmd_nnoremap
routes[r'nun(?:map)?'] = scan_cmd_nunmap
routes[r'ono(?:remap)?'] = scan_cmd_onoremap
routes[r'on(?:ly)?(?=!$|$)'] = scan_cmd_only
routes[r'ounm(?:ap)?'] = scan_cmd_ounmap
routes[r'p(?:rint)?$'] = scan_cmd_print
routes[r'pwd?$'] = scan_cmd_pwd
routes[r'q(?!a)(?:uit)?'] = scan_cmd_quit
routes[r'qa(?:ll)?'] = scan_cmd_qall
routes[r'r(?!eg)(?:ead)?'] = scan_cmd_read
routes[r'reg(?:isters)?(?=\s+[a-z0-9]+$|$)'] = scan_cmd_registers
routes[r's(?:ubstitute)?(?=[%&:/=]|$)'] = scan_cmd_substitute
routes[r'se(?:t)?(?=$|\s)'] = scan_cmd_set
routes[r'setl(?:ocal)?'] = scan_cmd_setlocal
routes[r'sh(?:ell)?'] = scan_cmd_shell
routes[r'snor(?:emap)?'] = scan_cmd_snoremap
routes[r'sp(?:lit)?'] = scan_cmd_split
routes[r'tabfir(?:st)?'] = scan_cmd_tabfirst
routes[r'tabl(?:ast)?'] = scan_cmd_tablast
routes[r'tabn(?:ext)?'] = scan_cmd_tabnext
routes[r'tabo(?:nly)?'] = scan_cmd_tabonly
routes[r'tabp(?:revious)?'] = scan_cmd_tabprevious
routes[r'tabr(?:ewind)?'] = scan_cmd_tabfirst
routes[r'una(?:bbreviate)?'] = scan_cmd_unabbreviate
routes[r'unm(?:ap)?'] = scan_cmd_unmap
routes[r'unvsplit$'] = scan_cmd_unvsplit
routes[r'vn(?:oremap)?'] = scan_cmd_vnoremap
routes[r'vu(?:nmap)?'] = scan_cmd_vunmap
routes[r'w(?:rite)?(?=(?:!?(?:\+\+|>>| |$)))'] = scan_cmd_write
routes[r'wqa(?:ll)?'] = scan_cmd_wqall
routes[r'xa(?:ll)?'] = scan_cmd_wqall
routes[r'wa(?:ll)?'] = scan_cmd_wall
routes[r'wq(?=[^a-zA-Z]|$)?'] = scan_cmd_wq
routes[r'y(?:ank)?'] = scan_cmd_yank
