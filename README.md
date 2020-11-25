# RedSquare

RedSquare is a discord moderation bot for leftist communities. Features are implemented as they are requested by users, so as to avoid
"complexity overload" for users. If you are looking for an all inclusive moderation tool, are confident in your technical literacy, and/or
are not a leftist community, kindly consider finding another project or discord bot to make use of. If you are a leftist community looking
for a moderation solution that works to your convenience, please feel free to reach out to me about any features you need, how to access
features that already exist, etc.

RedSquare is currently under development, but when it's ready to be used an invite link will be available here.

## Development

RedSquare is built in Python 3.8 using discord.py along with some supplemental development tools that you should get acquainted with
if you intend to directly contribute to RedSquare, such as pyre-check and black.

## Building

RedSquare uses `poetry` as a management tool, so make sure you [install](https://python-poetry.org/docs/#installation) it before continuing.

```
$ poetry install
$ poetry run python src/main.py
```
