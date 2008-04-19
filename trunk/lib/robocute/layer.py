import pyglet

'''
Copy and pasted from pyglet's SpriteGroup ...
'''

class Group(pyglet.graphics.Group):
    def __init__(self, texture, blend_src, blend_dest, parent=None):
        super(Group, self).__init__(parent)
        self.texture = texture
        self.blend_src = blend_src
        self.blend_dest = blend_dest

    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPushAttrib(GL_COLOR_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)

    def unset_state(self):
        glPopAttrib()
        glDisable(self.texture.target)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.texture.target == other.texture.target and
                self.texture.id == other.texture.id and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest)

    def __hash__(self):
        return hash((id(self.parent),
                     self.texture.id, self.texture.target,
                     self.blend_src, self.blend_dest))


class Layer(pyglet.graphics.OrderedGroup):
    def __init__(self, name, order = 0):
        super(Layer, self).__init__(order)
        self.name = name
        self.nodes = []
        self.layers = []
    
    def create_layer(self, name):
        order = len(self.layers)
        layer = Layer(self, order)
        self.layers.append(layer)
        return layer
    
    def create_layers(self, cls, name):
        layerCount = len(self.layers)
        layer = cls(self, layerCount)
        self.layers.append(layer)
        return layer        
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def remove_node(self, node):
        self.nodes.remove(node)
        
    def draw_nodes(self, graphics):
        pass
    
    def find_group(self, texture, blend_src, blend_dest):
        group = Group(texture, blend_src, blend_dest, self)
        if group in self.groups:
            group = self.groups.index(group)
        else:
            self.groups.append(group)
        return group
