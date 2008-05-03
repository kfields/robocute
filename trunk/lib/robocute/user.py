#lib
from robocute.camera import *
from robocute.keyboard import *
from robocute.mouse import *
#system
import sys

from robocute.robo.message import *
from robocute.node import *
from robocute.block import *
from robocute.tool import *

from robocute.builder import build, build_thing, build_thing_at

#fudge = (0, 0)
#fudge = (50, 50) #fixme:hack for camera
fudge = (BLOCK_WIDTH * .5, BLOCK_ROW_HEIGHT * .5) #fixme:hack for camera

class UserKeybox(MultiKeybox):
    def __init__(self, user):
        super(UserKeybox, self).__init__()
        self.user = user
        win = user.window
        #
        def on_key_press(symbol, modifiers):
            self.on_key_press(symbol, modifiers)
        win.on_key_press = on_key_press

    def on_key_press(self, symbol, modifiers):
        super(UserKeybox, self).on_key_press(symbol, modifiers)
        user = self.user
        if symbol == key.NUM_ADD:
            user.camera.zoom(.1, .1)
        elif symbol == key.NUM_SUBTRACT:
            user.camera.zoom(-.1, -.1)

class UserMousebox(MultiMousebox):
    def __init__(self, user):
        super(UserMousebox, self).__init__()
        self.user = user
        win = user.window
        #
        def on_mouse_motion(x, y, dx, dy):
            self.on_mouse_motion(x, y, dx, dy)            
        win.on_mouse_motion = on_mouse_motion

        def on_mouse_press(x, y, button, modifiers):
            self.on_mouse_press(x, y, button, modifiers)        
        win.on_mouse_press = on_mouse_press

        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        win.on_mouse_drag = on_mouse_drag

    def on_mouse_motion(self, x, y, dx, dy):
        super(UserMousebox, self).on_mouse_motion(x, y, dx, dy)
        self.user.mouse.x = x
        self.user.mouse.y = y

    def on_mouse_press(self, x, y, button, modifiers):
        super(UserMousebox, self).on_mouse_press(x, y, button, modifiers)
        #self.inject(MousePressed(x, y, button, modifiers))
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super(UserMousebox, self).on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        self.user.mouse.x = x
        self.user.mouse.y = y

class User(object):
    def __init__(self, app):
        self.app = app
        win = app.window
        self.window = win        
        self.scene = app.scene
        self.world = app.world
        #
        self.keybox = UserKeybox(self)
        self.mousebox = UserMousebox(self)
        #
        self.camera = self.scene.create_camera()
        self.camera.deviceWidth = win.width
        self.camera.deviceHeight = win.height        
        #
        self.tool = None
        self.tools = []
        tool = self.create_avatar("Designer()")
        self.push_tool(tool)
        #
        win.set_mouse_visible(False)
        self.mouse = Mouse()
        self.scene.add_mouse(self.mouse)
        #
        self.coord = Coord(0,0)
    
    def bind_tool(self, tool):
        self.tool = tool        
        tool.bind(self)
        if isinstance(tool, Tool):
            return
        #else
        self.move_to(tool.coord)
        def on_tool_move():
            self.move_to(self.tool.coord)                        
        self.tool.on_move = on_tool_move

    def unbind_tool(self, tool):
        tool.unbind()
        tool.on_move = None
        
    def push_tool(self, tool):
        if not tool:
            return None
        if self.tool:
            self.unbind_tool(self.tool)
        self.tools.append(tool)
        self.bind_tool(tool)

    def pop_tool(self):
        tool = self.tools[-1]
        self.unbind_tool(tool)
        self.tools.remove(tool)
        self.tool = self.tools[-1]
        self.bind_tool(self.tool)
        return tool
        
    def add_keybox(self, box):
        self.keybox.add_box(box)
        
    def remove_keybox(self, box):
        self.keybox.remove_box(box)

    def add_mousebox(self, box):
        self.mousebox.add_box(box)
        
    def remove_mousebox(self, box):
        self.mousebox.remove_box(box)
        
    def create_avatar(self, text):
        homes = self.app.homes
        if len(homes) != 0:
            home = homes[0] #fixme:multiple homes?
        else:
            home = Coord(0,0)

        cell = self.world.get_cell_at(home)
        node = build(self.app, text, home, cell)
        if(not node):
            raise Exception('No Avatar found in scene!!!')
        brain = node.brain
        if(brain == None):
           raise Exception("This node has no brain!")
        #
        return brain
                                           
    def dispatch_events(self):
        self.window.dispatch_events()
            
    def move_to(self, coord):
        self.coord = coord
        block = self.world.get_top_block_at(coord)        
        t = self.world.get_bottom_transform_at(coord) #fixme:this really needs to be fixed!
        self.camera.look_at(t.x + fudge[0], t.y + fudge[1])
        
    