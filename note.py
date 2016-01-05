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

from settings import *


def main():
    """
    Main run function, determines what functions to call via the first arg parameter.
    """
    args = sys.argv
    if len(args) > 1:
        command = args[1].lower()
        if command == 'create' or command == 'new':
            note_create(args)
        elif command == 'last':
            note_last()
        elif command == 'list' or command == 'all':
            note_tag_all()
        elif command == 'search' or command == 'find':
            note_search(args)
        elif command == 'push':
            helper_space_print("  Feature coming soon.")
            # todo: add push feature
        elif command == 'pull':
            helper_space_print("  Feature coming soon.")
            # todo: add pull feature
        elif command == 'help':
            note_help()
        elif command == 'tag' or command == 'tags':
            try:
                sub_command = args[2].lower()
                if sub_command == 'find':
                    note_tag_find(args)
                elif sub_command == 'peek':
                    note_tag_find(args, peek=True)
                elif sub_command == 'all' or sub_command == 'list':
                    note_tag_all()
            except IndexError:
                note_tags()
        else:
            helper_space_print("  Command not found.  Enter note help for command list")
    else:
        helper_space_print("  Enter note help for a command list")

    return


def note_search(args):
    if len(args) <= 2:
        print(helper_colorify("\n  No search term provided.\n", 'red'))
        sys.exit(0)
    else:
        list_of_words = args[2:]

    results = helper_grep_notes_search(list_of_words)

    display_list = []
    if not results:
        print(helper_colorify("\n  No matches found.\n", 'red'))
    else:
        # results[file_path] = [[line_number, keyword],[line_number, keyword]]
        for file_path in results.keys():
            matches = results[file_path]
            keywords = {}
            for item in matches:

                # Group by keyword.
                line_number = item[0]
                keyword = item[1]
                if keyword not in keywords.keys():
                    keywords[keyword] = [line_number]
                else:
                    keywords[keyword].append(line_number)

            match_list = []
            for keyword in keywords:
                match_list.append("{match}(ln(s) {line_num})".format(
                        match=keyword,
                        line_num=helper_stringify_list(keywords[keyword])
                ))

            display_list.append((file_path, helper_stringify_list(match_list)))
        helper_display_matches(display_list, "File Match (ln(s): #)")
    return


def note_last():
    file_list = os.listdir(NOTES_DIR)
    file_list = filter(lambda x: not os.path.isdir(x), file_list)
    file_list = [os.path.join(NOTES_DIR, x) for x in file_list]
    newest = max(file_list, key=lambda x: os.stat(x).st_mtime)
    helper_open_editor(newest)
    return


def note_tags():
    """
    Display all tags used in note folder
    """
    grep_output = helper_grep_notes_tags()
    if not grep_output:
        print(helper_colorify("\n  No tags found.\n", 'red'))
        sys.exit(0)

    # Get all tags found in folder
    tags = []
    for grep_info in grep_output:
        for tag in grep_info['tags']:
            if tag not in tags:
                tags.append(tag)

    if not tags:
        print(helper_colorify("\n  No tags found.\n", 'red'))
        sys.exit(0)

    # Print tags
    print("\n  {}\n  {}\n".format(
            helper_colorify("FastNotes", 'blue'),
            helper_colorify("Tags in use:", 'red')
    ))

    for tag in tags:
        print("  {tag}".format(tag=helper_colorify(tag, 'red')))

    print()
    return


def note_tag_all(peek=None):
    """
    Display all notes in note folder
    """
    grep_output = helper_grep_notes_tags()
    if not grep_output:
        print(helper_colorify("\n  No notes found.\n", 'red'))
        sys.exit(0)

    display_results = []
    for grep_info in grep_output:
        display_results.append((grep_info['file_path'], helper_stringify_list(grep_info['tags'])))

    helper_display_matches(display_results, "Tags", peek=peek)


def note_tag_find(args, peek=None):
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
                print("  Please enter a tag to search for.")
                sys.exit(0)
        elif arg.lower() in ['and', 'or']:
            next_tags.append((arg, args[i+1]))

    if not first_tag:
        print("  Command not found.  Enter notes help for help")
        return

    # Grep the home folder and get all tag matches
    grep_output = helper_grep_notes_tags()

    if not grep_output:
        print(helper_colorify("\n  No tags found.\n", 'red'))
        sys.exit(0)

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
    # Matches schema = [(file_path, tags)]
    matches = []
    for file in all_files:
        if file in failed_list:
            continue
        elif file not in failed_list:
            for grep_info in grep_output:
                if grep_info['file_path'] == file:
                    matches.append((grep_info['file_path'], helper_stringify_list(grep_info['tags'])))

    if not matches:
        print(helper_colorify("\n  No matches found.\n", 'red'))
        sys.exit(0)

    helper_display_matches(matches, third_column="Tags", peek=peek)

    return


def helper_display_matches(results, third_column_title, peek=None):
    """
    Helper function to display matches.
    results schema = [(file_name, third_column)]
    """
    # Todo: add in pagination so if there are more than x notes, you can cycle through them.

    # Display matches with numbers and wait for user input.
    buf_max = 22  #Display column max width
    date_buf = 13
    third_col_buffer = 28
    int_buf_max = 3
    while True:
        print()
        print("  {}  Choose a file.".format(helper_colorify("FastNotes", 'blue')))
        print("  #{int_buf} | {}{head_buf1}| {}{head_buf2}| {}".format(
                helper_colorify("Note Title", 'cyan'),
                helper_colorify("Date Created", 'magenta'),
                helper_colorify(third_column_title, 'red'),
                head_buf1=" "*(buf_max-len("Note Title")),
                head_buf2=" "*(date_buf-len("Date Created")),
                int_buf=" "*(int_buf_max-2)
        ))


        for i, tuple_values in enumerate(results):
            if not tuple_values:
                break

            file_name = os.path.split(tuple_values[0])[1]
            file_name_split = file_name.split("__")

            try:
                third_column = tuple_values[1]
            except IndexError:
                third_column = ""

            try:
                note_title = file_name_split[0].replace("_", " ")[0:buf_max]
            except IndexError:
                note_title = tuple_values[0]


            file_path = os.path.join(NOTES_DIR, tuple_values[0])
            date_created = helper_get_created_date(file_path)

            print("  {i}{int_buf}| {path}{buf1}| {date_created}{buf2}| {third_col}".format(
                    i=i,
                    third_col=helper_colorify(third_column, 'red'),
                    path=helper_colorify(note_title, 'cyan'),
                    date_created=helper_colorify(date_created, 'magenta')[0:third_col_buffer],
                    buf1=" "*(buf_max - len(note_title)),
                    buf2=" "*(date_buf - len(date_created)),
                    int_buf=" "*(int_buf_max - len(str(i))),
            ))

        print("\n  q: Quit program (or Ctrl-c)\n")


        try:
            choice = input(helper_colorify("  Open file # >> ", 'crimson'))
            if choice.lower() == 'q' or choice == 'quit':
                print()
                sys.exit(0)
            choice = int(choice)
        except ValueError:
            print(helper_colorify("\n  Please enter a valid choice.\n", 'red'))
            continue

        if choice < len(results):
            file_to_open = results[choice][0]
            helper_open_editor(file_to_open, peek=peek)
            print("  Opening file {}\n\n".format(file_to_open))
            break
        else:
            print(helper_colorify("\n  Please enter a valid choice.\n", 'red'))

    return


def helper_get_modified_date(file_path):
    """
    Helper to get file modified date.
    """
    unix_time = os.path.getmtime(file_path)
    date_string = datetime.datetime.fromtimestamp(unix_time).strftime('%m-%d-%Y')
    return date_string


def helper_get_created_date(file_path):
    """
    Helper to get file created date.
    """
    unix_time = os.path.getctime(file_path)
    date_string = datetime.datetime.fromtimestamp(unix_time).strftime('%m-%d-%Y')
    return date_string


def helper_colorify(string, color):
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


def helper_stringify_list(list_object):
    """
    Helper function to convert a list object to a nicely formatted comma separated string.
    """
    converted = str(list_object).replace("'", '')
    stripped = converted[1:len(converted)-1]
    return stripped


def helper_grepper(command):
    grep_values = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    found_items = grep_values.communicate()[0].decode('UTF-8').split('\n')
    return found_items


def helper_grep_notes_search(search_words_list):
    """
    Generally search notes folder for a list of words
    :param search_words_list: List of strings to search with grep.
    :return:
    return_items[file_path] = [[line_number, keyword],[line_number, keyword]]
    """
    search_string = "\|".join(search_words_list)
    command = "grep -rnwo '{}' -e '{}'".format(NOTES_DIR, search_string)
    found_items = helper_grepper(command)
    return_items = {}

    for found_item in found_items:
        if not found_item:
            continue

        found_item_list = found_item.split(":")
        file_path = found_item_list[0]
        line_number = found_item_list[1]
        found_keyword = found_item_list[2]
        return_items.setdefault(file_path, []).append([line_number, found_keyword])

    return return_items


def helper_grep_notes_tags():
    """
    Grep notes folder and return tags.

    return items schema:

        return_items.append({
        'file_path': file_path,
        'line_number': line_number,
        'tags': tags
        })
    """
    search_string = "Tags:"
    command = "grep -rnw '{}' -e '{}'".format(NOTES_DIR, search_string)
    found_items = helper_grepper(command)

    return_items = []
    for item in found_items:
        if item == "":
            continue
        if 'binary file' in item.lower():
            continue

        found_item = item.split(":")
        file_path = found_item[0]

        # If there is a note open, find will fail to process the .swp file.  Temp fix is to exclude all non txt files.
        #if not file_path.lower().endswith('.txt'):
        #    continue

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


def note_help():
    """
    Prints basic help documentation
    """
    help = """

    FastNotes Help

    Commands:
    Commands in parenthesis are optional.
    =====================================================
    note create/new (note_title tag1 tag2 ... tagn)
    note tag find tag1 (and tag2 or tag3 ... and/or tagn)
    note tag peek tag1 (and tag2 or tag3 ... and/or tagn)
    note tag all/list
    note tags
    note last
    note search/find
    note push
    note pull
    =====================================================
    Author: Patrick Lee https://github.com/patleeman/FastNotes

    """
    print(help)


def note_create(args):
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
    helper_verify_notes_directory()

    # Generate file name and path with arguments
    file_name = helper_generate_file_name(note_name)
    file_path = os.path.join(NOTES_DIR, file_name)

    # Get tags from argument and convert to string
    if len(args) > 3:
        add_at = str(["{}{}".format(TAG_SYMBOL, x.lower()) for x in args[3:]])
        tags = helper_stringify_list(add_at)
    else:
        tags = ""

    # Template lines to add to every file:
    date = datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")
    note_title = note_title.replace("_", " ")

    # Read template
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user', 'NoteTemplate.txt')
    with open(template_path) as template_file:
        template_base = template_file.read()

    template = template_base.format(
        date=date,
        note_title=note_title,
        tags=tags
    )

    helper_create_base_file(file_path, template=template)
    helper_open_editor(file_path)

    print("\n  Note created: {}".format(file_path))
    print("  Tags added: {}\n".format(tags))

    #Todo: Add ability to scan file for new title and rename file to new note_title.


def helper_open_editor(file_path, peek=None):
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


def helper_generate_file_name(note_name):
    """
    Helper function to generate file name.
    """
    date_string = datetime.datetime.now().strftime("%m-%d-%Y__%H-%M")
    note_full_name = "{note_name}{date}.txt".format(note_name=note_name, date=date_string)
    return note_full_name


def helper_create_base_file(file_path, template=None):
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


def helper_space_print(string):
    """
    Helper function to add new lines around print output.
    """
    print("\n" + string + "\n")


def helper_verify_notes_directory():
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
