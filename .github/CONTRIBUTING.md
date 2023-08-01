# Contributing

- :sparkles: For a full list of supported Vim features, please refer to our [roadmap](https://github.com/NeoVintageous/NeoVintageous/blob/master/ROADMAP.md).
- :rocket: The [changelog]() outlines the breaking/major/minor updates between releases.
- :page_facing_up: Vim's full documentation is accessible via`:help {subject}` and online at [vimhelp.org](https://vimhelp.org).
- Report missing features/bugs on [GitHub](https://github.com/NeoVintageous/NeoVintageous/issues).

## Running the tests

The [UnitTesting](https://github.com/randy3k/UnitTesting) package by the awesome @randy3k is used to run the tests.

- Install UnitTesting
- Open the Command Palette, type "UnitTesting", press `Enter`
- Type "NeoVintageous" as the package to test, press `Enter`

### When submitting a Pull Request

- Please make sure [CI](https://github.com/NeoVintageous/NeoVintageous/actions) is passing.
- [Flake8](https://flake8.pycqa.org) is used for coding guidelines.

## Debugging

To view console logging: Menu → View → Show Console

To enable command and input logging run the following in the console:

```
sublime.log_commands(True)
sublime.log_input(True)
```

To enable full logging set the environment variable `SUBLIME_NEOVINTAGEOUS_DEBUG`:

**Example:** Linux

```
$ export SUBLIME_NEOVINTAGEOUS_DEBUG=y; subl
```

**Example:** Windows

```
> set SUBLIME_NEOVINTAGEOUS_DEBUG=y& "C:\Program Files\Sublime Text 3\subl.exe"
```

## Reverting to a freshly installed state

See [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation).

## Cleaning for a fresh state

For Linux and OSX you can use this [sublime-clean](https://github.com/gerardroche/dotfiles/blob/master/src/bin/sublime-clean) script. It will clean caches, indexes, workspaces, sessions, and other generated files.

### Reverting vs Cleaning

**Reverting** removes everything including installed packages and configurations.

**Cleaning** only removes files that are generated at runtime e.g. caches, indexes, sessions.
