from robocute.brain import BaseBrain


class Tool(BaseBrain):
    def __init__(self, dna=None):
        super().__init__(None)  # no node ...

    def on_key_press(self, event):
        key = event.key
        if key == key.ESCAPE:
            self.view.pop_tool()
        else:
            super().on_key_press(event)
