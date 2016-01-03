#!/usr/bin/python3
"""
This script will execute all necessary commands to set up the note alias on your computer.
"""
import os

from settings import FAST_NOTES_ALIAS
# todo: Add script to set up alias.

def run():
    note_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'note.py')
    alias = 'alias {}="/usr/bin/python3 {}"'.format(FAST_NOTES_ALIAS, note_path)
    commands = [
        "\n\n",
        "# Alias for FastNotes CLI tool.\n",
        alias,
        "\n\n",
    ]

    bashrc = os.path.join(os.path.expanduser('~'), '.bashrc')

    # Open bashrc file
    with open(bashrc, 'a') as f:
        f.writelines(commands)

    print("The alias {} has been added to your .bashrc file.".format(FAST_NOTES_ALIAS))

if __name__ == '__main__':
    run()
