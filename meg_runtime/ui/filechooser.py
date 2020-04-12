
from PyQt5 import QtWidgets

import os


class FileChooser(object):
    """File chooser view (using composition)."""

    def __init__(self, tree_view, path, **kwargs):
        """File chooser constructor."""
        super().__init__(**kwargs)
        self.tree_view = tree_view
        model = QtWidgets.QDirModel()
        self.tree_view.setModel(model)
        self.tree_view.setRootIndex(model.index(path))

    def get_selected_paths(self):
        """Return the selected paths in the chooser."""
        paths = []
        indexes = self.tree_view.selectedIndexes()
        for index in indexes:
            p = [index.data()]
            parent = index.parent()
            while parent.isValid():
                p.insert(0, parent.data())
                parent = parent.parent()
            path = '/'.join(p)
            # Handle Windows backslash
            if os.name == 'nt':
                path = '\\'.join(p)
            paths.append(path)
        return paths
