#!/usr/bin/python3

import sys
import datetime
import subprocess

from settings import *

def main():
    """
    Main run function, determines what functions to call via the first arg parameter.
    """
    args = sys.argv
    if len(args) > 1:
        command = args[1].lower()
        if command == 'create':
            create_note(args)
        elif command == 'find':
            space_print("Feature coming soon.")
            # todo: Add find feature
        elif command == 'last':
            space_print("Feature coming soon.")
            # todo: add last feature
        elif command == 'push':
            space_print("Feature coming soon.")
            # todo: add push feature
        elif command == 'help':
            send_help()
        else:
            space_print("Command not found.  Enter help for commands")
    else:
        space_print("Please supply a command.")

def send_help():
    """
    Prints basic help documentation
    """
    space_print("note create note_name tag1 tag2 ... tagN")
    # todo: add more help

def create_note(args):
    """
    Creates a basic note in the notes directory with a note title, date, time, and tags.
    """
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

    print()
    print("Note created: {}".format(file_path))
    print("Tags added: {}".format(tags))
    print()


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

def space_print(string):
    print("\n" + string + "\n")

if __name__ == '__main__':
    main()