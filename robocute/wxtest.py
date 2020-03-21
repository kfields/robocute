#!/usr/bin/python
# $Id:$

import sys
import os

import wx
import pyglet

from robocute.window.wxpython import WxCanvas
from robocute.app import App


class TestCanvas(WxCanvas):
    def __init__(self, parent, id=-1, config=None, context=None):
        super().__init__(parent, id, config, context)        
        self.app = App(self)
        self.app.on_run()
        #
        self.timer = wx.Timer(self, -1)
        self.timer.Start(100)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
                
    def OnTimer(self, event):
        self.app.step()
        
    def on_draw(self):
        #self.app.step()
        pass

    def set_mouse_visible(self, val):
        pass

    # Event dispatching
    
    def dispatch_events(self):
        self._allow_dispatch_event = True
        self.dispatch_pending_events()
        self._allow_dispatch_event = False

    def dispatch_pending_events(self):
        while self._event_queue:
            event = self._event_queue.pop(0)
            pyglet.event.EventDispatcher.dispatch_event(self, *event)
        
class TestFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(640, 480))
        self.canvas = TestCanvas(self)
        self.msgWindow = wx.TextCtrl(self, wx.ID_ANY,
                                     "Look Here for output from events\n",
                                     style = (wx.TE_MULTILINE |
                                              wx.TE_READONLY |
                                              wx.SUNKEN_BORDER)
                                     )
        
        ##Create a sizer to manage the Canvas and message window
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.canvas, 4, wx.EXPAND)
        mainSizer.Add(self.msgWindow, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(mainSizer)

class TestApp(wx.App):
    def OnInit(self):
        self.frame = TestFrame(None, 'Test wxPython + pyglet')
        self.SetTopWindow(self.frame)

        self.frame.Show(True)
        return True            
'''
if __name__ == '__main__':
    TestApp(redirect=False).MainLoop()
'''