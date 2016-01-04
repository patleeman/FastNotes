#!/usr/bin/python3
"""
This script will execute all necessary commands to set up the note alias on your computer.
"""
import os

from settings import FAST_NOTES_ALIAS
# todo: Add script to set up alias.

def run():
    note_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'note.py')
    alias = """

    # Alias for FastNotes CLI tool.
    alias {alias}=\"/usr/bin/python3 {note_path}\"

    """.format(
        alias=FAST_NOTES_ALIAS,
        note_path=note_path,
    )

    bash_alias = os.path.join(os.path.expanduser('~'), '.bash_aliases')

    # Open bash_alias file
    with open(bash_alias, 'a+') as f:
        f.write(alias)
    print("The alias {} has been added to your .bash_aliases file.".format(FAST_NOTES_ALIAS))

if __name__ == '__main__':
    run()
