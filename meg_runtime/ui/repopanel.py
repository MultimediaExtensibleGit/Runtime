
from kivy.uix.boxlayout import BoxLayout
from os.path import dirname


class RepoPanel(BoxLayout):
    """Setup the main file panel.
    """
    def __init__(self, manager, repo=None, **kwargs):
        super().__init__(padding=40, spacing=40, **kwargs)
        self.repo = repo
        self.manager = manager
        # TODO: Setup repo information, etc.

    def open_main_menu(self):
        # TODO
        self.manager.open_clone_panel(self)

    def view_repos(self):
        self.manager.open_main_menu(self)


