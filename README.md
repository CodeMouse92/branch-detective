# Branch Detective

Are you baffled by backports? Confused by cherry-picks? Muddled by merges?
Branch Detective is the easy way to see what commits are present in one
branch and absent from the other.

To use, just run `branch-detective` from the Git repository you're
examining, and pass the two branches you're comparing. The first branch is
the **source** branch, where commits are coming *from*. The second branch
is the **destination** branch, which you're search through for the commits in.
If a commit is present in source, but not in destination, that commit is
considered "missing".

If you don't specify the source, the current branch will be used, and if you don't
specify the destination, the local copy of the default branch (e.g. `main`) will be
used. Thus, `branch-detective` without any arguments will display the commits present
in the current branch, but absent from `main`.

To keep things simple, Branch Detective will not tell you about commits
present in the destination branch, but not in the source branch. To see these,
rerun Branch Detective with the branches swapped.

## Pretty PR Descriptions!

You can output the list of commits in Markdown format, for copying and pasting
as your Pull Request/Merge Request description. Just pass the `--markdown`
or `-m` option.

If all your commits consist either of a single line _or_ have a blank line between
the header line and the body of the commit, then the first line will be formatted
as a heading 2 (`## like this`). If your commits don't follow this structure,
horizontal rules with dashes will be used to separate commits instead (`-----`).

## Search by Message or SHA

Different Git platforms handle your repository in different ways. In some,
it is possible to directly compare the unique SHAs of commits in different
branches. However, in many cases, these SHAs are changed through merges,
cherry-picks, rebases, and other history-altering changes.

By default, Branch Detective uses the **commit message** to determine if two
commits are identical. It also knows how to ignore "cherry pick" footers
to minimize false positives for missing commits.

If you prefer, you can pass the argument `--by-sha` to compare by
**commit SHA** instead. This will check for commits in the destination
branch that match the SHA either directly or via the cherry pick footer.
Thus, if commit `a1b2c3` is cherry-picked from the source branch into
the destination branch, while it will actually have a different SHA, it will
be considered a match by Branch Detective, since the cherry pick footer will
contain the source SHA `a1b2c3`.

## Ignore Merges...or Don't

If your Git platform generates merge commits *in addition* to the regular
commits themselves, Branch Detective allows you to ignore merge commits
altogether. This cuts through the muck of the merge process and shows you only
those missing commits that actually contain real code changes.

By default, merge commits are considered. To ignore merge commits, pass the
`--ignore-merge` flag.

## Since When?

If you want to only inspect commits in a particular time range, you can use
the `--since` and/or `--before` options. For both, pass a date in the form
`YYYY-MM-DD` (e.g. `--since 2022-01-01` or `--before 2021-05-04`).

## Show Some or Show All

By default, Branch Detective shows you one commit at a time, and waits for
you to hit enter to continue. However, if you want to see all the commits
at once, such as if you're exporting the output to a file, pass the
`--show-all` or `-a` flag to show all the missing commits at once.

```bash
branch-detective devel main --show-all
```

## Potential Pitfalls

Branch Detective either looks at the commit message or the SHA. To minimize
false positives or false negatives due to workflow, we ignore dates and authors
as part of commit matching.

This does mean that if you have multiple commits with the same message, if
only one is present in the destination branch, it will not see *any* of the
commits in the source branch with the matching commit message as missing.

## Installing Branch Detective

You can install Branch Detective directly from [PyPI][2] via pip.
(We recommend you do this in a virtual environment.)

```bash
pip install branch-detective
```

## Found a Bug? Need a Feature?

Please report bugs and missing features on the
[Branch Detective repository][1]. Pull requests are also encouraged!

[1]: https://github.com/codemouse92/branch-detective
[2]: https://pypi.org/project/branch-detective/
