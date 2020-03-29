
from kivy.uix.boxlayout import BoxLayout
from os.path import dirname


class RepoPanel(BoxLayout):
    """Setup the main file panel.
    """
    def __init__(self, manager, repo=None, repo_path=None, **kwargs):
        super().__init__(padding=40, spacing=40, **kwargs)
        self.repo = repo
        self.manager = manager
        if repo_path is not None:
            self.ids.file_chooser.path = repo_path
        # TODO: Setup repo information, etc.

    def open_main_menu(self):
        """Open the main menu."""
        self.manager.close(self)
        self.manager.open_main_menu()


