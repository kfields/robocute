# wxPython + pyglet integration, by subclassing wx.Window.
# Win32 works fine, though flickery resize.
# GDK sort of works, but keeps getting overdrawn by the window background
#   (resize to see).

import wx
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from robocute.window.wxpython.constants import *
from robocute.window.wxpython.wxkey import *

import sys

if sys.platform == 'win32':
    from pyglet.window.win32 import _user32
    from pyglet.gl import wgl
elif sys.platform == 'linux2':
    from pyglet.image.codecs.gdkpixbuf2 import gdk
    from pyglet.gl import glx

#class AbstractCanvas(pyglet.event.EventDispatcher):
class AbstractCanvas(pyglet.window.BaseWindow):
    def __init__(self, context, config):
        self._event_handlers = {}
        self._event_queue = []
        # Create context (same as pyglet.window.Window.__init__)
        if not config:
            platform = pyglet.window.get_platform()
            display = platform.get_default_display()
            screen = display.get_screens()[0]
            for template_config in [
                pyglet.gl.Config(double_buffer=True, depth_size=24),
                pyglet.gl.Config(double_buffer=True, depth_size=16)]:
                try:
                    config = screen.get_best_config(template_config)
                    break
                except pyglet.window.NoSuchConfigException:
                    pass
            if not config:
                raise pyglet.window.NoSuchConfigException(
                    'No standard config is available.')

        if not config.is_complete():
            config = screen.get_best_config(config)

        if not context:
            context = config.create_context(pyglet.gl.current_context)

        self._display = display
        self._screen = screen
        self._config = config
        self._context = context

    def on_resize(self, width, height):
        self.switch_to()
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def switch_to(self):
        self._switch_to_impl()
        self._context.set_current()
        pyglet.gl.gl_info.set_active_context()
        pyglet.gl.glu_info.set_active_context()

    def _switch_to_impl(self):
        raise NotImplementedError('abstract')

    def flip(self):
        raise NotImplementedError('abstract')
    
AbstractCanvas.register_event_type('on_draw')
AbstractCanvas.register_event_type('on_resize')

class AbstractWxCanvas(wx.Panel, AbstractCanvas):
    def __init__(self, parent, id=-1, config=None, context=None):
        wx.Window.__init__(self, parent, id, style=wx.FULL_REPAINT_ON_RESIZE)
        AbstractCanvas.__init__(self, config, context)

        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_SIZE, self._OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._OnEraseBackground)
        # Bind mouse events
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        #
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        # set the cursor for the window
        # TODO:         
        cursor = wx.StockCursor(wx.CURSOR_BLANK)    
        self.SetCursor(cursor) 
        
    def OnMotion(self, event):
        x = event.GetX()
        y = self.height - event.GetY()
        dx = 0
        dy = 0
        self.dispatch_event('on_mouse_motion', x, y, dx, dy)
        
    def OnLeftDown(self, event):
        self.SetFocus() #TODO:is this going to be a problem? 
        x = event.GetX()
        y = self.height - event.GetY()
        button = mouse.LEFT
        modifiers = 0
        self.dispatch_event('on_mouse_press', x, y, button, modifiers)
        
    def OnRightDown(self, event):
        x = event.GetX()
        y = self.height - event.GetY()
        button = mouse.RIGHT
        modifiers = 0
        self.dispatch_event('on_mouse_press', x, y, button, modifiers)

    def OnKeyDown(self, event):
        kc = event.GetKeyCode()        
        symbol = keymap.get(kc, None)
        if symbol is None:
            ch = kc #???
            symbol = chmap.get(ch)
        if symbol is None:
            symbol = key.user_key(wParam)
        modifiers = 0
        self.dispatch_event('on_key_press', symbol, modifiers)
        
    def _OnPaint(self, event):
        # wx handler for EVT_PAINT
        wx.PaintDC(self)
        self.dispatch_event('on_draw')
        self.flip()

    def _OnEraseBackground(self, event):
        pass

    def _OnSize(self, event):
        # wx handler for EVT_SIZE
        width, height = self.GetClientSize()
        self.dispatch_event('on_resize', width, height) 
    ###
    def set_size(self, width, height):
        pass    
    def get_size(self):
        return self.GetClientSize()

class Win32WxCanvas(AbstractWxCanvas):
    def __init__(self, parent, id=-1, config=None, context=None):
        super().__init__(parent, id, config, context)

        self._hwnd = self.GetHandle()
        self._dc = _user32.GetDC(self._hwnd)
        self._context._set_window(self)
        self._wgl_context = self._context._context
        self.switch_to()
         
    def _switch_to_impl(self):
        wgl.wglMakeCurrent(self._dc, self._wgl_context)

    def flip(self):
        wgl.wglSwapLayerBuffers(self._dc, wgl.WGL_SWAP_MAIN_PLANE)

class GTKWxCanvas(AbstractWxCanvas):
    _window = None

    def __init__(self, parent, id=-1, config=None, context=None):
        super().__init__(parent, id, config, context)

        self._glx_context = self._context._context
        self._x_display = self._config._display
        self._x_screen_id = self._screen._x_screen_id

        # GLX 1.3 doesn't work here (BadMatch error)
        self._glx_1_3 = False # self._display.info.have_version(1, 3)

    def _OnPaint(self, event):
        if not self._window:
            self._window = self.GetHandle()

            # Can also get the GDK window... (not used yet)
            gdk_window = gdk.gdk_window_lookup(self._window)

            if self._glx_1_3:
                self._glx_window = glx.glXCreateWindow(self._x_display,
                    self._config._fbconfig, self._window, None)
            self.switch_to()
        super()._OnPaint(event)

    def _switch_to_impl(self):
        if not self._window:
            return

        if self._glx_1_3:
            glx.glXMakeContextCurrent(self._x_display,
                self._glx_window, self._glx_window, self._glx_context)
        else:
            glx.glXMakeCurrent(self._x_display, self._window, self._glx_context)

    def flip(self):
        if not self._window:
            return

        if self._glx_1_3:
            glx.glXSwapBuffers(self._x_display, self._glx_window)
        else:
            glx.glXSwapBuffers(self._x_display, self._window)

if sys.platform == 'win32':
    WxCanvas = Win32WxCanvas
elif sys.platform == 'linux2':
    WxCanvas = GTKWxCanvas
else:
    assert False