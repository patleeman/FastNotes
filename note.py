#!/usr/bin/python3
"""
Script to create a note template, and open chosen text editor.
API:
./note.py note_name tag1 tag2 ... tagN
"""

import sys
import datetime
import subprocess

from settings import *

def main():
    # Get arguments
    args = sys.argv
    if len(args) <= 1:
        return "Please supply a command."
    if len(args) > 1:
        command = args[1].lower()
        print(args, command)
        if command == 'create':
            create_note(args)
        elif command == 'find':
            print("Feature coming soon.")
        elif command == 'last':
            print("Feature coming soon.")
        elif command == 'push':
            print("Feature coming soon.")
        elif command == 'help':
            send_help()
        else:
            print("Command not found.  Enter help for commands")

def send_help():
    print("note create note_name tag1 tag2 ... tagN")


def create_note(args):
    # Get Note Title
    try:
        note_name = args[2] + "_"
        note_title = args[2]
    except:
        note_name = ""
        note_title = ""

    # Generate file name and path with arguments
    file_name = generate_file_name(note_name)
    file_path = "{}{}".format(NOTES_DIR, file_name)

    # Get tags from argument and convert to string
    if len(args) > 3:
        add_at = str(["{}{}".format(TAG_SYMBOL, x) for x in args[3:]])
        tags = add_at[1:len(add_at)-1].replace("'", "")
    else:
        tags = ""

    # Template lines to add to every file:
    TEMPLATE_LINES = [
        'Dated: {}\n'.format(datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")),
        'Note Name: {}\n'.format(note_title.replace("_", " ")),
        'Tags: {}\n'.format(tags),
        '\n\n', # Add two additional spaces to the end of the header
    ]

    create_file(file_path, lines=TEMPLATE_LINES)
    open_text_editor(file_path)

    print("Tags added: {}".format(tags))
    print("Note created: {}".format(file_path))


def open_text_editor(file_path):
    EDITOR_COMMAND.append(file_path)
    subprocess.call(EDITOR_COMMAND)
    return


def generate_file_name(note_name):
    """
    Helper function to generate file name.
    """
    date_string = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M")
    note_full_name = "{note_name}{date}.txt".format(note_name=note_name, date=date_string)
    return note_full_name


def create_file(file_path, lines=None):
    """
    Helper function to create note file and populate it with templated information
    """
    with open(file_path, 'w') as f:
        if lines:
            f.writelines(lines)
        else:
            # Create empty file.
            pass
    return


if __name__ == '__main__':
    main()