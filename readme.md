***Fast Notes***

A CLI tool to help you take notes faster.

Features:
1. Generate notes with basic templates and call your favorite text editor.
2. Find notes by tags.
3. Add, Commit, and Push your notes to your git repo.

The first argument is the command.
  * create - Create a new note named note_name with the following tags.  (Underscores as note name will be converted to spaces inside the note template)
        example:
        ```./note.py create note_name tag1 tag2 tag3```
  * find - Command line tool to find notes based on tags or date and to quickly open them.
  * last - Open the last edited note.
  * push - Push notes to your git repo
  
The second argument is the name of your note and will be added to the file name.
Every argument after that will be considered a tag and will be added to the Tag line with an "@" added to the front of it to denote a tag.  This can be changed in settings.py.
