"""
Settings File.
"""
import json
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
USER_PATH = os.path.join(BASE_PATH, 'user')
with open(os.path.join(USER_PATH, 'settings.json')) as f:
    settings = json.loads(f.read())

# CLI command for your favorite text editor.
# Add additional commands as list items if you want to execute other CLI commands.
# ["vim", '+normal Go', '+startinsert'] Starts vim, goes to the last line and enters insert mode.
EDITOR_COMMAND = settings['EDITOR_COMMAND']
PEEK_COMMAND = settings['PEEK_COMMAND']

# Default note directory where all notes will be saved
# /home/<username>/notes
NOTES_DIR = settings['NOTES_DIR']

# Tag Symbol to denote a tag
TAG_SYMBOL = settings['TAG_SYMBOL']

# Command Line interface alias that setup_alias uses.
# Note that if you change this, you must run InitialSetup.py again.
# If you want to remove the alias, open up the file ~/.bashrc and remove
# the two lines added.
FAST_NOTES_ALIAS = settings['FAST_NOTES_ALIAS']