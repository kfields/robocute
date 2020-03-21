
import pyglet
from pyglet.gl import *

from base import *

QUAD_SW = 0
QUAD_SE = 1
QUAD_NE = 2
QUAD_NW = 3

'''
Quad
'''
class Quad(Base):
    def __init__(self, texture):
        super().__init__()
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.vertices = None
        #self.indices = [None] * 4
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        #            
        self.validate()
    
    def get_tex_coord(self, ndx):
        tex_coords = self.texture.tex_coords
        u = tex_coords[ndx * 3]
        v = tex_coords[ndx * 3 + 1]
        r = tex_coords[ndx * 3 + 2]
        return (u, v, r)
        
    def validate(self):
        super().validate()

    '''
    Compose
    '''         

    def compose(self, g, mesh):
        x1 = g.x
        y1 = g.y
        x2 = x1 + self.width
        y2 = y1 + self.height        
        vertices = [ (x1, y1), (x2, y1), (x2, y2), (x1, y2) ]
        self.compose_sw(vertices, mesh)
        self.compose_se(vertices, mesh)        
        self.compose_ne(vertices, mesh)
        self.compose_nw(vertices, mesh)

    def compose_sw(self, vertices, mesh):
        indice = mesh.add_vertex( vertices[QUAD_SW] )
        mesh.set_tex_coord(indice, self.get_tex_coord(QUAD_SW))
        #self.indices[QUAD_SW] = indice

    def compose_se(self, vertices, mesh):
        #if not self.east:
            indice = mesh.add_vertex(vertices[QUAD_SE])
            mesh.set_tex_coord(indice, self.get_tex_coord(QUAD_SE))
            #self.indices[QUAD_SE] = indice

    def compose_ne(self, vertices, mesh):
        #if not self.north and not self.east:
            indice = mesh.add_vertex(vertices[QUAD_NE])
            mesh.set_tex_coord(indice, self.get_tex_coord(QUAD_NE))
            #self.indices[QUAD_NE] = indice 

    def compose_nw(self, vertices, mesh):
        #if not self.north:
            indice = mesh.add_vertex(vertices[QUAD_NW])
            mesh.set_tex_coord(indice, self.get_tex_coord(QUAD_NW))
            #self.indices[QUAD_NW] = indice
            
    '''
    PostCompose
    '''
    
    def postcompose(self, mesh):
        self.postcompose_sw()
        self.postcompose_se()        
        self.postcompose_ne()
        self.postcompose_nw()
        #mesh.indices.extend(self.indices)
        
    def postcompose_sw(self):
        pass

    def postcompose_se(self):
        if self.east:
            self.indices[QUAD_SE] = self.east.indices[QUAD_SW]

    def postcompose_ne(self):
        if self.north:
            self.indices[QUAD_NE] = self.north.indices[QUAD_SE]        
        elif self.east:
            self.indices[QUAD_NE] = self.east.indices[QUAD_NW]

    def postcompose_nw(self):
        if self.north:
            self.indices[QUAD_NW] = self.north.indices[QUAD_SW]
        
    def draw(self, graphics):
        if self.texture:
            self.texture.blit(graphics.x, graphics.y, graphics.z)
        if graphics.query:
            self.query(graphics)
            
'''
QuadContainer
'''
class QuadContainer(Base):
    def __init__(self):
        super().__init__()
        self.quads = []

    def validate(self):
        super().validate()
        
    def add_quad(self, quad):
        self.invalidate()
        self.quads.append(quad)
        
    def repeat(self, quad, count):
        self.invalidate()
        i = 0
        while i < count:
            add_quad(quad.copy())
                                    
'''
QuadRow
'''
class QuadRow(QuadContainer):
    def __init__(self):
        super().__init__()
        self.north = None
        self.south = None
        self.height = None
    
    def validate(self):
        super().validate()
        lastQuad = None
        for quad in self.quads:
            if lastQuad:
                lastQuad.east = quad
            quad.west = lastQuad
            lastQuad = quad
        self.height = lastQuad.height 
            
    def compose(self, graphics, mesh):
        if self.invalid:
            self.validate()
            
        for quad in self.quads:
            quad.compose(graphics, mesh)
            graphics.x += quad.width
        '''
        #fixme:reinstate this when shared vertices get figured out.
        for quad in self.quads:
            quad.postcompose(mesh)
        '''
'''
QuadColumn
'''
class QuadColumn(QuadContainer):
    def __init__(self):
        super().__init__()
            
    def validate(self):
        super().validate()
        lastQuad = None
        for quad in self.quads:
            if lastQuad:
                lastQuad.north = quad
            quad.south = lastQuad
            lastQuad = quad
            
    def compose(self, graphics, mesh):
        if self.invalid:
            self.validate()
            
        for quad in self.quads:
            quad.compose(graphics, mesh)
            graphics.y += quad.height

        '''
        #fixme:reinstate this when shared vertices get figure out.
        for quad in self.quads:
            quad.postcompose(mesh)
        '''
        return
    
'''
QuadGrid
'''
class QuadGrid(QuadContainer):
    def __init__(self):
        super().__init__()

    def add_row(self, row):
        self.add_quad(row)
    
    def validate(self):
        super().validate()
        lastRow = None
        for row in self.quads:
            if lastRow:
                lastRow.north = row #fixme:going to use this?
                quadNdx = 0
                for quad in row.quads:
                    lastRow.quads[quadNdx].north = quad
            row.south = lastRow
            lastRow = row
            
    def compose(self, graphics, mesh):
        if self.invalid:
            self.validate()
        gX = graphics.x
        for row in self.quads:
            row.compose(graphics, mesh)
            graphics.x = gX
            graphics.y += row.height
        '''
        #fixme:reinstate this when shared vertices get figure out.
        for row in self.rows:
            row.postcompose(mesh)
        '''
        return
    
'''
QuadMesh
'''    
class QuadMesh(Base):
    def __init__(self, texture):
        super().__init__()
        self.texture = texture
        #self.indices = []
        self.vertices = []
        self.tex_coords = []
        #self.domain = pyglet.graphics.vertexdomain.create_indexed_domain('v2i/dynamic', 't3f')
        self.domain = pyglet.graphics.vertexdomain.create_domain('v2i/dynamic', 't3f')
            
    def add_vertex(self, vertex):
        self.vertices.append(vertex[0])
        self.vertices.append(vertex[1])
        self.tex_coords.extend([0.]*3)
        return len(self.vertices) / 2 - 1
    
    def set_tex_coord(self, indice, tex_coord):
        self.tex_coords[indice * 3] = tex_coord[0] 
        self.tex_coords[indice * 3 + 1] = tex_coord[1]
        self.tex_coords[indice * 3 + 2] = tex_coord[2]
        
    def create_vertex_list(self):
        #vertexList = self.domain.create(len(self.vertices)/2, len(self.indices))
        vertexList = self.domain.create(len(self.vertices)/2)
        #vertexList.indices = self.indices
        vertexList.vertices = self.vertices
        vertexList.tex_coords = self.tex_coords
        return vertexList
    
    def draw(self):
        vertexList = self.create_vertex_list()
        
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
        
        vertexList.draw(GL_QUADS)
        
        glDisable(self.texture.target)
        
        
        
