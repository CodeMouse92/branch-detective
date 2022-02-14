import re

from datetime import datetime
from typing import List, Optional


class Commit:
    """Stores the data for a single commit, as parsed out of 'git log'.
    """

    DATETIME_FORMAT_STR: str = '%a %b %d %H:%M:%S %Y %z'
    CHERRY_PICK_REGEX: str = r'\(cherry picked from commit \w+\)'

    def __init__(self, raw_commit: str):
        """Initiates a new commit object from the raw string output
        of 'git log'. Only picks up the following data:
        * SHA
        * Author
        * Date, as a datetime
        * Merge (optional)
        * Message, sans "cherry pick" footers
        * Cherry Pick (optional), parsed from first "cherry pick" footer
        """

        # Split the raw 'git log' data into lines.
        lines = [line for line in raw_commit.split('\n')]

        # The first line is always the commit, in format 'commit THE_SHA_HERE'
        self.sha = lines[0].split()[1]

        # Process headings first (any line starting with a "Key" and colon)
        headings = {}
        for line in lines[1:]:
            if not line or line.startswith('    '):
                break
            key, value = line.split(': ')
            headings[key.strip().lower()] = value.strip()

        # Parse the 'Author:' field (required)
        try:
            self.author: str = headings['author']
        except KeyError:
            raise RuntimeError(f"Commit {self.sha} missing 'Author:' field.")

        # Parse the 'Date:' field as a datetime object (required)
        try:
            self.date: datetime = datetime.strptime(
                headings['date'], self.DATETIME_FORMAT_STR
            )
        except KeyError:
            raise RuntimeError(f"Commit {self.sha} missing 'Date:' field.")

        # Parse the 'Merge:' field (optional)
        self.merge: Optional[str] = None
        self.is_merge: bool = False

        try:
            self.merge = headings['merge']
            self.is_merge = True
        except KeyError:
            # it is reasonable for a commit to lack a Merge: field
            pass

        # Parse out the commit message, removing leading whitespace, but
        # preserving original line breaks.
        message = '\n'.join(
            (
                line.lstrip(' ')
                for line in lines
                if line.startswith('    ') or not line
            )
        )
        message = message.strip()

        # Parse out the cherry pick from the commit message (optional),
        # also removing it from the commit message itself.
        self.cherry_pick: Optional[str] = None
        cherry_pick = re.search(self.CHERRY_PICK_REGEX, message)
        if cherry_pick:
            cherry_pick = cherry_pick.group()
            self.cherry_pick = cherry_pick.split('commit')[-1][:-1].strip()

        self.message = re.sub(self.CHERRY_PICK_REGEX, '', message).strip()

    def __str__(self) -> str:
        """Return the Commit as a string, similar to the output of 'git log',
        but reconstituted from the parsed data."""
        return "\n".join([
            f"commit {self.sha}",
            f"Author: {self.author}",
            f"Date: {self.date.strftime(self.DATETIME_FORMAT_STR)}",
            f"Merge: {self.merge}\n" if self.merge else "",
            f"{self.message}",
            ""
        ])


class CommitLog:
    """A collection of Commit objects, parsed from the raw output of 'git log'.
    """

    COMMIT_REGEX: str = r'commit \w+\n(?:\w+: .+\n)+\n(?:    .*\n)+'

    def __init__(self, raw_log: Optional[str] = None):
        """Create a new commit log, optionally initializing it from the raw
        output of 'git log'.
        """
        self.commits: List[Commit] = []

        # If a raw log (string) was provided, parse out each commit
        # as a Commit object.
        if raw_log:
            commits = re.findall(self.COMMIT_REGEX, raw_log)
            self.commits = [Commit(commit) for commit in commits]

    def __iter__(self):
        """Iterate over the commits, sorted by date (ascending)."""
        self.sort_by_date()
        return iter(self.commits)

    def __len__(self) -> int:
        """Returns the number of commits in the log."""
        return len(self.commits)

    def includes_commit_by_message(self, message):
        """Check for a commit based on its commit message."""
        # note: cherry pick footers are removed from commit messages
        # during parsing in Commit.__init__(), so they won't cause
        # false negatives here.
        for commit in self.commits:
            if message == commit.message:
                return True
        return False

    def includes_commit_by_sha(self, sha, include_cherry_pick=True):
        """Check for a commit based on its SHA."""
        for commit in self.commits:
            if sha == commit.sha:
                return True
            if include_cherry_pick and sha == commit.cherry_pick:
                return True
        return False

    def append(self, commit: Commit) -> None:
        """Store a commit."""
        self.commits.append(commit)

    def sort_by_date(self) -> None:
        """Sort the commits in the commit log by date (ascending).
        Ordinarily, you don't need to call this directly; iterating
        over the CommitLog calls this automatically up front."""
        self.commits = sorted(self.commits, key=lambda x: x.date)
