"""MutInt's own version.

Same shape as mutint_common/version.py, and discovered by the same `version`
management command because this app is installed -- so `./mutint version` reports
MutInt alongside the mutint-core it runs on, and `--component MutInt --bump patch`
rewrites this file.

NAME is what the command and the sidebar call it; without it the command would
fall back to the app label, `mutint_app`.
"""

NAME = "MutInt"

__version__ = "0.0.1"


def get_version():
    return __version__
