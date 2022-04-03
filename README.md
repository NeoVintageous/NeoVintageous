![NeoVintageous Logo](res/neovintageous.png)

<p align="center">
    <a href="https://github.com/NeoVintageous/NeoVintageous/actions/workflows/ci.yml"><img alt="Continuous Integration" src="https://github.com/NeoVintageous/NeoVintageous/actions/workflows/ci.yml/badge.svg?branch=master"></a>
    <a href="https://ci.appveyor.com/project/gerardroche/neovintageous"><img alt="Build status" src="https://ci.appveyor.com/api/projects/status/g4pkv4ws1k2r1xna?svg=true"></a>
    <a href="https://coveralls.io/github/NeoVintageous/NeoVintageous?branch=master"><img alt="Coveralls" src="https://img.shields.io/coveralls/NeoVintageous/NeoVintageous/master.svg?style=flat-square&amp;label=coveralls"></a>
    <a href="https://codecov.io/gh/NeoVintageous/NeoVintageous/branch/master"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/NeoVintageous/NeoVintageous/master?style=flat-square&amp;label=codecov"></a>
    <a href="https://packagecontrol.io/packages/NeoVintageous"><img alt="Downloads" src="https://img.shields.io/packagecontrol/dt/NeoVintageous.svg?style=flat-square"></a>
</p>

## About NeoVintageous

NeoVintageous is an advanced Vim emulation layer for Sublime Text.

* Strong defaults
* Highly configurable
* Plugins out-of-the-box
    * Abolish
    * Commentary
    * Highlighted Yank
    * Indent Object
    * Multiple cursors
    * Surround
    * Sneak (disabled by default)
    * Targets
    * Unimpaired
* Integrations: [GitGutter](https://github.com/jisaacks/GitGutter), [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3), [Origami](https://github.com/SublimeText/Origami)
* Drop-in replacement for Vintageous

## Installation

### Package Control installation

The preferred method of installation is [Package Control](https://packagecontrol.io/packages/NeoVintageous).

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

A number of popular Vim plugins have been ported and are available out-of-the-box. Feature-parity is an ongoing effort and functional differences from Vim are not always documented. Please open issues to request missing features.

Plugin | Documentation | Original Vim Plugin
------ | ------------- | -------------------
Abolish | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-abolish](https://github.com/tpope/vim-abolish)
Commentary | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-commentary](https://github.com/tpope/vim-commentary)
Highlighted Yank | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-highlightedyank](https://github.com/machakann/vim-highlightedyank)
Indent Object | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-indent-object](https://github.com/michaeljsmith/vim-indent-object)
Multiple Cursors | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-multiple-cursors](https://github.com/terryma/vim-multiple-cursors)
Surround | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-surround](https://github.com/tpope/vim-surround)
Sneak | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-sneak](https://github.com/justinmk/vim-sneak)
Targets | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-targets](https://github.com/wellle/targets.vim)
Unimpaired | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-unimpaired](https://github.com/tpope/vim-unimpaired)

## Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

NeoVintageous is a fork of the discontinued Vintageous plugin.

## License

Released under the [GPL-3.0-or-later License](LICENSE).
