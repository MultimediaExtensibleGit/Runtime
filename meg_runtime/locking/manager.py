"""MEG system file locking

To be used to lock files, unlock files, override locks, and view locks
Will confirm user roles and preform required git operations

All file paths are relitive to the repository directory
Working directory should be changed by the git module
"""

import os
from meg_runtime.locking.lockFile import LockFile
from meg_runtime.logger import Logger

LOCKFILE_DIR = ".meg" + os.sep
LOCKFILE_NAME = "locks.json"

class LockingManager:
    """Used to prefrom all locking operations
    To be used to lock files, unlock files, override locks, and view locks
    Will confirm user roles and preform required git operations
    """

    def __init__(self, user, permissionsManager, repoManager):
        """
        Args:
            user (string): username of user
            permissionsManager (PermissionsManager): the active permissions manager
            repoManager (GitRepository): the currenly open repository
        """
        self._lockFile = LockFile(LOCKFILE_DIR + LOCKFILE_NAME)
        self.user = user
        self.permissionsManager = permissionsManager
        self.repoManager = repoManager

    def addLock(self, filepath):
        """Sync the repo, adds the lock, sync the repo
        Args:
            filepath (string): path to the file to lock
        Returns:
            (bool): was lock sucessfuly added
        """
        self.updateLocks()
        if(not self._lockFile.findLock(filepath) is None):
            return False
        else:
            self._lockFile.addLock(filepath, self.user)
            self.updateLocks()
            return True
        

    def removeLock(self, filepath):
        """Sync the repo, remove a lock from a file, and sync again
        Args:
            filepath (string): path to file to unlock
        Returns:
            (bool): is there still a lock (was the user permitted to remove the lock)
        """
        self.updateLocks()
        lock = self._lockFile.findLock(filepath)
        if(lock is None):
            return True
        elif(lock["user"] == self.user):
            self._lockFile.removeLock(filepath)
        else:
            if(False): #TODO check that user role can remove other user's locks
                self._lockFile.removeLock(filepath)
            else:
                return False
        self.updateLocks()
        return True
        

    def findLock(self, filepath):
        """Find if there is a lock on the file, does not automatily sync the lock file
        Args:
            filepath (string): path of file to look for
        Returns:
            (dictionary): lockfile entry for the file
            (None): There is no entry
        """
        return self._lockFile.findLock(filepath)

    @property
    def locks(self):
        return self._lockFile.locks

    def updateLocks(self):
        """Syncronizes the local locks with the remote locks, manually merge local data with remote
        """
        #TODO Sync with repo, as described below
        """
        https://www.quora.com/How-can-I-pull-one-file-from-a-Git-repository-instead-of-the-entire-project/answer/Aarti-Dwivedi
        fetch
        checkout from latest commit lock and permissions files
        create new LockFile object off of it and merge with current object
        save date
        if lockfile has changed stage, commit, and push it
        """
        self._lockFile.save()
        self._lockFile.load()