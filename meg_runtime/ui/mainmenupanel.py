
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

        def callback(instance):
            self.open_repo_panel(instance.repo_path)

        # Add the repo buttons to the menu
        for repo in Config.get('repos', []):
            button = Button(text=repo, size_hint_y=None, height=40)
            button.repo_path = repo
            button.bind(on_press=callback)
            self.ids.repos.add_widget(button)

    def open_repo_clone(self):
        """Open a repository."""
        self.manager.close(self)
        self.manager.open_clone_panel()

    def open_repo_panel(self, repo_path):
        self.manager.close(self)
        self.manager.open_repo_panel(repo_path)
