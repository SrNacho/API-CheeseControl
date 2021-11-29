#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv


def main():
    """Run administrative tasks."""
    dotenv_path = os.path.join(os.path.dirname(__file__), 'VARIABLES.env')
    dotenv.read_dotenv(dotenv_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'api_cheesecontrol.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
