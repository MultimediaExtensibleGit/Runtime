
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from os.path import dirname

from .loginpanel import LoginPanel
from .repopanel import RepoPanel

class UIManager(BoxLayout):
    """Main UI manager for the MEG system."""

    def __init__(self, **kwargs):
        """UI manager constructor."""
        super().__init__(**kwargs)
        self.add_widget(RepoPanel(self))

    def connect(self, login_panel, repo_url, username, password):
        self.remove_widget(login_panel)
        self.add_widget(RepoPanel(self))

    def open_repository(self, repo_panel):
        self.remove_widget(repo_panel)
        self.add_widget(LoginPanel(self))
