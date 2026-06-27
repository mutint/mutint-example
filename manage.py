#!/usr/bin/env python
"""
Entry point for standalone mutint-app development.
Mirrors the pattern in aledb-core/aledb but for this app's config.
"""
import os
import sys


def main():
    # Project root is always first so `import config` finds THIS config/, not aledb-core's.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
