# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from pyglet.window import key
#from pyglet.window.win32.constants import *
#from robocute.window.wxpython.constants import *
import wx

keymap = {
    ord('A'): key.A,
    ord('B'): key.B,
    ord('C'): key.C,
    ord('D'): key.D,
    ord('E'): key.E,
    ord('F'): key.F,
    ord('G'): key.G,
    ord('H'): key.H,
    ord('I'): key.I,
    ord('J'): key.J,
    ord('K'): key.K,
    ord('L'): key.L,
    ord('M'): key.M,
    ord('N'): key.N,
    ord('O'): key.O,
    ord('P'): key.P,
    ord('Q'): key.Q,
    ord('R'): key.R,
    ord('S'): key.S,
    ord('T'): key.T,
    ord('U'): key.U,
    ord('V'): key.V,
    ord('W'): key.W,
    ord('X'): key.X,
    ord('Y'): key.Y,
    ord('Z'): key.Z,
    ord('0'): key._0,
    ord('1'): key._1,
    ord('2'): key._2,
    ord('3'): key._3,
    ord('4'): key._4,
    ord('5'): key._5,
    ord('6'): key._6,
    ord('7'): key._7,
    ord('8'): key._8,
    ord('9'): key._9,
    ord('\b'): key.BACKSPACE,

    # By experiment:
    0x14: key.CAPSLOCK,
    0x5d: key.MENU,

#    VK_LBUTTON: , 
#    VK_RBUTTON: , 
    wx.WXK_CANCEL: key.CANCEL, 
#    wx.WXK_MBUTTON: , 
#    wx.WXK_BACK: , 
    wx.WXK_TAB: key.TAB, 
#    wx.WXK_CLEAR: , 
    wx.WXK_RETURN: key.RETURN, 
    wx.WXK_SHIFT: key.LSHIFT, 
    wx.WXK_CONTROL: key.LCTRL, 
    wx.WXK_MENU: key.LALT, 
    wx.WXK_PAUSE: key.PAUSE, 
#    wx.WXK_CAPITAL: , 
#    wx.WXK_KANA: , 
#    wx.WXK_HANGEUL: , 
#    wx.WXK_HANGUL: , 
#    wx.WXK_JUNJA: , 
#    wx.WXK_FINAL: , 
#    wx.WXK_HANJA: , 
#    wx.WXK_KANJI: , 
    wx.WXK_ESCAPE: key.ESCAPE, 
#    wx.WXK_CONVERT: , 
#    wx.WXK_NONCONVERT: , 
#    wx.WXK_ACCEPT: , 
#    wx.WXK_MODECHANGE: , 
    wx.WXK_SPACE: key.SPACE, 
    wx.WXK_PRIOR: key.PAGEUP, 
    wx.WXK_NEXT: key.PAGEDOWN, 
    wx.WXK_END: key.END, 
    wx.WXK_HOME: key.HOME, 
    wx.WXK_LEFT: key.LEFT, 
    wx.WXK_UP: key.UP, 
    wx.WXK_RIGHT: key.RIGHT, 
    wx.WXK_DOWN: key.DOWN, 
#    wx.WXK_SELECT: , 
    wx.WXK_PRINT: key.PRINT, 
#    wx.WXK_EXECUTE: , 
#    wx.WXK_SNAPSHOT: , 
    wx.WXK_INSERT: key.INSERT, 
    wx.WXK_DELETE: key.DELETE, 
    wx.WXK_HELP: key.HELP, 
    wx.WXK_WINDOWS_LEFT: key.LWINDOWS,
    wx.WXK_WINDOWS_RIGHT: key.RWINDOWS, 
#    wx.WXK_APPS: , 
    wx.WXK_NUMPAD0: key.NUM_0, 
    wx.WXK_NUMPAD1: key.NUM_1, 
    wx.WXK_NUMPAD2: key.NUM_2, 
    wx.WXK_NUMPAD3: key.NUM_3, 
    wx.WXK_NUMPAD4: key.NUM_4, 
    wx.WXK_NUMPAD5: key.NUM_5, 
    wx.WXK_NUMPAD6: key.NUM_6, 
    wx.WXK_NUMPAD7: key.NUM_7, 
    wx.WXK_NUMPAD8: key.NUM_8, 
    wx.WXK_NUMPAD9: key.NUM_9,
    #wx.WXK_SEPARATOR: , 
    
    wx.WXK_MULTIPLY: key.NUM_MULTIPLY, 
    wx.WXK_NUMPAD_MULTIPLY: key.NUM_MULTIPLY,
    
    wx.WXK_ADD: key.NUM_ADD,
    wx.WXK_NUMPAD_ADD: key.NUM_ADD,
    
    wx.WXK_SUBTRACT: key.NUM_SUBTRACT,
    wx.WXK_NUMPAD_SUBTRACT: key.NUM_SUBTRACT,
    
    wx.WXK_DECIMAL: key.NUM_DECIMAL, 
    wx.WXK_DIVIDE: key.NUM_DIVIDE, 
    wx.WXK_F1: key.F1, 
    wx.WXK_F2: key.F2, 
    wx.WXK_F3: key.F3, 
    wx.WXK_F4: key.F4, 
    wx.WXK_F5: key.F5, 
    wx.WXK_F6: key.F6, 
    wx.WXK_F7: key.F7, 
    wx.WXK_F8: key.F8, 
    wx.WXK_F9: key.F9, 
    wx.WXK_F10: key.F10, 
    wx.WXK_F11: key.F11, 
    wx.WXK_F12: key.F12, 
    wx.WXK_F13: key.F13, 
    wx.WXK_F14: key.F14, 
    wx.WXK_F15: key.F15, 
    wx.WXK_F16: key.F16, 
#    wx.WXK_F17: , 
#    wx.WXK_F18: , 
#    wx.WXK_F19: , 
#    wx.WXK_F20: , 
#    wx.WXK_F21: , 
#    wx.WXK_F22: , 
#    wx.WXK_F23: , 
#    wx.WXK_F24: , 
    wx.WXK_NUMLOCK: key.NUMLOCK, 
    wx.WXK_SCROLL: key.SCROLLLOCK, 
    #wx.WXK_LSHIFT: key.LSHIFT,
    wx.WXK_SHIFT: key.LSHIFT,
    #wx.WXK_RSHIFT: key.RSHIFT, 
    #wx.WXK_LCONTROL: key.LCTRL,
    wx.WXK_CONTROL: key.LCTRL,
    #wx.WXK_RCONTROL: key.RCTRL, 
    #wx.WXK_LMENU: key.LALT,
    wx.WXK_WINDOWS_MENU: key.LALT,
    #wx.WXK_RMENU: key.RALT, 
#    wx.WXK_PROCESSKEY: , 
#    wx.WXK_ATTN: , 
#    wx.WXK_CRSEL: , 
#    wx.WXK_EXSEL: , 
#    wx.WXK_EREOF: , 
#    wx.WXK_PLAY: , 
#    wx.WXK_ZOOM: , 
#    wx.WXK_NONAME: , 
#    wx.WXK_PA1: , 
#    wx.WXK_OEM_CLEAR: , 
#    wx.WXK_XBUTTON1: , 
#    wx.WXK_XBUTTON2: , 
#    wx.WXK_VOLUME_MUTE: , 
#    wx.WXK_VOLUME_DOWN: , 
#    wx.WXK_VOLUME_UP: , 
#    wx.WXK_MEDIA_NEXT_TRACK: , 
#    wx.WXK_MEDIA_PREV_TRACK: , 
#    wx.WXK_MEDIA_PLAY_PAUSE: , 
#    wx.WXK_BROWSER_BACK: , 
#    wx.WXK_BROWSER_FORWARD: , 
}

# Keys that must be translated via MapVirtualKey, as the virtual key code
# is language and keyboard dependent.
chmap = {
    ord('!'): key.EXCLAMATION,
    ord('"'): key.DOUBLEQUOTE,
    ord('#'): key.HASH,
    ord('$'): key.DOLLAR,
    ord('%'): key.PERCENT,
    ord('&'): key.AMPERSAND,
    ord("'"): key.APOSTROPHE,
    ord('('): key.PARENLEFT,
    ord(')'): key.PARENRIGHT,
    ord('*'): key.ASTERISK,
    ord('+'): key.PLUS,
    ord(','): key.COMMA,
    ord('-'): key.MINUS,
    ord('.'): key.PERIOD,
    ord('/'): key.SLASH,
    ord(':'): key.COLON,
    ord(';'): key.SEMICOLON,
    ord('<'): key.LESS,
    ord('='): key.EQUAL,
    ord('>'): key.GREATER,
    ord('?'): key.QUESTION,
    ord('@'): key.AT,
    ord('['): key.BRACKETLEFT,
    ord('\\'): key.BACKSLASH,
    ord(']'): key.BRACKETRIGHT,
    ord('\x5e'): key.ASCIICIRCUM,
    ord('_'): key.UNDERSCORE,
    ord('\x60'): key.GRAVE,
    ord('`'): key.QUOTELEFT,
    ord('{'): key.BRACELEFT,
    ord('|'): key.BAR,
    ord('}'): key.BRACERIGHT,
    ord('~'): key.ASCIITILDE,
}
