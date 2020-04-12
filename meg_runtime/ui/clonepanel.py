
from PyQt5 import QtWidgets

from meg_runtime.config import Config
from meg_runtime.ui.basepanel import BasePanel
from meg_runtime.ui.filechooser import FileChooser
from meg_runtime.ui.helpers import PanelException


class ClonePanel(BasePanel):
    """Setup the cloning panel.
    """

    # The singleton configuration instance
    __instance = None

    def __init__(self, manager, **kwargs):
        if ClonePanel.__instance is not None:
            raise PanelException(self.__class__.__name__ + " is a singleton!")
        elif manager is None:
            raise PanelException(self.__class__.__name__
                                 + " requires a manager!")
        else:
            super().__init__(**kwargs)
            self._manager = manager

            # Attach handlers
            self.ok_button = self.findChild(QtWidgets.QPushButton, 'okButton')
            self.ok_button.clicked.connect(self.clone)
            self.back_button = self.findChild(QtWidgets.QPushButton,
                                              'backButton')
            self.back_button.clicked.connect(self.return_to_main_menu)
            self.server_text_edit = self.findChild(QtWidgets.QTextEdit,
                                                   'server')
            self.username_text_edit = self.findChild(QtWidgets.QTextEdit,
                                                     'username')
            self.password_text_edit = self.findChild(QtWidgets.QTextEdit,
                                                     'password')

            ClonePanel.__instance = self
            ClonePanel.load()

    def clone(self):
        """Clone the repository."""
        repo_url = self.server_text_edit.toPlainText()
        username = self.username_text_edit.toPlainText()
        password = self.password_text_edit.toPlainText()
        path = self._tree_view.get_selected_path()
        repo_path = None
        if path is not None:
            repo_path = path
        # Pass control to the manager
        self._manager.clone(username, password, repo_url, repo_path)

    def return_to_main_menu(self):
        """Return to the main menu."""
        self._manager.return_to_main_menu()

    @staticmethod
    def get_instance(manager=None, **kwargs):
        """Get an instance of the singleton."""
        if ClonePanel.__instance is None:
            ClonePanel(manager, **kwargs)
        return ClonePanel.__instance

    @staticmethod
    def get_title():
        """Get the title of this panel."""
        return 'Clone Panel'

    @staticmethod
    def load():
        """Load dynamic elements within the panel."""
        instance = ClonePanel.get_instance()
        # Add the file viewer/chooser
        instance._tree_view = FileChooser(
            instance.findChild(QtWidgets.QTreeView, 'treeView'),
            Config.get('path/user')
        )
