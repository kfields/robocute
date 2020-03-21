
import pyglet

import robocute.tool

from robocute.widget.document import *

class FileTool(robocute.tool.Tool):
    def __init__(self, dna = None):
        super().__init__()
        self.widget = None
        self.keybox = robocute.tool.ToolKeybox(self)
        self.mousebox = robocute.tool.ToolMousebox(self)

    def bind(self, user):
        super().bind(user)
        self.show_widget()
        user.add_keybox(self.keybox)
        user.add_mousebox(self.mousebox)
        
    def unbind(self):
        self.user.remove_keybox(self.keybox)
        self.user.remove_mousebox(self.mousebox)
        self.hide_widget()
        super().unbind()        

    def show_widget(self):
        if not self.widget:
            self.create_widget()
        self.scene.dash.add_node(self.widget)

    def hide_widget(self):
        self.scene.dash.remove_node(self.widget)
        
    def create_widget(self):
        self.widget = None

class FileOpener(FileTool):
    def __init__(self, dna = None):
        super().__init__()
    def create_widget(self):
        self.widget = DocWidget('data/html/file_open.html')

class FileSaver(FileTool):
    def __init__(self, dna = None):
        super().__init__()
    def create_widget(self):
        self.widget = DocWidget('data/html/file_save.html')
        doc = self.widget.document
        pos = len(doc.text)
        doc.insert_text(pos, '\nSaving ...\n')
        self.app.save_game()
        pos = len(doc.text)
        doc.insert_text(pos, '\nGame saved.\n')
                        
class Helper(FileTool):
    def __init__(self, dna = None):
        super().__init__()
                
    def create_widget(self):
        self.widget = DocWidget('data/html/file_help.html')

class Exiter(FileTool):
    def __init__(self, dna = None):
        super().__init__()
    def create_widget(self):
        self.widget = DocWidget('data/html/file_exit.html')
