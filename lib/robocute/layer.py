class Layer(object):
    def __init__(self, scene):
        self.scene = scene
        self.nodes = []
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def remove_node(self, node):
        self.nodes.remove(node)
        
    def draw_nodes(self, graphics):
        pass
    
class BubbleLayer(Layer):
    def __init__(self, scene):
        super(BubbleLayer, self).__init__(scene)
        
    def draw(self, graphics):
        g = graphics.copy()
        for node in self.nodes:
            vu = node.vu
            if(vu != None):
                t = node.get_transform()
                g.translate(t.x, t.y)
                vu.draw(g)

class WidgetLayer(Layer):
    def __init__(self, scene):
        super(WidgetLayer, self).__init__(scene)
        
    def draw(self, graphics):
        g = graphics.copy()
        for node in self.nodes:
            vu = node.vu
            if(vu != None):
                t = node.get_transform()
                g.translate(t.x, t.y)
                vu.draw(g)

class MouseLayer(Layer):
    def __init__(self, scene):
        super(MouseLayer, self).__init__(scene)
        
    def draw(self, graphics):
        g = graphics.copy() #fixme:necessary?
        for node in self.nodes:                
            vu = node.vu
            g.x = node.x
            g.y = node.y - vu.height #fixme:mouse.hotx & hoty!!!
            vu.draw(g)
