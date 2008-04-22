
import robocute.robo
from robocute.catalog import *
from robocute.ods.catalog import *
from message import *
from robocute.keyboard import *
from robocute.mouse import *

class DesignerMouseQuery(MouseQuery):
    def __init__(self, box, event):
        super(DesignerMouseQuery, self).__init__(event)
        self.box = box
        self.brain = box.brain
        
    def process(self):
        if(len(self.results) == 0):
            return
        #else
        #get last result, highest z
        result = self.results[-1]
        
        #if(not isinstance(result.node, Block)):
        #    return super(DesignerMouseQuery, self).process()
        if result.node.fn :
            return super(DesignerMouseQuery, self).process()        
        #else
        #event = self.events[0]
        event = self.event
        print result.node, event
        
        modifiers = event.modifiers
        brain = self.brain
        if modifiers & key.MOD_CTRL:
            brain.clone_at(result)
        elif  modifiers & key.MOD_SHIFT:
            brain.clear_clones()
            brain.clone_to(result)
        else:
            brain.clear_clones()
            brain.transfer_to(result)
        
class DesignerKeybox(Keybox):    
    def __init__(self, brain):
        super(DesignerKeybox, self).__init__()
        self.brain = brain
                
    def on_key_press(self, symbol, modifiers):
        brain = self.brain
        if symbol == key.ESCAPE:
            if brain.has_clones():
                brain.clear_clones()
            else:
                sys.exit()
        elif symbol == key.T:
            self.brain.take_control()
        elif symbol == key.DELETE:
            brain.do(DoDelete())
        elif symbol == key.W:
            brain.do(GoNorth())
        elif symbol == key.D:
            brain.do(GoEast())
        elif symbol == key.S:
            brain.do(GoSouth())
        elif symbol == key.A:
            brain.do(GoWest())
        else:
            super(DesignerKeybox, self).on_key_press(symbol, modifiers)

class DesignerMousebox(Mousebox):    
    def __init__(self, brain):
        super(DesignerMousebox, self).__init__()
        self.brain = brain

    def on_mouse_press(self, x, y, button, modifiers):
        super(DesignerMousebox, self).on_mouse_press(x, y, button, modifiers)
        self.brain.scene.query = DesignerMouseQuery(self, MousePressed(x, y, button, modifiers))
                    
class AbstractDesignerBrain(robocute.robo.brain.Brain):
    def __init__(self, node):
        super(AbstractDesignerBrain, self).__init__(node)
    def build(self, item):
        cell = self.grid.get_cell_at(self.coord)
        cell.remove_node(self.node)
        self.app.build(item.body, self.coord, cell, item)
        cell.push_node(self.node)
        
    def delete(self):
        cell = self.grid.get_cell_at(self.coord)
        if(len(cell) == 1): #that's us!!
            return
        cell.remove_node(self.node)        
        #cell.remove(cell[len(cell)-1])
        node = cell.pop_node()
        node.delete()
        cell.push_node(self.node)
        
    def can_transfer(self, node, srcCoord, dstCoord):
        #boundary check
        if(not self.grid.valid_coord(dstCoord)):
            return False
        return True
    
    def transfer(self, node, srcCoord, dstCoord):
       if(not self.can_transfer(node, srcCoord, dstCoord)):
           return False
       #else
       srcCell = self.grid.get_cell_at(srcCoord)
       srcCell.remove_node(node)
       #
       dstCell = self.grid.get_cell_at(dstCoord)
       # 
       dstCell.push_node(node)
       #
       self.coord = dstCoord

    def do(self, msg):
        if(isinstance(msg, DoBuild)):
           self.build(msg.item)
        elif(isinstance(msg, DoDelete)):
           self.delete()
        else:        
            super(AbstractDesignerBrain, self).do(msg)
       
       
class DesignerCloneBrain(AbstractDesignerBrain):
    def __init__(self, node):
        super(DesignerCloneBrain, self).__init__(node)

class DesignerBrain(AbstractDesignerBrain):
    def __init__(self, node):
        super(DesignerBrain, self).__init__(node)
        self.clones = []
        self.drawer = None
        self.keybox = DesignerKeybox(self)
        self.mousebox = DesignerMousebox(self)

    def bind(self, user):
        super(DesignerBrain, self).bind(user)
        self.show_dash()        
        user.add_keybox(self.keybox)
        user.add_mousebox(self.mousebox)

    def unbind(self):
        self.user.remove_keybox(self.keybox)
        self.user.remove_mousebox(self.mousebox)
        self.hide_dash()
        super(DesignerBrain, self).unbind()        

    def show_dash(self):
        if not self.drawer:
            self.create_drawer()
        self.scene.dash.add_node(self.drawer)

    def hide_dash(self):
        self.scene.dash.remove_node(self.drawer)
        
    def update_dash(self):
        pass
    
    def create_drawer(self):
        def nextPage(node):
            self.drawer.remove_node(self.page)
            self.page = self.catalog.get_next_page(self.page.name)
            self.drawer.add_node(self.page)
        def prevPage(node):
            self.drawer.remove_node(self.page)
            self.page = self.catalog.get_prev_page(self.page.name)
            self.drawer.add_node(self.page)            
        #items = [Text('Catalog')]
        items = [Image('icon/actions/1leftarrow.png', prevPage), Image('icon/actions/1rightarrow.png', nextPage)]
        
        def build(item):
            self.do(DoBuild(item))
        self.catalog = Catalog(items)
        rdr = Reader(self.catalog, 'catalog/Default.ods', build)
        rdr.read()
        
        self.drawer = self.scene.dash.create_drawer('Catalog', self.catalog)
        self.page = self.catalog.get_page('Character')
        self.drawer.add_node(self.page)
        
    def take_control(self):
        cell = self.grid.get_cell_at(self.coord)
        node = cell[-2]
        avatar = node.brain
        self.user.push_tool(avatar)
        
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
        while(r >= r2): #rows in sheet
            c = c1
            while(c <= c2): #cells in row
                #cell = self.scene.grid[r][c]
                self.clone_at(Coord(c,r))
                c += 1
            r -= 1         
        
    def filter_coord(self, coord):
        #filter invalid coord
        if(not self.grid.valid_coord(coord)):
            return False
        #filter out current coord
        if( coord.x == self.coord.x and coord.y == self.coord.y):
            return False
        #else
        return True

    def clone_at(self, coord):
        if(not self.filter_coord(coord)):
            return
        #else
        clone = self.node.clone(self.app, coord)
        cell = self.grid.get_cell_at(coord)
        cell.push_node(clone)
        #
        cloneBrain = clone.brain
        #cloneBrain.scene = self.scene
        #cloneBrain.coord = coord
        self.clones.append(cloneBrain)        
        
    def do(self, msg):
        super(DesignerBrain, self).do(msg)
        for clone in self.clones:
            clone.do(msg)
            