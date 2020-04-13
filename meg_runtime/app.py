"""MEG Application Class
"""
from PyQt5 import QtWidgets
import pkg_resources
import sys

from meg_runtime.config import Config
from meg_runtime.plugins import PluginManager
from meg_runtime.ui import UIManager, ClonePanel, MainMenuPanel, RepoPanel
from meg_runtime.logger import Logger


# MEG client application
class App(QtWidgets.QApplication):
    """Multimedia Extensible Git (MEG) Client Application"""

    PANELS = [
        ClonePanel,
        MainMenuPanel,
        RepoPanel,
    ]
    APP_NAME = "Multimedia Extensible Git"

    # Constructor
    def __init__(self):
        """Application constructor"""
        # Initialize super class constructor
        super().__init__([])

    def on_start(self):
        """On application start"""
        # Log debug information about home directory
        Logger.debug('MEG: Home <' + Config.get('path/home') + '>')
        # Load configuration
        Config.load()
        # Log debug information about cache and plugin directories
        Logger.debug('MEG: Cache <' + Config.get('path/cache') + '>')
        Logger.debug('MEG: Plugins <' + Config.get('path/plugins') + '>')
        # Update plugins information
        PluginManager.update()
        # Load enabled plugins
        PluginManager.load_enabled()

    # On application stopped
    def on_stop(self):
        """On application stopped"""
        PluginManager.unload_all()

    # Run the application
    def run(self, **kwargs):
        """Run the application UI"""
        self.on_start()
        icon_path = pkg_resources.resource_filename(__name__, 'meg.ico')
        UIManager.setup(icon_path=icon_path, **kwargs)

        # Launch
        ret = self.exec_()

        self.on_stop()
        sys.exit(ret)
