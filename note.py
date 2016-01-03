#!/usr/bin/python3

import sys
import datetime
import subprocess
import os

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
            find_tags(args)
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


def find_tags(args):

    # Parse args and group conditional and tag together.
    first_tag = None
    next_tags = []
    for i, arg in enumerate(args):
        if arg == 'tag':
            try:
                first_tag = args[i+1]
            except IndexError:
                print("Please enter a tag.")
                sys.exit(0)
        elif arg.lower() in ['and', 'or']:
            next_tags.append((arg, args[i+1]))

    if not first_tag:
        print("Command not found.  Please use command note find tag <tag> and/or <tag> and/or <tag>")

    # Grep the home folder and get all tag matches
    grep_output = grep_notes("Tags:")

    if len(grep_output) == 0:
        print("No matches found.")

    # Conditionals for and/or tag searching.
    all_files = []
    failed_list = []
    for found_item in grep_output:
        tag_list = found_item['tags']
        all_files.append(found_item['file_path'])

        # Handle cases where there are no and/or conditions and only a single tag is supplied.
        if not next_tags:
            if first_tag in tag_list:
                continue
            else:
                failed_list.append(found_item['file_path'])

        # Handle all other cases where there are and/or conditions.
        else:
            for condition, tag in next_tags:
                if 'and' in condition:
                    if first_tag in tag_list:
                        if tag in tag_list:
                            continue
                        else:
                            failed_list.append(found_item['file_path'])
                    else:
                        failed_list.append(found_item['file_path'])


                elif 'or' in condition:
                    if first_tag in tag_list or tag in tag_list:
                        continue
                else:
                    failed_list.append(found_item['file_path'])
                    break

    matches = []
    for file in all_files:
        if file in failed_list:
            continue
        elif file not in failed_list:
            matches.append(file)

    print(matches)


def grep_notes(search_string):
    command = "grep -rnw '{}' -e '{}'".format(NOTES_DIR, search_string)
    grep_values = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    found_items = grep_values.communicate()[0].decode('UTF-8').split('\n')
    return_items = []
    for item in found_items:
        if item == "":
            continue
        found_item = item.split(":")
        file_path = found_item[0]
        line_number = found_item[1]
        tags = []
        for tag_field in found_item[2:]:
            split_tag_field = tag_field.split(',')
            for individual_tag in split_tag_field:
                if "@" in individual_tag:
                    tags.append(individual_tag.replace(" ", "").replace("@", ""))
        return_items.append({
            'file_path': file_path,
            'line_number': line_number,
            'tags': tags
        })
    return return_items


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

    # Verify notes directory
    verify_notes_directory()

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
    """
    Helper function to add new lines around print output.
    """
    print("\n" + string + "\n")


def verify_notes_directory():
    """
    Helper function that makes sure the notes directory exists.
    """
    exists = os.path.isdir(NOTES_DIR)
    if exists:
        pass
    else:
        while True:
            create_dir = input("Notes directory does not exist, create it? (y/n): ").lower()
            if create_dir == 'y':
                os.makedirs(NOTES_DIR)
                break
            elif create_dir == 'n':
                sys.exit(0)



if __name__ == '__main__':
    main()