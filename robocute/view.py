
from loguru import logger

from crunge import sdl

from crunge.engine.d2.view import SceneView2D
from crunge.engine.d2.scene import Scene2D
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.overlay import Overlay
from crunge.core.dispatch import DispatchResult, EVENT_HANDLED

from robocute import globe
from robocute.dash import Dash
from .base import Coord
from .tool import Tool
from .builder import build
from .block import BLOCK_WIDTH, BLOCK_ROW_HEIGHT
from .camera import GameCamera

fudge = (BLOCK_WIDTH * 0.5, BLOCK_ROW_HEIGHT * 0.5)  # fixme:hack for camera


class BubbleLayer(Overlay):
    def __init__(self, name):
        super().__init__(name)


class MouseLayer(Overlay):
    def __init__(self, name):
        super().__init__(name)


class GameView(SceneView2D):
    def __init__(self, scene: Scene2D) -> None:
        super().__init__(scene)
        globe.view = self
        self.bubbles: BubbleLayer = None
        self.dash: Dash = None
        self.mice: MouseLayer = None
        self.app = globe.app
        self.world = self.app.world
        #
        self.tool = None
        self.tools = []
        #
        # win.set_mouse_visible(False)
        # self.mouse = Mouse()
        # self.scene.add_mouse(self.mouse)
        #
        self.coord = Coord(0, 0)

    def create_camera(self):
        self.camera = GameCamera()

    def _create(self):
        super()._create()
        self.bubbles = self.add_overlay(BubbleLayer("bubbles"))
        #
        self.dash = self.add_overlay(Dash("dash"))
        #
        self.mice = self.add_overlay(MouseLayer("mice"))
        #
        self.query = None

    def _enable(self):
        super()._enable()
        tool = self.create_avatar("Designer()")
        self.push_tool(tool)

    def dispatch(self, event) -> DispatchResult:
        # The widget tree gets first refusal, then the active avatar's
        # controller. Avatars live in the scene rather than the widget tree,
        # so nothing reaches them through the normal structural walk.
        if super().dispatch(event):
            return EVENT_HANDLED
        tool = self.tool
        # logger.debug(f"Dispatching event to tool: {tool}")
        result = bool(
            tool and tool.dispatch(event)
        )
        # logger.debug(f"Event dispatch result: {result}")
        return result

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        # logger.debug(f"{self.title}:on_mouse_wheel")
        self.camera.zoom_pct = self.camera.zoom_pct + event.y * 10

    def bind_tool(self, tool: Tool):
        self.tool = tool
        tool.bind(self)
        if isinstance(tool, Tool):
            return

        # else
        def on_tool_move():
            self.move_to(self.tool.coord)

        self.tool.on_move = on_tool_move

    def unbind_tool(self, tool: Tool):
        tool.unbind()
        tool.on_move = None

    def push_tool(self, tool: Tool):
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

    def create_avatar(self, text: str):
        homes = self.app.homes
        if len(homes) != 0:
            home = homes[0]  # fixme:multiple homes?
        else:
            home = Coord(0, 0)

        cell = self.world.get_cell_at(home)
        node = build(self.app, text, home, cell)
        logger.debug(f"Created avatar node: {node} at {home}")
        if not node:
            raise Exception("No Avatar found in scene!!!")
        brain = node.brain
        if brain == None:
            raise Exception("This node has no brain!")
        #
        return brain

    def move_to(self, coord):
        self.coord = coord
        block = self.world.get_top_block_at(coord)
        t = self.world.get_bottom_transform_at(
            coord
        )  # fixme:this really needs to be fixed!
        self.camera.look_at(t.x + fudge[0], t.y + fudge[1])
