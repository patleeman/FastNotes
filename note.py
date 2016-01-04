#!/usr/bin/python3
"""
FastNotes
Fast Notes is a command line tool for people who want simplicity, extendability,
and functionality in their note taking app.


Todo:
  - Add last command
  - Add push command
  - Add note tag list command - list all notes in tag folder and add pagination
    for multiple pages.
"""
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
        elif command == 'tag':
            if args[2].lower() == 'find':
                find_tags(args)
            elif args[2].lower() == 'peek':
                find_tags(args, peek=True)
        elif command == 'last':
            space_print("Feature coming soon.")
            # todo: add last feature
        elif command == 'push':
            space_print("Feature coming soon.")
            # todo: add push feature
        elif command == 'help':
            send_help()
        else:
            space_print("Command not found.  Enter notes help for help")
    else:
        space_print("Command not found.")


def find_tags(args, peek=None):
    """
    Find tags, display results and open text editor.
    Todo: Split this function up into small functions.
    """
    # Parse args and group conditional and tag together.
    first_tag = None
    next_tags = []
    for i, arg in enumerate(args):
        if arg == 'tag':
            try:
                first_tag = args[i+2]
            except IndexError:
                print("Please enter a tag to search for.")
                sys.exit(0)
        elif arg.lower() in ['and', 'or']:
            next_tags.append((arg, args[i+1]))

    if not first_tag:
        print("Command not found.  Enter notes help for help")
        return

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
                else:
                    failed_list.append(found_item['file_path'])
                    break

    # Filter out negative matches from full list, remaining should be positive matches
    matches = []
    for file in all_files:
        if file in failed_list:
            continue
        elif file not in failed_list:
            for grep_info in grep_output:
                if grep_info['file_path'] == file:
                    matches.append((grep_info['file_path'], grep_info['tags']))

    if not matches:
        print(colorify("\nNo matches found.\n", 'red'))
        sys.exit(0)

    # Display matches with numbers and wait for user input.
    buf_max = 20  #Display column max width
    while True:
        print()
        print("  {}  Choose a file.  Ctrl-C to quit.".format(colorify("FastNotes", 'blue')))
        print("  #: {}{head_buf1}| {}{head_buf2}| {}".format(
                colorify("Note Title", 'cyan'),
                colorify("Date Created", 'magenta'),
                colorify("Tags", 'red'),
                head_buf1=" "*(buf_max-len("Note Title")),
                head_buf2=" "*(buf_max-len("Date Created")),
        ))

        for i, tuple_values in enumerate(matches):
            tag_text = stringify_list(tuple_values[1])
            file_name = os.path.split(tuple_values[0])[1]
            file_name_split = file_name.split("__")
            note_title = file_name_split[0].replace("_", " ")[0:buf_max]
            date_created = file_name_split[1][0:buf_max]

            buf1 = buf_max - len(note_title)
            buf2 = buf_max - len(date_created)

            print("  {i}: {path}{buf1}| {date_created}{buf2}| {tags}".format(
                    i=i,
                    tags=colorify(tag_text, 'red'),
                    path=colorify(note_title, 'cyan'),
                    date_created=colorify(date_created, 'magenta'),
                    buf1=" "*buf1,
                    buf2=" "*buf2,
            ))
        print()

        try:
            choice = int(input("Open option #: "))
        except ValueError:
            print("Please enter a valid choice.")
            continue

        if choice < len(matches):
            file_to_open = matches[choice][0]
            open_text_editor(file_to_open, peek=peek)
            print("Opening file {}\n\n".format(file_to_open))
            break
        else:
            print("Please enter a valid choice.")

    return


def colorify(string, color):
    """
    Add color to console output.
    https://stackoverflow.com/questions/2330245/python-change-text-color-in-shell
    """
    colors = {
        'red': "\033[1;31m{string}\033[1;m",
        'gray': "\033[1;30m{string}\033[1;m",
        'green': "\033[1;32m{string}\033[1;m",
        'yellow': "\033[1;33m{string}\033[1;m",
        'blue': "\033[1;34m{string}\033[1;m",
        'cyan': "\033[1;36m{string}\033[1;m",
        'magenta': "\033[1;35m{string}\033[1;m",
        'white': "\033[1;37m{string}\033[1;m",
        "crimson": "\033[1;38m{string}\033[1;m"
    }

    if sys.stdout.isatty():
        try:
            output = colors[color].format(string=string)
        except ValueError:
            output = string
    else:
        output = string

    return output


def stringify_list(list_object):
    """
    Helper function to convert a list object to a nicely formatted comma separated string.
    """
    converted = str(list_object).replace("'", '')
    stripped = converted[1:len(converted)-1]
    return stripped


def grep_notes(search_string):
    """
    Search file folder using grep and return a list of lists containing search results.
    Todo: Generalize function beyond returning tags.
    """
    command = "grep -rnw '{}' -e '{}'".format(NOTES_DIR, search_string)
    grep_values = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    found_items = grep_values.communicate()[0].decode('UTF-8').split('\n')
    return_items = []
    for item in found_items:
        if item == "":
            continue
        found_item = item.split(":")
        file_path = found_item[0]

        # If there is a note open, find will fail to process the .swp file.  Temp fix is to exclude all non txt files.
        if not file_path.endswith('.txt'):
            continue

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
    help = """

    FastNotes Help

    Commands:
    Commands in parenthesis are optional.
    =====================================================
    note create (note_title tag1 tag2 ... tagn)
    note find tag tag1 (and tag2 or tag3 ... and/or tagn)
    note peek tag tag1 (and tag2 or tag3 ... and/or tagn)
    note last
    note push
    =====================================================
    Author: Patrick Lee https://github.com/patleeman/FastNotes

    """
    print(help)


def create_note(args):
    """
    Creates a basic note in the notes directory with a note title, date, time, and tags.
    """
    try:
        note_name = args[2] + "__"
        note_title = args[2]
    except:
        note_name = "Untitled__"
        note_title = "Untitled Note"

    # Verify notes directory
    verify_notes_directory()

    # Generate file name and path with arguments
    file_name = generate_file_name(note_name)
    file_path = "{}{}".format(NOTES_DIR, file_name)

    # Get tags from argument and convert to string
    if len(args) > 3:
        add_at = str(["{}{}".format(TAG_SYMBOL, x.lower()) for x in args[3:]])
        tags = stringify_list(add_at)
    else:
        tags = ""

    # Template lines to add to every file:
    date = datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")
    note_title = note_title.replace("_", " ")

    # Read template
    with open('NoteTemplate.txt') as template_file:
        template_base = template_file.read()

    template = template_base.format(
        date=date,
        note_title=note_title,
        tags=tags
    )

    create_file(file_path, template=template)
    open_text_editor(file_path)

    print("\nNote created: {}".format(file_path))
    print("Tags added: {}\n".format(tags))

    #Todo: Add ability to scan file for new title and rename file to new note_title.

def open_text_editor(file_path, peek=None):
    """
    Helper function that opens text editor.
    """
    if not peek:
        EDITOR_COMMAND.append(file_path)
        subprocess.call(EDITOR_COMMAND)
    elif peek is True:
        PEEK_COMMAND.append(file_path)
        subprocess.call(PEEK_COMMAND)
    return


def generate_file_name(note_name):
    """
    Helper function to generate file name.
    """
    date_string = datetime.datetime.now().strftime("%m-%d-%Y__%H-%M")
    note_full_name = "{note_name}{date}.txt".format(note_name=note_name, date=date_string)
    return note_full_name


def create_file(file_path, template=None):
    """
    Helper function to create note file and populate it with templated information
    """
    with open(file_path, 'w') as f:
        if template:
            f.writelines(template)
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
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\n")
        sys.exit(0)
