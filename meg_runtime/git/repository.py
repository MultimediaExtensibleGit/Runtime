"""Git repository"""

import pygit2
from pygit2 import init_repository, clone_repository, Repository, GitError
from meg_runtime.logger import Logger
from meg_runtime.config import Config
from meg_runtime.locking import LockingManager


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

    def pull(self, remote_ref_name='refs/remotes/origin/master'):
        """Pull and merge
        Merge is done fully automaticly, currently uses 'ours' on conflicts
        TODO: Preform a proper merge with the locking used to resolve conflicts
        TODO: Test

        Args:
            remote_ref_name (string): name of reference to the remote being pulled from
        """
        self.fetch_all()
        #Stage changes that are allowd by locking system
        self.index.add_all()
        for changedFile in self.index:
            lockEntry = LockingManager.findLock(changedFile.path)
            if not lockEntry is None:
                if lockEntry["user"] != Config.get('user/username'):
                    self.index.rm(changedFile.path)

        #Commit and prepare for a merge
        remoteId = self.lookup_reference(remote_ref_name).target
        mergeState, _ = self.merge_analysis(remoteId)
        
        if mergeState & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
            #Fastforward and checkout remote
            self.checkout_tree(self.get(remoteId))
            self.head.set_target(remoteId)
            self.checkout_head()
        elif mergeState & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
            #Preform merge
            '''TODO: Preform a proper merge with the locking
            self.merge(remoteId)
            #conflit (IndexEntry(ancester, ours, theirs))
            for conflit in self.index.conflicts:'''
            self.merge_commits(self.head.peel(), self.lookup_reference(remote_ref_name).peel(), favor='ours')
            author = self.default_signature
            tree = self.index.write_tree()
            commit = self.create_commit('HEAD', author, author, "MEG MERGE", tree, [self.head.target, remoteId])
        self.state_cleanup()
        
    def push(self, remote_name='origin'):
        """Pushes current commits
        TODO: Ensure that the config keys are correct
        TODO: Test

        Args:
            remote_name (string, optional): name of the remote to push to
        """
        creds = pygit2.UserPass(Config.get('user/username'), Config.get('user/password'))
        remote = self.remotes[remote_name]
        remote.credentials = creds
        try:
            remote.push([self.head.name], callbacks=pygit2.RemoteCallbacks(credentials=creds))
        except GitError as e:
            Logger.warning("MEG Git Repository: Failed to push commit")

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
        self.create_commit(self.head.name, author, author, message, tree, [self.head.get_object().hex])
        self.push(remote_name)
        
    def isChanged(self):
        return len(self.index.diff_to_workdir()) > 0

    def sync(self, remote_ref_name='refs/remotes/origin/master'):
        """Pulls and then pushes, merge conflicts automaticly resolved by pull
        """
        if self.isChanged():
            self.pull()
            self.push()
        else:
            self.pull()

