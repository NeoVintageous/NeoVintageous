![NeoVintageous Logo](res/neovintageous.png)

<p align="center">
    <a href="https://github.com/NeoVintageous/NeoVintageous/actions/workflows/ci.yml"><img alt="Continuous Integration" src="https://github.com/NeoVintageous/NeoVintageous/actions/workflows/ci.yml/badge.svg?branch=master"></a>
    <a href="https://ci.appveyor.com/project/gerardroche/neovintageous"><img alt="Build status" src="https://ci.appveyor.com/api/projects/status/g4pkv4ws1k2r1xna?svg=true"></a>
    <a href="https://codecov.io/gh/NeoVintageous/NeoVintageous"><img alt="Codecov" src="https://codecov.io/gh/NeoVintageous/NeoVintageous/branch/master/graph/badge.svg?token=PAaE5LdlOR"></a>
    <a href="https://packagecontrol.io/packages/NeoVintageous"><img alt="Downloads" src="https://img.shields.io/packagecontrol/dt/NeoVintageous.svg?style=flat-square"></a>
</p>

## About NeoVintageous

NeoVintageous is an advanced Vim emulator for [Sublime Text](https://www.sublimetext.com).

- :sparkles: For a full list of supported Vim features, please refer to our [roadmap](https://github.com/NeoVintageous/NeoVintageous/blob/master/ROADMAP.md).
- :rocket: The [changelog](CHANGELOG.md) outlines the breaking/major/minor updates between releases.
- :page_facing_up: Vim's full documentation is accessible via `:help {subject}` and [online](https://vimhelp.org).
- Report missing features/bugs on [GitHub](https://github.com/NeoVintageous/NeoVintageous/issues).
- Drop-in replacement for Vintageous
- Zero configuration required

<details>
 <summary><strong>Table of Contents</strong> (click to expand)</summary>

- [About NeoVintageous](#about-neovintageous)
- [Installation](#installation)
- [Settings](#settings)
- [Modes](#modes)
- [neovintageousrc](#neovintageousrc)
- [Key mapping](#key-mapping)
  - [Leader mapleader](#leader-mapleader)
  - [LocalLeader maplocalleader](#localleader-maplocalleader)
  - [Map commands](#map-commands)
    - [map-overview](#map-overview)
    - [Mapping Ex Commands](#mapping-ex-commands)
    - [Mapping Sublime Text Commands](#mapping-sublime-text-commands)
    - [Mapping Specific File-Types](#mapping-specific-file-types)
    - [Mapping Super-Keys](#mapping-super-keys)
    - [Mapping Case-Sensitivity](#mapping-case-sensitivity)
    - [Mapping for Toggling the Side Bar](#mapping-for-toggling-the-side-bar)
    - [Mapping for Revealing the Side Bar](#mapping-for-revealing-the-side-bar)
    - [Mapping Capslock to Escape](#mapping-capslock-to-escape)
- [Options](#options)
- [Search Highlighting](#search-highlighting)
- [Plugins](#plugins)
  - [Highlighted Yank](#highlighted-yank)
    - [Customize Highlighted Yank Colors](#customize-highlighted-yank-colors)
  - [Input Method :rocket: :new: <small>Since v1.32</small>](#input-method-rocket-new-since-v132)
  - [Markology :rocket: :new: <small>Since v1.32</small>](#markology-rocket-new-since-v132)
    - [Customize Markology Mark Colors](#customize-markology-mark-colors)
  - [Multiple Cursors](#multiple-cursors)
- [F.A.Q.](#faq)
  - [Key Presses are Laggy or Slow](#key-presses-are-laggy-or-slow)
    - [On macOS (OSX):](#on-macos-osx)
    - [On Ubuntu (GNOME desktop):](#on-ubuntu-gnome-desktop)
    - [On KDE:](#on-kde)
    - [On X11 Systems (generic method):](#on-x11-systems-generic-method)
- [Contributing](#contributing)
  - [Enable Pre-Release Upgrades](#enable-pre-release-upgrades)
- [Changelog](#changelog)
- [Credits](#credits)
- [License](#license)

</details>

## Installation

**Package Control Installation**

1. Open Sublime Text.
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to open the Command Palette.
3. Type "Package Control: Install Package" and press `Enter`.
4. In the input field, type "NeoVintageous" and select it from the list of available packages.

**Git Repository Installation**

1. Open a terminal or command prompt.
2. Navigate to the Sublime Text Packages directory:
    - On Windows: `%APPDATA%\Sublime Text\Packages`
    - On macOS: `~/Library/Application Support/Sublime Text/Packages`
    - On Linux: `~/.config/sublime-text/Packages`
3. Clone the plugin repository directly into the Packages directory using Git:
   ```
   git clone https://github.com/NeoVintageous/NeoVintageous.git
   ```

## Settings

Command Palette → Preferences: NeoVintageous Settings

| Setting                                           | Default   | Type      | Description
| :------------------------------------------------ | :-------- | :-------- | :----------
| highlightedyank                                   | true      | Boolean   | Plugin. A port of https://github.com/machakann/vim-highlightedyank.
| highlightedyank_duration                          | 1000      | Integer   | Assign number of time in milliseconds.
| highlightedyank_style                             | "fill"    | String    | Highlighted Yank style. Valid values are: fill, outline, underline, squiggly_underline, stippled_underline.
| neovintageous_search_cur_style                    | "fill"    | String    | Current match search style. Valid values are: fill, outline, underline, squiggly_underline, stippled_underline
| neovintageous_search_inc_style                    | "fill"    | String    | Incremental search style. Valid values are: fill, outline, underline, squiggly_underline, stippled_underline
| neovintageous_search_occ_style                    | "fill"    | String    | Search occurrences style. Valid values are: fill, outline, underline, squiggly_underline, stippled_underline
| vintageous_auto_complete_exit_from_insert_mode    | true      | Boolean   | Close auto complete, if visible, when leaving Insert mode and entering Normal mode. When set to false only the auto complete is closed.
| vintageous_auto_nohlsearch_on_normal_enter        | true      | Boolean   | If enabled, search highlighting is cleared entering normal mode. This typically means the `<Esc>` key has been pressed. <br><br>To clear search highlighting use: <br><br>`:noh[lsearch]` <br><br>Example mapping: <br><br>`noremap <C-l> :nohlsearch<CR>`
| vintageous_auto_switch_input_method               | false     | Boolean   | Enable automatic switching of input methods.
| vintageous_auto_switch_input_method_default       | ""        | String    | The default input method to be used.
| vintageous_auto_switch_input_method_get_cmd       | ""        | String    | The full path to the command used to retrieve the current input method key.
| vintageous_auto_switch_input_method_set_cmd       | ""        | String    | The full path to the command used to switch input methods, where `{im}` is a placeholder for the input method key.
| vintageous_bell                                   | "blink"   | String    | Visual bell style. Valid values are: blink, view, views.
| vintageous_bell_color_scheme                      | "dark"    | String    | Visual bell color-scheme. Valid values are: dark, light, or a color scheme resource. Example: Packages/Name/Name.color-scheme
| vintageous_clear_auto_indent_on_esc               | true      | Boolean   | If you do not type anything on a new line e.g. pressing `<Esc>` after "o" or "O", the indent is deleted again. To preserve the leading white-space on after pressing `<esc>` set this setting to false.
| vintageous_default_mode                           | ""        | String    | Default mode to use when activating or switching views. Valid values are: "insert" or "". <br><br>insert: Enter insert mode when opening or switching views or when the window receives focus and is not in visual mode i.e. visual mode selections are retained when the window loses focus.
| vintageous_enable_abolish                         | true      | Boolean   | Plugin. A port of https://github.com/tpope/vim-abolish.
| vintageous_enable_commentary                      | true      | Boolean   | Plugin. A port of https://github.com/tpope/vim-commentary.
| vintageous_enable_multiple_cursors                | true      | Boolean   | Plugin. A port of https://github.com/terryma/vim-multiple-cursors.
| vintageous_enable_sneak                           | false     | Boolean   | Plugin. A port of https://github.com/justinmk/vim-sneak.
| vintageous_enable_sublime                         | true      | Boolean   | Plugin. Sublime Text tweaks.
| vintageous_enable_surround                        | true      | Boolean   | Plugin. A port of https://github.com/tpope/vim-surround.
| vintageous_enable_unimpaired                      | true      | Boolean   | Plugin. A port of https://github.com/tpope/vim-unimpaired.
| vintageous_exit_when_quiting_last_window          | true      | Boolean   | When quitting the last window exit Sublime.
| vintageous_handle_keys                            | \{\}      | Dict      | Delegate configured keys to be handled by Sublime Text. For example to use native Sublime Text behaviour for ctrl+f:<br> `"vintageous_handle_keys": {"<C-f>": false}` <br><br> Keys can be handled for specific modes by using a prefix:<br><br> n_ - Normal<br> i_ - Insert<br> v_ - Visual<br> V_ - Visual line<br> b_ - Visual block<br> s_ - Select<br><br> For example to only delegate <C-w> in insert and visual modes:<br><br> `"vintageous_handle_keys": {"i_<C-w>": false "v_<C-w>": false}`
| vintageous_i_escape_jj                            | false     | Boolean   | Enable Insert mode jj escape.
| vintageous_i_escape_jk                            | false     | Boolean   | Enable Insert mode jk escape.
| vintageous_i_escape_kj                            | false     | Boolean   | Enable Insert mode kj escape.
| vintageous_lsp_save                               | false     | Boolean   | Override native save to handle LSP Code-Actions-On-Save. <br>See https://github.com/sublimelsp/LSP/issues/1725
| vintageous_multi_cursor_exit_from_visual_mode     | false     | Boolean   | Exit visual multi cursor visual on quit key.<br> When false then pressing a quit key (e.g. `<Esc>` or J) in multiple cursor visual mode the visual mode exits to normal mode but keeps the cursors.<br> When true then pressing a quit key (e.g. `<Esc>` or J) in multiple cursor visual mode the visual mode exits all multiple cursors.
| vintageous_reset_mode_when_switching_tabs         | true      | Boolean   | Reset to normal mode when a tab is activated.
| vintageous_save_async                             | false     | Boolean   | Asynchronous file saving with commands like :w, :wq.
| vintageous_shell_silent                           | false     | Boolean   | Show output panel from shell commands.
| vintageous_show_marks_in_gutter                   | true      | Boolean   | Show marks in the gutter.
| vintageous_sneak_use_ic_scs                       | 0         | Integer   | 0: Always case-sensitive<br> 1: Case sensitivity is determined by `'ignorecase'` and `'smartcase'`.
| vintageous_source                                 | null      | String    | Read Ex commands from a resource before the neovintageourc resource is sourced. This means you can still override these ex commands in your neovintageousrc file. <br>Example: Packages/NeoVintageousDvorak/dvorak.neovintageous <br>Example: Packages/NeoVintageousColemak/colemak.neovintageous
| vintageous_terminal                               | null      | String    | Name of program to use when starting a ":shell". <br>Example: gnome-terminal
| vintageous_use_ctrl_keys                          | true      | Boolean   | Enable Vim Ctrl keys.
| vintageous_use_super_keys                         | true      | Boolean   | Enable Vim Super keys. Super key is an alternative name for what is commonly labelled as the Windows key or Command key (Macintosh).
| vintageous_use_sys_clipboard                      | false     | Boolean   | Propagate copy actions to the system clipboard.

## Modes

`[count]` - An optional number that may precede the command to multiply or iterate the command.

| Mode                               | Description
| :----------------------------------| :----------
| Insert mode                        | `[count]i`
| Normal mode                        | `<Esc>` or `CTRL-[` or `CTRL-c`
| Visual mode                        | `v`
| Visual line mode                   | `[count]V`
| Visual block mode                  | `CTRL-v`
| Replace mode                       | `R`
| Operator&#8209;pending&nbsp;mode   | Like Normal mode, but after an operator command has start, and Vim is waiting for a `{motion}` to specify the text that the operator will work on.
| Command-line mode<br>Cmdline mode  | `:`, `/`, `?`, `!`
| Multiple-cursor mode               | `CTRL-n` or `gh`

## neovintageousrc

A file that contains initialization commands is typically referred to as a 'vimrc' file. In NeoVintageous, this file is called 'neovintageousrc.' Each line in the neovintageousrc file is executed as an Ex command at startup.

To edit the neovintageousrc file, follow these steps:

1. Open the Command Palette: `Command Palette → NeoVintageous: Open neovintageous file`.

2. Make the necessary changes to the file.

3. To apply the changes, reload the neovintageousrc from the Command Palette: `Command Palette → NeoVintageous: Reload neovintageous file`.

## Key mapping

### `<Leader>` `mapleader`

To define a mapping which uses the "g:mapleader" variable, the special string
"`<Leader>`" can be used.  It is replaced with the string value of
"g:mapleader".  If "g:mapleader" is not set or empty, a backslash is used
instead. Example:

```vim
noremap <Leader>A  oanother line<Esc>
```

Works like:

```vim
noremap \A  oanother line<Esc>
```

But after:

```vim
let mapleader=,
```

It works like:

```vim
noremap ,A  oanother line<Esc>
```

Note that the value of "g:mapleader" is used at the moment the mapping is
defined.  Changing "g:mapleader" after that has no effect for already defined
mappings.

### `<LocalLeader>` `maplocalleader`

`<LocalLeader>` is just like `<Leader>`, except that it uses "maplocalleader"
instead of "mapleader".  Example:

```vim
let maplocalleader=,
noremap: <LocalLeader>A  oanother line<Esc>
```

### Map commands

There are commands to enter new mappings, remove mappings and list mappings.
See [map-overview](#map-overview) for the various forms of "map" and their relationships with
modes.

`{lhs}`   means left-hand-side.

`{rhs}`   means right-hand-side.

| Commands | Description
| -------: | :----------
| :no[remap]&nbsp;`{lhs}`&nbsp;`{rhs}` <br>:nn[oremap]&nbsp;`{lhs}`&nbsp;`{rhs}` <br>:ino[remap]&nbsp;`{lhs}`&nbsp;`{rhs}` <br>:vn[oremap]&nbsp;`{lhs}`&nbsp;`{rhs}` <br>:xn[oremap]&nbsp;`{lhs}`&nbsp;`{rhs}` <br>:snor[emap]&nbsp;`{lhs}`&nbsp;`{rhs}` <br>:ono[remap]&nbsp;`{lhs}`&nbsp;`{rhs}` | Map the key sequence `{lhs}` to `{rhs}` for the modes where the map command applies.  Disallow mapping of `{rhs},` to avoid nested and recursive mappings.  Often used to redefine a command.

#### map-overview

Overview of which map command works in which mode.  More details below.

| COMMAND   | COMMAND | MODES
| :-------- | :------ | :----
| :noremap  | :unmap  | Normal, Visual, Select, Operator-pending
| :nnoremap | :nunmap | Normal
| :inoremap | :iunmap | Insert <br>:warning: Insert mode mappings are very limited. Very few keys are mappable out-of-the-box, but you can configure any key to be mappable. This may be improved in a future release.
| :vnoremap | :vunmap | Visual and Select
| :xnoremap | :xunmap | Visual
| :snoremap | :sunmap | Select <br>:warning: Currently represents Multiple-cursor mode; this may change in a future release. The multiple-cursor mode is likely to get its own dedicated mode. Probably :mnoremaap?
| :onoremap | :ounmap | Operator-pending

Same information in a table:

|          Mode  | Norm | Ins | Vis | Sel | Opr |
|:---------------|:----:|:---:|:---:|:---:|:---:|
| [nore]map      | yes  |  -  | yes | yes | yes |
| n[nore]map     | yes  |  -  |  -  |  -  |  -  |
| i[nore]map     |  -   | yes |  -  |  -  |  -  |
| v[nore]map     |  -   |  -  | yes | yes |  -  |
| x[nore]map     |  -   |  -  | yes |  -  |  -  |
| s[nore]map     |  -   |  -  |  -  | yes |  -  |
| o[nore]map     |  -   |  -  |  -  |  -  | yes |

#### Mapping Ex Commands

**Example:** Map CTRL-l to the :nohlsearch command to stop the highlighting for the 'hlsearch' option.

```vim
noremap <C-l> :nohlsearch<CR>
```

#### Mapping Sublime Text Commands

Sublime Text commands are mappable. The command must be PascalCase and the parameters must be space separated.

**Example:** Map `,f` to the `show_overlay` command with arguments `{"overlay": "goto", "text": "@"}`

```vim
nnoremap ,f :ShowOverlay overlay=goto text=@<CR>
```

#### Mapping Specific File-Types

File type specific mappings are supported by the `FileType` keyword that accepts a comma-delimited list of file-types.

**Example:** Map `gd` to the `lsp_symbol_definition` command for \*.go and \*.html files.

```vim
nnoremap FileType go,html gd :LspSymbolDefinition<CR>
```

#### Mapping Super-Keys

Super keys, also known as the Windows key or Command key (⌘) on Mac, are denoted as `<D-...>`.

For example, to map the `<D-i>` combination to the `goto_symbol_in_project` command, add the following configuration to your NeoVintageous `neovintageousrc` file:

```vim
nnoremap <D-i> :GotoSymbolInProject<CR>
```

With this mapping in place, pressing the Super key (Windows key or Command key on Mac) together with the 'i' key will trigger the `goto_symbol_in_project` command in NeoVintageous.

Please note that this example demonstrates mapping the `<D-i>` combination for illustrative purposes. You can map other Super-key combinations or any desired key combinations to different commands based on your needs and preferences.

#### Mapping Case-Sensitivity

All keys are case-sensitive in Sublime Text. This means that `<D-i>` and `<D-I>` are treated as two distinct key events, allowing you to map actions to both.

**Example:** Map "Goto Symbol in Project" and "Goto Symbol in File" using case-sensitive mappings

To map the Super-key (Windows key or Command key on Mac) together with the 'i' key to the "Goto Symbol in Project" command, add the following configuration to your NeoVintageous `neovintageousrc` file:

```vim
noremap <D-i> :GotoSymbolInProject<CR>
```

To map the Super-key together with the 'Shift' and 'i' keys (`<D-I>`) to the "Goto Symbol in File" command, add the following configuration to your NeoVintageous `neovintageousrc` file:

```vim
noremap <D-I> :ShowOverlay overlay=goto text=@<CR>
```

With these mappings in place, you can now use both `<D-i>` and `<D-I>` combinations to trigger different commands in NeoVintageous.

Feel free to modify and customize these mappings based on your preferences and workflow. The case-sensitivity of the keys allows you to create distinct mappings for different actions, providing you with greater flexibility in your keybindings.

#### Mapping for Toggling the Side Bar

To toggle the side bar using your preferred mapping (in this example, `<leader>d`), first, add the following configuration to your NeoVintageous `neovintageousrc` file:

```vim
let mapleader=,
nnoremap <leader>d :Neovintageous action=toggle_side_bar<CR>
```

Next, open the Command Palette and navigate to `Preferences: Key Bindings`. Add the following JSON key binding to be triggered when the side bar has focus:

```json
{
    "keys": [",", "d"],
    "command": "neovintageous",
    "args": {
        "action": "toggle_side_bar"
    },
    "context": [
        { "key": "control", "operand": "sidebar_tree" }
    ]
}
```

Please note that the provided example uses `<leader>d` as the mapping, but you can customize it to your preferred mapping by modifying the `<leader>` part and updating the key binding to match your leader and preferred key. For instance, if your preferred mapping is `<leader>t`, you can modify the mapping as follows:

1. Update the mapping in your NeoVintageous `neovintageousrc` file:

```vim
let mapleader=,
nnoremap <leader>t :Neovintageous action=toggle_side_bar<CR>
```

2. Open the Command Palette and navigate to `Preferences: Key Bindings`. Add the following JSON key binding to be triggered when the side bar has focus, using your preferred key combination:

```json
{
    "keys": [",", "t"],
    "command": "neovintageous",
    "args": {
        "action": "toggle_side_bar"
    },
    "context": [
        { "key": "control", "operand": "sidebar_tree" }
    ]
}
```

By making these modifications, you can now use your preferred mapping (e.g., `<leader>t`) to easily toggle the side bar while using NeoVintageous in Sublime Text. This flexibility allows you to choose a keyboard combination that suits your workflow and personal preferences.

#### Mapping for Revealing the Side Bar

To reveal the side bar using your preferred mapping (in this example, `<leader><leader>`), first, add the following configuration to your NeoVintageous `neovintageousrc` file:

```vim
let mapleader=,
nnoremap <leader><leader> :Neovintageous action=reveal_side_bar<CR>
```

Next, open the Command Palette and navigate to `Preferences: Key Bindings`. Add the following JSON key binding to be triggered when the side bar has focus:

```json
{
    "keys": [",", ","],
    "command": "focus_group",
    "args": {
        "group": 0
    },
    "context": [
        { "key": "control", "operand": "sidebar_tree" }
    ]
}
```

With this setup, you can now use the specified key bindings to easily toggle and reveal the side bar while using NeoVintageous in Sublime Text.

Please note that the provided example uses `<leader><leader>` as the mapping, but you can customize it to your preferred mapping by modifying the `<leader>` part and updating the key binding to match your leader and preferred key. See [Mapping for Toggling the Side Bar](#mapping-for-toggling-the-side-bar) for a more detailed example.

#### Mapping Capslock to Escape

Neovintageous cannot directly remap the CapsLock key; however, you can achieve this remapping at the operating system level. For instance, on Ubuntu, you can map the CapsLock key to Escape using a tool called `gsettings`. Follow these steps to make the remapping:

1. Open a terminal.

2. Run the following command to map CapsLock to Escape using `gsettings`:

```bash
gsettings set org.gnome.desktop.input-sources xkb-options "['caps:escape']"
```

After executing this command, the CapsLock key will act as the Escape key in your system. This means that when using Neovintageous or any other application, pressing CapsLock will have the same effect as pressing the Escape key.

Please note that the specific method to remap keys might vary depending on your operating system or desktop environment. Be sure to check the documentation or forums related to your OS for any variations or additional steps.

## Options

The list below includes all options, presented with their full names and corresponding abbreviations, where applicable. You can use either form interchangeably. Certain options act as proxies to Sublime Text settings, meaning they utilize the underlying Sublime Text setting. Modifying the option will consequently alter the corresponding Sublime Text setting.

| Option                          | Type    | Default                                         | Description
| :------------------------------ | :-------| :-----------------------------------------------| :----------
| `'autoindent'`<br>`'ai'`        | String  | `auto_indent` <br>sublime setting               |
| `'belloff'`<br>`'bo'`           | String  | `''`; accepts 'all'                             |
| `'equalalways'`                 | Boolean | On                                              |
| `'expandtab'`<br>`'et'`         | Boolean | `translate_tabs_to_spaces` <br>sublime setting  |
| `'hlsearch'`<br>`'hls'`         | Boolean | On                                              | When there is a previous search pattern, highlight all its matches. See also: `'incsearch'`. When you get bored looking at the highlighted matches, you can turn it off with `:nohlsearch`.  This does not change the option value, as soon as you use a search command, the highlighting comes back.
| `'ignorecase'`<br>`'ic'`        | Boolean | Off                                             |
| `'incsearch'`<br>`'is'`         | Boolean | On                                              | While typing a search command, show where the pattern, as it was typed so far, matches.  The matched string is highlighted.  If the pattern is invalid or not found, nothing is shown.  The screen will be updated often.<br> Note that the match will be shown, but the cursor will return to its original position when no match is found and when pressing `<Esc>.`  You still need to finish the search command with `<Enter>` to move the cursor to the match.<br> When `'hlsearch'` is on, all matched strings are highlighted too while typing a search command. See also: `'hlsearch'.`
| `'list'`                        | Boolean | `draw_white_space` <br>sublime setting          | Useful to see the difference between tabs and spaces and for trailing blanks.
| `'magic'`                       | Boolean | On                                              |
| `'menu'`                        | Boolean | On                                              |
| `'minimap'`                     | Boolean | On                                              |
| `'modeline'`<br>`'ml'`          | Boolean | On                                              |
| `'modelines'`<br>`'mls'`        | Number  | 5                                               |
| `'number'`<br>`'nu'`            | Boolean | `line_numbers` <br>sublime setting              | Print the line number in front of each line.
| `'relativenumber'`<br>`'rnu'`   | Boolean | `relative_line_numbers` <br>sublime setting     | Show the line number relative to the line with the cursor in front of each line. Relative line numbers help you use the `count` you can precede some vertical motion commands (e.g., `j` `k` `+` `-`) with, without having to calculate it yourself. Especially useful in combination with other commands (e.g., `y` `d` `c` `<` `>` `gq` `gw` `=`).
| `'scrolloff'`<br>`'so'`         | Number  | `scroll_context_lines` <br>sublime setting      |
| `'shell'`                       | String  | `$SHELL` or `"sh"`, Win32: `"cmd.exe"`          |
| `'sidebar'`                     | Boolean | On                                              |
| `'smartcase'`<br>`'scs'`        | Boolean | Off                                             |
| `'spell'`                       | Boolean | `spell_check` <br>sublime setting               |
| `'statusbar'`                   | Boolean | On                                              |
| `'tabstop'`<br>`'ts'`           | Number  | `tab_size` <br>sublime setting                  |
| `'textwidth'`<br>`'tw'`         | Number  | `wrap_width` <br>sublime setting                |
| `'winaltkeys'`<br>`'wak'`       | String  | `menu`                                          |
| `'wrap'`                        | Boolean | `word_wrap` <br>sublime setting                 | This option changes how text is displayed.  It doesn't change the text in the buffer, see `'textwidth'` for that.<br> When on, lines longer than the width of the window will wrap and displaying continues on the next line.  When off lines will not wrap and only part of long lines will be displayed.  When the cursor is moved to a part that is not shown, the screen will scroll horizontally.
| `'wrapscan'`<br>`'ws'`          | Boolean | On                                              |

## Search Highlighting

You can customize the colors for search highlighting in Sublime Text.

For example, if you are using a color scheme named "Monokai," you can create an override file named `Monokai.sublime-color-scheme` in the User directory. To find the User directory location, go to `Preferences → Browse Packages...`.

Inside the `Monokai.sublime-color-scheme` file, you can define styles for different search highlighting scopes:

- `neovintageous_search_inc`: This scope is used for highlighting the current search incrementally as you type.

- `neovintageous_search_cur`: This scope is used for highlighting the current search term.

- `neovintageous_search_occ`: This scope is used for highlighting all occurrences of the search term.

Here's an example of how to define the styles for these scopes:

```json
{
    "rules": [
        {
            "scope": "neovintageous_search_inc",
            "background": "#a1efe4",
            "foreground": "#272822"
        },
        {
            "scope": "neovintageous_search_cur",
            "background": "#a1efe4",
            "foreground": "#272822"
        },
        {
            "scope": "neovintageous_search_occ",
            "background": "#e6db74",
            "foreground": "#272822"
        }
    ]
}
```

In this example, we are setting custom background and foreground colors for each of the search highlighting scopes. You can replace the color values (`"#a1efe4"`, `"#e6db74"`, etc.) with the colors you prefer.

By customizing the search highlighting colors, you can make search results more visually distinct and easily identifiable in your code, enhancing your overall coding experience.

## Plugins

Experience the power of Vim with NeoVintageous, which seamlessly integrates several impressive Vim plugins right out of the box. While we continuously strive for feature parity, please note that some functional differences might exist, and they may not always be fully documented.

If you come across any missing features or observe variations in functionality, we warmly encourage you to create issues to request enhancements. For a comprehensive inventory of supported Vim features and a detailed development roadmap, kindly consult our [roadmap](https://github.com/NeoVintageous/NeoVintageous/blob/master/ROADMAP.md).

| Plugin              | Original Vim plugin
| :------------------ | :------------------
| Abolish             | [vim-abolish](https://github.com/tpope/vim-abolish)
| Commentary          | [vim-commentary](https://github.com/tpope/vim-commentary)
| Highlighted Yank    | Inspired by [vim-highlightedyank](https://github.com/machakann/vim-highlightedyank)
| Input Method        | Inspired by [vim-xkbswitch](https://github.com/lyokha/vim-xkbswitch) and [VSCodeVim/Vim](https://github.com/VSCodeVim/Vim#input-method) :rocket: :new:
| Indent Object       | [vim-indent-object](https://github.com/michaeljsmith/vim-indent-object)
| Markology           | Inspired by [vim-markology](https://github.com/jeetsukumaran/vim-markology) :rocket: :new:
| Multiple Cursors    | Inspired by [vim-multiple-cursors](https://github.com/terryma/vim-multiple-cursors) and [mg979/vim-visual-multi](https://github.com/mg979/vim-visual-multi)
| Sneak               | [vim-sneak](https://github.com/justinmk/vim-sneak) (disabled by default)
| Surround            | [vim-surround](https://github.com/tpope/vim-surround)
| Targets             | [vim-targets](https://github.com/wellle/targets.vim)
| Unimpaired          | [vim-unimpaired](https://github.com/tpope/vim-unimpaired)

**Additional plugins, install via Package Control:**

- [NeoVintageous Files](https://packagecontrol.io/packages/NeoVintageousFiles): Single key side bar and overlay file commands. :rocket: :new:
- [NeoVintageous Highlight Line](https://packagecontrol.io/packages/NeoVintageousHighlightLine): Auto-disable highlight line when entering Insert mode and Visual modes. :rocket: :new:
- [NeoVintageous Line Numbers](https://packagecontrol.io/packages/NeoVintageousLineNumbers): Auto-disable relative line numbers when entering Insert mode. :rocket: :new:
- [NeoVintageous Toggle](https://packagecontrol.io/packages/NeoVintageousToggle): Toggle NeoVintageous on and off from the command palette.

**Enhanced support, install via Package Control:**

- [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3): Required for jump-to lint-error commands (i.e., `[l` and `]l`).
- [Origami](https://github.com/SublimeText/Origami): Required for some window commands (e.g., `CTRL-w s`, `CTRL-w v`, `CTRL-w ]`).

**Additional keyboard layouts, manual installation:**

- [NeoVintageous Dvorak](https://github.com/gerardroche/NeoVintageousDvorak): Dvorak key mappings. :rocket: :new:
- [NeoVintageous Colemak](https://github.com/gerardroche/NeoVintageousColemak): Colemak key mappings. :rocket: :new:

**Blog**

- [blog.gerardroche.com](https://blog.gerardroche.com): Releases, guides, and tips.

### Highlighted Yank

HighlightedYank is a plugin designed to highlight the yanked region in Sublime Text.

When new text is yanked, the old highlighting is automatically deleted. This ensures that the highlighting remains relevant to the most recent yanked text. Similarly, when former lines are edited, the highlighting is cleared to prevent shifting the position of the highlighting.

You can customize the highlighted yank duration and style using the following settings:

- `highlightedyank_duration`: This setting allows you to configure the duration for which the yanked region will be highlighted. You can set the duration according to your preferences.

- `highlightedyank_style`: This setting allows you to customize the style of the highlighted yank region. You can modify the background and foreground colors to suit your color scheme.

#### Customize Highlighted Yank Colors

To tailor the colors of highlighted yanks to your preference, you can create a color scheme override using the following steps:

1. Open the Command Palette: `UI Customize Color Scheme`.
2. Add the following styles using the "highlightedyank" scope, and adjust the background and foreground colors as desired:

```json
{
    "rules": [
        {
            "scope": "highlightedyank",
            "background": "#e6db74",
            "foreground": "#272822"
        }
    ]
}
```

By customizing the colors of highlighted yanks, you can make yanked regions more visually distinctive and ensure they align with your preferred color scheme, enhancing your editing experience in the Sublime Text editor.

### Input Method :rocket: :new: <small>Since v1.32</small>

Automatically switch the input method when entering and exiting Insert Mode.

Any third-party program can be used to switch input methods. Below are some examples.

Below, you'll find instructions for installing and using input method switchers on various operating systems.

| Setting                                           | Default                  | Type      | Description
| :------------------------------------------------ | :------------------------ | :-------- | :----------
| vintageous_auto_switch_input_method               | false                     | Boolean   | Enable automatic switching of input methods.
| vintageous_auto_switch_input_method_default       | ""                        | String    | The default input method to be used.
| vintageous_auto_switch_input_method_get_cmd       | ""                        | String    | The full path to the command used to retrieve the current input method key.
| vintageous_auto_switch_input_method_set_cmd       | ""                        | String    | The full path to the command used to switch input methods, where `{im}` is a placeholder for the input method key.

The `{im}` argument in the configurations below represents a command-line option that will be passed to the input switcher command, indicating the desired input method for switching. If you're using an alternative program for input method switching, you should incorporate a similar option into the configuration. For instance, if the alternate program's syntax for switching input methods is `my-program -s im`, then the `vintageous_auto_switch_input_method_set_cmd` should be set to `/path/to/my-program -s {im}`. This ensures compatibility with different input method switching tools.

#### Linux:

1. **Install an Input Method Switcher**:

   Choose from popular options like:

   - **ibus**: A powerful input method framework.

   - **xkb-switch**: A lightweight utility for XKB-based layouts.

   - **fcitx**: A flexible and feature-rich input method platform.

   - **gdbus**: A command-line tool for switching input methods.

      Put the following into `im-get` e.g., `~/bin/im-get`.

      You may need to make the script executable e.g., `chmod 744 ~/bin/im-get`.

      ```sh
      #!/bin/sh
      gdbus call \
          --session \
          --dest org.gnome.Shell \
          --object-path /org/gnome/Shell \
          --method org.gnome.Shell.Eval \
          "imports.ui.status.keyboard.getInputSourceManager().currentSource.index" | \
          awk -F'[^0-9]*' '{print $2}'
      ```

      Put the following into `im-set` e.g., `~/bin/im-set`.

      You may need to make the script executable e.g., `chmod 744 ~/bin/im-set`.

      ```sh
      #!/bin/sh
      gdbus call \
          --session \
          --dest org.gnome.Shell \
          --object-path /org/gnome/Shell \
          --method org.gnome.Shell.Eval \
          "imports.ui.status.keyboard.getInputSourceManager().inputSources[$1].activate()"
      ```

   - **qdbus**: A D-Bus tool for communication with input methods.

2. **Determine your Default Input Method**:

   Switch your input method to English and execute the following commands in your terminal:

   - **ibus**: Run `ibus engine`. Example output: `xkb:us::eng`
   - **xkb-switch**: Run `xkb-switch`. Example output: `us`
   - **fcitx**: Run `fcitx-remote`. Example output: `1`
   - **gdbus**: Run `/path/to/im-get`. Example output: `0`
   - **qdbus**: Run `/usr/bin/qdbus org.kde.keyboard /Layouts getLayout`. Example output: `0`

3. **Configure the Input Method Auto Switcher**:

   1. Open the Command Palette by using the shortcut `Ctrl+Shift+P`.
   2. Add the following JSON configuration:

      **ibus**

      ```json
      {
          "vintageous_auto_switch_input_method": true,
          "vintageous_auto_switch_input_method_default": "xkb:us::eng",
          "vintageous_auto_switch_input_method_get_cmd": "/usr/bin/ibus engine",
          "vintageous_auto_switch_input_method_set_cmd": "/usr/bin/ibus engine {im}"
      }
      ```

      **xkb-switch**

      ```json
      {
          "vintageous_auto_switch_input_method": true,
          "vintageous_auto_switch_input_method_default": "us",
          "vintageous_auto_switch_input_method_get_cmd": "/usr/local/bin/xkb-switch",
          "vintageous_auto_switch_input_method_set_cmd": "/usr/local/bin/xkb-switch -s {im}"
      }
      ```

      **fcitx**

      ```json
      {
          "vintageous_auto_switch_input_method": true,
          "vintageous_auto_switch_input_method_default": "1",
          "vintageous_auto_switch_input_method_get_cmd": "/usr/bin/fcitx-remote",
          "vintageous_auto_switch_input_method_set_cmd": "/usr/bin/fcitx-remote -t {im}"
      }
      ```

      **gdbus**

      ```json
      {
          "vintageous_auto_switch_input_method": true,
          "vintageous_auto_switch_input_method_default": "0",
          "vintageous_auto_switch_input_method_get_cmd": "/path/to/im-get",
          "vintageous_auto_switch_input_method_set_cmd": "/path/to/im-set {im}"
      }
      ```

      **qdbus (KDE)**

      ```json
      {
          "vintageous_auto_switch_input_method": true,
          "vintageous_auto_switch_input_method_default": "0",
          "vintageous_auto_switch_input_method_get_cmd": "/usr/bin/qdbus org.kde.keyboard /Layouts getLayout",
          "vintageous_auto_switch_input_method_set_cmd": "/usr/bin/qdbus org.kde.keyboard /Layouts setLayout {im}"
      }
      ```

#### Mac:

1. **Install an Input Method Switcher**:

   Choose from popular options like:

   - **[im-select](https://github.com/daipeihust/im-select)**: A versatile input switching tool.

2. **Determine Your Default Input Method**:

   Switch your input method to English and execute the following commands in your terminal:

   - **im-select**: Run `im-select`. Example output: `com.apple.keylayout.US`

3. **Configure the Input Method Auto Switcher**:

   1. Open the Command Palette by using the shortcut `Cmd+Shift+P`.
   2. Add the following JSON configuration:

      **im-select**

      Given the input method key of `com.apple.keylayout.US` and `im-select` located at `/usr/local/bin.` The configuration is:

      ```json
      {
          "vintageous_auto_switch_input_method": true,
          "vintageous_auto_switch_input_method_default": "com.apple.keylayout.US",
          "vintageous_auto_switch_input_method_get_cmd": "/usr/local/bin/im-select",
          "vintageous_auto_switch_input_method_set_cmd": "/usr/local/bin/im-select {im}"
      }
      ```

#### Windows:

1. **Install an Input Method Switcher**:

   Choose from popular options like:

   - **[im-select](https://github.com/daipeihust/im-select)**: A versatile input switching tool.

2. **Determine Your Default Input Method**:

   Switch your input method to English and execute the following commands in your terminal:

   - **im-select**: Run `im-select`. Example output: `1033`

3. **Configure the Input Method Auto Switcher**:

   1. Open the Command Palette by using the shortcut `Ctrl+Shift+P`.
   2. Add the following JSON configuration:

      **im-select**

      Given the input method key of `1033` (en_US) and `im-select.exe` located at `D:/bin`. The configuration is:

      ```json
      {
          "vintageous_auto_switch_input_method": true,
          "vintageous_auto_switch_input_method_default": "1033",
          "vintageous_auto_switch_input_method_get_cmd": "D:\\bin\\im-select.exe",
          "vintageous_auto_switch_input_method_set_cmd": "D:\\bin\\im-select.exe {im}"
      }
      ```

### Markology :rocket: :new: <small>Since v1.32</small>

Markology displays marks associated with the current line in the gutter. You can disable this feature by modifying the setting `vintageous_show_marks_in_gutter`.

To do so, follow these steps:

1. Open the Command Palette: `Preferences: NeoVintageous Settings`.
2. Add the following JSON configuration:

```json
{
    "vintageous_show_marks_in_gutter": false
}
```

By adjusting this setting, you can control whether marks are displayed in the gutter for the current line.

#### Customize Markology Mark Colors

If you wish to personalize the color of the marks displayed by Markology, you can follow these steps to create a color scheme override:

1. Open the Command Palette: `UI Customize Color Scheme`.
2. Add the following JSON configuration, adjusting the color as desired:

```json
{
    "rules": [
        {
            "scope": "neovintageous.mark",
            "foreground": "yellow"
        }
    ]
}
```

By customizing the color of the marks, you can ensure they are visually distinct and align with your preferred color scheme, providing you with a more tailored and visually appealing editing experience in Sublime Text.

### Multiple Cursors

NeoVintageous provides multiple cursor support in normal mode and visual mode. This feature allows you to work with multiple cursors simultaneously, making repetitive editing tasks more efficient.

**Normal and Visual Mode Commands**

| Command               | Description
| :---------------------| :----------
| `<C-n>` or `gh`       | Start multiple cursor.
| `<C-n>` or `n` or `j` | Add next match.
| `<C-x>` or `q` or `l` | Skip next match.
| `<C-p>` or `Q` or `k` | Remove current match.
| `<M-n>` or `A`        | Select all matches.
| `<Esc>` or `J`        | Quit and enter normal mode.
| `v`                   | Enter normal mode.
| `gH`                  | Select all search occurrences (`/`, `?`, `*`, `#`).

You can now use visual commands such as `c`, `I`, `x`, and `y`, which work without any issues.

You could also go to Normal mode by pressing `v` and use normal commands there.

At any time, you can press `<Esc>` to exit back to regular Vim.

To change the behaviour of `<Esc>`, you can set the `vintageous_multi_cursor_exit_from_visual_mode` setting. When set to false, pressing a quit key (e.g., `<Esc>` or `J`) in multiple cursor visual mode exits to normal mode but keeps the cursors. When set to true, pressing a quit key (e.g., `<Esc>` or `J`) in multiple cursor visual mode exits all multiple cursors.

With the multiple cursor feature, you can speed up your editing workflow by applying commands to multiple locations simultaneously, increasing productivity and convenience.

## F.A.Q.

### Key Presses are Laggy or Slow

If you are experiencing laggy or slow key presses, it could be due to the system configuration. Here are some steps you can take to improve the responsiveness of key presses:

#### On macOS (OSX):

1. Enable Key Repeat:
   If holding down a key like "j" does not repeat the command (a feature of macOS), you can enable key repeat by running this command once at the terminal:

   ```bash
   defaults write com.sublimetext.3 ApplePressAndHoldEnabled -bool false
   ```

#### On Ubuntu (GNOME desktop):

1. Configure Keyboard Repeat Interval and Delay:
   You can adjust the keyboard repeat interval and delay using `gsettings`. Open a terminal and run the following commands:

   ```bash
   gsettings set org.gnome.desktop.peripherals.keyboard repeat-interval 15
   gsettings set org.gnome.desktop.peripherals.keyboard delay 180
   ```

#### On KDE:

1. Adjust Keyboard Delay and Rate:
   For KDE users, you can change the keyboard delay and rate by running the following command:

   ```bash
   systemsettings5 kcm_keyboard
   ```

   This will bring up a window where you can change the 'Delay' and 'Rate' settings as required.

#### On X11 Systems (generic method):

1. Directly Set Keyboard Repeat Rate:
   For X11 type systems, you can directly set the keyboard repeat rate using `xset`. Open a terminal and run the following command:

   ```bash
   xset r rate <milliseconds_before_repeating> <repetitions_per_second>
   ```

   For example, to set a 300 milliseconds delay before repeating and a repetition rate of 30 repetitions per second, use:

   ```bash
   xset r rate 300 30
   ```

By adjusting these settings, you can enhance the responsiveness of key presses and improve your typing experience in Sublime Text or any other applications on your system.

## Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

### Enable Pre-Release Upgrades

Pre-release versions of packages allow you to access the latest features, improvements, and bug fixes before they are officially released. If you're eager to test out new functionalities in NeoVintageous, you can enable pre-release installation with a simple configuration.

1. Open the Command Palette by using the shortcut `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS). Type and select `Preferences: Package Control Settings` to open the settings file for Package Control.

2. In the user settings file, add the "install_prereleases" setting and specify "NeoVintageous" in the list of packages to enable pre-release installation:

   ```json
   {
       "install_prereleases": ["NeoVintageous"]
   }
   ```

   Save the settings file.

3. After saving the settings, you can now install the pre-release version of NeoVintageous. Open the Command Palette again and type `Package Control: Upgrade Package` to install the pre-release version.

4. Enjoy the Latest Features:

   With pre-release installation enabled, you'll receive updates to NeoVintageous before they are officially released. Enjoy exploring and testing the latest features and improvements.

**Note:**

Pre-release versions might contain experimental features or changes that are still being refined. If you encounter any issues or have feedback, feel free to share it with us on the NeoVintageous GitHub repository.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

NeoVintageous is a fork of the discontinued Vintageous plugin.

## License

Released under the [GPL-3.0-or-later License](LICENSE).
