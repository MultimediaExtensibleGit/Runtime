"""MEG Application Class
"""

import sys
import pkg_resources
from PyQt5 import QtWidgets
from meg_runtime.config import Config
from meg_runtime.plugins import PluginManager
from meg_runtime.logger import Logger
from meg_runtime import ui


# MEG client application
class App(QtWidgets.QApplication):
    """Multimedia Extensible Git (MEG) Client Application"""

    PANELS = [
        'ClonePanel',
        'MainMenuPanel',
        'RepoPanel',
    ]

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
        panels = []
        for panel in App.PANELS:
            panel_ctor = getattr(ui, panel)
            panels.append(panel_ctor())
        icon_path = pkg_resources.resource_filename(__name__, 'meg.ico')
        ui.UIManager.setup(panels=panels, icon_path=icon_path, **kwargs)

        # Launch
        ret = self.exec_()

        self.on_stop()
        sys.exit(ret)
