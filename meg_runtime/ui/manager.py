"""MEG UI Manager
"""
from PyQt5 import QtWidgets, QtGui

from meg_runtime.config import Config
from meg_runtime.logger import Logger
from meg_runtime.git import GitManager, GitRepository


class UIManager(QtWidgets.QStackedWidget):
    """Main UI manager for the MEG system."""

    APP_NAME = "Multimedia Extensible Git"

    # The singleton instance
    __instance = None

    def __init__(self, panels=None, icon_path=None, **kwargs):
        """UI manager constructor."""
        if UIManager.__instance is not None:
            # Except if another instance is created
            raise Exception(self.__class__.__name__ + " is a singleton!")
        else:
            super().__init__(**kwargs)
            UIManager.__instance = self
            # Set the open repository
            self._open_repo = None
            if panels:
                for panel in panels:
                    self.addWidget(panel.get_title(), panel)
            self.change_view('Main Menu')
            # Set the default size
            self.resize(1000, 600)
            # Set the icon
            if icon_path is not None:
                self.setWindowIcon(QtGui.QIcon(icon_path))

    @staticmethod
    def get_instance(**kwargs):
        """Get an instance of the singleton."""
        if UIManager.__instance is None:
            UIManager(**kwargs)
        return UIManager.__instance

    @staticmethod
    def setup(**kwargs):
        """Run initial setup of the UI manager."""
        instance = UIManager.get_instance(**kwargs)
        instance.show()

    @staticmethod
    def open_clone_panel():
        """"Download" or clone a project."""
        # TODO
        UIManager.change_view('Clone Panel')

    @staticmethod
    def clone(username, password, repo_url, repo_path):
        """Clone a repository."""
        # TODO: Handle username + password
        repo = GitManager.clone(repo_url, repo_path)
        repos = Config.get('path/repos', defaultValue=[])
        repos.append({'url': repo_url, 'path': repo_path})
        # Set the config
        Config.set('path/repos', repos)
        Config.save()
        RepoPanel(repo_url, repo_path, repo)
        UIManager.change_view('Repo Panel')

    @staticmethod
    def open_repo(repo_url, repo_path):
        """Open a specific repo."""
        try:
            repo = GitRepository(repo_path)
            RepoPanel.set_repo(repo_url, repo_path, repo)
            UIManager.change_view(RepoPanel)
        except Exception as e:
            # TODO: add a popup
            Logger.warning(f'MEG UIManager: Could not load repo in "{repo_path}"')

    @staticmethod
    def return_to_main_menu():
        """Return to the main menu screen"""
        UIManager.change_view('Main Menu')

    @staticmethod
    def get_changes(repo):
        """Get changes for the given repo (do a pull)."""
        repo.pull()

    @staticmethod
    def send_changes(repo):
        """Send changes for the given repo."""
        # TODO
        pass

    @staticmethod
    def change_view(panel):
        """Change the current panel being viewed. """
        # Reload the panel before changing the view
        instance = UIManager.get_instance()
        instance.setWindowTitle(f'{UIManager.APP_NAME} - {panel}')
        instance.setCurrentIndex(UIManager.index(panel))

    # TODO: Add more menu opening/closing methods here
