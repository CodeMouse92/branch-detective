import pytest

from datetime import datetime, timedelta, timezone

from branch_detective.commits import Commit, CommitLog
from . import mock_commits, mock_source, mock_dest


@pytest.mark.parametrize(
    "mock_commit, expected",
    (
        (
            mock_commits['amazing'],
            'a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1'
        ),
        (
            mock_commits['flerm'],
            'b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2'
        ),
        (
            mock_commits['plootash'],
            'c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3'
        ),
        (
            mock_commits['flerm_cherry'],
            'd4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4'
        ),
    )
)
def test_commit_sha(mock_commit, expected):
    commit = Commit(mock_commit)
    assert commit.sha == expected


@pytest.mark.parametrize(
    "mock_commit, expected",
    (
        (
            mock_commits['amazing'],
            'Bob Smith <bob@example.com>'
        ),
        (
            mock_commits['flerm'],
            'Jane Plain <jane@example.com>'
        ),
        (
            mock_commits['plootash'],
            'Jane Plain <jane@example.com>'
        ),
        (
            mock_commits['flerm_cherry'],
            'Jane Plain <jane@example.com>'
        ),
    )
)
def test_commit_author(mock_commit, expected):
    commit = Commit(mock_commit)
    assert commit.author == expected


@pytest.mark.parametrize(
    "mock_commit, expected",
    (
        (
            mock_commits['amazing'],
            datetime(
                year=2022, month=2, day=1,
                hour=14, minute=22, second=33,
                tzinfo=timezone(timedelta(hours=-5))
            )
        ),
        (
            mock_commits['flerm'],
            datetime(
                year=2022, month=3, day=13,
                hour=9, minute=8, second=7,
                tzinfo=timezone(timedelta(hours=-7))
            )
        ),
        (
            mock_commits['plootash'],
            datetime(
                year=2022, month=3, day=14,
                hour=11, minute=15, second=27,
                tzinfo=timezone(timedelta(hours=-7))
            )
        ),
        (
            mock_commits['flerm_cherry'],
            datetime(
                year=2022, month=3, day=17,
                hour=9, minute=8, second=7,
                tzinfo=timezone(timedelta(hours=-7))
            )
        ),
    )
)
def test_commit_date(mock_commit, expected):
    commit = Commit(mock_commit)
    assert commit.date == expected


@pytest.mark.parametrize(
    "mock_commit, expected_flag, expected_value",
    (
        (
            mock_commits['amazing'],
            False,
            None
        ),
        (
            mock_commits['flerm'],
            False,
            None
        ),
        (
            mock_commits['plootash'],
            True,
            '0z0z0z0 1y1y1y1'
        ),
        (
            mock_commits['flerm_cherry'],
            False,
            None
        ),
    )
)
def test_commit_merge(mock_commit, expected_flag, expected_value):
    commit = Commit(mock_commit)
    assert commit.is_merge == expected_flag
    assert commit.merge == expected_value


@pytest.mark.parametrize(
    "mock_commit, expected",
    (
        (
            mock_commits['flerm'],
            None
        ),
        (
            mock_commits['flerm_cherry'],
            'b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2'
        ),
    )
)
def test_commit_cherrypick(mock_commit, expected):
    commit = Commit(mock_commit)
    assert commit.cherry_pick == expected


@pytest.mark.parametrize(
    "mock_commit, expected",
    (
        (
            mock_commits['amazing'],
            """feat: amazing feature

amazing feature does amazing things amazingly
it's so amazing
such wow"""
        ),
        (
            mock_commits['flerm'],
            """bug: fix flerminator

flerminator was flermming incorrectly
now it flerms flermily"""
        ),
        (
            mock_commits['plootash'],
            """Merge feature/plootash into devel

feat: plootash

plootash can be flermed when flerming requires target
because that makes sense"""
        ),
        (
            mock_commits['flerm_cherry'],
            """bug: fix flerminator

flerminator was flermming incorrectly
now it flerms flermily"""
        ),
    )
)
def test_commit_message(mock_commit, expected):
    commit = Commit(mock_commit)
    for line, expected_line in zip(commit.message.split('\n'), expected.split('\n')):
        assert line == expected_line


@pytest.mark.parametrize(
    "raw, expected_shas",
    (
        (
            mock_source,
            [
                'a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1',
                'b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2',
                'c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3',
            ],
        ),
        (
            mock_dest,
            [
                'e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5',
                'd4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4',
            ]
        )
    )
)
def test_commitlog(raw, expected_shas):
    log = CommitLog(raw)
    for commit, expect in zip(log, expected_shas):
        assert commit.sha == expect
