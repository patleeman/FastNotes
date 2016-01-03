"""
Settings File.
"""

# CLI command for your favorite text editor.
# Add additional commands as list items if you want to execute other CLI commands.
# ["vim", '+normal Go', '+startinsert'] Starts vim, goes to the last line and enters insert mode.
EDITOR_COMMAND = ["vim", '+normal Go', '+startinsert']

# Default note directory where all notes will be saved
# /home/<username>/notes
NOTES_DIR = "/home/patrick/notes/"

# Tag Symbol to denote a tag
TAG_SYMBOL = "@"

# Command Line interface alias that setup_alias uses.
# Note that if you change this, you must run setup_alias.py again.
# If you want to remove the alias, open up the file ~/.bashrc and remove
# the two lines added.
FAST_NOTES_ALIAS = 'note'