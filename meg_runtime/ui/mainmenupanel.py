
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from meg_runtime.config import Config
from os.path import dirname

Builder.load_file(dirname(__file__) + '/mainmenupanel.kv')

class MainMenuPanel(BoxLayout):
    """Setup a list of cloned repos.
    """
    def __init__(self, ui_manager, **kwargs):
        super().__init__(**kwargs)
        self.ui_manager = ui_manager
        for repo in Config.get('repos', []):
            self.ids.repos.add_widget(Button(text=repo, size_hint_y=None, height=40))

    def open_repository(self):
        """Open a repository."""
        self.ui_manager.open_repository_view(self)
