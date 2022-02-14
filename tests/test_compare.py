import pytest

from branch_detective import compare
from branch_detective.commits import CommitLog

from . import mock_source, mock_dest, mock_dest_2


def test_missing_by_message():
    source = CommitLog(mock_source)
    dest = CommitLog(mock_dest)
    missing = compare.find_missing_by_message(source, dest)

    expected_missing = [
        'c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3'
    ]
    for commit, expected in zip(missing, expected_missing):
        assert commit.sha == expected


@pytest.mark.parametrize(
    "simulate, expected_missing",
    (
        (
            mock_dest, [
                'a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1',
                'c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3',
            ],
        ),
        (
            mock_dest_2, [
                'a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1',
            ],
        ),
    )
)
def test_missing_by_sha(simulate, expected_missing):
    source = CommitLog(mock_source)
    dest = CommitLog(simulate)
    missing = compare.find_missing_by_sha(source, dest)

    for commit, expected in zip(missing, expected_missing):
        assert commit.sha == expected
