#!/usr/bin/env python
import os
import sys
from pathlib import Path

from django.core.management import execute_from_command_line
from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    load_dotenv(Path(__file__).parent / '.env.dev')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
