## VintageousPlus
[![Build Status](https://travis-ci.org/trishume/VintageousPlus.svg?branch=master)](https://travis-ci.org/trishume/VintageousPlus)

**VintageousPlus** is a fork of the awesome [Vintageous](https://github.com/guillermooo/Vintageous) plugin for Sublime Text 3. The original author [@guillermooo](https://github.com/guillermooo) doesn't seem to be maintaining it anymore, so this fork steps up to merge outstanding PRs and add some new features.

I don't ever intend to merge this upstream, because I plan on adding some settings and making some changes in the spirit of Atom's [vim-mode-plus](https://github.com/t9md/atom-vim-mode-plus/wiki/YouDontKnowVimModePlus) that deviate from and improve on standard Vim behaviour when it makes sense. It's my understanding that this is contrary to @guillermooo's philosophy. The Github convention for forks that don't plan on merging is to not have it be a fork on Github, hence the fact that this isn't marked as a fork.

### Changes from Vintageous

One major change that isn't a code change is that if you submit PRs, I will review them and likely merge them. **Please help me make Vintageous better!**

#### Fixes some minor bugs

- `c_` and `d_` no longer cause an error

#### The following outstanding PRs have been merged

- [Add Support for Sublime Wrap Plus](https://github.com/guillermooo/Vintageous/pull/1077)
- [Fix interactive commands not working after mapped commands](https://github.com/guillermooo/Vintageous/pull/1042)
- [Fix for P newline pasting](https://github.com/guillermooo/Vintageous/pull/1041)
- [Settings, Menus, Run tests keymaps](https://github.com/guillermooo/Vintageous/pull/1030)
- [New text objects](https://github.com/guillermooo/Vintageous/pull/1074)

### Installing

**Make sure that Vintage
is in the `ignored_packages` list
in your user preferences.**

You can install VintageousPlus in multiple ways:

##### Package Control

I'll try and get this on Package Control soon

##### Building from Source

1. Clone this repository
2. Optionally, update to a specific tag
3. Run `./bin/build.sh` (OS X/Linux) or `bin/Publish.ps1` (Windows).

Refer to the [wiki](https://github.com/guillermooo/Vintageous/wiki) for more information.

### Settings

See [VintageousPlus/Preferences.sublime-settings](https://github.com/trishume/VintageousPlus/blob/master/Preferences.sublime-settings) for a comprehensive list of settings.
