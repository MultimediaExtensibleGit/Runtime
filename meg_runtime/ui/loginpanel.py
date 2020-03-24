
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from os.path import dirname

Builder.load_file(dirname(__file__) + '/loginpanel.kv')

class LoginPanel(BoxLayout):
    """Setup the main login panel.
    """
    def __init__(self, ui_manager, **kwargs):
        super().__init__(**kwargs)
        self.ui_manager = ui_manager

    def open_repository(self):
        """Connect to a given repository."""
        # TODO: Handle connection and validation
        self.ui_manager.connect(self,
                                self.ids.repo_url.text,
                                self.ids.username.text,
                                self.ids.password.text)

