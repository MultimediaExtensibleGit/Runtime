"""Git repository"""

from pygit2 import init_repository, clone_repository, Repository, GitError
from meg_runtime.logger import Logger
from meg_runtime.config import Config


# Git exception
class GitException(Exception):
    """Git exception"""

    # Git exception constructor
    def __init__(self, message, **kwargs):
        """Git exception constructor"""
        super().__init__(message, **kwargs)


# Git repository
class GitRepository(Repository):
    """Git repository"""

    # Git repository constructor
    def __init__(self, path, url=None, checkout_branch=None, bare=False, init=False, *args, **kwargs):
        """Git repository constructor"""
        # Check for special construction
        if init:
            # Initialize a new repository
            self.__dict__ = init_repository(path, bare=bare, workdir_path=path, origin_url=url).__dict__
        elif url is not None:
            # Clone a repository
            self.__dict__ = clone_repository(url, path, bare=bare, checkout_branch=checkout_branch).__dict__
        # Initialize the git repository super class
        super().__init__(path, *args, **kwargs)

    # Git repository destructor
    def __del__(self):
        # Free the repository references
        self.free()

    # Fetch remote
    def fetch(self, remote_name='origin'):
        for remote in self.remotes:
            if remote.name == remote_name:
                remote.fetch()

    # Fetch all remotes
    def fetch_all(self):
        for remote in self.remotes:
            remote.fetch()

    # TODO: Pull the remote repository
    def pull(self, remote_name='origin'):
        pass

    def commit_push(self, tree, message, remote_name='origin'):
        """Commits and pushes staged changes in the tree
        TODO: Ensure that the config keys are correct
        TODO: Test

        Args:
            tree (Oid): Oid id created from repositiory index (ex: repo.index.write_tree()) containing the tracked file changes (proably)
            message (string): commit message
            remote_name (string, optional): name of the remote to push to
        """
        author = pygit2.Signature(Config.get('user/name'), Config.get('user/email'))
        #Create commit on current branch, parent is current commit, author and commiter is the user
        oid = self.create_commit(self.head.name, author, author, message, tree, [self.head.get_object().hex])
        creds = pygit2.UserPass(Config.get('user/username'), Config.get('user/password'))
        remote = self.remotes[remote_name]
        remote.credentials = creds
        try:
            remote.push([self.head.name], callbacks=pygit2.RemoteCallbacks(credentials=creds))
        except GitError as e:
            Logger.warning("MEG Git Repository: Failed to push commit")
