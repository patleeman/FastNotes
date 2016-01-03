#Fast Notes
##A CLI tool to help you take notes faster.

######Fast Notes is a command line tool written in Python 3 which helps you create tagged note templates very quickly in a pre-defined location.  The motivation behind this tool is to have a lightweight, versatile, self hosted note taking application with basic tagging capabilities.

####Features:
  1. Generate notes with basic templates and call your favorite text editor in a single command.
  2. Find notes by tags.
  3. Add, Commit, and Push your notes to a git repo in a single command.

####Commands:
* create - Create a new note with an unlimited number of tags in a single command.

    ```bash
    #Create a note using the pre-defined template named Cool_test_note with the following tags...*
    note create Cool_test_note python bash work
    #Hint: Use underscores to denote spaces in the note title*
    ```

* find - Find notes based on tags and quickly open them.

    ```bash
    #Example:
    #Find all notes tagged with @python:
    note find tag python

    #Find notes tagged with and/or
    note find tag python or bash and work
    ```

* last - Open the last modified note in your notes directory.

    ```bash
    note last
    ```

* push - If you've set up your note directory as a git repository, this command will add all changed files in directory, commit it with a basic comment and push to a remote repository.

    ```
    #Push all changes to your note directory to your origin repository
    note push
    ```

####Installing
Make sure you have git and python3 installed.  If you're not sure run the commands:

    sudo apt-get install python3 python3-pip git

Once that's complete, run:

    ```bash
    cd ~/
    git clone https://github.com/patleeman/FastNotes.git && cd FastNotes
    chmod +x setup_alias.py
    chmod +x note.py
    ./setup_alias.py
    ```

This will download the application into your home folder, set the two script files as executable, and then run setup_alias.py which will add an alias to your bashrc file so that the command note will call the script instead of usr/bin/python3 /home/username/FastNotes/note.py

