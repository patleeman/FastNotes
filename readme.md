#Fast Notes
##A CLI tool to help you take notes faster.

######Fast Notes is a command line tool for people who want simplicity, extendability, and functionality in their note taking app.


####Main Features:
  1. Create notes, fast.
  2. Bring your own text editor.
  3. Easily tag and search your note directory by tags.
  4. Add, Commit, and Push your notes to a git repo in a single command. (Coming soon)
  5. Ease of migration.  All notes are in plain-text and human-readable.  **No xml/json file structures.**
  6. Easily create and use templates for your notes. (Coming soon)
  7. Easily add fields to your templates with custom Python3 code. (Coming soon)
  
####Commands:

Create a new note:
  Usage:
    note create
    note create [<note title>] [<tag> <tag> ...]

*Note: To add additional tags while in a note, append the tag with @<tag> in the tag line.

Working with tags:
  See a list of tags:
    Usage:
      note tag

  Find one or more tags using and/or syntax:
    Usage:
      note tag find <tag> [(and <tag> | or <tag>)]

  Find one or more tags and output file contents to command line:
    Usage:
      note tag peek <tag> [(and <tag> | or <tag>)]

  Find a file by tag:
    Usage:
      note tag find

Working with files:
  Edit last modified file in notes folder:
    Usage:
      note last

  Search full text for words within notes folder.
    Usage:
      note search <word> [<word> <word> ...]

Syncing with git (Add, Commit and Push or Pull from a repo):
  Usage:
    note push
    note pull


####Installing
Make sure you have git and python3 installed.  If you're not sure run the commands:

    sudo apt-get install python3 python3-pip git

Once that's complete, run:

    ```bash
    cd ~/
    git clone https://github.com/patleeman/FastNotes.git && cd FastNotes
    chmod +x InitialSetup.py
    chmod +x note.py
    ./InitialSetup.py
    ```

This will download the application into your home folder, set the two script files as executable, and then run setup_alias.py which will add an alias to your ~/.bash_alias file so that the command note will call the script instead of usr/bin/python3 /path/to/FastNotes/note.py


####Setup

#####Chaning your default editor:
All settings are found in the user directory in the settings.json file.  Remember that all changes must adhere to the json file format specs (mainly commas after list arrays and using double quotes).

To change your default text editor or peek editor, edit user/settings.json:

    "EDITOR_COMMAND": [
    "vim",
    "+normal Go",
    "+startinsert"
    ],
    
    "PEEK_COMMAND": [
    "cat"
    ],
    
For example, if you prefer to use Nano as your default editor:
    
    "EDITOR_COMMAND": [
    "nano"
    ],
    
You can append command line options as strings within the EDITOR_COMMAND list:

    "EDITOR_COMMAND": [
    "nano",
    "--nowrap",
    ],


#####Changing your notes folder:
To change the path of your notes directory simply edit the NOTES_DIR setting in settings.json:

from:

    "NOTES_DIR": "/home/patrick/notes",
    
to:

    "NOTES_DIR": "/path/to/notes/folder",
    
    
Useful if you want to places your notes folder inside your cloud storage folder.
