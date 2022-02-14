import click

from datetime import datetime, timezone
from typing import Optional

from branch_detective.repository import RepositoryLens
from branch_detective.compare import find_missing_by_message, find_missing_by_sha


def overwrite(message: str, nl: bool = False) -> None:
    click.echo(f"{' '*64}\r", nl=False)
    if nl:
        click.echo(f"{message}", nl=True)
    else:
        click.echo(f"{message}\r", nl=False)


def verify_date(date: str, arg_name: str) -> Optional[datetime]:
    if date:
        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise RuntimeError(
                f"Time stamp for {arg_name} must be in format 'YYYY-MM-DD'"
            )
        else:
            dt = dt.astimezone(timezone.utc)
            return dt
    else:
        return None


@click.command(help="""branch-detective examines a Git repository to determine
which commits are present on a SOURCE branch, but are absent from a DEST
branch.""")
@click.argument(
    'source_branch'
)
@click.argument(
    'dest_branch'
)
@click.option(
    '--by-message/--by-sha', default=True,
    help='search for duplicates by commit message or by commit sha'
)
@click.option(
    '-s', '--since', default=None,
    help="the date (as 'YYYY-MM-DD') before which commits should be ignored."
)
@click.option(
    '-b', '--before',
    help="the date (as 'YYYY-MM-DD') after which commits should be ignored."
)
@click.option(
    '--ignore-merge', is_flag=True, default=False,
    help="ignore merge commits"
)
@click.option(
    '-a', '--show-all', is_flag=True, default=False,
    help="automatically display all missing commits instead of paging"
)
@click.pass_context
def main(
    ctx, source_branch: str, dest_branch: str,
    by_message: bool, ignore_merge: bool,
    since: str, before: str,
    show_all: bool
):
    try:
        since_dt: Optional[datetime] = verify_date(since, '--since')
        before_dt: Optional[datetime] = verify_date(before, '--before')
    except RuntimeError as e:
        click.echo(e, err=True)
        ctx.exit(1)
        return

    overwrite("Examining branches...", nl=False)

    try:
        repo = RepositoryLens(source_branch, dest_branch)
        source_log = repo.source_log
        dest_log = repo.dest_log
    except RuntimeError as e:
        click.echo(e, err=True)
        ctx.exit(1)
        return

    overwrite("Comparing commits...", nl=False)

    if by_message:
        missing = find_missing_by_message(
            source_log, dest_log, ignore_merge=ignore_merge,
            since=since_dt, before=before_dt
        )
    else:
        missing = find_missing_by_sha(
            source_log, dest_log, ignore_merge=ignore_merge,
            since=since_dt, before=before_dt
        )

    overwrite("Elementary, dear Watson!", nl=True)

    click.echo(
        f"{len(missing)} commits from {source_branch} missing in {dest_branch}"
    )

    missing_count = len(missing)
    for num, commit in enumerate(missing, start=1):
        click.echo(f' {num} of {missing_count} '.center(50, '='))
        click.echo()
        click.echo(commit)
        if (
            not show_all and
            not num == missing_count and
            not click.confirm('Show next?', default=True)
        ):
            break
