
from kivy.uix.boxlayout import BoxLayout
from os.path import dirname
from meg_runtime.git import GitManager
from meg_runtime.config import Config


class ClonePanel(BoxLayout):
    """Setup the cloning panel.
    """
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager

    def clone(self):
        """Connect to a given repository."""
        if not self.ids.repo_url.text:
            self.ids.error_msg.text = '* Please enter a repository/project URL'
            return

        repo_path = self.ids.repo_path.text or None
        repo = GitManager.clone(self.ids.repo_url.text, repo_path=repo_path)
        repos = Config.get('repos', [])
        repos.append(repo.path)
        Config.set('repos', repos)
        Config.save(Config.get('path/config'))
        
        # TODO: Need to open up actual view of repo here
        self.manager.close(self)
        self.manager.open_repo_panel(repo, repo_path=repo_path)

    def back(self):
        """Go back a page."""
        self.manager.close(self)
        self.manager.open_main_menu()

