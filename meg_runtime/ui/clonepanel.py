
from PyQt5 import QtWidgets, uic
import pkg_resources

from meg_runtime.git import GitManager
from meg_runtime.config import Config
from meg_runtime.logger import Logger
from meg_runtime.ui.basepanel import BasePanel
from meg_runtime.ui.filechooser import FileChooser


class ClonePanel(BasePanel):
    """Setup the cloning panel.
    """
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager

        self.ok_button = self.findChild(QtWidgets.QPushButton, 'okButton')
        self.ok_button.clicked.connect(self.clone)
        self.back_button = self.findChild(QtWidgets.QPushButton, 'backButton')
        self.back_button.clicked.connect(self.return_to_main_menu)

        # Add the file viewer/chooser
        self.tree_view = FileChooser(
            self.findChild(QtWidgets.QTreeView, 'treeView'),
            Config.get('path/user')
        )

    def clone(self):
        """Clone the repository."""
        # Pass control to the manager
        repo_url = self.findChild(QtWidgets.QTextEdit, 'server').toPlainText()
        username = self.findChild(QtWidgets.QTextEdit, 'username').toPlainText()
        password = self.findChild(QtWidgets.QTextEdit, 'password').toPlainText()
        paths = self.tree_view.get_selected_paths()
        repo_path = None
        if len(paths) > 0:
            repo_path = paths[0]
        self.manager.clone(username, password, repo_url, repo_path)

    def return_to_main_menu(self):
        """Return to the main menu."""
        self.manager.return_to_main_menu()

    def reload(self):
        """Reload the panel."""
        pass
