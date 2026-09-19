from robocute.widget.catalog import *
from robocute.robo.message import *
from robocute.robo.avatar import *
from robocute.tool import *

from robocute.builder import build, build_thing, build_thing_at

from ..widget import Image

from .brain import RoboBrain

class DesignerMouseQuery(MouseQuery):
    def __init__(self, box, event):
        super().__init__(event)
        self.box = box
        self.brain = box.brain

    def process(self):
        if len(self.results) == 0:
            return
        # else
        # get last result, highest z
        result = self.results[-1]

        if result.node.fn:
            return super().process()
        # else
        event = self.event
        print(result.node, event)

        modifiers = event.modifiers
        brain = self.brain
        if modifiers & key.MOD_CTRL:
            brain.clone_at(result)
        elif modifiers & key.MOD_SHIFT:
            brain.clear_clones()
            brain.clone_to(result)
        else:
            brain.clear_clones()
            brain.transfer_to(result)


class DesignerKeybox(AvatarKeybox):
    def on_key_press(self, symbol, modifiers):
        brain = self.brain
        if symbol == key.ESCAPE:
            if brain.has_clones():
                brain.clear_clones()
            else:
                brain.exit()
        elif symbol == key.T:
            self.brain.take_control()
        elif symbol == key.DELETE:
            brain.do(DoDelete())
        else:
            super().on_key_press(symbol, modifiers)


class DesignerMousebox(AvatarMousebox):
    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        self.brain.scene.query = DesignerMouseQuery(
            self, MousePressed(x, y, button, modifiers)
        )


class BaseDesignerBrain(RoboBrain):
    def build(self, dna):
        cell = self.node.grid.get_cell_at(self.coord)
        cell.remove_node(self.node)
        build_thing_at(self.app, dna, self.coord, cell)
        cell.push_node(self.node, self.coord)

    def delete(self):
        cell = self.grid.get_cell_at(self.coord)
        if len(cell) == 1:  # that's us!!
            return
        cell.remove_node(self.node)
        node = cell.pop_node()
        node.delete()
        cell.push_node(self.node, self.coord)

    def can_transfer(self, node, srcCoord, dstCoord):
        # boundary check
        if not self.grid.valid_coord(dstCoord):
            return False
        return True

    def transfer(self, node, srcCoord, dstCoord):
        if not self.can_transfer(node, srcCoord, dstCoord):
            return False
        # else
        srcCell = self.grid.get_cell_at(srcCoord)
        srcCell.remove_node(node)
        #
        dstCell = self.grid.get_cell_at(dstCoord)
        dstCell.push_node(node, dstCoord)
        #
        #self.coord = dstCoord

    def do(self, msg):
        if isinstance(msg, DoBuild):
            self.build(msg.dna)
        elif isinstance(msg, DoDelete):
            self.delete()
        else:
            super().do(msg)


class DesignerCloneBrain(BaseDesignerBrain):
    def __init__(self):
        super().__init__()


class DesignerBrain(BaseDesignerBrain):
    def __init__(self):
        super().__init__()
        self.clones = []
        self.drawer = None
        self.keybox = DesignerKeybox(self)
        self.mousebox = DesignerMousebox(self)
        #
        self.avatar = None  # avatar that we passed control to.

    @property
    def dash(self):
        return self.view.dash

    def exit(self):
        self.clear_clones()
        self.hide_node()
        self.app.exit()

    def bind(self, view):
        super().bind(view)
        self.show_dash()
        #
        if self.avatar:
            self.release_control()

    def unbind(self):
        self.hide_dash()
        #
        if self.avatar:
            self.hide_node()
        super().unbind()

    def show_dash(self):
        if not self.drawer:
            self.create_drawer()

    def hide_dash(self):
        self.dash.remove_child(self.drawer)

    def update_dash(self):
        pass

    def create_drawer(self):
        def next_page(node):
            self.dash.remove_child(self.page)
            self.page = self.catalog_bubble.get_next_page(self.page.name)
            self.dash.add_child(self.page)

        def prev_page(node):
            self.dash.remove_child(self.page)
            self.page = self.catalog_bubble.get_prev_page(self.page.name)
            self.dash.add_child(self.page)

        items = [
            Image("icon/actions/1leftarrow.png", prev_page),
            Image("icon/actions/1rightarrow.png", next_page),
        ]

        def on_item(item):
            if item.dna.type == "tool":
                exit()
                self.build_tool(item.dna)
            else:
                self.do(DoBuild(item.dna))

        self.app.catalog.on_item = on_item

        self.catalog_bubble = CatalogBubble(items, self.app.catalog)

        self.drawer = self.dash.create_drawer("Catalog", self.catalog_bubble)
        self.page = self.catalog_bubble.get_page("Main")

        self.dash.add_child(self.drawer)
        self.dash.add_child(self.page)

    def take_control(self):
        # self.hide_node()
        #
        cell = self.grid.get_cell_at(self.coord)
        node = cell[-2]
        # node = cell[-1]
        self.avatar = node.brain
        self.view.push_tool(self.avatar)

    def release_control(self):
        self.coord = self.avatar.coord
        self.show_node()
        self.avatar = None

    def show_node(self):
        cell = self.grid.get_cell_at(self.coord)
        cell.push_node(self.node)

    def hide_node(self):
        cell = self.grid.get_cell_at(self.coord)
        cell.remove_node(self.node)

    def has_clones(self):
        return not len(self.clones) == 0

    def clear_clones(self):
        for clone in self.clones:
            cell = self.grid.get_cell_at(clone.coord)
            cell.remove_node(clone.node)
        self.clones = []

    def start(self):
        pass

    def clone_to(self, coord):
        myCoord = self.coord
        #
        r1 = myCoord.y
        #
        r2 = coord.y
        #
        c1 = myCoord.x
        #
        c2 = coord.x
        #
        r = r1
        while r >= r2:  # rows in sheet
            c = c1
            while c <= c2:  # cells in row
                # cell = self.scene.grid[r][c]
                self.clone_at(Coord(c, r))
                c += 1
            r -= 1

    def filter_coord(self, coord):
        # filter invalid coord
        if not self.grid.valid_coord(coord):
            return False
        # filter out current coord
        if coord.x == self.coord.x and coord.y == self.coord.y:
            return False
        # else
        return True

    def clone_at(self, coord):
        if not self.filter_coord(coord):
            return
        # else
        clone = self.node.clone(self.app, coord)
        cell = self.grid.get_cell_at(coord)
        cell.push_node(clone)
        #
        cloneBrain = clone.brain
        # cloneBrain.scene = self.scene
        # cloneBrain.coord = coord
        self.clones.append(cloneBrain)

    def do(self, msg):
        super().do(msg)
        for clone in self.clones:
            clone.do(msg)

    def build_tool(self, dna):
        tool = build_thing(dna, self.app)
        self.view.push_tool(tool)
