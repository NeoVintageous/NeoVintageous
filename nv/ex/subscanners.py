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
from .cmd_print_working_dir import scan_cmd_print_working_dir
from .cmd_quit import scan_cmd_quit
from .cmd_quit_all import scan_cmd_quit_all
from .cmd_read_shell_out import scan_cmd_read_shell_out
from .cmd_register import scan_cmd_register
from .cmd_set import scan_cmd_set
from .cmd_set_local import scan_cmd_set_local
from .cmd_shell import scan_cmd_shell
from .cmd_shell_out import scan_cmd_shell_out
from .cmd_snoremap import scan_cmd_snoremap
from .cmd_split import scan_cmd_split
from .cmd_substitute import scan_cmd_substitute
from .cmd_tab_first import scan_cmd_tab_first
from .cmd_tab_last import scan_cmd_tab_last
from .cmd_tab_next import scan_cmd_tab_next
from .cmd_tab_only import scan_cmd_tab_only
from .cmd_tab_prev import scan_cmd_tab_prev
from .cmd_unabbreviate import scan_cmd_unabbreviate
from .cmd_unmap import scan_cmd_unmap
from .cmd_unvsplit import scan_cmd_unvsplit
from .cmd_vnoremap import scan_cmd_vnoremap
from .cmd_vsplit import scan_cmd_vsplit
from .cmd_vunmap import scan_cmd_vunmap
from .cmd_write import scan_cmd_write
from .cmd_write_all import scan_cmd_write_all
from .cmd_write_and_quit import scan_cmd_write_and_quit
from .cmd_write_and_quit_all import scan_cmd_write_and_quit_all
from .cmd_yank import scan_cmd_yank


# TODO: compile regexes. ??
patterns = OrderedDict()
patterns[r'!(?=.+)'] = scan_cmd_shell_out
patterns[r'&&?'] = scan_cmd_double_ampersand
patterns[r'ab(?:breviate)?'] = scan_cmd_abbreviate
patterns[r'bro(?:wse)?'] = scan_cmd_browse
patterns[r'clo(?:se)?'] = scan_cmd_close
patterns[r'co(?:py)?'] = scan_cmd_copy
patterns[r'cq(?:uit)?'] = scan_cmd_cquit
patterns[r'd(?:elete)?'] = scan_cmd_delete
patterns[r'exi(?:t)?'] = scan_cmd_exit
patterns[r'f(?:ile)?'] = scan_cmd_file
patterns[r'g(?:lobal)?(?=[^ ])'] = scan_cmd_global
patterns[r'h(?:elp)?'] = scan_cmd_help
patterns[r'(?:ls|files|buffers)!?'] = scan_cmd_buffers
patterns[r'vs(?:plit)?'] = scan_cmd_vsplit
patterns[r'x(?:it)?$'] = scan_cmd_exit
patterns[r'^cd(?=[^d]|$)'] = scan_cmd_cd
patterns[r'^cdd'] = scan_cmd_cdd
patterns[r'e(?:dit)?(?= |$)?'] = scan_cmd_edit
patterns[r'let\s'] = scan_cmd_let
patterns[r'm(?:ove)?(?=[^a]|$)'] = scan_cmd_move
patterns[r'no(?:remap)'] = scan_cmd_noremap
patterns[r'new'] = scan_cmd_new
patterns[r'nn(?:oremap)?'] = scan_cmd_nnoremap
patterns[r'nun(?:map)?'] = scan_cmd_nunmap
patterns[r'ono(?:remap)?'] = scan_cmd_onoremap
patterns[r'on(?:ly)?(?=!$|$)'] = scan_cmd_only
patterns[r'ounm(?:ap)?'] = scan_cmd_ounmap
patterns[r'p(?:rint)?$'] = scan_cmd_print
patterns[r'pwd?$'] = scan_cmd_print_working_dir
patterns[r'q(?!a)(?:uit)?'] = scan_cmd_quit
patterns[r'qa(?:ll)?'] = scan_cmd_quit_all
patterns[r'r(?!eg)(?:ead)?'] = scan_cmd_read_shell_out
patterns[r'reg(?:isters)?(?=\s+[a-z0-9]+$|$)'] = scan_cmd_register
patterns[r's(?:ubstitute)?(?=[%&:/=]|$)'] = scan_cmd_substitute
patterns[r'se(?:t)?(?=$|\s)'] = scan_cmd_set
patterns[r'setl(?:ocal)?'] = scan_cmd_set_local
patterns[r'sh(?:ell)?'] = scan_cmd_shell
patterns[r'snor(?:emap)?'] = scan_cmd_snoremap
patterns[r'sp(?:lit)?'] = scan_cmd_split
patterns[r'tabfir(?:st)?'] = scan_cmd_tab_first
patterns[r'tabl(?:ast)?'] = scan_cmd_tab_last
patterns[r'tabn(?:ext)?'] = scan_cmd_tab_next
patterns[r'tabo(?:nly)?'] = scan_cmd_tab_only
patterns[r'tabp(?:revious)?'] = scan_cmd_tab_prev
patterns[r'tabr(?:ewind)?'] = scan_cmd_tab_first
patterns[r'una(?:bbreviate)?'] = scan_cmd_unabbreviate
patterns[r'unm(?:ap)?'] = scan_cmd_unmap
patterns[r'unvsplit$'] = scan_cmd_unvsplit
patterns[r'vn(?:oremap)?'] = scan_cmd_vnoremap
patterns[r'vu(?:nmap)?'] = scan_cmd_vunmap
patterns[r'w(?:rite)?(?=(?:!?(?:\+\+|>>| |$)))'] = scan_cmd_write
patterns[r'wqa(?:ll)?'] = scan_cmd_write_and_quit_all
patterns[r'xa(?:ll)?'] = scan_cmd_write_and_quit_all
patterns[r'wa(?:ll)?'] = scan_cmd_write_all
patterns[r'wq(?=[^a-zA-Z]|$)?'] = scan_cmd_write_and_quit
patterns[r'y(?:ank)?'] = scan_cmd_yank
