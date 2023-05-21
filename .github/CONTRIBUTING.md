# CONTRIBUTING

## Documentation

You can open the built-in help file by running `:help nv` and [view it online](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt).

## Debugging

### Console

To view console logging: **Menu → View → Show Console**

### Performance

To view plugin performance: **Menu → Tools → Developer → Profile Plugins**

### Logging

To enable Sublime Text command and input logging run the following in the console:

```
sublime.log_commands(True)
sublime.log_input(True)
```

To enable NeoVintageous logging set the environment variable `SUBLIME_NEOVINTAGEOUS_DEBUG`:

Linux

```
$ export SUBLIME_NEOVINTAGEOUS_DEBUG=y; subl
```

Windows

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

## Testing

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press `Enter`, and input **"NeoVintageous"** as the package to test.
