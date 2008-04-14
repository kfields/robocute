
from player import *
from robocute.catalog import *

class AbstractDesignerBrain(PlayerBrain):
    def __init__(self, node):
        super(AbstractDesignerBrain, self).__init__(node)
    def build(self, item):
        cell = self.scene.get_cell_at(self.coord)
        cell.remove_node(self.node)
        self.scene.builder.produce(item.body, self.coord, cell, item)
        cell.push_node(self.node)
        
    def delete(self):
        cell = self.scene.get_cell_at(self.coord)
        if(len(cell) == 1): #that's us!!
            return
        cell.remove_node(self.node)        
        cell.remove(cell[len(cell)-1])
        cell.push_node(self.node)
        
    def can_transfer(self, node, srcCoord, dstCoord):
        #boundary check
        if(not self.scene.valid_coord(dstCoord)):
            return False
        return True
    
    def transfer(self, node, srcCoord, dstCoord):
       if(not self.can_transfer(node, srcCoord, dstCoord)):
           return False
       #else
       srcCell = self.scene.get_cell_at(srcCoord)
       srcCell.remove_node(node)
       #if(len(srcCell) == 0):
       #     print 'emptySrc'       
       #
       dstCell = self.scene.get_cell_at(dstCoord)
       #if(len(dstCell) == 0):
       #     print 'emptyDst'
       # 
       dstCell.push_node(node)
       #
       self.set_coord(dstCoord)

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

    def has_clones(self):
        return not len(self.clones) == 0
    
    def clear_clones(self):
        for clone in self.clones:
            cell = self.scene.get_cell_at(clone.coord)
            cell.remove_node(clone.node)
        self.clones = []
                
    def start(self):
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
        self.catalog = Catalog('catalog/RoboCuteCatalog.ods', build, items)
        self.drawer = self.scene.dash.create_drawer('Catalog', self.catalog)
        self.page = self.catalog.get_page('Terrain')
        self.drawer.add_node(self.page)
        
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
        if(not self.scene.valid_coord(coord)):
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
        clone = self.node.clone()
        cell = self.scene.get_cell_at(coord)
        cell.push_node(clone)
        #
        cloneBrain = clone.brain
        cloneBrain.scene = self.scene
        cloneBrain.coord = coord
        self.clones.append(cloneBrain)        
        
    def do(self, msg):
        super(DesignerBrain, self).do(msg)
        for clone in self.clones:
            clone.do(msg)