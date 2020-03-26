
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from os.path import dirname
from meg_runtime.git import GitManager
from meg_runtime.config import Config

Builder.load_file(dirname(__file__) + '/clonepanel.kv')

class ClonePanel(BoxLayout):
    """Setup the cloning panel.
    """
    def __init__(self, ui_manager, **kwargs):
        super().__init__(**kwargs)
        self.ui_manager = ui_manager

    def open_repository(self):
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
        self.ui_manager.open_repo_panel(self, repo)

