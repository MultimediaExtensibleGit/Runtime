
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from os.path import dirname

Builder.load_file(dirname(__file__) + '/repopanel.kv')

class RepoPanel(BoxLayout):
    """Setup the main file panel.
    """
    def __init__(self, ui_manager, **kwargs):
        super().__init__(padding=40, spacing=40, **kwargs)
        self.ui_manager = ui_manager

    def open_repository(self):
        # TODO
        self.ui_manager.open_repository(self)

