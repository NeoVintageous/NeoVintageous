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


class _VintageSettings():

    def __init__(self, view):
        self.view = view
        if view is not None and not isinstance(view.settings().get('vintage'), dict):
            view.settings().set('vintage', dict())

    def __getitem__(self, key: str):
        return self.view.settings().get('vintage').get(key)

    def __setitem__(self, key: str, value) -> None:
        settings = self.view.settings().get('vintage')
        settings[key] = value
        self.view.settings().set('vintage', settings)


class SettingsManager():

    def __init__(self, view):
        self.vi = _VintageSettings(view)
