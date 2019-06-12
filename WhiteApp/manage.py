#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import requests
from async_message import send
from async_message import receive


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WhiteApp.settings')
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

    response = requests.get("http://localhost:5000/time")
    if response:
        print('Success!')
        print(response.text)
    else:
        print('An error has occurred.')

    send.send()
    receive.receive()
