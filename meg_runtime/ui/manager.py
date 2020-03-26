
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from os.path import dirname

from meg_runtime.ui.mainmenupanel import MainMenuPanel
from meg_runtime.ui.clonepanel import ClonePanel
from meg_runtime.ui.repopanel import RepoPanel

class UIManager(BoxLayout):
    """Main UI manager for the MEG system."""

    def __init__(self, **kwargs):
        """UI manager constructor."""
        super().__init__(**kwargs)
        # self.add_widget(RepoPanel(self))
        self.add_widget(MainMenuPanel(self))

    def open_repo_panel(self, login_panel, repo):
        """Open a repository view."""
        self.remove_widget(login_panel)
        self.add_widget(RepoPanel(self, repo))

    def open_repository_view(self, repo_panel):
        self.remove_widget(repo_panel)
        self.add_widget(ClonePanel(self))

    def open_main_menu(self, panel):
        """Open the main menu, closing the old panel."""
        self.remove_widget(panel)
        self.add_widget(MainMenuPanel(self))

    # TODO: Add more menu opening/closing methods here
