"""MEG UI Manager
"""
from PySide2.QtWidgets import QApplication

from os.path import dirname

from meg_runtime.ui.mainmenupanel import MainMenuPanel
from meg_runtime.ui.clonepanel import ClonePanel
from meg_runtime.ui.repopanel import RepoPanel
from meg_runtime.logger import Logger


class UIManager(object):
    """Main UI manager for the MEG system."""

    PANELS = [
        MainMenuPanel,
        ClonePanel,
        RepoPanel,
    ]

    # Instance for the UI manager
    __instance = None

    def __init__(self, **kwargs):
        """UI manager constructor."""
        if UIManager.__instance is not None:
            raise Exception(self.__class__.__name__ + ' is a singleton!')
        else:
            super().__init__(**kwargs)

            # Load all the kv UI files 
            for panel in self.PANELS:
                path = f'{dirname(__file__)}/{panel.__name__.lower()}.kv'
                try:
                    Builder.load_file(path)
                except Exception as e:
                    Logger.warning('MEG UI Manager: {0}'.format(e))
                    Logger.warning('MEG UI Manager: Could not load {0} file.'
                                   .format(path))

            # TODO: State change
            main_menu = MainMenuPanel(UIManager)

    @staticmethod
    def run():
        """Get the instance for the UI Manager."""
        if UIManager.__instance is None:
            UIManager.__instance = UIManager()
        return UIManager.__instance

    @staticmethod
    def open_repo_panel(repo, **kwargs):
        """Open a repository panel."""
        manager = UIManager.get_instance()
        manager.add_widget(RepoPanel(UIManager, repo, **kwargs))

    @staticmethod
    def open_clone_panel():
        """Open panel for repo cloning."""
        manager = UIManager.get_instance()
        manager.add_widget(ClonePanel(UIManager))

    @staticmethod
    def open_main_menu():
        """Open the main menu, closing the old panel."""
        manager = UIManager.get_instance()
        manager.add_widget(MainMenuPanel(UIManager))

    @staticmethod
    def close(panel):
        manager = UIManager.get_instance()
        manager.remove_widget(panel)

    # TODO: Add more menu opening/closing methods here
