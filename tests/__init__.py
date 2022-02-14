# NOTE: Because VS Code strips trailing whitespace from lines, I am using
# '%' in place of deliberate spaces in the strings below, and then replacing
# '%' with ' '. This ensures the messages follow the same format as the ones
# actually returned by 'git log'

mock_commits = {
    "amazing": """commit a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1
Author: Bob Smith <bob@example.com>
Date:   Tue Feb 1 14:22:33 2022 -0500

%%%%feat: amazing feature
%%%%
%%%%amazing feature does amazing things amazingly
%%%%it's so amazing
%%%%such wow
""".replace('%', ' '),

    "flerm": """commit b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2
Author: Jane Plain <jane@example.com>
Date:   Thu Mar 13 09:08:07 2022 -0700

%%%%bug: fix flerminator
%%%%
%%%%flerminator was flermming incorrectly
%%%%now it flerms flermily
""".replace('%', ' '),

    "plootash": """commit c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3
Merge: 0z0z0z0 1y1y1y1
Author: Jane Plain <jane@example.com>
Date:   Fri Mar 14 11:15:27 2022 -0700

%%%%Merge feature/plootash into devel
%%%%
%%%%feat: plootash
%%%%
%%%%plootash can be flermed when flerming requires target
%%%%because that makes sense
""".replace('%', ' '),

    "flerm_cherry": """commit d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4
Author: Jane Plain <jane@example.com>
Date:   Thu Mar 17 09:08:07 2022 -0700

%%%%bug: fix flerminator
%%%%
%%%%flerminator was flermming incorrectly
%%%%now it flerms flermily
%%%%
%%%%(cherry picked from commit b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2)
""".replace('%', ' '),

    "amazing_b": """commit e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5
Author: Bob Smith <bob@example.com>
Date:   Tue Feb 1 14:28:19 2022 -0500

%%%%feat: amazing feature
%%%%
%%%%amazing feature does amazing things amazingly
%%%%it's so amazing
%%%%such wow
""".replace('%', ' ')
}

mock_source = '\n\n'.join([
    mock_commits['amazing'],
    mock_commits['flerm'],
    mock_commits['plootash']
])

mock_dest = '\n\n'.join([
    mock_commits['flerm_cherry'],  # will sort to index 1
    mock_commits['amazing_b'],  # will sort to index 0
])

mock_dest_2 = '\n\n'.join([
    mock_commits['flerm'],
    mock_commits['amazing_b'],
])
