from datetime import datetime
from typing import Optional

from branch_detective.commits import CommitLog


def find_missing_by_message(
    source: CommitLog, dest: CommitLog,
    ignore_merge: bool = False,
    since: Optional[datetime] = None, before: Optional[datetime] = None
) -> CommitLog:
    """Find the commits that are present in 'source', but absent in 'dest',
    using the commit message for lookup.

    source: the CommitLog commits are coming from
    dest: the CommitLog we're looking for missing commits in
    ignore_merge: whether to ignore merge commits (default False)
    since: if defined, the date before which (source) commits are ignored.
    before: if defined, the date after which (source) commits are ignored.
    """

    missing_commits = CommitLog()

    # Look through all the commits in the source log
    for commit in source:
        # Skip merge commits if requested
        if ignore_merge and commit.is_merge:
            continue
        # Skip commits after the "before" date, if one is defined
        if before and commit.date > before:
            continue
        # Skip commits before the "since" date, if one is defined
        if since and commit.date < since:
            continue

        # Search the destination log for the commit message being considered.
        if not dest.includes_commit_by_message(commit.message):
            # If the commit is missing in destination, track it.
            missing_commits.append(commit)

    return missing_commits


def find_missing_by_sha(
    source: CommitLog, dest: CommitLog,
    ignore_merge: bool = False,
    since: datetime = None, before: datetime = None
) -> CommitLog:

    missing_commits = CommitLog()

    for commit in source:
        if ignore_merge and commit.is_merge:
            continue
        if since and commit.date < since:
            continue
        if before and commit.date > before:
            continue
        if not dest.includes_commit_by_sha(commit.sha):
            missing_commits.append(commit)

    missing_commits.sort_by_date()
    return missing_commits
