def is_using_conventional_commits(messages):
    """Return false if any of the messages does not have a header line, meaning it contains
    more than one line, but the second line is not blank.
    """
    for message in messages:
        lines = message.split('\n')
        # If any of the commits do not use header lines, assume we don't use conventional commits.
        if len(lines) > 1 and lines[1] != "":
            return False
    return True

def format_message_as_markdown(message, conventional):
    """Format the message in markdown.

    message - the raw commit message to format
    conventional - if True, make the header line a real header; otherwise, separate commits with lines.
    """
    lines = message.split('\n')
    if conventional:
        lines[0] = f"## {lines[0]}"
    else:
        lines.append('\n-----')
    return '\n'.join(lines)

def markdown_description(commits):
    """Convert list of commits to a string in markdown for use as a PR description.
    """
    messages = [
        commit.message
        for commit in commits
    ]
    conventional = is_using_conventional_commits(messages)
    formatted_messages = [
        format_message_as_markdown(message, conventional)
        for message in messages
    ]

    return "\n\n".join(formatted_messages)
