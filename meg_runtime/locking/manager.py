"""MEG system file locking

To be used to lock files, unlock files, override locks, and view locks
Will confirm user roles and preform required git operations

All file paths are relitive to the repository directory
Working directory should be changed by the git module
"""

import os
from meg_runtime.locking.lockFile import LockFile


class LockingManager:
    """Used to prefrom all locking operations
    To be used to lock files, unlock files, override locks, and view locks
    Will confirm user roles and preform required git operations
    """
    LOCKFILE_DIR = ".meg" + os.sep
    LOCKFILE_NAME = "locks.json"
    __instance = None

    def __init__(self):
        if LockingManager.__instance is not None:
            raise Exception("Trying to create a second instance of LockingManager, which is a singleton")
        else:
            LockingManager.__instance = self
            LockingManager.__instance._lockFile = LockFile(LockingManager.LOCKFILE_DIR + LockingManager.LOCKFILE_NAME)

    @staticmethod
    def addLock(repo, filepath, username):
        """Sync the repo, adds the lock, sync the repo
        Args:
            repo (GitRepository): currently open repository that the file belongs to
            filepath (string): path to the file to lock
            username (string): username of current user
        Returns:
            (bool): was lock successfully added
        """
        if LockingManager.__instance is None:
            LockingManager()
        repo.setPermissionsUser(username)
        if not repo.permissions.can_lock():
            return False
        LockingManager.__instance.pullLocks(repo)
        if filepath in LockingManager.__instance._lockFile:
            return False
        else:
            LockingManager.__instance._lockFile[filepath] = username
            LockingManager.__instance.pushLocks(repo)
            return True

    @staticmethod
    def removeLock(repo, filepath, username):
        """Sync the repo, remove a lock from a file, and sync again
        Args:
            repo (GitRepository): currently open repository that the file belongs to
            filepath (string): path to file to unlock
            username (string): username of current user
        Returns:
            (bool): is there still a lock (was the user permitted to remove the lock)
        """
        if LockingManager.__instance is None:
            LockingManager()
        LockingManager.__instance.pullLocks(repo)
        lock = LockingManager.__instance._lockFile[filepath]
        repo.setPermissionsUser(username)
        if(lock is None):
            return True
<<<<<<< HEAD
        elif(lock["user"] == username or repo.permissions.can_remove_lock()):
            del LockingManager.__instance._lockFile[filepath] 
=======
        elif(lock["user"] == username or False):
            # TODO: check that user role can remove other user's locks
            del LockingManager.__instance._lockFile[filepath]
>>>>>>> 92915ef9bb62dc34149b5b5d6f1402700b38d0cb
        else:
            return False
        LockingManager.__instance.pushLocks(repo)
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
        if LockingManager.__instance is None:
            LockingManager()
        LockingManager.__instance._lockFile.load()
        return LockingManager.__instance._lockFile[filepath]

    @staticmethod
    def locks():
        """Get the LockFile object
        """
        LockingManager.__instance._lockFile.load()
        return LockingManager.__instance._lockFile

    @staticmethod
<<<<<<< HEAD
    def pullLocks(repo):
        """Pulls the lock file from remote and loads it

        Args:
            repo(GitRepository): currently open repository that the file belongs to
        """
        if LockingManager.__instance is None:
            LockingManager()
        if repo is None:
            Logger.warning("MEG Locking: Could not open repositiory")
            return False
         
        #Fetch current version
        if not repo.pullPaths([LockingManager.LOCKFILE_DIR[:-1] + '/' + LockingManager.LOCKFILE_NAME]):
            Logger.warning("MEG Locking: Could not download newest lockfile")

        LockingManager.__instance._lockFile.load()

    @staticmethod
    def pushLocks(repo):
        """Saves the lock settigs to the remote repository

        Args:
            repo(GitRepository): currently open repository that the file belongs to
        """
=======
    def updateLocks():
        """Syncronizes the local locks with the remote locks, manually merge local data with remote
        """
        # TODO: Sync with repo, as described below
        # https://www.quora.com/How-can-I-pull-one-file-from-a-Git-repository-instead-of-the-entire-project/answer/Aarti-Dwivedi
        # fetch
        # checkout from latest commit lock and permissions files
        # create new LockFile object off of it and merge with current object
        # save date
        # if lockfile has changed stage, commit, and push it
>>>>>>> 92915ef9bb62dc34149b5b5d6f1402700b38d0cb
        if LockingManager.__instance is None:
            LockingManager()
        #Save current lockfile
        LockingManager.__instance._lockFile.save()
        #Stage lockfile changes
        #Must be relitive to worktree root
        repo.index.add(LockingManager.LOCKFILE_DIR[:-1] + '/' + LockingManager.LOCKFILE_NAME)
        repo.index.write()
        tree = repo.index.write_tree()
        #Commit and push
        repo.commit_push(tree, "MEG LOCKFILE UPDATE")


