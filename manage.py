#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# manage.py
import os
import sys
import asyncio
from bot.bot import main


def main_sync():
    # This is a synchronous wrapper for your asynchronous main() function
    asyncio.run(main())


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_conf.settings')

    try:
        from django.core.management import execute_from_command_line

        # Check if 'runserver' is in command-line arguments
        if 'runbot' in sys.argv:
            # If yes, call the synchronous entry point
            main_sync()
        else:
            # If not, proceed with Django's normal execution
            execute_from_command_line(sys.argv)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


