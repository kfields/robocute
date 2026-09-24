from crunge.engine.widget import Widget


class Bubble(Widget):
    def __init__(self, children):
        super().__init__(children=children)


class DashBubble(Bubble):
    def __init__(self, children):
        super().__init__(children)
