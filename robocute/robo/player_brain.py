import random

from loguru import logger

from crunge.engine.scheduler import Scheduler
import robocute.robo.brain
from robocute.robo.avatar import *
from robocute.widget import DashBubble, Text, Image, ItemImage
from robocute.item import *
from robocute.block import *


class State:
    """
    One step of the player's turn loop.

    Phases are dispatched to `on_<key>` methods. Every task a state schedules is
    tracked and cancelled when the brain transitions away, so delayed messages
    from an old state can never land in a new one.
    """

    initial_phase = "enter"

    def __init__(self, brain):
        self.brain = brain
        brain.state = self
        self.phase = Phase(self.initial_phase)
        self.tasks = []

    # Entering the state runs its initial phase.
    def __call__(self):
        self.do(self.phase)

    @property
    def active(self):
        return self.brain.state is self

    def do(self, phase):
        # Ignore phases from stale UI callbacks (e.g. clicking an old bubble icon).
        if not self.active:
            return
        handler = getattr(self, f"on_{phase.key}", None)
        if handler is None:
            logger.warning(f"{type(self).__name__} has no handler for phase '{phase.key}'")
            return
        handler()

    def schedule(self, msg, seconds=0.0):
        if not self.active:
            return None
        task = self.brain.schedule(msg, seconds)
        self.tasks = [t for t in self.tasks if not t.cancelled]
        self.tasks.append(task)
        return task

    def cancel_tasks(self):
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()

    def say(self, *parts):
        self.brain.do(Say(list(parts)))

    def i_love_pyweek(self):
        self.say(Text("I "), Image("Heart.png"), Text(" PyWeek!!! "))


class StartState(State):
    def on_enter(self):
        self.say(Text("Welcome to RoboCute!"))
        self.schedule(Phase("explain"), 3.0)

    def on_explain(self):
        self.say(Text("Click icons to do stuff!"))
        self.schedule(Phase("play"), 3.0)

    def on_play(self):
        def on_click(_):
            self.schedule(Transition("main"), 0.5)

        self.say(Text("Let's play!"), Image("icon/actions/lc_browseforward.png", on_click))


class MainState(State):
    def __init__(self, brain):
        super().__init__(brain)
        self.rolled = False

    def on_enter(self):
        self.brain.update_dash()
        self.say(
            Text("Roll!"),
            Image("icon/d12_128x128.png", lambda _: self.do(Phase("roll"))),
        )

    def on_roll(self):
        if self.rolled:  # One roll per turn, however many times the die is clicked
            return
        self.rolled = True
        die = random.randint(1, 12)
        self.brain.die = die
        self.say(Text(f"You rolled a {die}!"))
        self.schedule(Transition("move"), 2.0)


class MoveState(State):
    def __init__(self, brain):
        super().__init__(brain)
        self.count = 0

    def on_enter(self):
        self.count = 0
        self.schedule(Phase("move"))

    def on_move(self):
        self.count += 1
        if self.count > self.brain.die:
            self.schedule(Transition("land"), 1.0)
            return

        vacancies = self.brain.find_vacancies()
        if vacancies:
            target = random.choice(vacancies)
        else:  # Dead end: back up the way we came
            target = self.brain.old_coord

        if target is not None:
            self.brain.move_to(target)

        self.say(Text(str(self.count)))
        self.schedule(Phase("move"), 0.5)


class LandState(State):
    def __init__(self, brain):
        super().__init__(brain)
        self.item = None

    def on_enter(self):
        items = self.brain.search_for_items()
        if not items:
            self.schedule(Phase("exit"))
            return
        self.brain.take_items(items)
        # Only one item per block for now.
        self.item = items[0]
        #self.say(Text(f"We found a {self.item.name}!"), self.item)
        self.say(Text(f"We found a {self.item.name}!"), ItemImage(self.item.dna))
        self.schedule(Phase("take_item"), 2.0)

    def on_exit(self):
        self.schedule(Transition("main"))

    def on_take_item(self):
        if isinstance(self.item, Treasure):
            self.take_treasure()
        self.schedule(Transition("main"), 1.0)

    def take_treasure(self):
        self.say(Text("Kaching!"))
        self.brain.worth += self.item.worth
        self.brain.update_dash()


class PlayerKeybox(AvatarKeybox):
    pass


class PlayerMousebox(AvatarMousebox):
    pass


class PlayerBrain(robocute.robo.brain.RoboBrain):
    states = {
        "start": StartState,
        "main": MainState,
        "move": MoveState,
        "land": LandState,
    }

    def __init__(self):
        super().__init__()
        self.keybox = PlayerKeybox(self)
        self.mousebox = PlayerMousebox(self)
        self.die = 0
        self.worth = 0  # Total treasure value
        self.dash_bubble = None
        self.dash_worth = Text(str(self.worth))
        self._started = False
        self.state = StartState(self)

    # ---------------------------------------------------------------- binding

    def bind(self, user):
        super().bind(user)
        self.show_dash()
        user.add_keybox(self.keybox)
        user.add_mousebox(self.mousebox)

    def unbind(self):
        if self.state:
            self.state.cancel_tasks()
        self.hide_dash()
        user = self.view
        user.remove_keybox(self.keybox)
        user.remove_mousebox(self.mousebox)
        super().unbind()

    # ------------------------------------------------------------------- dash

    def show_dash(self):
        if not self.dash_bubble:
            self.dash_bubble = DashBubble([Image("Mini Chest.png"), self.dash_worth])
        self.view.dash.add_node(self.dash_bubble)
        self.update_dash()

    def hide_dash(self):
        if self.dash_bubble:
            self.view.dash.remove_node(self.dash_bubble)

    def update_dash(self):
        if not self.dash_bubble:
            return
        self.dash_worth.vu.text.text = str(self.worth)
        self.dash_bubble.vu.validate()

    # ------------------------------------------------------------- messaging

    def start(self):
        # Moving between cells re-parents the node, which can re-fire the
        # owner's ready hook. Only the first start should enter the state.
        if self._started:
            return
        self._started = True
        self.state()

    def schedule(self, msg, seconds=0.0):
        """Deliver `msg` to this brain after `seconds` of game time. Returns the Task."""
        return Scheduler().schedule_once(lambda _elapsed: self.do(msg), seconds)

    def do(self, msg):
        if isinstance(msg, Phase):
            self.state.do(msg)
        elif isinstance(msg, Transition):
            self.do_transition(msg)
        else:
            super().do(msg)

    def do_transition(self, transition):
        state_cls = self.states.get(transition.key)
        if state_cls is None:
            logger.warning(f"Unknown transition '{transition.key}'")
            return
        if self.state:
            self.state.cancel_tasks()
        state_cls(self)()

    # --------------------------------------------------------------- movement

    def find_vacancies(self):
        """Orthogonal neighbours that are on the grid, not where we just were, and open."""
        x, y = self.coord.x, self.coord.y
        vacancies = []
        for coord in (Coord(x, y - 1), Coord(x - 1, y), Coord(x + 1, y), Coord(x, y + 1)):
            if not self.filter_coord(coord):
                continue
            block = self.grid.get_top_block_at(coord)
            if block and block.vacancy:
                vacancies.append(coord)
        return vacancies

    def filter_coord(self, coord):
        if not self.grid.valid_coord(coord):
            return False
        if coord.x == self.coord.x and coord.y == self.coord.y:
            return False
        old = self.old_coord
        if old is not None and coord.x == old.x and coord.y == old.y:
            return False
        return True

    def move_to(self, new_coord):
        self.del_bubble()
        moved = self.transfer(self.node, self.coord, new_coord)
        # Always notify the camera: re-centring after a blocked move is a no-op,
        # and it doesn't depend on transfer() returning a value.
        if self.on_move:
            self.on_move()
        return moved

    # ------------------------------------------------------------------ items

    def search_for_items(self):
        block = self.grid.get_top_block_at(self.coord)
        if not isinstance(block, GroupBlock):
            return []
        return [node for node in block.nodes if isinstance(node, Item)]

    def take_items(self, items):
        cell = self.grid.get_cell_at(self.coord)
        for item in items:
            cell.remove_node(item)