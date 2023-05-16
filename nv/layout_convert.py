import sublime
import sublime_plugin
statusName = '07_NeoVintageous' # number defines the order of custom status bar statuses

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

import time, threading
class LogToStatus:
  def __init__(self):
    self.timeout  = 3
    self.timer    = None
    self.tag      = statusName

  def s(self, view, msg, overwrite=False):
    self.set_status(view, msg, overwrite)
  def set_status(self, view, msg, overwrite=False):
    self.cancel_timer()
    self.view = view
    if overwrite:
      self.view.set_status(self.tag, msg)
    else:
      status_cur  = view.get_status(self.tag)
      sep         = '; ' if status_cur else ''
      self.view.set_status(self.tag, status_cur +sep+ msg)
    self.start_timer()

  def cancel_timer(self):
    if self.timer != None:
      self.timer.cancel()

  def start_timer(self):
    self.timer = threading.Timer(self.timeout, self.clear)
    self.timer.start()

  def clear(self):
    self.view.erase_status(self.tag)
_l = LogToStatus()


import re
def getUserKeymap(keymap_len):
  view        = sublime.active_window().active_view()
  cfg         = view.settings()
  cfg_key     = 'neo_vintageous'
  cfg_key_map = 'keymap'
  cfg_key_low = 'lower'
  cfg_key_upp = 'upper'
  nv_cfg      = cfg.get(cfg_key)

  if not nv_cfg:
    msg_error = f"no '{cfg_key}' setting value in 'Preferences.sublime-settings'"
    log.error(msg_error); _l.s(view, msg_error)
    return
  if not isinstance(nv_cfg, dict):
    msg_error = f"'{cfg_key}' setting should be a dictionary, not {type(nv_cfg)} (in 'Preferences.sublime-settings')"
    log.error(msg_error); _l.s(view, msg_error)
    return
  if not cfg_key_map in nv_cfg:
    msg_error = f"'{cfg_key}' setting has no '{cfg_key_map}' field (in 'Preferences.sublime-settings')"
    log.error(msg_error); _l.s(view, msg_error)
    return
  keymap = nv_cfg[cfg_key_map]
  if not 'upper' in keymap:
    msg_error = f"'{cfg_key}' → '{cfg_key_map}' setting has no 'upper' field (in 'Preferences.sublime-settings')"
    log.error(msg_error); _l.s(view, msg_error)
    return
  if not cfg_key_low in keymap:
    msg_error = f"'{cfg_key}' → '{cfg_key_map}' setting has no '{cfg_key_low}' field (in 'Preferences.sublime-settings')"
    log.error(msg_error); _l.s(view, msg_error)
    return
  low = re.sub(r'\s','',keymap[cfg_key_low])
  upp = re.sub(r'\s','',keymap[cfg_key_upp])
  if not (ln := len(low)) == keymap_len:
    msg_error = f"'{cfg_key}' → '{cfg_key_map}' → '{cfg_key_low}' setting should have '{keymap_len}' characters, not '{ln}' (in 'Preferences.sublime-settings')"
    log.error(msg_error); _l.s(view, msg_error)
    return
  if not (ln := len(upp)) == keymap_len:
    msg_error = f"'{cfg_key}' → '{cfg_key_map}' → '{cfg_key_upp}' setting should have '{keymap_len}' characters, not '{ln}' (in 'Preferences.sublime-settings')"
    log.error(msg_error); _l.s(view, msg_error)
    return

  return({"low":low,"upp":upp})

class Symbol:
  def __init__(self, name=''):
    self.name = f"Symbol({name})"
  def __repr__(self):
    return self.name

from enum import Enum
class lyt(Enum):
  qwerty      = Symbol('qwerty')
  dvorak      = Symbol('dvorak')
  colemak     = Symbol('colemak')
  workman     = Symbol('workman')
  asset       = Symbol('asset')
  colemak_dh  = Symbol('colemak_dh')
  neo2        = Symbol('neo2')
  ru_pc       = Symbol('ru_pc')
  ru_mac      = Symbol('ru_mac')
  user        = Symbol('user')

class LayoutConverter:
  def __init__(self):
    layout_str        = {
      lyt.qwerty      :{'low' : R'''`1234567890-=\ qwertyuiop[] asdfghjkl;' zxcvbnm,./'''
       ,                'upp' : R'''~!@#$%^&*()_+| QWERTYUIOP{} ASDFGHJKL:" ZXCVBNM<>?'''},
      lyt.dvorak      :{'low' : R'''`1234567890[]\ ',.pyfgcrl/= aoeuidhtns- ;qjkxbmwvz'''
       ,                'upp' : R'''~!@#$%^&*(){}| "<>PYFGCRL?+ AOEUIDHTNS_ :QJKXBMWVZ'''},
      lyt.colemak     :{'low' : R'''`1234567890-=\ qwfpgjluy;[] arstdhneio' zxcvbkm,./'''
       ,                'upp' : R'''~!@#$%^&*()_+| QWFPGJLUY:{} ARSTDHNEIO" ZXCVBKM<>?'''},
      lyt.workman     :{'low' : R'''`1234567890-=\ qdrwbjfup;[] ashtgyneoi' zxmcvkl,./'''
       ,                'upp' : R'''~!@#$%^&*()_+| QDRWBJFUPP{} ASHTGYNEOI" ZXMCVKL<>?'''},
      lyt.asset       :{'low' : R'''`1234567890-=\ qwjfgypul;[] asetdhnior' zxcvbkm,./'''
       ,                'upp' : R'''~!@#$%^&*()_+| QWJFGYPUL;{} ASETDHNIO:" ZXCVBKM<>?'''},
      lyt.colemak_dh  :{'low' : R'''`1234567890-=\ qwfpbjluy;[] arstgkneio' zxcdvmh,./'''
       ,                'upp' : R'''~!@#$%^&*()_+| QWFPBJLUY:{} ARSTGKNEIO" ZXCDVMH<>?'''},
      lyt.neo2        :{'low' : R'''^1234567890-`\ xvlcwkhgfqß´ uiaeosnrtdy üöäpzbm,.j'''
       ,                'upp' : R'''ˇ°§ℓ»«$€„“”—¸| XVLCWKHGFQẞ˜ UIAEOSNRTDY ÜÖÄPZBM–•J'''},
      lyt.ru_pc       :{'low' : R'''ё1234567890-=\ йцукенгшщзхъ фывапролджэ ячсмитьбю.'''
       ,                'upp' : R'''Ё!"№;%:?*()_+/ ЙЦУКЕНГШЩЗХЪ ФЫВАПРОЛДЖЭ ЯЧСМИТЬБЮ,'''},
      lyt.ru_mac      :{'low' : R''']1234567890-=ё йцукенгшщзхъ фывапролджэ ячсмитьбю/'''
       ,                'upp' : R'''[!"№;%,.;()_+Ё ЙЦУКЕНГШЩЗХЪ ФЫВАПРОЛДЖЭ ЯЧСМИТЬБЮ?'''},
    }
    for k,v in layout_str.items():
      v['low'] = v['low'].replace(' ','')
      v['upp'] = v['upp'].replace(' ','')
    keymap_len  = len(layout_str[lyt.qwerty]['low'])

    userKeymap = getUserKeymap(keymap_len)
    if userKeymap:
      layout_str[lyt.user] = userKeymap
      self.isUser = True

    translations = dict() # generate translation dictionaries for use in str.translate(dict)
    for   layout_from in layout_str:
      translations[layout_from] = dict()
      for layout_to   in layout_str:
        string_from = layout_str[layout_from  ]['low'] + layout_str[layout_from ]['upp']
        string_to   = layout_str[layout_to    ]['low'] + layout_str[layout_to   ]['upp']
        translations[layout_from][layout_to] =  str.maketrans(string_from, string_to)
    self.layout_str   = layout_str
    self.layouts      = list(layout_str.keys())
    self.translations = translations

  def convert(self, src, layout_from, layout_to):
    view          = sublime.active_window().active_view()
    translations  = self.translations
    layouts       = self.layouts
    if not layout_from in layouts: # todo: or fail silently and return src?
      msg_error = f"'{layout_from}' invalid, must be one of '{layouts}')"
      log.error(msg_error); _l.s(view, msg_error)
      return None
    if not layout_to   in layouts:
      msg_error = f"'{layout_to}' invalid, must be one of '{layouts}')"
      log.error(msg_error); _l.s(view, msg_error)
      return None
    return src.translate(translations[layout_from][layout_to])
