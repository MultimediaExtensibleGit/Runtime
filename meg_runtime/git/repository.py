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

    def stageChanges(self):
        """Adds changes to the index
        Only adds changes allowd by locking module
        """
        self.index.add_all()
        entriesToAdd = []
        for changedFile in self.index:
            lockEntry = LockingManager.findLock(changedFile.path)
            if lockEntry is None or lockEntry["user"] == Config.get('user/username'):
                entriesToAdd.append(changedFile)
        self.index.read(force=True)
        for entry in entriesToAdd:
            self.index.add(entry)
        self.index.write()

    def pull(self, remote_name='origin', fail_on_conflict=False):
        """Pull and merge
        Merge is done fully automaticly, currently uses 'ours' on conflicts
        TODO: Preform a proper merge with the locking used to resolve conflicts
        4/13/20 21 - seems to be working for both merge types

        Args:
            remote_ref_name (string): name of reference to the remote being pulled from
        """
        self.fetch_all()

        #Branches are not handled very elegently in pygit2s
        headBranch = None
        for branch in pygit2.repository.Branches(self):
            if pygit2.repository.Branches(self)[branch].is_head():
                headBranch = pygit2.repository.Branches(self)[branch]

        if self.isChanged():
            #Stage changes that are allowd by locking system
            self.stageChanges()
            self.create_commit('HEAD', self.default_signature, self.default_signature, "MEG PULL OWN", self.index.write_tree(), [self.head.target])

        #Prepare for a merge
        remoteId = self.lookup_reference(headBranch.upstream_name).target
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
            if fail_on_conflict:
                self.state_cleanup()
                return False
            self.merge_commits(self.head.peel(), self.lookup_reference(headBranch.upstream_name).peel(), favor='ours')
            author = self.default_signature
            tree = self.index.write_tree()
            commit = self.create_commit('HEAD', author, author, "MEG MERGE", tree, [self.head.target, remoteId])
        self.state_cleanup()
        return True
        
    def push(self, remote_name='origin', username=None, password=None):
        """Pushes current commits
        4/13/20 21 - seems to be working

        Args:
            remote_name (string, optional): name of the remote to push to
            username (string, optional): username of user account used for pushing
            password (string, optional): password of user account used for pushing
        """
        if username is None:
            username = Config.get('user/username')
        if password is None:
            password = Config.get('user/password')
        creds = pygit2.UserPass(username, password)
        remote = self.remotes[remote_name]
        remote.credentials = creds
        try:
            remote.push([self.head.name], callbacks=pygit2.RemoteCallbacks(credentials=creds))
        except GitError as e:
            Logger.warning("MEG Git Repository: Failed to push commit")

    def commit_push(self, tree, message, remote_name='origin', username=None, password=None):
        """Commits and pushes staged changes in the tree
        TODO: Ensure that the config keys are correct
        4/13/20 21 - seems to be working

        Args:
            tree (Oid): Oid id created from repositiory index (ex: repo.index.write_tree()) containing the tracked file changes (proably)
            message (string): commit message
            remote_name (string, optional): name of the remote to push to
            username (string, optional): username of user account used for pushing
            password (string, optional): password of user account used for pushing
        """
        #Create commit on current branch, parent is current commit, author and commiter is the default signature
        self.create_commit(self.head.name, self.default_signature, self.default_signature, message, tree, [self.head.target])
        self.push(remote_name, username, password)

    def isChanged(self):
        """Are there local changes from the last commit
        Only counts changes for locking module commitable files
        """
        for diff in self.index.diff_to_workdir():
            lockEntry = LockingManager.findLock(diff.delta.old_file.path)
            if lockEntry is None or lockEntry["user"] == Config.get('user/username'):
                return True
        return False

    def sync(self, remote_name='origin', username=None, password=None):
        """Pulls and then pushes, merge conflicts resolved by pull

        Args:
            username (string, optional): username of user account used for pushing
            password (string, optional): password of user account used for pushing
        """
        self.pull(remote_name)
        self.push(remote_name, username=None, password=None)

