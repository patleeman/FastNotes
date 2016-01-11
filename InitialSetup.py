#!/usr/bin/python3
"""
This script will execute all necessary commands to set up the note alias on your computer.
"""
import os
import json

from settings import FAST_NOTES_ALIAS


def run():
    note_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'note.py')
    alias = """# Alias for FastNotes CLI tool.alias\n {alias}=\"/usr/bin/python3 {note_path}\"""".format(
        alias=FAST_NOTES_ALIAS,
        note_path=note_path,
    )

    bash_alias = os.path.join(os.path.expanduser('~'), '.bash_aliases')

    # Open bash_alias file
    with open(bash_alias, 'a+') as f:
        f.write(alias)
    print("The alias {} has been added to your .bash_aliases file.\n".format(FAST_NOTES_ALIAS))

    notes_dir_set = find_home_directory()
    if notes_dir_set:
        print("Default notes directory has been set to {}".format(notes_dir_set))
        print("To change it, edit user/settings.json")


def find_home_directory():
    """Locates home directory and sets notes directory to home/user/notes in settings.json"""
    home_directory = os.path.expanduser('~')
    notes_directory = os.path.join(home_directory, 'notes')

    with open('user/settings.json') as f:
        settings = json.loads(f.read())
        if not settings['NOTES_DIR']:
            settings['NOTES_DIR'] = notes_directory
            with open('user/settings.json', 'w') as f:
                f.write(
                        json.dumps(
                                settings,
                                sort_keys=True,
                                indent=4,
                                separators=(',', ': ')
                        )
                )
            return notes_directory

        else:
            return None


if __name__ == '__main__':
    run()
