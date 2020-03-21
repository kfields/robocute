class Messenger(object):
    def __init__(self, name):
        super().__init__()

    def connect(self, slot):
        slot.add_subscriber(self)        
        self.uplink = slot

    def disconnect(self):
        uplink.remove_subscriber(self)

    def send(self, msg):
        uplink.send(msg)

    def receive(msg, selfReflective = False):
        #This is how we prevent a sender from receiving it's own message!
        if self.downlink != msg.sender:
            self.downlink.receive(msg)


class Mailbox(object):
    def __init__(self, name = None):
        super().__init__()
        self.boxes = []
    
    def add_box(self, box):
        self.boxes.append(box)

    def remove_box(self, box):
        self.boxes.remove(box)

class BufferedMailbox(Mailbox):
    def __init__(self, name):
        super().__init__()
        self.messages = []
        
    def receive(self, msg):
        self.messages.append(msg)
        