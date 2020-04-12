
from PyQt5 import QtWidgets, uic
import os.path
import pkg_resources

from meg_runtime.config import Config
from meg_runtime.logger import Logger
from meg_runtime.ui.basepanel import BasePanel


class MainMenuPanel(BasePanel):
    """Setup a list of cloned repos.
    """
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager

        self.download_button = self.findChild(QtWidgets.QPushButton,
                                              'downloadButton')
        # TODO: Attach handlers
        self.download_button.clicked.connect(self.download)
        # Load the repos
        # TODO: Get this from the GitManager
        self.tree_widget = self.findChild(QtWidgets.QTreeWidget, 'treeWidget')
        repos = Config.get('path/repos')
        repos = [QtWidgets.QTreeWidgetItem([os.path.basename(repo['path'])])
                 for repo in repos]
        self.tree_widget.addTopLevelItems(repos)

    def download(self):
        """"Download" or clone a project."""
        # Pass control to the manager
        self.manager.open_clone_panel()

    def reload(self):
        """Reload the window."""
        # TODO
        pass
