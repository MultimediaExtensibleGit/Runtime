"""MEG system lockfile parser

Can be used to parse the lock file and preform operations on the lockfile
Only interacts with the lockfile, does not preform any git actions
Does not check permissions before actions are taken

All file paths are relitive to the repository directory
Working directory should be changed by the git module
"""

import json
import os.path
import time
from meg_runtime.logger import Logger

class LockFile:
    """Parse a lockfile and preform locking operations
    """

    def __init__(self, filepath):
        """Open a lockfile and initalize class with it
        Args:
            filepath (string): path to the lockfile
        """
        self.load(filepath)

    def save(self):
        """Saves current data into the lockfile, overriding its contents
        Must be ran to save any new or removed locks
        Will create file if it doesn't already exist
        """
        json.dump(self._lockData, open(self._filepath, 'w'))

    def load(self, filepath=None):
        """Loads this object with the current data in the lockfile, overrideing its current data
        If the file doesn't exist, create one
        Args:
            filepath (string): path to the lockfile
        Returns:
            (bool): False if lockfile cannot be read

        """
        if(filepath is None):
            filepath = self._filepath
        else:
            self._filepath = filepath
            if(not os.path.exists(filepath)):
                self._createLockFile(filepath)

        try:
            self._lockData = json.load(open(filepath))
        except json.decoder.JSONDecodeError:
            self._createLockFile(filepath)
            try:
                self._lockData = json.load(open(filepath))
            except json.decoder.JSONDecodeError:
                Logger.warning("Lockfile corrupted")
                return False
        return True

    def addLock(self, filepath, username):
        """Adds the lock to the lockfile
        Args:
            filepath (string): path to the file to lock
            username (string): name of locking user
        """
        self._lockData["locks"].append({
            "file": filepath,
            "user": username,
            "date": time.time()
        })

    def removeLock(self, filepath):
        """Remove any lock for the given file
        Args:
            filepath (string): path to the file to unlock
        """
        for entry in self._lockData["locks"]:
            if(entry["file"] == filepath):
                self._lockData["locks"].remove(entry)

    def findLock(self, filepath):
        """Find if there is a lock on the file
        Args:
            filepath (string): path of file to look for
        Returns:
            (dictionary): lockfile entry for the file
            (None): There is no entry
        """
        for entry in self._lockData["locks"]:
            if(entry["file"] == filepath):
                return entry
        return None

    @property
    def locks(self):
        """Returns the list of locks
        """
        return self._lockData["locks"]

    def _createLockFile(self, filepath):
        self._locks = {
                    "comment": "MEG System locking file, avoid manually editing",
                    "locks": []
                }
        newFile = open(filepath, 'w')
        newFile.write(json.dumps(self._locks))
        newFile.close()






        

