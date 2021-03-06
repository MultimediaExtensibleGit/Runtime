
from PyQt5 import QtWidgets
from meg_runtime.app import App
from meg_runtime.plugins import PluginManager
from meg_runtime.ui.basepanel import BasePanel


class AddPluginPanel(BasePanel):
    """Setup the plugin panel."""

    def __init__(self, plugins_panel, **kwargs):
        super().__init__(**kwargs)
        self.selected_file = None
        self._plugins_panel = plugins_panel

    def get_title(self):
        """Get the title of this panel."""
        return 'Add New Plugin'

    def get_plugins_panel(self):
        """Get the plugins panel that spawned this panel."""
        return self._plugins_panel

    def on_load(self):
        """Load dynamic elements within the panel."""
        instance = self.get_widgets()
        # add button
        self.add_button = instance.findChild(QtWidgets.QPushButton, 'addButton')
        self.add_button.clicked.connect(self.add_plugin)
        # available plugin handlers
        self.available_radio_button = instance.findChild(QtWidgets.QRadioButton, 'availableRadioButton')
        self.available_radio_button.clicked.connect(self.enable_available_selection)
        self.available_plugin_list = instance.findChild(QtWidgets.QTreeWidget, 'availablePluginList')
        self.refresh_available_button = instance.findChild(QtWidgets.QPushButton, 'refreshAvailableButton')
        self.refresh_available_button.clicked.connect(self.refreshAvailableList)
        # file plugin handlers
        self.file_radio_button = instance.findChild(QtWidgets.QRadioButton, 'fileRadioButton')
        self.file_radio_button.clicked.connect(self.enable_file_selection)
        self.choose_file_button = instance.findChild(QtWidgets.QPushButton, 'chooseFileButton')
        self.choose_file_button.clicked.connect(self.open_file_dialog)
        self.file_label = instance.findChild(QtWidgets.QLabel, 'fileLabel')
        # url plugin handlers
        self.url_radio_button = instance.findChild(QtWidgets.QRadioButton, 'urlRadioButton')
        self.url_radio_button.clicked.connect(self.enable_url_selection)
        self.url_field = instance.findChild(QtWidgets.QLineEdit, 'urlField')

    def on_show(self):
        """Showing the panel."""
        if not self.visible():
            self.selected_file = None
            self.file_label.setText('')
            self.url_field.setText('')
            self.available_radio_button.click()
        PluginManager.update_cache()
        # Add all available plugins to the available plugin list
        self.available_plugin_list.clear()
        available_plugins = PluginManager.get_all_available()
        for plugin in available_plugins:
            self.available_plugin_list.addTopLevelItem(QtWidgets.QTreeWidgetItem([
                plugin.name(),
                plugin.version(),
                plugin.author(),
                plugin.description()
            ]))

    def add_plugin(self):
        """Add the chosen plugin or show a message"""
        message = self._add_plugin()
        if message is not None:
            QtWidgets.QMessageBox().critical(App.get_window(), App.get_name(), message)
        else:
            window = App.get_window()
            window.set_view(self.get_plugins_panel())
            window.remove_view(self)

    def _add_plugin(self):
        """Chose a plugin or return a message"""
        if self.available_radio_button.isChecked():
            selectedPlugin = self.available_plugin_list.currentItem()
            if selectedPlugin is None:
                return 'Please select an available plugin to install'
            elif not PluginManager.install(selectedPlugin.text(0)):
                return f'Could not install plugin "{selectedPlugin}"'
        elif self.file_radio_button.isChecked():
            if self.selected_file is None:
                return 'Please choose a plugin archive to install'
            elif not PluginManager.install_archive(self.selected_file):
                return f'Could not install plugin from archive "{self.selected_file}"'
        elif self.url_radio_button.isChecked():
            url = self.url_field.text()
            if url is None:
                return 'Please provide a plugin url to install'
            elif not PluginManager.install_archive_from_url(url):
                return f'Could not install plugin from URL "{url}"'
        return None

    def enable_available_selection(self):
        """enable available plugin selection"""
        self.available_plugin_list.setEnabled(True)
        self.refresh_available_button.setEnabled(True)
        self.disable_file_selection()
        self.disable_url_selection()

    def enable_file_selection(self):
        """enable plugin file selection, disables everything else"""
        self.choose_file_button.setEnabled(True)
        self.file_label.setEnabled(True)
        self.disable_available_selection()
        self.disable_url_selection()

    def enable_url_selection(self):
        """enable plugin url selection"""
        self.url_field.setEnabled(True)
        self.disable_available_selection()
        self.disable_file_selection()

    def disable_available_selection(self):
        """disables the available selection fields"""
        self.available_plugin_list.setEnabled(False)
        self.refresh_available_button.setEnabled(False)

    def disable_file_selection(self):
        """disables the file selection fields"""
        self.choose_file_button.setEnabled(False)
        self.file_label.setEnabled(False)

    def disable_url_selection(self):
        """disables the url selection fields"""
        self.url_field.setEnabled(False)

    def open_file_dialog(self):
        """open file dialog, save chosen file to self.selected_file"""
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        filters = [
            'Plugin Archives Files (*.zip *.tar *.tar.gz *.tar.bz2 *.tar.xz)',
            'Any Files (*)'
        ]
        fileDialog.setNameFilters(filters)
        if fileDialog.exec_():
            self.selected_file = fileDialog.selectedFiles()[0]
            self.file_label.setText(self.selected_file)

    def refreshAvailableList(self):
        """refresh list of available plugins"""
        PluginManager.update_cache()
        self.bind_available_plugins()
