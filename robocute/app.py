from importlib.resources import files
from random import seed

from loguru import logger
import glm

from robocute.view import GameView
from crunge.engine.app import App as CrungeApp
from crunge.engine.resource.resource_manager import ResourceManager

from robocute.game.default import DefaultGame

from robocute import globe

class App(CrungeApp):

    def __init__(self, game_name="Default"):
        super().__init__()
        globe.app = self
        self.game_name = game_name

        resource_root = files("robocute.resources")
        ResourceManager().add_path_variable("resources", resource_root)

        #
        self.homes = []
        #
        self.isRunning = False

    def setup(self):
        super().setup()

        game = self.load_or_create_game(self.game_name)
        self.game = game
        self.catalog = game.catalog
        self.world = game.world
        self.scene = game.scene
        logger.debug("Scene: {}", self.scene)

        # Temporary until we can fix camera
        #grid = self.world.get_grid(0, 0)
        #self.world.add_grid(grid)


        self.create_view()

    def create_view(self):
        self.display = GameView(self.scene)
        self.camera = self.display.camera
        #self.center_camera()
        #grid = self.world.get_grid(0, 0)

    def center_camera(self):
        if self.camera:
            ppu = self.camera.ppu
            view_width_units = self.viewport.width / ppu
            view_height_units = self.viewport.height / ppu
            self.camera.position = glm.vec2(view_width_units / 2, view_height_units / 2)

    def on_size(self):
        super().on_size()
        #self.center_camera()


    def load_or_create_game(self, game_name):
        game = self.load_game(game_name)
        if not game:
            game = self.create_game(game_name)
        return game

    def load_game(self, game_name):
        game = None
        return game

    def create_game(self, game_name):
        game = DefaultGame(self, game_name)  # fixme: Need game factory ...
        return game

    def save_game(self):
        self.game.save()

    def _ready(self):
        super()._ready()
        seed()
        #self.isRunning = True
        #
        # Create our FPS clock
        '''
        self.fps_text = pyglet.text.Label(
            "0", font_name="Verdana", font_size=28, x=self.window.width - 200, y=10
        )
        '''

    def exit(self):
        self.isRunning = False
        self.on_exit()

    def on_exit(self):
        self.game.save()

    """
    Avatar Support
    """

    def add_home(self, home, coord):
        self.homes.append(coord)

    '''
    def run(self):
        self.on_run()
        #
        """
        while not self.window.has_exit and self.isRunning:
            self.update()
        """
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        pyglet.app.run()
    '''

    '''
    def update(self, dt):
        scene = self.scene
        user = self.user
        fps_text = self.fps_text
        #
        worldGraphics = user.camera.graphics
        layerGraphics = Graphics()
        #
        # user.dispatch_events()
        #
        dt = clock.tick()
        #
        # win.clear()
        #
        scene.draw(layerGraphics, worldGraphics)
        #
        # fps_text.text = ("fps: %d") % (clock.get_fps())
        # fps_text.draw()
        #
        # win.flip()
        #
        if len(self.callbacks) != 0:
            for callback in self.callbacks:
                callback()
            self.callbacks = []
    '''