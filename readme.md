#Fast Notes
##A CLI tool to help you take notes faster.

######Fast Notes is a command line tool for people who want simplicity, extendability, and functionality in their note taking app.


####Features:
  1. Create notes fast.
  2. BYOTE - Bring your own text editor.  Configure Fast Notes to use your favorite text editor.
  3. Search your notes by tags.
  4. Add, Commit, and Push your notes to a git repo in a single command.
  5. Ease of migration.  All notes are in a human-readable format in plain-text.

####Commands:
* **create** - Create a new note with an unlimited number of tags in a single command.

    Create a basic untitled note and open it up in your favorite text editor.

    ```bash
    note create
    
    or
    
    note new
    ```

    *Hint: If you want to add tags to a file, in your text editor, add tags by adding a @ in front of it on the tag line.*


    Create a note named my_note with the tags tag1 and tag2...

        note create my_note tag1 tag2

        note new my_note tag1 tag2

    *Hint: Use underscores to denote spaces in the note title*

    ![](/media/create_note.gif?raw=true)

* **tag** - Find notes based on tags and quickly open them.


    Find all notes tagged with python and open it in your favorite text editor:

        note tag find python

    Find notes tagged with multiple tags with and/or operators

        note tag find python or bash and work

    ![](/media/find_note.gif?raw=true)

    Peek into files with tag peek which will print file contents to your console window.

        note tag peek python

    Peek at files with multiple tags utilizing and/or

        note tag peek python or bash and work

    ![](/media/find_note_peek.gif?raw=true)
    
    List all notes in note folder
    
        note tag all
        note tag list
        note list
        note all
        
    List all used tags in notes folder
    
        note tag
        note tags
    
* **last** - Open the last modified note in your notes directory.

        note last

* **search** - Search note directory for one or more keywords.

        note search python bash recipe
        
        or 
        
        note find python bash recipe

* **push** - If you've set up your note directory as a git repository, this command will add all changed files in directory, commit it with a basic comment and push to a remote repository.

    Push all changes to your note directory to your origin repository

        note push

* **pull** - Will execute a git pull command in your notes directory

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


####Cheat Sheet

Commands in the parenthesis are optional

    note create/new (note_title tag1 tag2 ... tagn)
    note tag find tag1 (and tag2 or tag3 ... and/or tagn)
    note tag peek tag1 (and tag2 or tag3 ... and/or tagn)
    note tag all/list
    note tags
    note last
    note search/find
    note push
    note pull

