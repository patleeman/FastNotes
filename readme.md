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
    ```

    *Hint: If you want to add tags to a file, in your text editor, add tags by adding a @ in front of it on the tag line.*


    Create a note named my_note with the tags tag1 and tag2...

        note create my_note tag1 tag2


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

* **last** - Open the last modified note in your notes directory.

        note last


* **push** - If you've set up your note directory as a git repository, this command will add all changed files in directory, commit it with a basic comment and push to a remote repository.


    Push all changes to your note directory to your origin repository

        note push


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


####Cheat Sheet

```bash
commands in the parenthesis are optional

note create (note_title tag1 tag2 ... tagn)
note find tag tag1 (and tag2 or tag3 ... and/or tagn)
note peek tag tag1 (and tag2 or tag3 ... and/or tagn)
note last
note push
```