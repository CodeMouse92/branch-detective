import git
from git.repo import Repo

from branch_detective.commits import CommitLog


class RepositoryLens:
    """Provides an interface to the repository in the current working
    directory."""

    def __init__(self, source_branch: str, dest_branch: str):
        """Initializes a new RepositoryLens that works with the Git
        repository in the current working directory, and which specifically
        verifies and examines the source and destination branches specified
        by the user.

        source_branch: the name of the branch from which commits are examined
        dest_branch: the name of the branch to check for missing commits
        """
        # Ensure the current working directory is a valid Git repository, and
        # create a connection to it.
        try:
            self.repo = Repo('.')
        except git.exc.InvalidGitRepositoryError:
            raise RuntimeError("This is not a valid Git repository.")

        # Verify the requested 'source' branch is valid.
        self.source_branch: str = source_branch
        if source_branch not in self.repo.heads:
            raise RuntimeError(f"Unknown source branch: {source_branch}")

        # Verify the requested 'dest' branch is valid.
        self.dest_branch: str = dest_branch
        if dest_branch not in self.repo.heads:
            raise RuntimeError(f"Unknown destination branch: {dest_branch}")

        # Ensure there are no uncommitted changes, so we can switch branches.
        if self.repo.is_dirty():
            raise RuntimeError("There are uncommitted changes. Aborting.")

        self._source_log: CommitLog = CommitLog()
        self._dest_log: CommitLog = CommitLog()

    @property
    def raw_source_log(self) -> str:
        """Retrieve the raw (text) output of 'git log' for the source branch.
        """
        active_branch = self.repo.active_branch.name
        self.repo.heads[self.source_branch].checkout()
        raw_log = self.repo.git.log()
        self.repo.heads[active_branch].checkout()
        return raw_log

    @property
    def raw_dest_log(self) -> str:
        """Retrieve the raw (text) output of 'git log' for the dest branch.
        """
        active_branch = self.repo.active_branch.name
        self.repo.heads[self.dest_branch].checkout()
        raw_log = self.repo.git.log()
        self.repo.heads[active_branch].checkout()
        return raw_log

    @property
    def source_log(self) -> CommitLog:
        """Return, and construct if necessary, the CommitLog generated from the
        raw (text) output of 'git log' for the source branch. This will not
        attempt to reparse the log after an initial call."""
        if not self._source_log:
            self._source_log = CommitLog(self.raw_source_log)
        return self._source_log

    @property
    def dest_log(self) -> CommitLog:
        """Return, and construct if necessary, the CommitLog generated from the
        raw (text) output of 'git log' for the dest branch. This will not
        attempt to reparse the log after an initial call."""
        if not self._dest_log:
            self._dest_log = CommitLog(self.raw_dest_log)
        return self._dest_log
