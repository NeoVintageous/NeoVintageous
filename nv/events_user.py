import os
import subprocess
import logging

from pathlib import Path

import sublime

from NeoVintageous.nv.vim import INSERT, INTERNAL_NORMAL, NORMAL, OPERATOR_PENDING, REPLACE, SELECT, UNKNOWN, VISUAL, VISUAL_BLOCK, VISUAL_LINE
from NeoVintageous.plugin import cfgU

__all__ = ['NeoVintageousEventsUser'] # User events: run cli commands on mode changes

PLATFORM = sublime.platform()
_log = logging.getLogger(__name__)

event_modes = {
    INSERT      	: 'Insert'
  , NORMAL      	: 'Normal'
  , REPLACE     	: 'Replace'
  , SELECT      	: 'Select'
  , VISUAL      	: 'Visual'
  , VISUAL_BLOCK	: 'VisualBlock'
  , VISUAL_LINE 	: 'VisualLine'
  }

def get_full_cmd(eventsU, event_name) -> list:
  if type(eventsU) is dict:
    eventsU_or_OS = None
    if PLATFORM in eventsU:
      if type(eventsU_OS := eventsU[PLATFORM]) is dict:
        eventsU_or_OS = eventsU_OS
    else:
      eventsU_or_OS   = eventsU
    if eventsU_or_OS and event_name in eventsU_or_OS:
      full_cmd = eventsU_or_OS[event_name]
      if   type(full_cmd) is list:
        return  full_cmd
      elif type(full_cmd) is str: # "path" → ["path"]
        return [full_cmd]

def on_mode_change  (view   , current_mode, new_mode) -> None:
  from NeoVintageous.plugin import cfgU
  _log.debug(f"mode Δ {current_mode} ⟶ {new_mode}")
  if not hasattr(cfgU, 'events'):
    return
  if not (eventsU := cfgU.events):
    return
  _log.debug(f"user events = {eventsU}")
  for mode, mode_cfg_name in event_modes.items():
    event_name = None
    if current_mode == mode:
      event_name = f'{mode_cfg_name}Leave'
    if new_mode     == mode:
      event_name = f'{mode_cfg_name}Enter'
    if event_name:
      if (full_cmd := get_full_cmd(eventsU, event_name)):
        run_command(full_cmd, current_mode, new_mode)

def run_command    (full_cmd, current_mode, new_mode) -> None:
  _log.debug(f"full_cmd = {full_cmd}")
  if (bin_path := Path(full_cmd[0]).expanduser()).exists():
    proc  = subprocess.run([bin_path] + full_cmd[1:],capture_output=True)
    out   = proc.stdout.decode().rstrip('\n')
    err   = proc.stderr.decode().rstrip('\n')
    retn  = proc.returncode
    if err:
      print(f"NeoVintageous ERROR while Δ mode ‘{current_mode}’ ⟶ ‘{new_mode}’\n and running ‘{full_cmd}’\n{err}")
  else:
    print(f"NeoVintageous ERROR while Δ mode ‘{current_mode}’ ⟶ ‘{new_mode},’\n executable does NOT exist: ‘{bin_path}’")
