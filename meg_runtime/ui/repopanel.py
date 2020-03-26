
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from os.path import dirname

Builder.load_file(dirname(__file__) + '/repopanel.kv')

class RepoPanel(BoxLayout):
    """Setup the main file panel.
    """
    def __init__(self, ui_manager, repo=None, **kwargs):
        super().__init__(padding=40, spacing=40, **kwargs)
        self.ui_manager = ui_manager
        self.repo = repo
        # TODO: Setup repo information, etc.

    def open_main_menu(self):
        # TODO
        self.ui_manager.open_repository(self)

    def view_repos(self):
        self.ui_manager.view_repos(self)
