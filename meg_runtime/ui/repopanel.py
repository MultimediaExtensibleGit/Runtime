
import os.path
from PyQt5 import QtWidgets

from meg_runtime.config import Config
from meg_runtime.logger import Logger
from meg_runtime.ui.basepanel import BasePanel
from meg_runtime.ui.filechooser import FileChooser
from meg_runtime.ui.helpers import PanelException


class RepoPanel(BasePanel):
    """Setup the main file panel.
    """

    # The singleton configuration instance
    __instance = None

    def __init__(self, manager, repo_url=None, repo_path=None, repo=None,
                 **kwargs):
        """RepoPanel constructor."""
        if RepoPanel.__instance is not None:
            raise PanelException(self.__class__.__name__ + " is a singleton!")
        elif manager is None:
            raise PanelException(self.__class__.__name__
                                 + " requires a manager!")
        else:
            super().__init__(**kwargs)
            self._manager = manager
            self._repo_url = repo_url
            self._repo_path = repo_path
            self._repo = repo

            self._main_menu_button = self.findChild(QtWidgets.QPushButton,
                                                    'mainMenu')
            self._main_menu_button.clicked.connect(self.return_to_main_menu)
            self._get_changes_button = self.findChild(QtWidgets.QPushButton,
                                                      'getChanges')
            self._get_changes_button.clicked.connect(self.get_changes)
            self._send_changes_button = self.findChild(QtWidgets.QPushButton,
                                                       'sendChanges')
            self._send_changes_button.clicked.connect(self.send_changes)
            self._branch_name_label = self.findChild(QtWidgets.QLabel,
                                                     'branchName')
            RepoPanel.__instance = self
            RepoPanel.load()

    def handle_double_clicked(self, item):
        """Handle double clicking of a file (open it with another program)."""
        # TODO
        path = self.tree_view.get_selected_path()
        print(path)

    def return_to_main_menu(self):
        """Return to the main menu."""
        # Pass control to the manager
        self._manager.return_to_main_menu()
        # TODO: Setup repo information, etc.

    def get_changes(self):
        """Get changes from a remote origin."""
        self._manager.get_changes(self._repo)

    def send_changes(self):
        """Send changes to a remote origin."""
        self._manager.send_changes(self._repo)

    @property
    def title(self):
        """Get the title for the panel."""
        return (os.path.basename(self._repo_path)
                if self._repo_path else 'Project')

    @staticmethod
    def get_instance(manager=None, **kwargs):
        """Get an instance of the singleton."""
        if RepoPanel.__instance is None:
            RepoPanel(manager, **kwargs)
        return RepoPanel.__instance

    @staticmethod
    def set_repo(repo_url, repo_path, repo):
        """Set the repo for the panel."""
        instance = RepoPanel.get_instance()
        instance._repo_url = repo_url
        instance._repo_path = repo_path
        instance._repo = repo
        instance._branch_name_label.text = instance.title

    @staticmethod
    def get_title():
        """Get the title of this panel."""
        instance = RepoPanel.get_instance()
        return instance.title

    @staticmethod
    def load():
        """Load dynamic elements within the panel."""
        instance = RepoPanel.get_instance()

        # Setup the tree view of the repo if the repo folder exists
        path = Config.get('paths/user')
        if instance._repo_path is not None:
            if os.path.exists(instance._repo_path):
                path = instance._repo_path
            else:
                Logger.warning('MEG RepoPanel: The path '
                               f'"{instance._repo_path}" for this repo '
                               'does not exist')
        instance.tree_view = FileChooser(
            instance.findChild(QtWidgets.QTreeView, 'treeView'),
            path
        )
        # Setup a double click function if necessary
        instance.tree_view.set_double_click_handler(
            instance.handle_double_clicked
        )
