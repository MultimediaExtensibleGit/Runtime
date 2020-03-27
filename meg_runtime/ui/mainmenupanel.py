
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from meg_runtime.config import Config
from os.path import dirname


class MainMenuPanel(BoxLayout):
    """Setup a list of cloned repos.
    """
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        for repo in Config.get('repos', []):
            self.ids.repos.add_widget(Button(text=repo, size_hint_y=None,
                                             height=40))

    def open_repo_clone(self):
        """Open a repository."""
        self.manager.open_clone_panel(self)


