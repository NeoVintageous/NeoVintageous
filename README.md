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
- :rocket: The [changelog]() outlines the breaking/major/minor updates between releases.
- :page_facing_up: Vim's full documentation is accessible via`:help {subject}` and [online](https://vimhelp.org).
- Report missing features/bugs on [GitHub](https://github.com/NeoVintageous/NeoVintageous/issues).
* Drop-in replacement for Vintageous
- Zero configuration required

## Installation

### Package Control installation

Install NeoVintageous via [Package Control](https://packagecontrol.io/packages/NeoVintageous).

### Manual installation

Close Sublime Text, then download or clone this repository to a directory named **NeoVintageous** in the Sublime Text Packages directory for your platform:

**Linux**

`git clone https://github.com/NeoVintageous/NeoVintageous.git ~/.config/sublime-text-3/Packages/NeoVintageous`

**OSX**

`git clone https://github.com/NeoVintageous/NeoVintageous.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/NeoVintageous`

**Windows**

`git clone https://github.com/NeoVintageous/NeoVintageous.git %APPDATA%\Sublime/ Text/ 3/Packages/NeoVintageous`

## Documentation

NeoVintageous is an emulation of Vim, feature-parity is an ongoing effort, some features are not implemented or implemented fully, and differences are not fully documented. See `:help nv` to learn about some of the differences.

Vim's full documentation system is accessible via the `:help {subject}` command, and is an extensive cross-referenced and hyperlinked reference. It's kept up-to-date with the software and can answer almost any question about Vim's functionality. An up-to-date version of Vim help, with hyperlinks, can be found on [vimhelp.org](https://vimhelp.org).

## Plugins

Some popular Vim plugins have been ported and are available out-of-the-box. Feature-parity is an ongoing effort and functional differences are not always documented. Please open issues to request missing features.

| Plugin              | Status             | Original Vim plugin
| :------------------ | :----------------- | :------------------
| Abolish             | :white_check_mark: | [vim-abolish](https://github.com/tpope/vim-abolish)
| Commentary          | :white_check_mark: | [vim-commentary](https://github.com/tpope/vim-commentary)
| Highlighted Yank    | :white_check_mark: | [vim-highlightedyank](https://github.com/machakann/vim-highlightedyank)
| Indent Object       | :white_check_mark: | [vim-indent-object](https://github.com/michaeljsmith/vim-indent-object)
| Multiple Cursors    | :white_check_mark: | [vim-multiple-cursors](https://github.com/terryma/vim-multiple-cursors)
| Sneak               | :white_check_mark: | [vim-sneak](https://github.com/justinmk/vim-sneak) - disabled by default
| Surround            | :white_check_mark: | [vim-surround](https://github.com/tpope/vim-surround)
| Targets             | :white_check_mark: | [vim-targets](https://github.com/wellle/targets.vim)
| Unimpaired          | :white_check_mark: | [vim-unimpaired](https://github.com/tpope/vim-unimpaired)

**Additional plugins, install via Package Control:**

- [Files](https://packagecontrol.io/packages/NeoVintageousFiles): single key side bar and overlay file commands.
- [Highlight Line](https://packagecontrol.io/packages/NeoVintageousHighlightLine): auto disable highlight line in Insert and Visual modes.
- [Line Numbers](https://packagecontrol.io/packages/NeoVintageousLineNumbers): auto disable relative line numbers in Insert mode.

**Enhanced support, install via Package Control:**

- [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3): required for jump to lint error commands.
- [Origami](https://github.com/SublimeText/Origami): required for some window commands.

**Additional keyboard layouts, manual installation:**

- [Dvorak](https://github.com/gerardroche/NeoVintageousDvorak): Dvorak key mappings.
- [Colemak](https://github.com/gerardroche/NeoVintageousColemak): Colemak key mappings.

**Blog**

- [blog.gerardroche.com](https://blog.gerardroche.com): Releases, guides, and tips.

## Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

NeoVintageous is a fork of the discontinued Vintageous plugin.

## License

Released under the [GPL-3.0-or-later License](LICENSE).
