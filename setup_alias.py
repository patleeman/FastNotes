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
    print(note_path)
    print(alias)
    # Open bashrc file
    #with

if __name__ == '__main__':
    run()
