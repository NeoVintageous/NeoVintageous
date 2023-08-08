# Contributing

- :sparkles: For a full list of supported Vim features, please refer to our [roadmap](https://github.com/NeoVintageous/NeoVintageous/blob/master/ROADMAP.md).
- :rocket: The [changelog](CHANGELOG.md) outlines the breaking/major/minor updates between releases.
- :page_facing_up: Vim's full documentation is accessible via`:help {subject}` and online at [vimhelp.org](https://vimhelp.org).
- Report missing features/bugs on [GitHub](https://github.com/NeoVintageous/NeoVintageous/issues).

## Installation

To work on the repository locally, install the package as a Git Repository. This allows you to use and work on the repository directly.

1. **Remove Existing Installation**

   1. Open Sublime Text.
   2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to open the Command Palette.
   3. Type "Package Control: Remove Package" and press `Enter`.
   4. In the input field, type "NeoVintageous" and select it from the list of available packages. If NeoVintageous is not installed, it won't appear in the list. You can skip to the next step.

2. **Git Repository Installation**

   1. Open a terminal or command prompt.
   2. Navigate to the Sublime Text Packages directory:
       - On Windows: `%APPDATA%\Sublime Text\Packages`
       - On macOS: `~/Library/Application Support/Sublime Text/Packages`
       - On Linux: `~/.config/sublime-text/Packages`
   3. Clone the plugin repository directly into the Packages directory using Git:
      ```
      git clone https://github.com/NeoVintageous/NeoVintageous.git
      ```

3. **Disabling Auto Updates for the Plugin in Package Control**

   By default, Package Control automatically updates all packages, including manually installed Git Repositories. To prevent auto-updating of a Git-installed package, follow these steps:

   1. Open Sublime Text.
   2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to open the Command Palette.
   3. Type "Preferences: Package Control Settings" and press `Enter`.
   4. Add or modify the setting "ignore_vcs_packages" to include the plugin:

      ```json
      {
         "ignore_vcs_packages": ["NeoVintageous"]
      }
      ```

      Alternatively, you can disable updating of all Git-installed plugins by setting the value to true:

      ```json
      {
         "ignore_vcs_packages": true
      }
      ```

      For more details on Package Control settings, please refer to the [Package Control documentation](https://packagecontrol.io/docs/settings).

By following these steps, you can ensure that the auto-updating behaviour of Package Control aligns with your preferences.

## Running Tests

To run tests for NeoVintageous, the [UnitTesting](https://github.com/randy3k/UnitTesting) package by the fantastic @randy3k is utilized.

Follow these steps to execute tests:

1. Install the UnitTesting package.
2. Open the Command Palette by pressing `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
3. Type "UnitTesting" and press `Enter`.
4. Enter "NeoVintageous" as the package to test and press `Enter`.

By following these instructions, you can effectively run tests for NeoVintageous using the UnitTesting package, ensuring the reliability and functionality of the plugin.

### Submitting a Pull Request

1. Ensure that the [Continuous Integration (CI)](https://github.com/NeoVintageous/NeoVintageous/actions) checks are passing successfully.
2. Follow the coding guidelines outlined by [Flake8](https://flake8.pycqa.org) to maintain code quality and consistency.

By following these steps, you contribute to the overall reliability and quality of NeoVintageous, making the PR review process smoother and enhancing the plugin's functionality.

## Debugging

Debugging NeoVintageous can be facilitated through various methods:

1. **Console Logging**: View console logging by navigating to `Menu → View → Show Console`.

2. **Command and Input Logging**: Enable command and input logging by running the following commands in the console:

   ```
   sublime.log_commands(True)
   sublime.log_input(True)
   ```

3. **Full Logging**: To enable debug logging set the following environment variable to a non-blank value or to a logging level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET.

   **Example:** Linux

   ```
   $ export SUBLIME_NEOVINTAGEOUS_DEBUG=1; subl
   ```

   Set a specific log level:

   ```
   $ export SUBLIME_NEOVINTAGEOUS_DEBUG=INFO; subl
   ```

   **Example:** Windows

   ```
   > set SUBLIME_NEOVINTAGEOUS_DEBUG=1& "C:\Program Files\Sublime Text 3\subl.exe"
   ```

   Set a specific log level:

   ```
   > set SUBLIME_NEOVINTAGEOUS_DEBUG=INFO& "C:\Program Files\Sublime Text 3\subl.exe"
   ```

By utilizing these debugging techniques, you can effectively diagnose issues and gain insights into the behaviour of NeoVintageous, facilitating the troubleshooting process.

## Reverting to a freshly installed state

See the Sublime Text documentation about [Reverting to a Freshly Installed State](https://www.sublimetext.com/docs/3/revert.html).

## Cleaning for a fresh state

For Linux and OSX you can use this [sublime-clean](https://github.com/gerardroche/dotfiles/blob/master/src/bin/sublime-clean) script. It will clean caches, indexes, workspaces, sessions, and other generated files.

## Reverting vs Cleaning

**Reverting** removes everything including installed packages and configurations.

**Cleaning** only removes files that are generated at runtime e.g. caches, indexes, sessions.
