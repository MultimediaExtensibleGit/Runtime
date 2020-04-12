
from PyQt5 import QtWidgets, uic
from os.path import dirname

from meg_runtime.logger import Logger
from meg_runtime.ui.basepanel import BasePanel
from meg_runtime.ui.filechooser import FileChooser


class RepoPanel(BasePanel):
    """Setup the main file panel.
    """
    def __init__(self, manager, repo=None, **kwargs):
        super().__init__(**kwargs)
        self.repo = repo
        self.manager = manager

        self.main_menu_button = self.findChild(QtWidgets.QPushButton, 'mainMenu')
        self.main_menu_button.clicked.connect(self.return_to_main_menu)
        self.tree_view = FileChooser(
            self.findChild(QtWidgets.QTreeView, 'treeView'),
            # TODO
            ''
        )

    def return_to_main_menu(self):
        """Return to the main menu."""
        # TODO: Display a warning?
        self.manager.return_to_main_menu()
        # TODO: Setup repo information, etc.

    def reload(self):
        """Reload the panel."""
        # TODO
        pass
