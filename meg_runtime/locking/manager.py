"""MEG system file locking

To be used to lock files, unlock files, override locks, and view locks
Will confirm user roles and preform required git operations

All file paths are relitive to the repository directory
Working directory should be changed by the git module
"""

import os
from meg_runtime.locking.lockFile import LockFile
from meg_runtime.logger import Logger


class LockingManager:
    """Used to prefrom all locking operations
    To be used to lock files, unlock files, override locks, and view locks
    Will confirm user roles and preform required git operations
    """
    LOCKFILE_DIR = ".meg" + os.sep
    LOCKFILE_NAME = "locks.json"
    _instance = None

    def __init__(self):
        """
        Args:
            permissionsManager (PermissionsManager): the active permissions manager
        """
        if not LockingManager._instance is None:
            raise Exception("Trying to create a second instance of LockingManager, which is a singleton")
        else:
            LockingManager._instance = self
            LockingManager._instance._lockFile = LockFile(LockingManager.LOCKFILE_DIR + LockingManager.LOCKFILE_NAME)

    @staticmethod
    def addLock(filepath, username):
        """Sync the repo, adds the lock, sync the repo
        Args:
            filepath (string): path to the file to lock
            username (string): username of cuerrent user
        Returns:
            (bool): was lock sucessfuly added
        """
        LockingManager._instance.updateLocks()
        if filepath in LockingManager._instance._lockFile:
            return False
        else:
            LockingManager._instance._lockFile[filepath] = username
            LockingManager._instance.updateLocks()
            return True
        
    @staticmethod
    def removeLock(filepath, username):
        """Sync the repo, remove a lock from a file, and sync again
        Args:
            filepath (string): path to file to unlock
            username (string): username of current user
        Returns:
            (bool): is there still a lock (was the user permitted to remove the lock)
        """
        LockingManager._instance.updateLocks()
        lock = LockingManager._instance._lockFile[filepath]
        if(lock is None):
            return True
        elif(lock["user"] == username or False): #TODO check that user role can remove other user's locks
            del LockingManager._instance._lockFile[filepath] 
        else:
            return False
        LockingManager._instance.updateLocks()
        return True
        
    @staticmethod
    def findLock(filepath):
        """Find if there is a lock on the file, does not automatily sync the lock file
        Args:
            filepath (string): path of file to look for
        Returns:
            (dictionary): lockfile entry for the file
            (None): There is no entry
        """
        return LockingManager._instance._lockFile[filepath]

    @staticmethod
    def locks():
        return LockingManager._instance._lockFile

    @staticmethod
    def updateLocks():
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
        LockingManager._instance._lockFile.save()
        LockingManager._instance._lockFile.load()
