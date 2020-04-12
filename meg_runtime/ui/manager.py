"""MEG UI Manager
"""
from PyQt5 import QtWidgets

from meg_runtime.config import Config
from meg_runtime.git import GitManager
from meg_runtime.ui.mainmenupanel import MainMenuPanel
from meg_runtime.ui.clonepanel import ClonePanel
from meg_runtime.ui.repopanel import RepoPanel


class UIManager(QtWidgets.QStackedWidget):
    """Main UI manager for the MEG system."""

    PANELS = [
        ClonePanel,
        MainMenuPanel,
        RepoPanel,
    ]

    def __init__(self, **kwargs):
        """UI manager constructor."""
        super().__init__(**kwargs)
        self._panels = {}
        for panel in self.PANELS:
            self._panels[panel.__name__] = panel(self)
            self.addWidget(self._panels[panel.__name__])
        self.change_view(MainMenuPanel)
        self.resize(600, 600)

    def open_clone_panel(self):
        """"Download" or clone a project."""
        # TODO
        self.change_view(ClonePanel)

    def clone(self, username, password, repo_url, repo_path):
        """Clone a repository."""
        # TODO: Handle username + password
        # Set the config
        GitManager.clone(repo_url, repo_path)
        repos = Config.get('path/repos', defaultValue=[])
        repos.append({'url': repo_url, 'path': repo_path})
        Config.set('path/repos', repos)
        Config.save()
        self.change_view(RepoPanel)

    def return_to_main_menu(self):
        """Return to the main menu screen"""
        self.change_view(MainMenuPanel)

    def change_view(self, panel):
        """Change the current panel being viewed. """
        # Get the actual widget
        widget = self._panels[panel.__name__]
        self.setCurrentIndex(self.PANELS.index(panel))
        # self.setGeometryUpdate()

    # TODO: Add more menu opening/closing methods here
