"""Initialization module for the application"""

import sys

from .controller import file_controller
from .models.entities import User


def run():
    # Expect receive -r or --reset flag
    if len(sys.argv) > 1:
        if sys.argv[1] == "-r" or sys.argv[1] == "--reset":
            print("Resetting databases...")
            file_controller.reset()

    user = User(id=1, name="j4breu", password="qwerty")
    user = file_controller.details(user)
    print(user)

    # user = file_controller.de()
    # print(user)

    print("Done!")
