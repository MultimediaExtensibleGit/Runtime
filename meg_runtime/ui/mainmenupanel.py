
from PyQt5 import QtWidgets
import os.path

from meg_runtime.config import Config
from meg_runtime.ui.basepanel import BasePanel
from meg_runtime.ui.helpers import PanelException


class MainMenuPanel(BasePanel):
    """Setup a list of cloned repos.
    """

    # The singleton configuration instance
    __instance = None

    def __init__(self, manager, **kwargs):
        """MainMenuPanel constructor."""
        if MainMenuPanel.__instance is not None:
            # Except if another instance is created
            raise PanelException(self.__class__.__name__ + " is a singleton!")
        elif manager is None:
            raise PanelException(self.__class__.__name__
                                 + " requires a manager!")
        else:
            super().__init__(**kwargs)
            self._manager = manager

            self.download_button = self.findChild(QtWidgets.QPushButton,
                                                  'downloadButton')
            # TODO: Attach handlers
            self.download_button.clicked.connect(self.download)
            self._tree_widget = self.findChild(QtWidgets.QTreeWidget,
                                               'treeWidget')
            self._tree_widget.itemDoubleClicked.connect(
                self.handle_double_click
            )
            MainMenuPanel.__instance = self
            MainMenuPanel.load()

    def handle_double_click(self, item):
        """Handle a double click."""
        # These columns were set in the load() method -- it would be nice
        # to find a way to get them by column name
        self._manager.open_repo(item.text(1), item.text(2))

    def download(self):
        """Download" or clone a project."""
        # Pass control to the manager
        self._manager.open_clone_panel()

    @staticmethod
    def get_instance(manager=None, **kwargs):
        """Get an instance of the singleton."""
        if MainMenuPanel.__instance is None:
            MainMenuPanel(manager, **kwargs)
        return MainMenuPanel.__instance

    @staticmethod
    def load():
        """Load dynamic elements within the panel."""
        instance = MainMenuPanel.get_instance()
        # Load the repos
        # TODO: Get this from the GitManager
        repos = Config.get('path/repos')
        repos = [
            QtWidgets.QTreeWidgetItem([
                os.path.basename(repo['path']),
                repo['url'],
                repo['path'],
            ])
            for repo in repos if repo['path'] and repo['url']
        ]
        instance._tree_widget.clear()
        instance._tree_widget.addTopLevelItems(repos)

    @staticmethod
    def get_title():
        """Get the title of this panel."""
        return 'Main Menu'
