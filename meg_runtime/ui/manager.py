
from kivy.lang.builder import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from os.path import dirname

from meg_runtime.ui.mainmenupanel import MainMenuPanel
from meg_runtime.ui.clonepanel import ClonePanel
from meg_runtime.ui.repopanel import RepoPanel


class UIManager(BoxLayout):
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

            # self.add_widget(RepoPanel(self))
            self.add_widget(MainMenuPanel(UIManager))

    @staticmethod
    def get_instance():
        """Get the instance for the UI Manager."""
        if UIManager.__instance is None:
            UIManager.__instance = UIManager()
        return UIManager.__instance

    @staticmethod
    def open_repo_panel(login_panel, repo):
        """Open a repository panel."""
        manager = UIManager.get_instance()
        manager.remove_widget(login_panel)
        manager.add_widget(RepoPanel(UIManager, repo))

    @staticmethod
    def open_clone_panel(repo_panel):
        """Open panel for repo cloning."""
        manager = UIManager.get_instance()
        manager.remove_widget(repo_panel)
        manager.add_widget(ClonePanel(UIManager))

    @staticmethod
    def open_main_menu(panel):
        """Open the main menu, closing the old panel."""
        manager = UIManager.get_instance()
        manager.remove_widget(panel)
        manager.add_widget(MainMenuPanel(UIManager))

    # TODO: Add more menu opening/closing methods here
