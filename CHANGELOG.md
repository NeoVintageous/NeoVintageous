# Changelog

All notable changes are documented in this file using the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## 1.32.0 - Unreleased

### Added

* [#373](https://github.com/NeoVintageous/NeoVintageous/issues/373): New Input Method plugin - Automatically switch the IM when entering and exiting Insert Mode
* [#948](https://github.com/NeoVintageous/NeoVintageous/issues/948): New `:delm[arks] {marks}` - Delete the specified marks.  Marks that can be deleted include A-Z and 0-9.
* [#948](https://github.com/NeoVintageous/NeoVintageous/issues/948): New `:delm[arks]!` - Delete all marks for the current buffer, but not marks A-Z or 0-9.
* [#919](https://github.com/NeoVintageous/NeoVintageous/issues/919): Support for Dvorak mappings via [NeoVintageousDvorak](https://github.com/gerardroche/NeoVintageousDvorak)
* [#918](https://github.com/NeoVintageous/NeoVintageous/issues/918): Support for Colemak mappings via [NeoVintageousColemak](https://github.com/gerardroche/NeoVintageousColemak)
* [#944](https://github.com/NeoVintageous/NeoVintageous/issues/944): New ability to map any character e.g., `nnoremap ø :marks<CR>`
* [#106](https://github.com/NeoVintageous/NeoVintageous/issues/106): New `g,` Go to `[count]` newer position in change list
* [#106](https://github.com/NeoVintageous/NeoVintageous/issues/106): New `g;` Go to `[count]` older position in change list
* [#942](https://github.com/NeoVintageous/NeoVintageous/issues/942): Add `CTRL-M` alias of `Enter`
* [#943](https://github.com/NeoVintageous/NeoVintageous/issues/943): Add `zuw` alias of `zug`
* [#841](https://github.com/NeoVintageous/NeoVintageous/issues/841): Add `vintageous_auto_nohlsearch_on_normal_enter` setting to keep highlighting after searches
* [#936](https://github.com/NeoVintageous/NeoVintageous/issues/936): Add edit settings command "Preferences: NeoVintageous Settings"
* [#924](https://github.com/NeoVintageous/NeoVintageous/issues/924): Enable super keys, also known as the Windows key or Command key (⌘) on Mac, by default
* [#915](https://github.com/NeoVintageous/NeoVintageous/issues/915): Show marks in gutter (disable via `vintageous_show_marks_in_gutter` setting)
* [#921](https://github.com/NeoVintageous/NeoVintageous/issues/921): New `'equalalways'` option. Default on. When on, all the views are made the same size after splitting a view.

### Changed

* [#947](https://github.com/NeoVintageous/NeoVintageous/issues/947): :vnoremap and vunmap now include Select mode
* [#946](https://github.com/NeoVintageous/NeoVintageous/issues/946): :noremap and unmap now include Select mode

### Deprecated

* [#819](https://github.com/NeoVintageous/NeoVintageous/issues/819): Setting vintageous_exit_when_quiting_last_window is deprecated, use vintageous_exit_when_quitting_last_window instead
* [#952](https://github.com/NeoVintageous/NeoVintageous/issues/952): Setting highlightedyank is deprecated, use vintageous_highlighted_yank instead
* [#952](https://github.com/NeoVintageous/NeoVintageous/issues/952): Setting highlightedyank_style is deprecated, use vintageous_highlighted_yank_style instead
* [#952](https://github.com/NeoVintageous/NeoVintageous/issues/952): Setting highlightedyank_duration is deprecated, use vintageous_highlighted_yank_duration instead
* [#952](https://github.com/NeoVintageous/NeoVintageous/issues/952): Setting neovintageous_search_cur_style is deprecated, use vintageous_search_cur_style instead
* [#952](https://github.com/NeoVintageous/NeoVintageous/issues/952): Setting neovintageous_search_inc_style is deprecated, use vintageous_search_inc_style instead
* [#952](https://github.com/NeoVintageous/NeoVintageous/issues/952): Setting neovintageous_search_occ_style is deprecated, use vintageous_search_occ_style instead

### Fixed

* [#929](https://github.com/NeoVintageous/NeoVintageous/issues/929): There is no syntax highlighting for `<LocalLeader>`
* [#879](https://github.com/NeoVintageous/NeoVintageous/issues/879): neovintageousrc file options only set on active view at startup
* [#922](https://github.com/NeoVintageous/NeoVintageous/issues/922): neovintageousrc file reloading should reset options

## 1.31.0 - 2023-07-12

### Added

* [#916](https://github.com/NeoVintageous/NeoVintageous/issues/916): Set mark `m{a-zA-Z}` at cursor position now persist on restart
* [#880](https://github.com/NeoVintageous/NeoVintageous/issues/880): Set global mark `m{A-Z}` at cursor position
* [#881](https://github.com/NeoVintageous/NeoVintageous/issues/881): `:marks` List all the current marks
* [#906](https://github.com/NeoVintageous/NeoVintageous/issues/906): `:tabnew` and `:tabe[dit]` open a new tab page with an empty view (requires [Origami](https://packagecontrol.io/packages/Origami))
* [#902](https://github.com/NeoVintageous/NeoVintageous/issues/902): `:vs[plit] [file]` like `:sp[lit] [file]`, but split vertically (requires [Origami](https://packagecontrol.io/packages/Origami))
* [#903](https://github.com/NeoVintageous/NeoVintageous/issues/903): `:sp[lit] [file]` split current view in two and if given, edit `[file]`in new window (requires [Origami](https://packagecontrol.io/packages/Origami))
* [#911](https://github.com/NeoVintageous/NeoVintageous/issues/911): `CTRL-w ^` and `CTRL-w CTRL-^` split the current view in two and edit the alternate file (requires [Origami](https://packagecontrol.io/packages/Origami))
* [#909](https://github.com/NeoVintageous/NeoVintageous/issues/909): `new [file]` create a new split and if given, start editing file `[file]` in it (requires [Origami](https://packagecontrol.io/packages/Origami))
* [#910](https://github.com/NeoVintageous/NeoVintageous/issues/910): `:vne[w] [file]` like `:new [file]`, but split vertically (requires [Origami](https://packagecontrol.io/packages/Origami))
* [#901](https://github.com/NeoVintageous/NeoVintageous/issues/901): `CTRL-W gT` same as `gT`
* [#901](https://github.com/NeoVintageous/NeoVintageous/issues/901): `CTRL-W gt` same as `gt`
* [#897](https://github.com/NeoVintageous/NeoVintageous/issues/897): `CTRL-W gF` same as `gF`
* [#897](https://github.com/NeoVintageous/NeoVintageous/issues/897): `CTRL-W gf` same as `gf`
* [#896](https://github.com/NeoVintageous/NeoVintageous/issues/896): `gF` same as `gf`, except the cursor is positioned on row:col
* [#897](https://github.com/NeoVintageous/NeoVintageous/issues/897): `gf` the '~' character is expanded, like in "~user/file"
* [#897](https://github.com/NeoVintageous/NeoVintageous/issues/897): `gf` environment variables are expanded.
* [#897](https://github.com/NeoVintageous/NeoVintageous/issues/897): `gf` in visual modes
* [#893](https://github.com/NeoVintageous/NeoVintageous/issues/893): Reveal Side Bar command to make side bar visible, if not already, and put focus on it
* [#904](https://github.com/NeoVintageous/NeoVintageous/issues/904): Start visual mode linewise, `V`, is now countable
* [#888](https://github.com/NeoVintageous/NeoVintageous/issues/888): `gg` in visual block mode
* [#888](https://github.com/NeoVintageous/NeoVintageous/issues/888): `G` is now countable in visual block mode
* [#888](https://github.com/NeoVintageous/NeoVintageous/issues/888): `G` in visual block mode

### Fixed

* [#881](https://github.com/NeoVintageous/NeoVintageous/issues/881): Invalid and unknown marks should emit a bell
* [#914](https://github.com/NeoVintageous/NeoVintageous/issues/914): `{backtick}{a-z}` jump to mark should center screen if cursor off screen
* [#913](https://github.com/NeoVintageous/NeoVintageous/issues/913): No animated smooth scrolling with `<C-d>` or `<C-u>`
* [#908](https://github.com/NeoVintageous/NeoVintageous/issues/908): `:new` should split like `:split`
* [#905](https://github.com/NeoVintageous/NeoVintageous/issues/905): `:close!` should close last view
* [#900](https://github.com/NeoVintageous/NeoVintageous/issues/900): Command-line output should not show white-space characters
* [#899](https://github.com/NeoVintageous/NeoVintageous/issues/899): I in multiple cursor mode should glue undo operations
* [#892](https://github.com/NeoVintageous/NeoVintageous/issues/892): Change surrounding HTML tags breaks with multiple tags with attributes
* [#897](https://github.com/NeoVintageous/NeoVintageous/issues/897): `gf` doesn't work in some cases
* [#889](https://github.com/NeoVintageous/NeoVintageous/issues/889): `{visual}G` should extend to first non-blank character
* [#890](https://github.com/NeoVintageous/NeoVintageous/issues/890): `G` should jump to first non-blank character

## 1.30.1 - 2023-06-16

### Fixed

* [#887](https://github.com/NeoVintageous/NeoVintageous/issues/887): Using arrow doesn't scroll the view in visual block mode

## 1.30.0 - 2023-06-05

### Added

* [#886](https://github.com/NeoVintageous/NeoVintageous/issues/886): Support visual modes in unimpaired goto conflict commands `]n` and `[n`
* [#854](https://github.com/NeoVintageous/NeoVintageous/issues/854): Add support for keys `à`, `è`, `ò`, `ù`
* [#867](https://github.com/NeoVintageous/NeoVintageous/issues/867): Support keypad numbers as count prefix
* [#878](https://github.com/NeoVintageous/NeoVintageous/issues/878): Allow leading whitespace for commands in neovintageousrc file
* [#877](https://github.com/NeoVintageous/NeoVintageous/issues/877): Add `unmap`, `nunmap`, `ounmap`, `sunmap`, `vunmap`, `xunmap` support in neovintageousrc file
* [#876](https://github.com/NeoVintageous/NeoVintageous/issues/876): Add `:xnoremap` and `:xunmap`
* [#874](https://github.com/NeoVintageous/NeoVintageous/issues/874): Toggle highlight gutter aswell as highlight line On/Off/Toggle `[oc`/`]oc`/`yoc`
* [#870](https://github.com/NeoVintageous/NeoVintageous/issues/870): `n` (next), `q` (skip), `Q` (remove) keys in multiple cursor mode
* [#863](https://github.com/NeoVintageous/NeoVintageous/issues/863): Persist last search pattern on restarts

### Fixed

* [#885](https://github.com/NeoVintageous/NeoVintageous/issues/885): `'expandtabs'` should be `'expandtab'`
* [#866](https://github.com/NeoVintageous/NeoVintageous/issues/866): Count doesn't work when remapping `<C-e>` and `<C-y>`
* [#871](https://github.com/NeoVintageous/NeoVintageous/issues/871): Should be able to paste into multiple cursor

## 1.29.1 - 2023-05-14

### Fixed

* [#854](https://github.com/NeoVintageous/NeoVintageous/issues/854): Add missing vim sneak help page
* [#868](https://github.com/NeoVintageous/NeoVintageous/issues/868): Add `CTRL` / `SUPER+END` keybindings

## 1.29.0 - 2023-04-06

### Added

* [#855](https://github.com/NeoVintageous/NeoVintageous/issues/855): `crp` PascalCase coercion, alias to `crm` (Abolish plugin)
* [#790](https://github.com/NeoVintageous/NeoVintageous/issues/790): Asynchronous file saving setting `vintageous_save_async`, false by default
* [#643](https://github.com/NeoVintageous/NeoVintageous/issues/643): Mapping by file type e.g. `nnoremap FileType go gd :LspSymbolDefinition<CR>`
* [#861](https://github.com/NeoVintageous/NeoVintageous/issues/861): `[count]` for `D`
* [#860](https://github.com/NeoVintageous/NeoVintageous/issues/860): `[count]` for `C`
* [#805](https://github.com/NeoVintageous/NeoVintageous/issues/805): `<k0>` alias for `0`
* [#858](https://github.com/NeoVintageous/NeoVintageous/issues/858): `[count]` for `S`

### Changed

* [#790](https://github.com/NeoVintageous/NeoVintageous/issues/790): Asynchronous file saving is now disabled by default

### Fixed

* [#804](https://github.com/NeoVintageous/NeoVintageous/issues/804): Change syntax highlighting when writing to a new file
* [#859](https://github.com/NeoVintageous/NeoVintageous/issues/859):  `ZZ` doesn't save and close a new file

## 1.28.0 - 2023-03-20

### Added

* [#796](https://github.com/NeoVintageous/NeoVintageous/issues/796): Registers are now persisted on restarts
* [#833](https://github.com/NeoVintageous/NeoVintageous/issues/833): Sessions are now saved on exit instead of at runtime (builds >= 4081)
* [#74](https://github.com/NeoVintageous/NeoVintageous/issues/74): Add `#` alternate file register
* [#74](https://github.com/NeoVintageous/NeoVintageous/issues/74): Add `<C-^>` (`<C-6>`) go to most recent used file
* [#833](https://github.com/NeoVintageous/NeoVintageous/issues/833): Macros on now persisted on restarts
* [#833](https://github.com/NeoVintageous/NeoVintageous/issues/833): Macros are now persisted globally

## 1.27.4 - 2022-12-16

### Fixed

* [#787](https://github.com/NeoVintageous/NeoVintageous/issues/787): Add `vintageous_lsp_save` setting to fix lsp format on save doesn't seem to work
* [#822](https://github.com/NeoVintageous/NeoVintageous/issues/822): `Esc` shouldn't close autocomplete-suggester *and* insert mode at the same time

## 1.27.3 - 2022-12-05

### Fixed

* [#853](https://github.com/NeoVintageous/NeoVintageous/issues/853): Tab key doesn't work properly with snippets
* [#852](https://github.com/NeoVintageous/NeoVintageous/issues/852): PowerShell does not work with `:shell`

## 1.27.2 - 2022-10-09

### Fixed

* [#848](https://github.com/NeoVintageous/NeoVintageous/issues/848): Ex print with `#` flag adds incorrect line numbers
* [#847](https://github.com/NeoVintageous/NeoVintageous/issues/847): Allow numbers in mapped user commands
* [#788](https://github.com/NeoVintageous/NeoVintageous/issues/788): Make `:g/pattern/p` include last line even if it doesn't end with `\n`

## 1.27.1 - 2022-10-01

### Fixed

* [#826](https://github.com/NeoVintageous/NeoVintageous/issues/826): `%` doesn't work correctly on html tags

## 1.27.0 - 2022-09-28

### Added

* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround change tag with `>` remove attributes e.g. `cst<div>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround change tag with `\n` (newline) to keep attributes e.g. `cst<div<CR>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround change tag with `<C-t>` to put tag on lines by themselves e.g. `cst<C-t>div>`, `cst<C-t>div<CR>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround yank `<C-t>` to put tags on lines by themselves e.g. `ysiW<C-t>div>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround change `<C-t>` to put tags on lines by themselves e.g. `cs"<C-t>div>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround yank tag with `t` (same as `<`) e.g. `ysiwtdiv>`, `ysiw<div>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround tag close with `>` e.g. `ysiwtdiv>`, `cs"tdiv>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround tag close with `\n` e.g. `ysiwtdiv<CR>`, `cs"tdiv<CR>` (Surround)
* [#768](https://github.com/NeoVintageous/NeoVintageous/issues/768): surround change tag close with newline e.g. `ysiwtdiv<CR>` (Surround)
* [#830](https://github.com/NeoVintageous/NeoVintageous/issues/830): Add surround `f` (function): press `ysWfprint<cr>` in `"hello"` to get  `print("hello")` (Surround)
* [#830](https://github.com/NeoVintageous/NeoVintageous/issues/830): Add surround `F` (function): press `ysWFprint<cr>` in `"hello"` to get  `print( "hello" )` (Surround)
* [#830](https://github.com/NeoVintageous/NeoVintageous/issues/830): Add surround `<C-f>` (function): press `ysW<C-f>print<cr>` in `"hello"` to get `(print "hello")` (Surround)
* [#828](https://github.com/NeoVintageous/NeoVintageous/issues/828): Add `S{char}` in visual line mode (Surround)
* [#838](https://github.com/NeoVintageous/NeoVintageous/issues/838): Add `<S-tab>`
* [#711](https://github.com/NeoVintageous/NeoVintageous/issues/711): Add `[count]` for `*`
* [#711](https://github.com/NeoVintageous/NeoVintageous/issues/711): Add `[count]` for `#`
* [#826](https://github.com/NeoVintageous/NeoVintageous/issues/826): Add jumps like `%` inside comments

## 1.26.3 - 2022-06-20

### Fixed

* [#827](https://github.com/NeoVintageous/NeoVintageous/issues/827): `Y` should work the same as `y` in visual line mode
* [#821](https://github.com/NeoVintageous/NeoVintageous/issues/821): Add German `Ü`, `§`, and `°` keys

## 1.26.2 - 2022-05-16

### Fixed

* [#821](https://github.com/NeoVintageous/NeoVintageous/issues/821): Add German `ü` and `ß` keys
* [#815](https://github.com/NeoVintageous/NeoVintageous/issues/815): Add `vintageous_i_escape_kj` setting for common escape mapping

## 1.26.1 - 2022-02-21

### Fixed

* [#807](https://github.com/NeoVintageous/NeoVintageous/issues/807): Delete register no longer working on selection made by other plugins

## 1.26.0 - 2022-01-10

### Added

* [#615](https://github.com/NeoVintageous/NeoVintageous/issues/615): Support for chaining ex commands with `<Bar>` (vertical bar)
* [#759](https://github.com/NeoVintageous/NeoVintageous/issues/759): Support for mapping multiple ex commands
* [#786](https://github.com/NeoVintageous/NeoVintageous/issues/786): Paste is now more flexible for multi cursors
* [#781](https://github.com/NeoVintageous/NeoVintageous/issues/781): New text objects `i,`, `i.`, `i;`, `i:`, `i+`, `i-`, `i=`, `i~`, `i_`, `i*`, `i#`, `i/`, `i|`, `i\`, `i&`, `i$` (port of https://github.com/wellle/targets.vim)
* [#781](https://github.com/NeoVintageous/NeoVintageous/issues/781): New text objects `a,`, `a.`, `a;`, `a:`, `a+`, `a-`, `a=`, `a~`, `a_`, `a*`, `a#`, `a/`, `a|`, `a\`, `a&`, `a$` (port of https://github.com/wellle/targets.vim)

### Fixed

* [#800](https://github.com/NeoVintageous/NeoVintageous/issues/800): scroll_context_lines setting for H and L
* [#806](https://github.com/NeoVintageous/NeoVintageous/issues/806): Quote-Quote and Quote-Backtick commands don't work
* [#786](https://github.com/NeoVintageous/NeoVintageous/issues/786): Pasting with p or P does not work when multiple cursors are enabled
* [#734](https://github.com/NeoVintageous/NeoVintageous/issues/734): Change In Tag deletes empty HTML tag instead of placing caret inside it
* [#740](https://github.com/NeoVintageous/NeoVintageous/issues/740): Change inside parentheses not working as expected?
* [#739](https://github.com/NeoVintageous/NeoVintageous/issues/739): Wrong behaviour for nested motions
* [#744](https://github.com/NeoVintageous/NeoVintageous/issues/744): Delete-surround not deleting the right pair
* [#644](https://github.com/NeoVintageous/NeoVintageous/issues/644): Surround plugin deletes non-matching parentheses
* [#745](https://github.com/NeoVintageous/NeoVintageous/issues/745): `ds` sometimes doesn't work when the cursor is on first target
* [#791](https://github.com/NeoVintageous/NeoVintageous/issues/791): Reset mode setting is ignored when mode is already normal
* [#790](https://github.com/NeoVintageous/NeoVintageous/issues/790): Various file saving edge-case issues
* [#790](https://github.com/NeoVintageous/NeoVintageous/issues/790): Asynchronous file saving with `:w`, `:wq`

## 1.25.0 - 2021-12-14

### Added

* [#789](https://github.com/NeoVintageous/NeoVintageous/issues/789): Support inverse global-command `:g!/pattern/cmd`

### Fixed

* [#797](https://github.com/NeoVintageous/NeoVintageous/issues/797): `:cd` not working as expected

## 1.24.1 - 2021-07-07

* [#782](https://github.com/NeoVintageous/NeoVintageous/issues/782): Toggle-able option to keep sublime open when quitting out of last file
* [#780](https://github.com/NeoVintageous/NeoVintageous/issues/780): Navigating in the command palette not working in (ST4)

## 1.24.0 - 2021-06-09

### Added

* [#767](https://github.com/NeoVintageous/NeoVintageous/issues/767): Support window splitting for latest version of Origami
* [#755](https://github.com/NeoVintageous/NeoVintageous/issues/755): New ex command `:inoremap` (note only a few keys are currently mappable in insert mode)

### Fixed

* [#772](https://github.com/NeoVintageous/NeoVintageous/issues/772): Backwards sneak special characters
* [#760](https://github.com/NeoVintageous/NeoVintageous/issues/760): `ci"` with space at the end of a string doesn't remove the space
* [#771](https://github.com/NeoVintageous/NeoVintageous/issues/771): `cit` leaves newline
* [#762](https://github.com/NeoVintageous/NeoVintageous/issues/762): `P` and `p` aren't supposed to paste lines starting from the current cursor position
* [#748](https://github.com/NeoVintageous/NeoVintageous/issues/748): `viw`, `vaw` behaviour does not copy Vim behaviour
* [#765](https://github.com/NeoVintageous/NeoVintageous/issues/765): `viw` wrong selection last character in `()`
* [#770](https://github.com/NeoVintageous/NeoVintageous/issues/770): `:q` (quit) on empty panes or non-existent files fails with "E32: No file name"

## 1.23.0 - 2020-12-12

### Added

* [#750](https://github.com/NeoVintageous/NeoVintageous/issues/750): New setting `vintageous_sneak_use_ic_scs` support sneak `'smartcase'`
* [#109](https://github.com/NeoVintageous/NeoVintageous/issues/109): Implement `i_ctrl-u` delete all entered characters before the cursor in the current line
* [#754](https://github.com/NeoVintageous/NeoVintageous/issues/754): Implement `ctrl-w_ctrl-]` split view and and jump to definition (ST4)
* [#470](https://github.com/NeoVintageous/NeoVintageous/issues/470): New setting `vintageous_handle_keys` for granular control of enabled keys

### Changed

* [#711](https://github.com/NeoVintageous/NeoVintageous/issues/711): Ctrl keys are now enabled by default, to disable set `vintageous_use_ctrl_keys` to false or use the new `vintageous_handle_keys` setting to disable specific keys

## 1.22.0 - 2020-10-25

### Added

* [#749](https://github.com/NeoVintageous/NeoVintageous/issues/749): Support for Python 3.8 (ST4)
* [#205](https://github.com/NeoVintageous/NeoVintageous/issues/205): `'scrolloff'` option (ST4)
* [#733](https://github.com/NeoVintageous/NeoVintageous/issues/733): `[or`, `]or`, `yor`, enable, disable, and toggle `'relativenumber'` (Unimpaired) (ST4)
* [#732](https://github.com/NeoVintageous/NeoVintageous/issues/732): new option `'relativenumber'` `'rnu'` `'norelativenumber'` `'nornu'` (ST4)

### Changed

* [#751](https://github.com/NeoVintageous/NeoVintageous/issues/751): All commands that started with an underscore have been renamed with prefix "nv_". You don't need to do anything unless you have customisations that use those commands. The reason for the change is in ST4 Python 3.8 leading underscored commands are ignored.

  Here are some some examples of changed commands:

  old | new
  --- | ---
  `_enter_normal_mode` | `nv_enter_normal_mode`
  `_enter_insert_mode` | `nv_enter_insert_mode`
  `_nv_feed_key` | `nv_feed_key`
  `_vi_w` | `nv_vi_w`
  `_vi_w` | `nv_vi_w`

## 1.21.5 - 2020-10-25

### Fixed

* [#747](https://github.com/NeoVintageous/NeoVintageous/issues/747): Key mapping doesn't work with foreign character č

## 1.21.4 - 2020-08-27

### Fixed

* [#742](https://github.com/NeoVintageous/NeoVintageous/issues/742): Escaping from ST's own multi-cursor selection removes all selections

## 1.21.3 - 2020-08-27

### Fixed

* [#742](https://github.com/NeoVintageous/NeoVintageous/issues/742): Escaping from ST's own multi-cursor selection removes all selections

## 1.21.2 - 2020-08-20

### Fixed

* [#741](https://github.com/NeoVintageous/NeoVintageous/issues/741): Latest version of Sublime Text (4082 and up) has breaking changes

## 1.21.1 - 2020-05-06

### Fixed

* [#731](https://github.com/NeoVintageous/NeoVintageous/issues/731): Disable Sneak plugin by default
* [#730](https://github.com/NeoVintageous/NeoVintageous/issues/730): S key starts search rather than correct Vi behaviour

## 1.21.0 - 2020-04-29

### Added

* [#457](https://github.com/NeoVintageous/NeoVintageous/issues/457): Port of vim-sneak; includes most features except label-modes
* [#718](https://github.com/NeoVintageous/NeoVintageous/issues/718): Settings to more easily enable mapping `jj` and `jk` to escape from insert mode
* [#727](https://github.com/NeoVintageous/NeoVintageous/issues/727): Display "h" indicator for hidden views in `:ls` output
* [#720](https://github.com/NeoVintageous/NeoVintageous/issues/720): `<C-w>W [N]` go to view by id
* [#721](https://github.com/NeoVintageous/NeoVintageous/issues/721): Alias `<bslash>` to `,`
* [#722](https://github.com/NeoVintageous/NeoVintageous/issues/722): `:set inv{option}` alias of `:set{option}!`

### Changed

* [#726](https://github.com/NeoVintageous/NeoVintageous/issues/726): `f`, `F`, `t`, `T`, `;`, and `,` noop now emits a visual bell
* [#724](https://github.com/NeoVintageous/NeoVintageous/issues/724): Ex mode noop operations now emit a visual bell
* [#725](https://github.com/NeoVintageous/NeoVintageous/issues/725): `ZZ` and `ZQ` are now only mapped for normal mode

### Removed

* [#715](https://github.com/NeoVintageous/NeoVintageous/issues/715): `neovintageous_open_my_rc_file` (cmd); use `neovintageous {action=open_rc_file}` instead
* [#715](https://github.com/NeoVintageous/NeoVintageous/issues/715): `neovintageous_reload_my_rc_file` (cmd); use `neovintageous {action=reload_rc_file}` instead
* [#715](https://github.com/NeoVintageous/NeoVintageous/issues/715): `neovintageous_toggle_side_bar` (cmd); use `neovintageous {action=toggle_side_bar}` instead

### Fixed

* [#723](https://github.com/NeoVintageous/NeoVintageous/issues/723): Command-line completions should ignore `no{option}` unless prefix "no"
* [#717](https://github.com/NeoVintageous/NeoVintageous/issues/717): Ex command ranges should ignore whitespace
* [#712](https://github.com/NeoVintageous/NeoVintageous/issues/712): `:help {subject}` is very slow (performance)
* [#716](https://github.com/NeoVintageous/NeoVintageous/issues/716): `yol` toggle list sometimes doesn't work (Unimpaired)
* [#714](https://github.com/NeoVintageous/NeoVintageous/issues/714): `^V` is not syntax highlighted like `^J` in command-line output bug (UI)
* [#709](https://github.com/NeoVintageous/NeoVintageous/issues/709): General performance improvements (performance)

## 1.20.0 - 2020-03-22

### Added

* [#705](https://github.com/NeoVintageous/NeoVintageous/issues/705): `/{pattern}\c` (`\c` ignore case, do not use the `'ignorecase'` option)
* [#705](https://github.com/NeoVintageous/NeoVintageous/issues/705): `/{pattern}\C` (`\C` match case, do not use the `'ignorecase'` option)
* [#707](https://github.com/NeoVintageous/NeoVintageous/issues/707): `[count]gT` Go `{count}` tab pages back
* [#631](https://github.com/NeoVintageous/NeoVintageous/issues/631): `i/`, `i_`, `a/`, and `a_` text objects e.g. `ci/`, `ca/`
* [#697](https://github.com/NeoVintageous/NeoVintageous/issues/697): `'smartcase'` option
* [#700](https://github.com/NeoVintageous/NeoVintageous/issues/700): "=" readonly buffer indicator for `:(ls|buffers|files)`
* [#701](https://github.com/NeoVintageous/NeoVintageous/issues/701): "+" modified buffer indicator for `(ls|buffers|files)`
* [#702](https://github.com/NeoVintageous/NeoVintageous/issues/702): `:(ls|buffers|files)` now uses view id as the unique number (this number will not change)
* [#294](https://github.com/NeoVintageous/NeoVintageous/issues/294): `:(ls|buffers|files)`improvements
* [#703](https://github.com/NeoVintageous/NeoVintageous/issues/703): Command-line output use the same panel and executed commands overwrite previous output
* [#703](https://github.com/NeoVintageous/NeoVintageous/issues/703): Command-line output panels now gain focus when a command is executed
* [#703](https://github.com/NeoVintageous/NeoVintageous/issues/703): Command-line output panels are now closable by pressing enter
* [#703](https://github.com/NeoVintageous/NeoVintageous/issues/703): Command-line output syntax improvements
* [#703](https://github.com/NeoVintageous/NeoVintageous/issues/703): Improved syntax for `:(ls|buffers|files)` command-line output
* [#703](https://github.com/NeoVintageous/NeoVintageous/issues/703): Improved syntax for `:reg[isters]` command-line output
* [#703](https://github.com/NeoVintageous/NeoVintageous/issues/703): Improved syntax for `:his[tory]` command-line output
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): keypad keys `<k0>`, `<k1>`, `<k2>`, `<k3>`, `<k4>`, `<k5>`, `<k6>`, `<k7>`, `<k8>`, `<k9>`, `<kdivide>`, `<kenter>`, `<kminus>`, `<kmultiply>`, `<kperiod>`, `<kplus>`

### Fixed

* [#706](https://github.com/NeoVintageous/NeoVintageous/issues/706): `gf` should emit visual bell when there is no file under cursor
* [#704](https://github.com/NeoVintageous/NeoVintageous/issues/704): `[n` and `]n` should not jump to invalid conflict markers
* [#699](https://github.com/NeoVintageous/NeoVintageous/issues/699): `N` after `?` (reverse search) followed by `n` moves in wrong direction (regression)
* [#612](https://github.com/NeoVintageous/NeoVintageous/issues/612): Searches bound to a keys in neovintageousrc are not repeatable by `n` or `N`
* [#698](https://github.com/NeoVintageous/NeoVintageous/issues/698): `:help {subject}` doesn't work for subjects > 35 chars
* [#691](https://github.com/NeoVintageous/NeoVintageous/issues/691): Undo should ring bell when already at oldest change
* [#694](https://github.com/NeoVintageous/NeoVintageous/issues/694): `<F2>` and `<S-F2>` next and previous bookmark keys wrong way around
* [#693](https://github.com/NeoVintageous/NeoVintageous/issues/693): `<C-S-b>` should show build with overlay
* [#10](https://github.com/NeoVintageous/NeoVintageous/issues/10): Repeating text changing doesn't work.

## 1.19.0 - 2020-02-19

### Added

* [#670](https://github.com/NeoVintageous/NeoVintageous/issues/670): Marks locations are updated on view changes
* [#689](https://github.com/NeoVintageous/NeoVintageous/issues/689): `<Return>` key alias for `<CR>`
* [#688](https://github.com/NeoVintageous/NeoVintageous/issues/688): `<Enter>` key alias for `<CR>`
* [#684](https://github.com/NeoVintageous/NeoVintageous/issues/684): `:shell` start a shell (use `vintageous_terminal` setting to set the terminal name)
* [#685](https://github.com/NeoVintageous/NeoVintageous/issues/685): `'shell'` option e.g. `:set shell=/bin/bash` (used for `:!{cmd}` commands)
* [#687](https://github.com/NeoVintageous/NeoVintageous/issues/687): `[range]:read !{cmd}` execute `{cmd}` and insert below cursor
* [#674](https://github.com/NeoVintageous/NeoVintageous/issues/674): Implement Vim modelines
* [#678](https://github.com/NeoVintageous/NeoVintageous/issues/678): `'textwidth'` option e.g. `:set textwidth`, `:set notextwidth`
* [#677](https://github.com/NeoVintageous/NeoVintageous/issues/677): `'tabstop'` option e.g. `:set tabstop`, `:set notabstop`
* [#679](https://github.com/NeoVintageous/NeoVintageous/issues/679): `'expandtabs'` option e.g. `:set expandtabs`, `:set noexpandtabs`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<D-bs>`, `<D-cr>`, `<D-del>`, `<D-down>`, `<D-home>`, `<D-left>`, `<D-pagedown>`, `<D-pageup>`, `<D-right>`, `<D-space>`, `<D-up>`, `<D-.>`, `<D-S-.>`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<M-left>` alias to `h`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<M-right>` alias to `l`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<C-space>`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<C-bs>` alias to `h`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<C-pageup>` alias to `gT`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<C-pagedown>` alias to `gt`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<C-home>` alias to `gg`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<insert>` alias to `i`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<S-down>` alias to `CTRL-f`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<S-up>` alias to `CTRL-b`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<C-left>` alias to `B`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<S-left>` alias to `b`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<C-right>` alias to `W`
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<S-right>` alias to `w`
* [#671](https://github.com/NeoVintageous/NeoVintageous/issues/671): Emit visual bell when ex command not found or invalid

### Changed

* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `'winaltkeys'` option is now "menu" by default
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `'ignorecase'` option is now false by default
* [#674](https://github.com/NeoVintageous/NeoVintageous/issues/674): `sublime:` specific modelines have been superseded by vim modelines
* [#675](https://github.com/NeoVintageous/NeoVintageous/issues/675): Modelines are no longer applied on save, only once on load

### Removed

* [#685](https://github.com/NeoVintageous/NeoVintageous/issues/685): `VintageousEx_linux_shell` setting; use `:set shell={value}` instead
* [#685](https://github.com/NeoVintageous/NeoVintageous/issues/685): `VintageousEx_osx_shell` setting; use `:set shell={value}` instead
* [#685](https://github.com/NeoVintageous/NeoVintageous/issues/685): `linux_shell` setting; use `:set shell={value}` instead
* [#686](https://github.com/NeoVintageous/NeoVintageous/issues/686): `VintageousEx_linux_terminal` setting; use `vintageous_terminal` instead
* [#686](https://github.com/NeoVintageous/NeoVintageous/issues/686): `VintageousEx_osx_terminal` setting; use `vintageous_terminal` instead

### Fixed

* [#690](https://github.com/NeoVintageous/NeoVintageous/issues/690): RC file syntax should only scope known valid keys
* [#687](https://github.com/NeoVintageous/NeoVintageous/issues/687): Various `:!{cmd}` inconsistencies
* [#683](https://github.com/NeoVintageous/NeoVintageous/issues/683): `'{a-z}` in visual line mode is inconsistent
* [#682](https://github.com/NeoVintageous/NeoVintageous/issues/682): Visual mode `m{a-z}` off-by-one
* [#681](https://github.com/NeoVintageous/NeoVintageous/issues/681): `m{a-z}` should not change mode
* [#680](https://github.com/NeoVintageous/NeoVintageous/issues/680): `{backtick}{a-z}` should position cursor at the specified location
* [#676](https://github.com/NeoVintageous/NeoVintageous/issues/676): Uppercase alt keys don't work when `winaltkeys=menu`
* [#672](https://github.com/NeoVintageous/NeoVintageous/issues/672): Status messages not displayed when `:set belloff=all`

## 1.18.0 - 2020-02-01

### Added

* [#630](https://github.com/NeoVintageous/NeoVintageous/issues/630): Visual block pasting
* [#668](https://github.com/NeoVintageous/NeoVintageous/issues/668): `[n` and `]n` to navigate between conflicts (Unimpaired)
* [#4](https://github.com/NeoVintageous/NeoVintageous/issues/4): Remember last search and ex command history on restarts (sessions)
* [#570](https://github.com/NeoVintageous/NeoVintageous/issues/570): Repeated text objects e.g. `vitit` to visually select inner tags
* [#75](https://github.com/NeoVintageous/NeoVintageous/issues/75): Add `:buffer [N]` command
* [#664](https://github.com/NeoVintageous/NeoVintageous/issues/664): Add visual line `CTRL-v` enter visual block
* [#666](https://github.com/NeoVintageous/NeoVintageous/issues/666): Add visual line `CTRL-n` add next multiple cursor match
* [#665](https://github.com/NeoVintageous/NeoVintageous/issues/665): Add visual block `CTRL-n` enter multiple cursor
* [#663](https://github.com/NeoVintageous/NeoVintageous/issues/663): Add `I` flag to `:substitute` command
* [#662](https://github.com/NeoVintageous/NeoVintageous/issues/662): Add `'ignorecase'` option support to `:substitute` command
* [#660](https://github.com/NeoVintageous/NeoVintageous/issues/660): Ex mode `<S-tab>` now cycles through completions in reverse
* [#657](https://github.com/NeoVintageous/NeoVintageous/issues/657): Auto complete in empty Command-line mode now triggers all completions
* [#641](https://github.com/NeoVintageous/NeoVintageous/issues/641): Support search modifiers `\v`, `\V`, `\m`, and `\M`
* [#655](https://github.com/NeoVintageous/NeoVintageous/issues/655): `*` and `#` searches are noop unless all cursor words match
* [#656](https://github.com/NeoVintageous/NeoVintageous/issues/656): `*` and `#` multiple cursor searches

### Changed

* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `vintageous_multi_cursor_exit_from_visual_mode` is now disabled by default

### Removed

* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `__vi_external_disable_keys` setting was removed (use `__vi_external_disable`)
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `is_vintageous_widget` setting was removed (unused internal setting)

### Fixed

* [#669](https://github.com/NeoVintageous/NeoVintageous/issues/669): Shell cmds should default to `sh` if `$SHELL` is not set
* [#667](https://github.com/NeoVintageous/NeoVintageous/issues/667): Pasting line breaks newline at the end of file
* [#654](https://github.com/NeoVintageous/NeoVintageous/issues/654): `cit` deletes inside the wrong tag
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): Various multiple cursor mode issues
* [#658](https://github.com/NeoVintageous/NeoVintageous/issues/658): `gU` and `gu` should never emit visual bell
* [#661](https://github.com/NeoVintageous/NeoVintageous/issues/661): Visual block yank should move cursor to beginning of selection
* [#659](https://github.com/NeoVintageous/NeoVintageous/issues/659): Ex mode auto complete is broken (ST4)
* [#653](https://github.com/NeoVintageous/NeoVintageous/issues/653): One char searches highlights two chars for current cursor

## 1.17.8 - 2020-01-12

### Fixed

* [#652](https://github.com/NeoVintageous/NeoVintageous/issues/652): Command-line output should all use the same output panel
* [#651](https://github.com/NeoVintageous/NeoVintageous/issues/651): Command-line output should be read-only
* [#650](https://github.com/NeoVintageous/NeoVintageous/issues/650): `C-g` (print cursor position) is incorrect
* [#649](https://github.com/NeoVintageous/NeoVintageous/issues/649): Enter visual block from visual selection is broken (ST4)
* [#647](https://github.com/NeoVintageous/NeoVintageous/issues/647): Replace character bug (ST4)

## 1.17.7 - 2019-10-18

### Fixed

* [#639](https://github.com/NeoVintageous/NeoVintageous/issues/639): `C-d` and `C-u` is broken

## 1.17.6 - 2019-10-18

### Fixed

* [#636](https://github.com/NeoVintageous/NeoVintageous/issues/636): `cs"<div class="x">` should strip class from closing tag
* [#636](https://github.com/NeoVintageous/NeoVintageous/issues/636): `ys{motion}<div class="x">` should strip class from closing tag
* [#636](https://github.com/NeoVintageous/NeoVintageous/issues/636): `ys{motion}tdiv>` alias "t" (`<`) does not work
* [#635](https://github.com/NeoVintageous/NeoVintageous/issues/635): Visual block mode resets to visual when switching view
* [#633](https://github.com/NeoVintageous/NeoVintageous/issues/633): `ds|`doesn't work

## 1.17.5 - 2019-09-02

### Fixed

* [#629](https://github.com/NeoVintageous/NeoVintageous/issues/629): Surround quote marks should only operate within the line
* [#628](https://github.com/NeoVintageous/NeoVintageous/issues/628): Surround commands should work with cursor on target
* [#627](https://github.com/NeoVintageous/NeoVintageous/issues/627): Yank and paste line to/from register doesn't work as expected

## 1.17.4 - 2019-08-16

### Fixed

* [#625](https://github.com/NeoVintageous/NeoVintageous/issues/625): visual block mode delete doesn't work

## 1.17.3 - 2019-08-08

### Fixed

* [#623](https://github.com/NeoVintageous/NeoVintageous/issues/623): `:[count]` doesn't move screen to keep cursor in view

## 1.17.2 - 2019-07-18

### Fixed

* [#621](https://github.com/NeoVintageous/NeoVintageous/issues/621): rc file loading encoding issue

## 1.17.1 - 2019-07-15

### Fixed

* [#620](https://github.com/NeoVintageous/NeoVintageous/issues/620): `Alt+{hotkeys}` not working

## 1.17.0 - 2019-07-11

### Added

* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `yoi`, `[oi`, and `]oi`, toggle, switch on, and switch off `'ignorecase'` (Unimpaired plugin)
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `yoh`, `[oh`, and `]oh`, toggle, switch on, and switch off `'hlsearch'` (Unimpaired plugin)
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `yo{char}` (previously `co[char}`) toggle option (Unimpaired plugin)
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): Support for `set {option}` in neovintageousrc file
* [#596](https://github.com/NeoVintageous/NeoVintageous/issues/596): `:set {option}!` toggle option
* [#611](https://github.com/NeoVintageous/NeoVintageous/issues/611): `:set {option}?` show option
* [#611](https://github.com/NeoVintageous/NeoVintageous/issues/611): `:set no{option}` switch option off
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set belloff`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set menu`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set minimap`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set number`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set sidebar`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set spell`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set statusbar`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set wrap`
* [#585](https://github.com/NeoVintageous/NeoVintageous/issues/585): `:set wrapscan`
* [#607](https://github.com/NeoVintageous/NeoVintageous/issues/607): `vai` (text-object) an indentation level and line above (indent object plugin)
* [#607](https://github.com/NeoVintageous/NeoVintageous/issues/607): `vii` (text-object) inner indentation level (no line above) (indent object plugin)
* [#607](https://github.com/NeoVintageous/NeoVintageous/issues/607): `vaI` (text-object) an indentation level and lines above/below (indent object plugin)
* [#607](https://github.com/NeoVintageous/NeoVintageous/issues/607): `viI` (text-object) inner indentation level (no lines above/below) (indent object plugin)
* [#607](https://github.com/NeoVintageous/NeoVintageous/issues/607): Allow plugins to be fully disabled by boolean setting `enable_{plugin_name}`
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `[s` move to prev misspelled word after the cursor (`'wrapscan'` applies)
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `]s` move to next misspelled word after the cursor (`'wrapscan'` applies)
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `:spellundo {word}` remove `{word}` from good word spell checking
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `:spellgood {word}` add `{word}` as a good word to spell checking
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `z=` for the word under/after the cursor suggest correctly spelled words
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `zug` undo `zg`, remove the word from the entry in spell checking dictionary
* [#599](https://github.com/NeoVintageous/NeoVintageous/issues/599): `zg` add word under the cursor as a good word to spell checking dictionary
* [#604](https://github.com/NeoVintageous/NeoVintageous/issues/604): `:set wrapscan` to disable wrapping on `*`, `#`, `n`, `N` (searches)
* [#604](https://github.com/NeoVintageous/NeoVintageous/issues/604): `:set wrapscan` to disable wrapping on `]c` and `[c` (jump to diffs)
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): `<Del>` delete `[count]` characters under and after the cursor (alias of `x`)
* [#404](https://github.com/NeoVintageous/NeoVintageous/issues/404): Support for function keys 13-20 in mappings e.g. `<f13>`, `<C-f16>`, `<C-S-f20>`
* [#593](https://github.com/NeoVintageous/NeoVintageous/issues/593): Highlight all occurrences on incremental searches
* [#589](https://github.com/NeoVintageous/NeoVintageous/issues/589): `:set incsearch` to highlight the pattern matches as it was typed so far
* [#589](https://github.com/NeoVintageous/NeoVintageous/issues/589): `:set winaltkeys` to enable `<A-...>` mappings
* [#579](https://github.com/NeoVintageous/NeoVintageous/issues/579): `<A-...>` ALT keys (alias of `<M-...>`)
* [#580](https://github.com/NeoVintageous/NeoVintageous/issues/580): `[count]gqgq` (alias of `gqq`)
* [#580](https://github.com/NeoVintageous/NeoVintageous/issues/580): `[count]gqq` format the current line with a count format that many lines

### Deprecated

* [#404](404): `vintageous_belloff` setting; use `set belloff` in neovintageousrc file
* [#404](404): `vintageous_hlsearch` setting; use `set hlsearch` in neovintageousrc file
* [#404](404): `vintageous_ignorecase` setting; use `set ignorecase` in neovintageousrc file
* [#404](404): `vintageous_incsearch` setting; use `set incsearch` in neovintageousrc file
* [#404](404): `vintageous_magic` setting; use `set magic` in neovintageousrc file
* [#404](404): `vintageous_modeline` setting; use `set modeline` in neovintageousrc file
* [#404](404): `vintageous_modelines` setting; use `set modelines` in neovintageousrc file
* [#404](404): `vintageous_winaltkeys` setting; use `set winaltkeys` in neovintageousrc file
* [#404](404): `vintageous_wrapscan` setting; use `set wrapscan` in neovintageousrc file

### Fixed

* [#617](https://github.com/NeoVintageous/NeoVintageous/issues/617): Some magic mode searches should be literal
* [#613](https://github.com/NeoVintageous/NeoVintageous/issues/613): Goto matching bracket `%` inherits strange behaviour from vim
* [#243](https://github.com/NeoVintageous/NeoVintageous/issues/243): Braces in strings mess up brace matching with `%`
* [#612](https://github.com/NeoVintageous/NeoVintageous/issues/612): Mapped searches are not repeatable by `n` or `N`
* [#373](https://github.com/NeoVintageous/NeoVintageous/issues/373): `vii` does not select the whole indented line
* [#606](https://github.com/NeoVintageous/NeoVintageous/issues/606): `]<Space>` and `[<Space>` cursor position on blank lines
* [#605](https://github.com/NeoVintageous/NeoVintageous/issues/605): `]c` and `[c` are off-by-one for blank lines
* [#598](https://github.com/NeoVintageous/NeoVintageous/issues/598): Text object registers should be linewise
* [#597](https://github.com/NeoVintageous/NeoVintageous/issues/597): `di(` and other text objects ignore indention
* [#591](https://github.com/NeoVintageous/NeoVintageous/issues/591): `?` (search forward) in visual modes is inconsistent
* [#590](https://github.com/NeoVintageous/NeoVintageous/issues/590): `/` (search backward) in visual modes is inconsistent
* [#588](https://github.com/NeoVintageous/NeoVintageous/issues/588): Visual mode incremental search highlighting is inconsistent

## 1.16.6 - 2019-07-09

### Fixed

* [#618](https://github.com/NeoVintageous/NeoVintageous/issues/618): Character `,` (comma) not supported as string in ex command

## 1.16.5 - 2019-07-09

### Fixed

* [#616](https://github.com/NeoVintageous/NeoVintageous/issues/616): Can't use characters like : and # in ex commands

## 1.16.4 - 2019-07-03

### Fixed

* [#609](https://github.com/NeoVintageous/NeoVintageous/issues/609): `<C-e>` and `<C-y>` are not working in visual line mode
* [#610](https://github.com/NeoVintageous/NeoVintageous/issues/610): invalid malformed mapping

## 1.16.3 - 2019-06-18

### Fixed

* [#579](https://github.com/NeoVintageous/NeoVintageous/issues/579):  error `'A-j'` is not a known key
* [#587](https://github.com/NeoVintageous/NeoVintageous/issues/587): `:wall` should only save dirty views

## 1.16.2 - 2019-06-14

### Fixed

* [#583](https://github.com/NeoVintageous/NeoVintageous/issues/583): `:move` has inconsistent cursor behaviour
* [#584](https://github.com/NeoVintageous/NeoVintageous/issues/584): `:copy` to EOF adds too many newlines

## 1.16.1 - 2019-06-13

### Fixed

* [#581](https://github.com/NeoVintageous/NeoVintageous/issues/581): Pasting complete line is invading new line
* [#582](https://github.com/NeoVintageous/NeoVintageous/issues/582): `u` (undo) after `:sort u` command needs to be pressed twice to fully undo

## 1.16.0 - 2019-06-05

### Added

* [#48](https://github.com/NeoVintageous/NeoVintageous/issues/48): `gp` just like `p`, but leave the cursor just after the new text
* [#48](https://github.com/NeoVintageous/NeoVintageous/issues/48): `gP` just like `P`, but leave the cursor just after the new text
* [#339](https://github.com/NeoVintageous/NeoVintageous/issues/339): `[p` and `[P` like `P`, but adjust the indent to current line
* [#339](https://github.com/NeoVintageous/NeoVintageous/issues/339): `]p` and `]P` like `p`, but adjust the indent to current line
* [#578](https://github.com/NeoVintageous/NeoVintageous/issues/578): Support trailing sequences in command mappings
* [#577](https://github.com/NeoVintageous/NeoVintageous/issues/577): `<C-Down>` (alias of `j` and `<down>`) can now be mapped
* [#576](https://github.com/NeoVintageous/NeoVintageous/issues/576): `<C-Up>` (alias of `k` and `<up>`) can now be mapped
* [#574](https://github.com/NeoVintageous/NeoVintageous/issues/574): `J` go to last child (sidebar)
* [#574](https://github.com/NeoVintageous/NeoVintageous/issues/574): `p` go to parent (sidebar)
* [#574](https://github.com/NeoVintageous/NeoVintageous/issues/574): `p` go to root (sidebar)
* [#574](https://github.com/NeoVintageous/NeoVintageous/issues/574): `q` close (sidebar)
* [#575](https://github.com/NeoVintageous/NeoVintageous/issues/575): `x` delete characters under cursor in multi cursor mode

### Fixed

* [#93](https://github.com/NeoVintageous/NeoVintageous/issues/93): `p` is inconsistent
* [#93](https://github.com/NeoVintageous/NeoVintageous/issues/93): multi line paste works badly
* [#573](https://github.com/NeoVintageous/NeoVintageous/issues/573): `P` in visual line mode characterwise should preserve trailing newline
* [#572](https://github.com/NeoVintageous/NeoVintageous/issues/572): `P` in visual line mode should leave cursor at start of selection

## 1.15.1 - 2019-05-24

### Fixed

* [#440](https://github.com/NeoVintageous/NeoVintageous/issues/440): Use setting `'vintageous_clear_auto_indent_on_esc'` to preserve leading whitespace on `<Esc>`
* [#569](https://github.com/NeoVintageous/NeoVintageous/issues/569): Repeated object select in visual mode doesn't work consistently

## 1.15.0 - 2019-05-22

### Added

* [#277](https://github.com/NeoVintageous/NeoVintageous/issues/277): Configure Insert Mode by default
* [#49](https://github.com/NeoVintageous/NeoVintageous/issues/49): `<S-Tab>` in ex mode go to previous match auto-complete (alias of `<C-p>`)
* [#73](https://github.com/NeoVintageous/NeoVintageous/issues/73): `<PageUp>` scroll window `[count]` pages Backwards (upwards) (alias of `<C-b>`)
* [#73](https://github.com/NeoVintageous/NeoVintageous/issues/73): `<PageDown>` scroll window `[count]` pages Forwards (downwards) (alias of `<C-f>`)
* [#565](https://github.com/NeoVintageous/NeoVintageous/issues/565): `P` put multiple cursor text before the cursor
* [#222](https://github.com/NeoVintageous/NeoVintageous/issues/222): `P` put text before cursor in visual line mode
* [#552](https://github.com/NeoVintageous/NeoVintageous/issues/552): `y` yank selection in multiple cursor mode
* [#553](https://github.com/NeoVintageous/NeoVintageous/issues/553): `[count]P` put the text before the cursor `[count]` times
* [#559](https://github.com/NeoVintageous/NeoVintageous/issues/559): `i` text object selection in visual line mode e.g. `ip`, `iw`, `i'`
* [#562](https://github.com/NeoVintageous/NeoVintageous/issues/562): `a` text object selection in visual line mode e.g. `ap`, `aw`, `a'`
* [#560](https://github.com/NeoVintageous/NeoVintageous/issues/560): `i` text object selection in visual block mode e.g. `ip`, `iw`, `i'`
* [#561](https://github.com/NeoVintageous/NeoVintageous/issues/561): `a` text object selection in visual block mode e.g. `ap`, `aw`, `a'`
* [#563](https://github.com/NeoVintageous/NeoVintageous/issues/563): `ga` print the ASCII value in visual modes
* [#551](https://github.com/NeoVintageous/NeoVintageous/issues/551): `<C-h>` `[count]` characters to the left (alias of `h`, `<left>`, and `<BS>`)
* [#551](https://github.com/NeoVintageous/NeoVintageous/issues/551): `g<up>` display lines upward (alias of `gk`)
* [#551](https://github.com/NeoVintageous/NeoVintageous/issues/551): `g<down>` display lines downward (alias of `gj`)
* [#551](https://github.com/NeoVintageous/NeoVintageous/issues/551): `<tab>` go to newer cursor position in jump list (alias of `<C-i>`)

### Fixed

* [#567](https://github.com/NeoVintageous/NeoVintageous/issues/567): some `ctrl` keys are not controlled by `'vintageous_use_ctrl_keys'`
* [#554](https://github.com/NeoVintageous/NeoVintageous/issues/554): `dl` should not advance to first non-blank
* [#555](https://github.com/NeoVintageous/NeoVintageous/issues/555): `cl` should include trailing whitespace
* [#556](https://github.com/NeoVintageous/NeoVintageous/issues/556): `d$` on a blank line should not delete the line
* [#557](https://github.com/NeoVintageous/NeoVintageous/issues/557): `c$` should include whitespace
* [#558](https://github.com/NeoVintageous/NeoVintageous/issues/558): `d|` should not move to first non-blank
* [#528](https://github.com/NeoVintageous/NeoVintageous/issues/528): Command-line input has dark background in adaptive light theme

## 1.14.2 - 2019-05-16

### Fixed

* [#550](https://github.com/NeoVintageous/NeoVintageous/issues/550): backslash is converted to `<bslash>` when sent to command line by a mapping
* [#549](https://github.com/NeoVintageous/NeoVintageous/issues/549): Upward paragraph motion in visual mode not working

## 1.14.1 - 2019-05-14

### Fixed

* [#548](https://github.com/NeoVintageous/NeoVintageous/issues/548): Visual selection should not be cleared when Sublime loses focus
* [#547](https://github.com/NeoVintageous/NeoVintageous/issues/547): `vnoremap` doesn't work for super keys in visual mode

## 1.14.0 - 2019-05-14

### Added

* [#546](https://github.com/NeoVintageous/NeoVintageous/issues/546): Support for mapping `super+]`
* [#545](https://github.com/NeoVintageous/NeoVintageous/issues/545): Support for mapping `super+[`

## 1.13.0 - 2019-05-14

### Added

* [#534](https://github.com/NeoVintageous/NeoVintageous/issues/534): `gn` search forward for the last used search pattern
* [#535](https://github.com/NeoVintageous/NeoVintageous/issues/535): `gN` like `gn` but searches backward, like with `N`
* [#382](https://github.com/NeoVintageous/NeoVintageous/issues/382): `cgn` change `gn` search forward for the last used search pattern
* [#536](https://github.com/NeoVintageous/NeoVintageous/issues/536): `cgN` change `gN` like `gn` but searches backward, like with `N`
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): option `vintageous_multi_cursor_exit_from_visual_mode` (quit or enter normal mode)
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `<C-n>` and `gh` from Visual mode now includes the next match
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `<C-n>` start multiple cursor
* [#543](https://github.com/NeoVintageous/NeoVintageous/issues/543): `d` delete text in multiple cursor mode
* [#542](https://github.com/NeoVintageous/NeoVintageous/issues/542): `Esc` in Visual block mode now leaves cursor on first non-blank
* [#540](https://github.com/NeoVintageous/NeoVintageous/issues/540): `=` in Visual block mode
* [#541](https://github.com/NeoVintageous/NeoVintageous/issues/541): `<` in Visual block mode
* [#539](https://github.com/NeoVintageous/NeoVintageous/issues/539): `=` now leaves cursor on first non-blank
* [#538](https://github.com/NeoVintageous/NeoVintageous/issues/538): `>>` in multiple cursor mode
* [#537](https://github.com/NeoVintageous/NeoVintageous/issues/537): `==` in multiple cursor mode
* [#533](https://github.com/NeoVintageous/NeoVintageous/issues/533): `==` now leaves cursor on first non-blank

### Fixed

* [#544](https://github.com/NeoVintageous/NeoVintageous/issues/544): `I` command has been broken in the last update (regression)
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `i` in multiple cursor mode should clear visual selection

## 1.12.0 - 2019-05-09

### Added

* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `<C-n>` in multiple cursor mode (add next match)
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `<C-p>` in multiple cursor mode (remove current match)
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `<C-x>` in multiple cursor mode (skip next match)
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `c` in multiple cursor mode
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `I` in multiple cursor mode
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `s` in multiple cursor mode
* [#251](https://github.com/NeoVintageous/NeoVintageous/issues/251): `v` in multiple cursor mode (go to Normal mode)
* [#493](https://github.com/NeoVintageous/NeoVintageous/issues/493): `:sil[ent] {command}` command
* [#513](https://github.com/NeoVintageous/NeoVintageous/issues/513): `:g[lobal]/{pattern}/d[elete]` command
* [#518](https://github.com/NeoVintageous/NeoVintageous/issues/518): `:his[tory]` command
* [#519](https://github.com/NeoVintageous/NeoVintageous/issues/519): `:noh[lsearch]` command
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `[count]g_`
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `cge` change backward to the end of word `[count]`
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `cgE` change backward to the end of WORD `[count]`
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `dge` delete backward to the end of word `[count]`
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `dgE` delete backward to the end of WORD `[count]`
* [#512](https://github.com/NeoVintageous/NeoVintageous/issues/512): `v` in Visual block mode (converts to Visual mode)
* [#511](https://github.com/NeoVintageous/NeoVintageous/issues/511): `V` in Visual block mode (converts to Visual line mode)
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `$` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `0` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `^` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `_` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `b` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `B` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `e` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `E` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `g_` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `ge` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `gE` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `w` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `W` in Visual block mode
* [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): `|` in Visual block mode
* [#490](https://github.com/NeoVintageous/NeoVintageous/issues/490): `[(` in Visual line mode
* [#490](https://github.com/NeoVintageous/NeoVintageous/issues/490): `[{` in Visual line mode
* [#490](https://github.com/NeoVintageous/NeoVintageous/issues/490): `])` in Visual line mode
* [#490](https://github.com/NeoVintageous/NeoVintageous/issues/490): `]}` in Visual line mode
* [#491](https://github.com/NeoVintageous/NeoVintageous/issues/491): `$` in Visual line mode
* [#492](https://github.com/NeoVintageous/NeoVintageous/issues/492): `(` in Visual line mode
* [#492](https://github.com/NeoVintageous/NeoVintageous/issues/492): `)` in Visual line mode
* [#499](https://github.com/NeoVintageous/NeoVintageous/issues/499): `<CR>` in Visual line mode
* [#500](https://github.com/NeoVintageous/NeoVintageous/issues/500): `-` in Visual line mode
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `_` in Visual line mode
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `e` in Visual line mode
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `g_` in Visual line mode
* [#502](https://github.com/NeoVintageous/NeoVintageous/issues/502): Visual bells are now configurable including styles "view", "views", and "blink"
* [#502](https://github.com/NeoVintageous/NeoVintageous/issues/502): Visual bells color scheme is now configurable including "light" and "dark" schemes
* [#284](https://github.com/NeoVintageous/NeoVintageous/issues/284): Support `%` (current file name) in `!` shell commands

### Changed

* Changed [#531](https://github.com/NeoVintageous/NeoVintageous/issues/531): `q{a-zA-Z}` now records macros per window
* Changed [#516](https://github.com/NeoVintageous/NeoVintageous/issues/516): Search occurrences default style is now set to "fill"
* Changed [#510](https://github.com/NeoVintageous/NeoVintageous/issues/510): Visual block mode now works closer to the way Vim block mode works

### Fixed

* [#530](https://github.com/NeoVintageous/NeoVintageous/issues/530): `c` does not work with multiple selections
* [#526](https://github.com/NeoVintageous/NeoVintageous/issues/526): Status line should show current register when recording
* [#532](https://github.com/NeoVintageous/NeoVintageous/issues/532): Window commands don't execute in macros `@{a-z}`
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `_` inconsistencies in Visual mode
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `_` inconsistencies for c operator
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `_` inconsistencies for d operator
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `M` operations should be linewise
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `L` operations should be linewise
* [#527](https://github.com/NeoVintageous/NeoVintageous/issues/527): `H` operations should be linewise
* [#525](https://github.com/NeoVintageous/NeoVintageous/issues/525): `I` in reverse Visual mode should enter Insert mode at start of line
* [#524](https://github.com/NeoVintageous/NeoVintageous/issues/524): `g_` should not include trailing white-space
* [#523](https://github.com/NeoVintageous/NeoVintageous/issues/523): `g_` in Visual mode is off-by-one
* [#522](https://github.com/NeoVintageous/NeoVintageous/issues/522): `B` in Visual mode is off-by-one
* [#521](https://github.com/NeoVintageous/NeoVintageous/issues/521): `[count]d|` off-by-one
* [#453](https://github.com/NeoVintageous/NeoVintageous/issues/453): `:%g/^$/d` doesn't work
* [#520](https://github.com/NeoVintageous/NeoVintageous/issues/520): Entering Visual block from Visual doesn't update status line
* [#517](https://github.com/NeoVintageous/NeoVintageous/issues/517): `gq` in reverse Visual line mode includes too many lines
* [#515](https://github.com/NeoVintageous/NeoVintageous/issues/515): `0` in Visual mode off-by-one
* [#18](https://github.com/NeoVintageous/NeoVintageous/issues/18): Visual block do no span across empty lines
* [#509](https://github.com/NeoVintageous/NeoVintageous/issues/509): `:global` should allow various separators and disallow others
* [#506](https://github.com/NeoVintageous/NeoVintageous/issues/506): `gqip` should leave cursor on first non blank
* [#505](https://github.com/NeoVintageous/NeoVintageous/issues/505): `dE` should only delete to end of big word
* [#504](https://github.com/NeoVintageous/NeoVintageous/issues/504): `e` in Visual mode doesn't work
* [#508](https://github.com/NeoVintageous/NeoVintageous/issues/508): `zH`, `zL`, `zM`, `zR`, and some other `z{a-z}` commands don't work
* [#234](https://github.com/NeoVintageous/NeoVintageous/issues/234): `<C-e>` and `<C-y>` in Normal mode cursor in wrapped lines
* [#498](https://github.com/NeoVintageous/NeoVintageous/issues/498): `<CR>` in Visual mode should include first character of line
* [#497](https://github.com/NeoVintageous/NeoVintageous/issues/497): `d(` should include first character of paragraph
* [#496](https://github.com/NeoVintageous/NeoVintageous/issues/496): `(` in Visual mode is inconsistent
* [#495](https://github.com/NeoVintageous/NeoVintageous/issues/495): `#` in Visual mode doesn't work after first jump
* [#494](https://github.com/NeoVintageous/NeoVintageous/issues/494): `*` in Visual line mode should include first character of match

## 1.11.3 - 2019-04-04

### Fixed

* [#501](https://github.com/NeoVintageous/NeoVintageous/issues/501): Default `mapleader` does not appear to be working
* [#489](https://github.com/NeoVintageous/NeoVintageous/issues/489): `gg` in Visual mode is inconsistent

## 1.11.2 - 2019-04-02

### Fixed

* [#488](https://github.com/NeoVintageous/NeoVintageous/issues/488): `gx` doesn't work on some markdown links
* [#487](https://github.com/NeoVintageous/NeoVintageous/issues/487): `{` in Visual mode is off-by-one
* [#486](https://github.com/NeoVintageous/NeoVintageous/issues/486): `}` in Visual mode is off-by-one
* [#485](https://github.com/NeoVintageous/NeoVintageous/issues/485): `'{a-z}` should jump to the first non-blank character in the line
* [#484](https://github.com/NeoVintageous/NeoVintageous/issues/484): `]}` in Visual mode is off-by-one
* [#483](https://github.com/NeoVintageous/NeoVintageous/issues/483): `'{a-z}` in Visual mode is inconsistent
* [#482](https://github.com/NeoVintageous/NeoVintageous/issues/482): `|` at start of line moves to previous line

## 1.11.1 - 2019-03-27

### Fixed

* [#481](https://github.com/NeoVintageous/NeoVintageous/issues/481): `M` in Visual mode is inconsistent
* [#480](https://github.com/NeoVintageous/NeoVintageous/issues/480): `L` in Visual mode is inconsistent
* [#479](https://github.com/NeoVintageous/NeoVintageous/issues/479): `H` in Visual mode is inconsistent
* [#478](https://github.com/NeoVintageous/NeoVintageous/issues/478): `:sort` should scroll cursor into view

## 1.11.0 - 2019-03-26

### Added

* [#379](https://github.com/NeoVintageous/NeoVintageous/issues/379): `[{` and `]}` VISUAL mode
* [#379](https://github.com/NeoVintageous/NeoVintageous/issues/379): `[(` and `])` VISUAL mode
* [#434](https://github.com/NeoVintageous/NeoVintageous/issues/434): Support mapping digits e.g. `<leader>0`
* [#196](https://github.com/NeoVintageous/NeoVintageous/issues/196): `z.` Redraw, line at center of window and put cursor at first non-blank
* [#454](https://github.com/NeoVintageous/NeoVintageous/issues/454): Support advanced ex command mapping
* [#99](https://github.com/NeoVintageous/NeoVintageous/issues/99): Support marks in line ranges
* [#464](https://github.com/NeoVintageous/NeoVintageous/issues/464): Support `:[sp]lit [file]` completions
* [#265](https://github.com/NeoVintageous/NeoVintageous/issues/265): Support `<S-Space>` (shift+space) key
* [#433](https://github.com/NeoVintageous/NeoVintageous/issues/433): Support case-insensitive key mappings
* [#460](https://github.com/NeoVintageous/NeoVintageous/issues/460): Add toggle SUPER keys (enable/disable) command
* [#459](https://github.com/NeoVintageous/NeoVintageous/issues/459): Add toggle CTRL keys (enable/disable) command

### Deprecated

* [#475](https://github.com/NeoVintageous/NeoVintageous/issues/475): `neovintageous_toggle_side_bar ` command; use the `neovintageous {'action': 'toggle_side_bar'}` instead
* [#475](https://github.com/NeoVintageous/NeoVintageous/issues/475): `neovintageous_reload_my_rc_file` command; use the `neovintageous {'action': 'reload_rc_file'}` instead
* [#475](https://github.com/NeoVintageous/NeoVintageous/issues/475): `neovintageous_open_my_rc_file` command; use the `neovintageous {'action': 'open_rc_file'}` instead

### Fixed

* [#477](https://github.com/NeoVintageous/NeoVintageous/issues/477): `}` VISUAL line off-by-one
* [#476](https://github.com/NeoVintageous/NeoVintageous/issues/476): `de` should delete leading whitespace
* [#134](https://github.com/NeoVintageous/NeoVintageous/issues/134): `(` and `)` not jumping correctly
* [#364](https://github.com/NeoVintageous/NeoVintageous/issues/364): Loss of clipboard copy and paste functionality in insert mode
* [#98](https://github.com/NeoVintageous/NeoVintageous/issues/98): Unable to map double quotes
* [#474](https://github.com/NeoVintageous/NeoVintageous/issues/474): `]}`, `])`, `[{`, and `[(` are inconsistent in NORMAL mode
* [#473](https://github.com/NeoVintageous/NeoVintageous/issues/473): `gq` on reverse selection is off-by-one
* [#469](https://github.com/NeoVintageous/NeoVintageous/issues/469): Unable to set mapleader to `<Space>`
* [#468](https://github.com/NeoVintageous/NeoVintageous/issues/468): `d{backtick}{a-z}` should work the same as `d{singlequote}{a-z}`
* [#467](https://github.com/NeoVintageous/NeoVintageous/issues/467): VISUAL mode operator pending command should stay in VISUAL mode
* [#465](https://github.com/NeoVintageous/NeoVintageous/issues/465): Repeating (`.`) when nothing to repeat, should invoke bell
* [#223](https://github.com/NeoVintageous/NeoVintageous/issues/223): Search does not work when cursor is on the word that is being searched
* [#466](https://github.com/NeoVintageous/NeoVintageous/issues/466): x, y, and z registers
* [#462](https://github.com/NeoVintageous/NeoVintageous/issues/462): `[count]G` and `[count]gg` EOF off-by-one
* [#458](https://github.com/NeoVintageous/NeoVintageous/issues/458): `d}` at EOL causes visual bell

## 1.10.0 - 2019-03-05

### Added

* [#448](https://github.com/NeoVintageous/NeoVintageous/issues/448): User command mappings should allow float arguments e.g. `nnoremap <leader>. :ToggleZoomPane fraction=0.98<CR>`
* [#445](https://github.com/NeoVintageous/NeoVintageous/issues/445): `:sort [i][u]` sort lines with case-insensitive and unique options
* [#71](https://github.com/NeoVintageous/NeoVintageous/issues/71): `gf` edit the file under cursor (mnemonic: "goto file")
* [#31](https://github.com/NeoVintageous/NeoVintageous/issues/31): `zl`, `zL`, `zh`, `zH` scroll horizontally
* [#442](https://github.com/NeoVintageous/NeoVintageous/issues/442): `:s/{search}/{replacement}/c` can now be cancelled

### Removed

* Removed [#441](https://github.com/NeoVintageous/NeoVintageous/issues/441): Non-standard `:cdd` command (use `:cd %:h` instead)

### Fixed

* [#452](https://github.com/NeoVintageous/NeoVintageous/issues/452): Jump to diff commands, `]c` and `[c`, gets stuck on lines with multiple changes
* [#451](https://github.com/NeoVintageous/NeoVintageous/issues/451): `{Visual}e` in reverse selection should move to end of word
* [#450](https://github.com/NeoVintageous/NeoVintageous/issues/450): `k` in SELECT mode should enter NORMAL mode if last selection
* [#449](https://github.com/NeoVintageous/NeoVintageous/issues/449): `v_W` causes error when end of selection is at BOF
* [#447](https://github.com/NeoVintageous/NeoVintageous/issues/447): `:h ctrl-w_o` should open help for `CTRL-W_o`
* [#446](https://github.com/NeoVintageous/NeoVintageous/issues/446): Many ex commands incorrectly accept an invalid trailing character
* [#443](https://github.com/NeoVintageous/NeoVintageous/issues/443): `:cd %:h` displays incorrect status message
* [#20](https://github.com/NeoVintageous/NeoVintageous/issues/20): `:e#` edits literal file
* [#444](https://github.com/NeoVintageous/NeoVintageous/issues/444): `vi[` and `vi]` should not select empty target line

## 1.9.0 - 2019-02-21

### Added

* [#437](https://github.com/NeoVintageous/NeoVintageous/issues/437): Builtin support for jump to diff `]c` and `[c` in `>=3189` (GitGutter is required for older versions)
* [#430](https://github.com/NeoVintageous/NeoVintageous/issues/430): Folding commands `zc`, `zo`, `zM`, and `zR`
* [#432](https://github.com/NeoVintageous/NeoVintageous/issues/432): `cs{target}{replacement}` target aliases `b`, `B`, `r`, and `a`
* [#431](https://github.com/NeoVintageous/NeoVintageous/issues/431): `ys{motion}{replacement}` replacement aliases `b`, `B`, `r`, and `a`
* [#418](https://github.com/NeoVintageous/NeoVintageous/issues/418): Surround Line `yss{replacement}`
* [#429](https://github.com/NeoVintageous/NeoVintageous/issues/429): Support `<bslash>` in vintageousrc
* [#428](https://github.com/NeoVintageous/NeoVintageous/issues/428): Support `<bar>` in vintageousrc
* [#424](https://github.com/NeoVintageous/NeoVintageous/issues/424): `[count]o` and `[count]O`

### Fixed

* [#439](https://github.com/NeoVintageous/NeoVintageous/issues/439): Repeat last `:substitute` doesn't work
* [#438](https://github.com/NeoVintageous/NeoVintageous/issues/438): `{Visual}[count]G` and `{Visual}[count]gg` should extend to first non blank
* [#366](https://github.com/NeoVintageous/NeoVintageous/issues/366): Folding with `zc` enters VISUAL mode
* [#380](https://github.com/NeoVintageous/NeoVintageous/issues/380): `<Esc>` directly after `O` or `o` should erase leading whitespace
* [#247](https://github.com/NeoVintageous/NeoVintageous/issues/247): Unable to map `<C-w>>` in vintageousrc
* [#427](https://github.com/NeoVintageous/NeoVintageous/issues/427): `{Visual}gv` should select previous selection
* [#423](https://github.com/NeoVintageous/NeoVintageous/issues/423): `:w` cannot find file and save, but `:Save` and `<Ctrl-s>` work
* [#425](https://github.com/NeoVintageous/NeoVintageous/issues/425): Reloading vintageousrc should unload existing mappings
* [#422](https://github.com/NeoVintageous/NeoVintageous/issues/422): `{Visual}y` should highlight the selection (HighlightedYank)

## 1.8.0 - 2019-01-23

### Added

* [#242](https://github.com/NeoVintageous/NeoVintageous/issues/242): `CTRL-d` and `CTRL-u` should keep horizontal position when scrolling

### Changed

* Setting `vintageous_visualbell`; use `vintageous_belloff` set to `all` to disable visual bells

### Fixed

* [#421](https://github.com/NeoVintageous/NeoVintageous/issues/421):  Direct shell command exec in project
* [#416](https://github.com/NeoVintageous/NeoVintageous/issues/416): `H` and `L` should move to highest/lowest line without scrolling (UX)
* [#417](https://github.com/NeoVintageous/NeoVintageous/issues/417): `CTRL-d` and `CTRL-u` count should be used as the number of lines to scroll
* [#362](https://github.com/NeoVintageous/NeoVintageous/issues/362):  `SHIFT+H` `SHIFT+M` `SHIFT+L` in VISUAL LINE mode does not work
* [#413](https://github.com/NeoVintageous/NeoVintageous/issues/413): `CTRL-d` and `CTRL-u` should put cursor on first non blank
* [#414](https://github.com/NeoVintageous/NeoVintageous/issues/414): `H`, `M`, and `L`, should put cursor on first non blank
* [#415](https://github.com/NeoVintageous/NeoVintageous/issues/415): `CTRL-d` and `CTRL-u` VISUAL mode bugs
* [#363](https://github.com/NeoVintageous/NeoVintageous/issues/363): Searching for regex characters like `(` and `[` doesn't work
* [#420](https://github.com/NeoVintageous/NeoVintageous/issues/420): `:help {subject}` should scroll subject into view
* [#410](https://github.com/NeoVintageous/NeoVintageous/issues/410): `J` should strip leading comment tokens from joined lines enhancement
* [#412](https://github.com/NeoVintageous/NeoVintageous/issues/412): `j` and `k` VISUAL in mode causes window to scroll two lines when next line is empty (UX)
* [#411](https://github.com/NeoVintageous/NeoVintageous/issues/411): `j` and `k` in VISUAL mode causes a jump to other end of visual selection (UX)

## 1.7.5 - 2019-01-17

### Fixed

* [#406](https://github.com/NeoVintageous/NeoVintageous/issues/406): `V_d` should put cursor on first non blank
* [#407](https://github.com/NeoVintageous/NeoVintageous/issues/407): `yi{motion}` should put cursor on first non blank at start of motion
* [#403](https://github.com/NeoVintageous/NeoVintageous/issues/403): `yi(` and other block-like motions should create linewise registers
* [#409](https://github.com/NeoVintageous/NeoVintageous/issues/409): `ga` doesn't work properly when cursor is on a NEWLINE, or TAB, or at EOF
* [#405](https://github.com/NeoVintageous/NeoVintageous/issues/405): `v_J` should enter NORMAL mode

## 1.7.4 - 2019-01-10

### Fixed

* [#402](https://github.com/NeoVintageous/NeoVintageous/issues/402): `>G` should not include line above cursor
* [#401](https://github.com/NeoVintageous/NeoVintageous/issues/401): `gcG` should not include line above cursor
* [#400](https://github.com/NeoVintageous/NeoVintageous/issues/400): `@@` no longer works (regression)
* [#399](https://github.com/NeoVintageous/NeoVintageous/issues/399): `>` VISUAL BLOCK indent should put cursor on first non blank
* [#398](https://github.com/NeoVintageous/NeoVintageous/issues/398): `gUU` should put cursor on first non blank
* [#397](https://github.com/NeoVintageous/NeoVintageous/issues/397): `v_g~` should put cursor at start of selection
* [#394](https://github.com/NeoVintageous/NeoVintageous/issues/394): `V` at EOF causes error bell
* [#396](https://github.com/NeoVintageous/NeoVintageous/issues/396): `gg` should move to first non blank character
* [#395](https://github.com/NeoVintageous/NeoVintageous/issues/395): `G` should move to first non blank character
* [#395](https://github.com/NeoVintageous/NeoVintageous/issues/395): `G` should reset xpos to 0
* [#393](https://github.com/NeoVintageous/NeoVintageous/issues/393): `v_gg` should reset xpos to 0

## 1.7.3 - 2019-01-09

### Fixed

* Lots of yank, paste, register issues
* [#292](https://github.com/NeoVintageous/NeoVintageous/issues/292): Visual mode block insert and append partially working
* [#358](https://github.com/NeoVintageous/NeoVintageous/issues/358): `Y` should copy all complete lines touched by the VISUAL selection
* [#392](https://github.com/NeoVintageous/NeoVintageous/issues/392): `V_gg` start and end cursor is backwards
* [#224](https://github.com/NeoVintageous/NeoVintageous/issues/224): `P` Pasting text ending with newline pastes to wrong line
* [#2](https://github.com/NeoVintageous/NeoVintageous/issues/2): `YP` not working correctly
* [#391](https://github.com/NeoVintageous/NeoVintageous/issues/391): `c{motion}` should fill the numbered registers
* [#390](https://github.com/NeoVintageous/NeoVintageous/issues/390): `cc` should fill the numbered registers
* [#389](https://github.com/NeoVintageous/NeoVintageous/issues/389): `dd` on last line leaves cursor at EOF

## 1.7.2 - 2019-01-04

### Fixed

* [#23](https://github.com/NeoVintageous/NeoVintageous/issues/23): `:set autoindent`
* [#35](https://github.com/NeoVintageous/NeoVintageous/issues/35): `:set ic` and `:set noic` has no effect
* [#368](https://github.com/NeoVintageous/NeoVintageous/issues/368): Disabling `vintageous_hlsearch` appears to have no effect
* [#388](https://github.com/NeoVintageous/NeoVintageous/issues/388): Executing register while recording causes recursion error
* [#94](https://github.com/NeoVintageous/NeoVintageous/issues/94): Executing a register with a count, `[count]@q{register}` doesn't work

## 1.7.1 - 2018-12-24

### Fixed

* [#377](https://github.com/NeoVintageous/NeoVintageous/issues/377): Add backtick mark jumps to jumplist

## 1.7.0 - 2018-09-02

### Added

* [#360](https://github.com/NeoVintageous/NeoVintageous/issues/360): Add search highlighting configuration; see `:h nv-search-highlighting`
* [#359](https://github.com/NeoVintageous/NeoVintageous/issues/359): Add HighlightedYank plugin; see `:h highlightedyank`

### Changed

* Renamed scope `nv_search_inc` to `neovintageous_search_inc`
* Renamed scope `nv_search_cur` to `neovintageous_search_cur`
* Renamed scope `nv_search_occ` to `neovintageous_search_occ`

### Removed

* `vintageous_visualyank` setting, use the new HighlightedYank plugin instead; see `:h highlightedyank`
* `highlighted.yank` scope, use the new HighlightedYank plugin instead; see `:h highlightedyank`

### Fixed

* [#367](https://github.com/NeoVintageous/NeoVintageous/issues/367): `gx` doesn't work for urls containing dashes

## 1.6.3 - 2018-05-31

### Fixed

* [#340](https://github.com/NeoVintageous/NeoVintageous/issues/340): `[{`, `[(`, `]}`, and `])` don't work
* [#260](https://github.com/NeoVintageous/NeoVintageous/issues/260): Black hole register `"_` doesn't work for some commands
* [#199](https://github.com/NeoVintageous/NeoVintageous/issues/199): `D` does not behave correctly in VISUAL mode

## 1.6.2 - 2018-05-23

### Fixed

* [#47](https://github.com/NeoVintageous/NeoVintageous/issues/47): Inserts text behind cursor when plugin is accessed via the command palette
* [#355](https://github.com/NeoVintageous/NeoVintageous/issues/355): Fix a typo in the name of a Wrap Plus setting used to detect it
* [#291](https://github.com/NeoVintageous/NeoVintageous/issues/291): Append multi line is off by one char

## 1.6.1 - 2018-05-20

### Fixed

* [#64](https://github.com/NeoVintageous/NeoVintageous/issues/64): `0` selects incorrect regions in visual mode

## 1.6.0 - 2018-05-19

### Added

* [#353](https://github.com/NeoVintageous/NeoVintageous/issues/353): Color scheme support for current match highlighting in `/`, `?`, `*`, and `#`
* [#312](https://github.com/NeoVintageous/NeoVintageous/issues/312): Map commands with arguments e.g. `nnoremap ,f :ShowOverlay overlay=goto text=@<CR>`
* [#345](https://github.com/NeoVintageous/NeoVintageous/issues/345): Map commands without executing immediately (no trailing `<CR>`) e.g `nnoremap ,r :reg`
* [#346](https://github.com/NeoVintageous/NeoVintageous/issues/346): Map commands with ranges and counts
* [#344](https://github.com/NeoVintageous/NeoVintageous/issues/344): Add buffer commands `:bf[irst]`, `:br[ewind]`, `:bp[revious]`, `:bN[ex]t`, `:bn[ext]`, and `:bl[ast]`
* [#343](https://github.com/NeoVintageous/NeoVintageous/issues/343): Add Unimpaired commands `[b`, `]b`, `[B`, `]B`, `]t`, `[t`, `]T`, and `[T`
* [#327](https://github.com/NeoVintageous/NeoVintageous/issues/327): Redo command (`<C-r>`) should invoke a UI bell if there are no more redo commands
* [#70](https://github.com/NeoVintageous/NeoVintageous/issues/70): Add show whitespace command `:set list`
* [#334](https://github.com/NeoVintageous/NeoVintageous/issues/334): Add tab command `:tabN[ext]`
* [#330](https://github.com/NeoVintageous/NeoVintageous/issues/330): Add tab command `:tabc[lose]`

### Fixed

* [#173](https://github.com/NeoVintageous/NeoVintageous/issues/173): `vi{` selects extra blank chars
* [#161](https://github.com/NeoVintageous/NeoVintageous/issues/161): `vit` `vat` work incorrect inside self closing tags
* [#180](https://github.com/NeoVintageous/NeoVintageous/issues/180): `%` doesn't work in VISUAL LINE mode
* [#354](https://github.com/NeoVintageous/NeoVintageous/issues/354): `:help ctrl-w` opens wrong help file section
* [#352](https://github.com/NeoVintageous/NeoVintageous/issues/352): `%` should jump to the next item in this line after the cursor
* [#263](https://github.com/NeoVintageous/NeoVintageous/issues/263): `x` should not delete empty lines
* [#350](https://github.com/NeoVintageous/NeoVintageous/issues/350): Multi-select `k` doesn't work with a count
* [#314](https://github.com/NeoVintageous/NeoVintageous/issues/314): `gj` and `gk` do not work in visual line mode
* [#341](https://github.com/NeoVintageous/NeoVintageous/issues/341): Multi-select should scroll viewport to end of selection
* [#273](https://github.com/NeoVintageous/NeoVintageous/issues/273): Sort Lines command sorts whole file
* [#338](https://github.com/NeoVintageous/NeoVintageous/issues/338): `gv` after visual line should be linewise
* [#349](https://github.com/NeoVintageous/NeoVintageous/issues/349): `>` and `<` should leave cursor on first non whitespace character
* [#348](https://github.com/NeoVintageous/NeoVintageous/issues/348): `gv` doesn't remember which visual mode was last used
* [#347](https://github.com/NeoVintageous/NeoVintageous/issues/347): `gv` doesn't work in visual mode
* [#336](https://github.com/NeoVintageous/NeoVintageous/issues/336): `*` and `#` should center match on screen if not visible
* [#328](https://github.com/NeoVintageous/NeoVintageous/issues/328): Entering normal mode should not put cursor on EOL character
* [#324](https://github.com/NeoVintageous/NeoVintageous/issues/324): Entering Normal mode from Visual Block mode creates multiple selection
* [#329](https://github.com/NeoVintageous/NeoVintageous/issues/329): Redo command should not leave cursor on EOL character
* [#209](https://github.com/NeoVintageous/NeoVintageous/issues/209): Jumping to mark in visual mode does not work
* [#335](https://github.com/NeoVintageous/NeoVintageous/issues/335): Help subjects should be case sensitive e.g. `help L` should open help for L not l
* [#333](https://github.com/NeoVintageous/NeoVintageous/issues/333): `:ou` (`:ounmap` alias) doesn't work
* [#332](https://github.com/NeoVintageous/NeoVintageous/issues/332): `:no` (`:noremap` alias) doesn't work
* [#331](https://github.com/NeoVintageous/NeoVintageous/issues/331): `:files` doesn't work
* [#325](https://github.com/NeoVintageous/NeoVintageous/issues/325): `:sunmap` doesn't work, prints message E492: Not an editor command
* [#324](https://github.com/NeoVintageous/NeoVintageous/issues/324): Entering Normal mode from Visual Block mode creates multiple selection
* [#323](https://github.com/NeoVintageous/NeoVintageous/issues/323): `:g!/222/p` is bailing out with error: 'str' object has no attribute 'consume'
* [#153](https://github.com/NeoVintageous/NeoVintageous/issues/153): Cursor gets stuck after a few edit operations
* [#322](https://github.com/NeoVintageous/NeoVintageous/issues/322): `:print` doesn't work
* [#320](https://github.com/NeoVintageous/NeoVintageous/issues/320): `:move`  `KeyError: 'next_sel'` when address is the same as current line
* [#321](https://github.com/NeoVintageous/NeoVintageous/issues/321): Entering cmdline-mode from Visual Block mode doesn't work
* [#319](https://github.com/NeoVintageous/NeoVintageous/issues/319): `:cd` should change the current directory to the home directory
* [#150](https://github.com/NeoVintageous/NeoVintageous/issues/150): Remove lines with regular expression
* [#148](https://github.com/NeoVintageous/NeoVintageous/issues/148): `:$` does not go to last line
* [#87](https://github.com/NeoVintageous/NeoVintageous/issues/87): Double front slash doesn't escape properly

### Deprecated

* SublimeLinter APIs

## 1.5.3 - 2018-03-24

### Fixed

* [#36](https://github.com/NeoVintageous/NeoVintageous/issues/36) `*` and `#` jump history doesn't work
* [#51](https://github.com/NeoVintageous/NeoVintageous/issues/51): Can't map umlauts
* [#144](https://github.com/NeoVintageous/NeoVintageous/issues/144): Can't repeat macros
* [#170](https://github.com/NeoVintageous/NeoVintageous/issues/170): `<` text object not finding the opening bracket correctly

## 1.5.2 - 2018-03-03

### Fixed

* `:registers` should display `^J` to indicate newlines
* `:registers` should truncate long lines
* Add missing delete surround punctuation marks `;:@#~*\\/` e.g. `ds@`, `ds*`, etc.
* [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cst<{tagname}>`
* [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cstt{tagname}>` ("t" an alias for "<")
* [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cst{replacement}`
* [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cs{target}<{tagname}>`
* [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cs{target}t{tagname}>` ("t" is alias for "<")
* [#136](https://github.com/NeoVintageous/NeoVintageous/issues/136): Saving to named register with `D` doesn't work
* [#306](https://github.com/NeoVintageous/NeoVintageous/issues/306): Triple-clicking doesn't select a line

## 1.5.1 - 2018-02-20

### Fixed

* [#305](https://github.com/NeoVintageous/NeoVintageous/issues/305): Surround multiple selections leave cursor in wrong position
* Edge-case infinite loop when special key is set with no default value
* [#304](https://github.com/NeoVintageous/NeoVintageous/issues/304): `:s/$/foo/gc` causes infinite loop
* [#210](https://github.com/NeoVintageous/NeoVintageous/issues/210): `:%s/$/,/` not working as expected
* `:shell` error

## 1.5.0 - 2018-02-06

### Added

* `:edit {file}` command
* [#288](https://github.com/NeoVintageous/NeoVintageous/issues/288): Command-line editing commands: `<C-b>`, `<C-e>`, `<C-h>`, `<C-n>`, `<C-p>`, `<C-u>`, and `<C-w>`
* [#279](https://github.com/NeoVintageous/NeoVintageous/issues/279): `CTRL-c` and `CTRL-[` should exit Command-line mode
* [#12](https://github.com/NeoVintageous/NeoVintageous/issues/12): Command-line search history with `/` and `?` (current session only)
* Selections are now cleared when leaving a the current view (UX)
* `NeovintageousToggleSideBar` command
* [#286](https://github.com/NeoVintageous/NeoVintageous/issues/286): Support for super-keys `<D-...>` (known as command-keys on OSX, and window-keys on Windows) (disabled by default)
* `highlighted.yank` scope to highlighted yank regions to allow color scheme customisation
* Switching windows using windowing commands no longer suddenly scrolls view (UX)
* `:sunm[ap]` command
* `:help {subject}` command now uses basic heuristics to find a relevant help topic if a subject is not found
* Support for `'vintageous_modelines'` option (defaults to `5`)
* [#254](https://github.com/NeoVintageous/NeoVintageous/issues/254): `:sp[lit] [file]` command
* Unimpaired status bar toggle `coe` (also toggle on `[oe`, and toggle off `]oe`)
* Unimpaired menu toggle `coa` (also toggle on `[oa`, and toggle off `]oa`)
* Support for the new SublimeLinter API using the Unimpaired goto to error commands `]l` and `[l`
* Support for the new GitGutter API using the Unimpaired goto change commands `]c` and `[c`
* `vintageousrc` (documentation)
* Default vim options (documentation)

### Removed

* Recursive mappings commands `:map`, `:nmap`, `:omap`, `:smap`, `:vmap`. Use the non recursive commands instead.

  The recursive mappings were removed because they were not implemented as recursive mappings, and removing them now in preference of the non-recursive may prevent some potential problems in the future if the recursive mapping commands are ever implemented.

  Here is a table of the recursive, which have been removed, and the non recursive mapping commands that you can use instead:

  Recursive command | Non recursive command
  ----------------- | ---------------------
  `map` | `noremap`
  `nmap` | `nnoremap`
  `omap` | `onoremap`
  `smap` | `snoremap`
  `vmap` | `vnoremap`

* Unused `vintageous_enable_cmdline_mode` setting

### Fixed

* Visual ex mode commands should enter normal mode after operation
* Ex mode shell command error (Windows)
* Unmap commands don't unmap visual mappings
* Can't unmap mappings with special keys e.g. `<leader>`
* Running tests shouldn't resets user vintageousrc mappings
* [#156](https://github.com/NeoVintageous/NeoVintageous/issues/156): `SHIFT-v` then `CTRL-b` doesn't work
* Help views should be read only
* Unknown registers raise an exception
* `gc{motion}` leaves cursor at wrong place
* `gcc` leaves cursor at wrong place
* Repeat searches (`n`/`N`) should scroll and show surrounds
* Goto next/prev change cursor position after motion (Unimpaired)
* [#285](https://github.com/NeoVintageous/NeoVintageous/issues/285): Page down `CTRL-f` does not work correctly in Visual Line mode
* [#296](https://github.com/NeoVintageous/NeoVintageous/issues/296): `de` leaves cursor at wrong place
* [#295](https://github.com/NeoVintageous/NeoVintageous/issues/295): `df{char}` leaves cursor at wrong place
* `df$` leaves cursor at wrong place
* `gq` cursor position after operation
* Mapping command status messages
* Error message typos and grammar
* [#254](https://github.com/NeoVintageous/NeoVintageous/issues/254): `:vs[plit] [file]` raises a TypeError

## 1.4.4 - 2018-01-07

### Fixed

* Error trying to Open My Rc File first time
* Help files shouldn't display rulers or indent guides
* `CTRL-a` and `CTRL-x` doesn't work in column one or between lines
* Update to latest vimdocs
* `:map` doesn't work in visual block or visual line mode
* Remove unused setting
* Settings should be erased when cleaning up views
* `gx` in quoted urls
* `gg` and `G` jump history forwards `CTRL-i` and backwards `CTRL-o`
* [#298](https://github.com/NeoVintageous/NeoVintageous/issues/298): `gd` can't jump back with `CTRL-o`
* [#241](https://github.com/NeoVintageous/NeoVintageous/issues/241): Leaving Insert mode still shows as being in Insert mode
* [#129](https://github.com/NeoVintageous/NeoVintageous/issues/129): Failing tests when ST hasn't got focus

## 1.4.3 - 2017-12-22

### Fixed

* [#297](https://github.com/NeoVintageous/NeoVintageous/issues/297): An occurred trying load NeoVintageous

## 1.4.2 - 2017-12-19

### Fixed

* [#238](https://github.com/NeoVintageous/NeoVintageous/issues/238): Simply search & replace not working for me
* [#111](https://github.com/NeoVintageous/NeoVintageous/issues/111): Bad command
* "Traling characters" Status message typo
* `:s[ubstitute]` No previous substitute error message is incorrect
* [#226](https://github.com/NeoVintageous/NeoVintageous/issues/226): Mouse does not reset cursor column
* `C-w _` (set current group height as high as possible) doesn't always work correctly
* `C-w |` (set current group width as wide as possible) doesn't always work correctly
* `C-w =` (resize all groups equally) doesn't always work correctly
* `gJ`
* `gx` should ignore trailing full stops
* `gx` doesn't work on markdown links
* `vintageousrc` mapping should not accept unescaped pipe characters
* Help syntax fixes
* Unimpaired toggles (documentation)

## 1.4.1 - 2017-11-09

### Fixed

* [#245](https://github.com/NeoVintageous/NeoVintageous/issues/245): `ZZ` and `ZQ` are broken again
* [#290](https://github.com/NeoVintageous/NeoVintageous/issues/290): Commands that start with underscore should not be mappable
* [#289](https://github.com/NeoVintageous/NeoVintageous/issues/289): `:help {subject}` should goto `:{subject}` if `{subject}` not found

## 1.4.0 - 2017-11-06

### Added

* `ds(`, `ds{`, `ds[`, and `ds<` now also trims contained whitespace (Surround plugin)
* `dsb` alias for `ds)` delete surrounding `()` (Surround plugin)
* `dsB` alias for `ds}` delete surrounding `{}` (Surround plugin)
* `dsr` alias for `ds]` delete surrounding `[]` (Surround plugin)
* `dsa` alias for `ds>` delete surrounding `<>` (Surround plugin)
* `ds<` delete surrounding `<>` (Surround plugin)
* `ds>` delete surrounding `<>` (Surround plugin)
* `dst` delete surrounding pair of HTML or XML tags (Surround plugin)
* `ds` followed by a target that is not one of the punctuation pairs, `()[]{}<>`, are now only searched for on the current line (Surround plugin)
* `ds{target}` cursor position is now moves to the start of first target (Surround plugin)
* `cs{target}` followed by one of `])}` now inserts an inner whitespace character (Surround plugin)
* `cs>{replacement}` now replaces surround tag characters `<>` with replacement (Surround plugin)
* `cs{target}` folowed by `>` now replaces target with replacement surroundings `<>` (Surround plugin)
* `cs{target}{replacement}` cursor position is now moves to the start of first target (Surround plugin)
* `:h[elp] {subject}` like ":help", additionally jump to the tag `{subject}`
* `:h[elp]` open a view and display the help file
* `gx` open url under cursor in browser
* Support for `:UserCommand<CR>` `.vintageousrc` mappings
* Support for `:excommand<CR>` `.vintageousrc` mappings
* `:snoremap` command
* `:smap` command
* `cot` toggle sidebar command (Unimpaired plugin)
* `[ot` toggle sidebar on command (Unimpaired plugin)
* `]ot` toggle sidebar off command (Unimpaired plugin)
* `com` toggle minimap command (Unimpaired plugin)
* `[om` toggle minimap on command (Unimpaired plugin)
* `]om` toggle minimap off command (Unimpaired plugin)
* Documentation command
* Edit Settings command
* How to map `jk` to `Esc` (documentation)

### Changed

* `ds<` no longer deletes surrounding tag; use `dst` instead (Surround plugin)
* `ds>` no longer deletes surrounding tag; use `dst` instead (Surround plugin)
* Modeline `vintageous_modeline` is disabled by default
* "Open Changelog" command caption changed to "Changelog"

### Removed

* `vintageous_surround_spaces` setting
* Unimplemented `tabopen` ex command

### Deprecated

* `neovintageous_toggle_use_ctrl_keys` command
* `neovintageous_reset` command
* `neovintageous_exit_from_command_mode` command
* `toggle_mode` command

### Fixed

* [#213](https://github.com/NeoVintageous/NeoVintageous/issues/213): No command accepts characters in a keybinding
* [#167](https://github.com/NeoVintageous/NeoVintageous/issues/167): Allow .vintageousrc to map any keybinds
* [#152](https://github.com/NeoVintageous/NeoVintageous/issues/152): `f<key>` doesn't jump to `<key>` if there is a mapping for `<key>`
* [#97](https://github.com/NeoVintageous/NeoVintageous/issues/97): Mapping commands
* [#81](https://github.com/NeoVintageous/NeoVintageous/issues/81): `ct<leader>` or `cf<leader>` doesn't work; need `ct<leader><leader>`
* [#282](https://github.com/NeoVintageous/NeoVintageous/issues/282): Surround doesn't work as expected on first symbol
* Several `.vintageousrc` syntax highlighting bugs
* Lots of Command-line mode syntax highlighting bugs

## 1.3.1 - 2017-07-31

* [#281](https://github.com/NeoVintageous/NeoVintageous/issues/281): `aW` text objects error if cursor starts at whitespace
* [#123](https://github.com/NeoVintageous/NeoVintageous/issues/123): text object `a<` or `i<` doesn't work!
* [#280](https://github.com/NeoVintageous/NeoVintageous/issues/280): `daW` / etc sometimes hang forever in LaTeX syntax
* Handle upgrades and loading errors gracefully

## 1.3.0 - 2017-07-21

### Added

* [#271](https://github.com/NeoVintageous/NeoVintageous/issues/271): `ctrl+w q` should close window if closing the last view
* [#269](https://github.com/NeoVintageous/NeoVintageous/issues/269): `:close` ex command
* `.vintageousrc` `<leader>` special string can be used more than once in a mapping e.g. `nnoremap <leader><leader> ggvG`
* `.vintageousrc` `<leader>` special string can be used anywhere in mapping e.g. `nnoremap g<leader> ggvG`
* `.vintageousrc` `noremap`, `nnoremap`, `vnoremap`, and `onoremap` commands
* `.vintageousrc` syntax highlighting
* `ctrl+n` and `ctrl+p` auto-complete navigation

  Command | Description
  ------- | -----------
  `ctrl+n` or `ctrl+j` | down
  `ctrl+p` or `ctrl+k` | up

* `ctrl+n` and `ctrl+p` overlay navigation

  Command | Description | Notes
  ------- | ----------- | -----
  `ctrl+n` | down | e.g. `ctrl+p` and `ctrl+shift+p` invoke overlays
  `ctrl+p` | up | e.g. `ctrl+p` and `ctrl+shift+p` invoke overlays

* Port of [unimpaired.vim](https://github.com/tpope/vim-unimpaired) go to error commands

  Command | Description | Documentation | Dependencies
  ------- | ----------- | ------------- | ------------
  `[l` | Jump to `[count]` next error. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | [Linter](https://github.com/SublimeLinter/SublimeLinter3)
  `]l` | Jump to `[count]` previous error.. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | [Linter](https://github.com/SublimeLinter/SublimeLinter3)

* Port of [unimpaired.vim](https://github.com/tpope/vim-unimpaired) option toggling commands

  On | Off | Toggle | Description | Documentation
  -- | --- | ------ | ----------- | -------------
  `[oc` | `]oc` | `coc` | ['cursorline'](https://vimhelp.appspot.com/options.txt.html#%27cursorline%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[ol` | `]ol` | `col` | ['list'](https://vimhelp.appspot.com/options.txt.html#%27list%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[on` | `]on` | `con` | ['number'](https://vimhelp.appspot.com/options.txt.html#%27number%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[os` | `]os` | `cos` | ['spell'](https://vimhelp.appspot.com/options.txt.html#%27spell%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[ow` | `]ow` | `cow` | ['wrap'](https://vimhelp.appspot.com/options.txt.html#%27wrap%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)

* Port of [abolish.vim](https://github.com/tpope/vim-abolish) coercion commands

  Command | Description | Documentation
  ------- | ----------- | -------------
  `crm` | Coerce word under cursor to MixedCase. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crc` | Coerce word under cursor to camelCase. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crs` | Coerce word under cursor to snake_case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr_` | Coerce word under cursor to snake_case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cru` | Coerce word under cursor to SNAKE_UPPERCASE. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crU` | Coerce word under cursor to SNAKE_UPPERCASE. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr-` | Coerce word under cursor to dash-case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crk` | Coerce word under cursor to kebab-case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr.` | Coerce word under cursor to dot.case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr<Space>` | Coerce word under cursor to space case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crt` | Coerce word under cursor to Title Case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)

* How to map `jj` to `Esc` (documentation)
* How to disable arrow keys (documentation)
* Commentary plugin usage (documentation)
* Surround plugin usage (documentation)

### Fixed

* Command-line syntax `:quit` highlighting
* Edge-case plugin conflict issues
* Edge-case Unimpaired plugin issue adding blanks
* Edge-case issue invalidating ex mode completions

## 1.2.0 - 2017-06-21

### Added

* [#252](https://github.com/NeoVintageous/NeoVintageous/issues/252): The package is now available in Package Control
* Git diff commands

  Command | Description | Documentation | Dependencies | Notes
  ------- | ----------- | ------------- | ------------ | -----
  `[c` | Jump backwards to the previous start of a change. | [diff](https://vimhelp.appspot.com/diff.txt.html#[c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)
  `]c` | Jump forwards to the next start of a change. | [diff](https://vimhelp.appspot.com/diff.txt.html#]c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)

* Port of [unimpaired.vim](https://github.com/tpope/vim-unimpaired) is provided by default. *The implementation may not be complete. Please open issues about missing features.* *Below is a table of what is currently available.*

  Command | Description | Documentation | Dependencies | Notes
  ------- | ----------- | ------------- | ------------ | -----
  `[<Space>` | Add `[count]` blank lines before the cursor. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |
  `]<Space>` | Add `[count]` blank lines after the cursor. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |
  `[e` | Exchange the current line with `[count]` lines above it. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |
  `]e` | Exchange the current line with `[count]` lines below it. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |

* [#275](https://github.com/NeoVintageous/NeoVintageous/issues/275): Commands in the `.vintageousrc` file don't need to be prefixed with `:` (colon)
* [#187](https://github.com/NeoVintageous/NeoVintageous/issues/187): Switching to specific tab with `[count]` `gt`
* `[count]` to `ctrl+e` and `ctrl+y` (scroll lines)
* Coveralls code coverage reporting
* Surround plugin usage (documentation)
* `.vintageousrc` usage (documentation)
* Modeline usage (documentation)
* Multiple cursor usage (documentation)
* Sidebar and Overlay navigation usage (documentation)

## 1.1.2 - 2017-06-05

### Fixed

* `gt` command should wrap around from the last tab to the first tab
* Command-line mode history edge-case error when no history available
* Command-line mode history not working (regression)
* [#192](https://github.com/NeoVintageous/NeoVintageous/issues/192): Closing last tab shouldn’t close sublime window with project (documentation)
* [#122](https://github.com/NeoVintageous/NeoVintageous/issues/122): `Tab` doesn't work in visual mode (`Shift+Tab` does) (documentation)

## 1.1.1 - 2017-05-31

### Fixed

* [#266](https://github.com/NeoVintageous/NeoVintageous/issues/266) `:nmap` doesn't work in `.vintageousrc` file
* `:omap` doesn't work in `.vintageousrc` file
* `:vmap` doesn't work in `.vintageousrc` file
* `:set` prints debug messages to console even when debugging is disabled
* [#268](https://github.com/NeoVintageous/NeoVintageous/issues/268): `:set` doesn't work in some cases e.g. `:set hlsearch`
* `:file` (`ctrl+g`) file name should be quoted
* Readme link to Linux and OSX cleaner script is broken
* [#267](https://github.com/NeoVintageous/NeoVintageous/issues/267): Settings – User `.vintageousrc` menu item is broken
* [#169](https://github.com/NeoVintageous/NeoVintageous/issues/169): How to map this using Vintageous? (documentation)

## 1.1.0 - 2017-05-28

### Added

* [ToggleNeoVintageous](https://github.com/NeoVintageous/ToggleNeoVintageous); A command to toggle NeoVintageous
* Reload My `.vintageousrc` File command
* [#63](https://github.com/NeoVintageous/NeoVintageous/issues/63): `/` search does not highlight well
* New commands

  Key | Context | Description
  --- | ------- | -----------
  `j` | Sidebar | down
  `k` | Sidebar | up
  `h` | Sidebar | close node / go to parent node
  `l` | Sidebar | open node
  `ctrl+j` | Overlay | down
  `ctrl+k` | Overlay | up
  `ctrl+[` | Normal | Same as `Esc` ([#249](https://github.com/NeoVintageous/NeoVintageous/issues/249))

### Fixed

* Error when reloading and upgrading NeoVintageous and NeoVintageous plugins
* [#119](https://github.com/NeoVintageous/NeoVintageous/issues/119): Loosing user settings when toggling ctrl keys
* [#84](https://github.com/NeoVintageous/NeoVintageous/issues/84): More detail or examples for mapping
* [#34](https://github.com/NeoVintageous/NeoVintageous/issues/34): Small note regarding wiki OSX note
* [#162](https://github.com/NeoVintageous/NeoVintageous/issues/162): Use `sublime.packages_path()`
* [#246](https://github.com/NeoVintageous/NeoVintageous/issues/246): Error when toggling vintageous
* `:!{cmd}` error (Windows)
* `:!!` error (Windows)
* `:new` error
* `:edit` error
* `:exit` error
* `:wq!` error
* `:wq` error

## 1.0.1 - 2017-04-28

### Fixed

* `gq` error
* error using registers
* error when searching
* running last ex command `!!` not working

## 1.0.0 - 2017-04-22

### Added

* New commands

  Command | Description | Documentation | Dependencies | Notes
  ------- | ----------- | ------------- | ------------ | -----
  `ctrl+]` | Jump to the definition of the keyword under the cursor | [tagsearch](https://vimhelp.appspot.com/tagsrch.txt.html#CTRL-\]) | |
  `ctrl-w h` | Move cursor to view left of current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_h) | |
  `ctrl-w j` | Move cursor to view below current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_j) | |
  `ctrl-w k` | Move cursor to view above current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_k) | |
  `ctrl-w l` | Move cursor to view right of current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_l) | |
  `ctrl-w b` | Move cursor to bottom-right view | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_b) | |
  `ctrl-w t` | Move cursor to top-left view | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_t) | |
  `ctrl-w H` | Move the current window to be at the very top | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_H) | | Only works in 2-col or 2-row layouts
  `ctrl-w =` | Make all views (almost) equally high and wide | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_=) | |
  `ctrl-w _` | Set current view height as high as possible | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W__) | |
  `ctrl-w \|` | Set current view width as wide as possible | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_bar) | |
  `ctrl-w o` | Make the current view the only one on the screen | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_o) | |
  `ctrl-w c` | Close current view | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_c) | |
  `ctrl-w x` | Exchange current view with next one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_x) | |
  `ctrl-w s` | Split current window in two | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_s) | [Origami](https://github.com/SublimeText/Origami) |
  `ctrl-w v` | Split current window in two (vertically) | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_v) | [Origami](https://github.com/SublimeText/Origami) |
  `ctrl-w J` | Move the current window to be at the very bottom | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_J) | | Only works in 2-col or 2-row layouts
  `ctrl-w K` | Move the current view to be at the far left | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_K) | | Only works in 2-col or 2-row layouts
  `ctrl-w L` | Move the current window to be at the far right | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_L) | | Only works in 2-col or 2-row layouts
  `ctrl-w n` | Create new view below current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_n) | |
  `ga` | Print the ascii value of the character under the cursor in dec, hex and oct | [various](https://vimhelp.appspot.com/various.txt.html#ga) | |
  `ctrl+c` | Exit select mode | |
  `ctrl+[` | Exit select mode | |

* Port of [surround.vim](https://github.com/tpope/vim-surround) is provided by default. It is based on the [Vintageous_Plugin_Surround](https://github.com/guillermooo/Vintageous_Plugin_Surround) plugin by @guillermooo
* `vi_search.comment` scope on search matches for better control of highlighting
* `vintageous_visualyank` setting to disable visual bells when yanking text
* [#1077](https://github.com/guillermooo/Vintageous/pull/1077): Support for Sublime Wrap Plus
* Command-line mode syntax uses new syntax format
* Open README and Open CHANGELOG command palette commands
* Package Control menus for opening README, CHANGELOG, and LICENSE

### Removed

* Settings

  Setting | Description | Notes
  ------- | ----------- | -----
  `vintageous_test_runner_keymaps` | Enable test runner keymaps | Tests are now run using [UnitTesting](https://github.com/randy3k/UnitTesting)
  `vintageous_log_level` | | No longer used for logging
  `vintageous_verbose` | | No longer used for logging

### Fixed

* Double loading and unnecessary loading, unloading, and loading of modules on start
* Logging messages printed multiple times
* `CTRL-W_H` and `CTRL-W-L` windowing commands
* Error raised trying to scroll in a transient view
* `Esc` closes console even if already in normal mode and have a multiple selection
* Console automatically closes on start
* Wrong file permissions
* `c_` and `d_` cause errors
* [#1042](https://github.com/guillermooo/Vintageous/pull/1042): Interactive commands not working after mapped commands
* [#1074](https://github.com/guillermooo/Vintageous/pull/1074): New text objects
* Command-line mode syntax should not be listed in syntax menus
