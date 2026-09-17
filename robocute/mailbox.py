from crunge.engine.sdl.event_handler import EventHandler, DispatchResult


class Mailbox(EventHandler):
    def __init__(self):
        super().__init__()
        self.boxes = []

    def add_box(self, box):
        self.boxes.append(box)

    def remove_box(self, box):
        self.boxes.remove(box)

    def dispatch(self, event) -> DispatchResult:
        # logger.debug(f"class:{self.__class__.__name__}, Dispatching event: {event}")
        # return super().dispatch(event) or self.handle(event)
        for box in self.boxes:
            box.handle_event(event)
